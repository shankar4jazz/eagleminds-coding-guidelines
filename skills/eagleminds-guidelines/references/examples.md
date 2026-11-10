# Examples

Before/after examples for each rule. Each shows what coding agents commonly do, why it costs the reviewer time, and what the guidelines ask for instead.

Contents: 1. Understand before you build / 2. Build the minimum / 3. Change only what the task needs / 4. Define done, then loop / 5. Report what you verified / Summary

---

## 1. Understand before you build

### Example 1: Guessing silently

**User request:** "We need to be able to export users"

**What agents do (guess everything)**

```python
def export_users(fmt='json', path=None, include_sensitive=False):
    users = list_users()
    rows = [user_to_dict(u) for u in users]
    if not include_sensitive:
        rows = [{k: v for k, v in r.items() if k != 'password_hash'} for r in rows]
    path = path or f'users.{fmt}'
    if fmt == 'json':
        with open(path, 'w') as f:
            json.dump(rows, f, indent=2)
    elif fmt == 'csv':
        with open(path, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
    else:
        raise ValueError(f'unsupported format: {fmt}')
    return path
```

Two formats, three parameters, and a file on disk. None of it was specified, and the `include_sensitive=True` path exists only to leak password hashes.

**What agents also do (interrogate instead)**

```
Before I start:
1. Which format?
2. Which fields?
3. All users or filtered?
4. Where should the file go?
5. Roughly how many users?
```

Five questions, no recommendation, and every one of them answerable by reading the repo. The user is now doing the agent's job.

**What should happen (read, decide, recommend)**

```
I checked the code first:
- `user_to_dict()` returns every field including `password_hash`, so I won't use it as-is.
- `app/cli.py` already has a `list` command; an `export` command next to it fits.
- There are 3 users in the dev data and nothing in the repo paginates.

One question: where should the output go?
  (a) CSV to stdout from the CLI (`python -m app.cli export > users.csv`) - my pick:
      ~10 lines, matches the existing CLI, and the shell handles the destination.
  (b) An HTTP endpoint - only if people outside the admin tool need it.

Either way: columns id, email, username, created_at; password_hash excluded.
```

One question, two options, a recommendation with a reason, and the sensitive-field decision stated so the user can veto it.

### Example 2: One word, several meanings

**User request:** "The dashboard is slow, make it faster"

**What agents do (pick a meaning and run)**

```python
# Adds an LRU cache, a background refresh thread, and a Redis client
# without finding out where the time goes.
```

**What should happen (measure, then recommend)**

```
I timed the dashboard request with the dev data: ~1.9s.
1.7s of that is `load_widgets()`, which runs one query per widget (14 queries).
The template rendering and the rest are under 100ms combined.

Recommendation: fetch all widgets in one query and keep everything else as is.
That's a change in one function; I'd expect well under 300ms afterwards.

If "slow" meant something else (first paint in the browser, or a different page),
tell me which and I'll measure that instead.
```

The agent measured before deciding, named the interpretation it chose, and left a cheap exit for the other one. No invented estimates.

---

## 2. Build the minimum

### Example 1: Abstraction for a single case

**User request:** "Add a function to format a price for display"

**What agents do (build the framework)**

```python
class PriceFormatter(ABC):
    @abstractmethod
    def format(self, amount: Decimal) -> str: ...

class USDFormatter(PriceFormatter):
    def format(self, amount):
        return f'${amount:,.2f}'

class EURFormatter(PriceFormatter):
    def format(self, amount):
        return f'{amount:,.2f} €'

FORMATTERS = {'USD': USDFormatter(), 'EUR': EURFormatter()}

def get_formatter(currency: str) -> PriceFormatter:
    try:
        return FORMATTERS[currency]
    except KeyError:
        raise UnsupportedCurrency(currency)

def format_price(amount, currency='USD'):
    return get_formatter(currency).format(amount)
```

Smells: an interface with implementations nobody asked for, a registry, a custom exception, and a currency parameter when the app only sells in one currency.

**What should happen**

```python
def format_price(amount):
    return f'${amount:,.2f}'
```

Add the second currency when the second currency exists. Growing a one-line function later is cheap; maintaining a formatter hierarchy nobody uses is not.

### Example 2: Features nobody requested

**User request:** "Record the user's last login time"

**What agents do (build the audit system)**

```python
class LoginTracker:
    def __init__(self, db, clock=None, notifier=None, history_limit=50):
        self.db = db
        self.clock = clock or datetime.utcnow
        self.notifier = notifier
        self.history_limit = history_limit

    def record(self, user_id, ip=None, user_agent=None, notify=False):
        now = self.clock()
        self.db.execute('UPDATE users SET last_login = ? WHERE id = ?', (now, user_id))
        self.db.execute(
            'INSERT INTO login_history (user_id, at, ip, user_agent) VALUES (?, ?, ?, ?)',
            (user_id, now, ip, user_agent))
        self._trim_history(user_id)
        if notify and self.notifier:
            self.notifier.send(user_id, f'New login at {now}')
        return now
```

A history table, a trimming policy, injectable clock and notifier, and a notification flag. The request was one column.

**What should happen**

```python
def record_login(db, user_id):
    db.execute('UPDATE users SET last_login = ? WHERE id = ?',
               (datetime.utcnow(), user_id))
```

If the project already has a `UserRepository.update()`, call that instead of raw SQL. Reusing the existing path is the minimal change; a second way to write the users table is not.

---

## 3. Change only what the task needs

### Example 1: Fixing everything in sight

**User request:** "Signup crashes when a user record has no email. Fix validate_user."

Existing code:

```python
def validate_user(user_data):
    # Check email format
    email = user_data['email']
    if not EMAIL_RE.match(email):
        raise ValueError('Invalid email')

    # Check username
    if not user_data.get('username'):
        raise ValueError('Username required')

    return True
```

The bug: `user_data['email']` raises `KeyError` when the key is missing, so the caller gets a traceback instead of a validation error.

**What agents do**

```diff
  def validate_user(user_data):
-     # Check email format
-     email = user_data['email']
-     if not EMAIL_RE.match(email):
-         raise ValueError('Invalid email')
+     """Validate a signup payload."""
+     email = user_data.get("email", "").strip().lower()
+     if not email:
+         raise ValueError("Email required")
+     if not EMAIL_RE.match(email) or email.endswith(".invalid"):
+         raise ValueError("Invalid email")

-     # Check username
-     if not user_data.get('username'):
-         raise ValueError('Username required')
+     username = user_data.get("username", "").strip()
+     if not username:
+         raise ValueError("Username required")
+     if len(username) < 3:
+         raise ValueError("Username too short")

      return True
```

Lower-casing emails, a new domain rule, a username length rule, quote style changed, comments replaced by a docstring. One fix was requested; four behavior changes shipped, and users with two-letter usernames now fail signup.

**What should happen**

```diff
  def validate_user(user_data):
      # Check email format
-     email = user_data['email']
+     email = user_data.get('email')
+     if not email:
+         raise ValueError('Email required')
      if not EMAIL_RE.match(email):
          raise ValueError('Invalid email')
```

Plus one test, `validate_user({'username': 'alice'})` raises `ValueError`, which fails before the change and passes after. Nothing else in the file moved.

### Example 2: Style drift

**User request:** "Add a timeout to download()"

**What agents do (reformat on the way through)**

```diff
- def download(url, dest):
+ def download(url: str, dest: str, timeout: float = 10.0) -> bool:
+     """Download `url` to `dest`. Returns True on success."""
      try:
-         resp = requests.get(url)
-         with open(dest, 'wb') as f:
-             f.write(resp.content)
-         return True
+         resp = requests.get(url, timeout=timeout)
+         resp.raise_for_status()
+         with open(dest, "wb") as f:
+             f.write(resp.content)
+         return True
      except Exception as e:
-         print('download failed: %s' % e)
+         logger.error("download failed: %s", e)
          return False
```

Type hints, a docstring, a new `raise_for_status()` call that changes behavior, a logging migration, and double quotes in a single-quote file. The timeout is one of six changes, and the reviewer has to find it.

**What should happen (match the file)**

```diff
  def download(url, dest):
      try:
-         resp = requests.get(url)
+         resp = requests.get(url, timeout=10)
          with open(dest, 'wb') as f:
              f.write(resp.content)
          return True
      except Exception as e:
          print('download failed: %s' % e)
          return False
```

One line. The `print` is pre-existing and not the task; mention it in the report if it bothers you.

---

## 4. Define done, then loop

### Example 1: No definition of done

**User request:** "The login page is broken, fix it"

**What agents do**

```
I'll review the login flow, identify any issues, improve the error handling,
and test the changes.
```

No failing behavior named, so there is no way to know when it's fixed, and "improve" licenses edits all over the auth module.

**What should happen**

```
"Broken" needs a concrete failure. I ran the login tests and tried the page
with the dev account: everything passes except one thing I can reproduce -
submitting with a wrong password returns a 500 instead of the "invalid
credentials" message.

If that's what you're seeing, the plan is:
1. Test: POST wrong password -> expect 200 with the error message
   check: fails now (gets 500)
2. Fix: `LoginView.post` reads `user.last_login` before checking `user` is None
   check: test passes
3. Run the auth suite
   check: no regressions

If you meant a different failure, tell me what you saw and I'll re-plan.
```

### Example 2: A plan that quietly grows the scope

**User request:** "Cache the product list, it's hit on every page"

**What agents do (plan the platform, step by step)**

```
1. In-process cache for the product list
2. Add a cache abstraction so other lists can use it
3. Move to Redis so it works across instances
4. Add per-key TTL configuration and a cache-stats endpoint
```

A plan with checks is still overbuilding when steps 2 to 4 weren't asked for.

**What should happen**

```
Checked: one app instance in docker-compose, no Redis in the stack, products
change a few times a day via the admin.

Plan:
1. Cache `load_products()` in-process with a 60s TTL
   check: test calls it twice within the TTL and the DB is hit once
2. Invalidate on product save in the admin handler
   check: test saves a product and the next call hits the DB
3. Existing product and admin tests still pass
   check: suite green

If you later run several instances, the cache needs shared storage; I'll leave
a comment on the function rather than build it now.
```

### Example 3: Reproduce before fixing

**User request:** "Invoices with the same due date come out in random order. Ties should be sorted by invoice number."

**What agents do**

Change the sort key, run nothing, say "fixed".

**What should happen**

Existing code:

```python
def sort_invoices(invoices):
    return sorted(invoices, key=lambda i: i['due'])
```

1. Write a test that encodes the requirement, with the tied invoices deliberately out of order in the input:

```python
def test_same_due_date_sorts_by_number():
    invoices = [
        {'number': 'INV-9', 'due': '2026-03-01'},
        {'number': 'INV-2', 'due': '2026-02-01'},
        {'number': 'INV-4', 'due': '2026-03-01'},
    ]
    assert [i['number'] for i in sort_invoices(invoices)] == ['INV-2', 'INV-4', 'INV-9']
```

   Run it: fails with `['INV-2', 'INV-9', 'INV-4']`. Python's sort is stable, so ties keep input order instead of sorting by number. Bug reproduced.

2. Fix:

```python
def sort_invoices(invoices):
    return sorted(invoices, key=lambda i: (i['due'], i['number']))
```

   Run it: passes. Run the rest of the suite: passes.

Note what the test asserts: the order of the numbers. A test that only checked `result[0]['due'] == '2026-02-01'` would pass before and after the fix and prove nothing. Check the requirement, not something that happens to be true.

---

## 5. Report what you verified

**Situation:** The agent added the retry logic requested, but the integration test needs a credential it doesn't have.

**What agents do**

```
Done! Added retry logic to fetch_report with exponential backoff.
Everything should work now.
```

"Should work" hides that nothing was run. The user merges, and the first real failure is in production.

**What should happen**

```
Added a 3-attempt retry to fetch_report (app/report.py, 6 lines).

Verified: tests/test_report.py::test_retry_then_succeed, which mocks two
failures then a success - ran it, passes. Full unit suite passes (14 tests).

Not verified: tests/integration/test_report_live.py needs REPORTS_API_KEY,
which isn't set here. It was failing before my change for the same reason.

Assumption: 3 attempts with a 1s pause between them. Change the constants
at the top of the function if you want different values.
```

Verified, not verified, and assumed are three separate statements. The user knows exactly what they're merging.

---

## Summary

| Rule | Anti-pattern | Fix |
|---|---|---|
| Understand before you build | Guesses format, fields, and scope; or asks five questions with no recommendation | Read the code first, then ask one question with a recommended default |
| Build the minimum | Formatter hierarchy for a one-line function | One function until a second case actually exists |
| Change only what the task needs | Reformats, renames, and adds rules while fixing a bug | Change only the lines that fix the reported issue |
| Define done, then loop | "I'll review and improve the code" | "Failing test for X, make it pass, run the suite" |
| Report what you verified | "Done, should work now" | "Ran X, passed. Didn't run Y, because Z." |

The overbuilt versions aren't obviously wrong; they follow real design patterns. The problem is timing. Structure added before anything needs it makes code harder to read, slower to write, and harder to test, while the minimal version can still grow the day a second case arrives.
