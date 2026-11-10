# 面向 AI 编程代理的 EagleMinds 编码准则

**一套 CLAUDE.md、Claude Code 技能、Cursor 规则和 AGENTS.md，让 LLM 编程代理不再瞎猜、过度设计、乱改无关代码，以及什么都没运行就说"完成"。** 基于 LLM 编程代理在实际任务中的真实失败方式，写成代理在执行中真正能遵循的规则，并做了有无准则的对比测试。

[English](./README.md) | 简体中文

适用于 **Claude Code**、**Cursor**、**OpenAI Codex**、**GitHub Copilot**、**Gemini CLI**、**OpenCode**、**Amp**，以及任何读取 `AGENTS.md` 的代理。

## 快速安装

**Claude Code 插件**（为所有项目添加 `eagleminds-guidelines` 技能和 `/eagleminds-review` 命令）：

```
/plugin marketplace add shankar4jazz/eagleminds-coding-guidelines
/plugin install eagleminds-guidelines@eagleminds-coding-guidelines
```

**CLAUDE.md**（按项目，供 Claude Code 使用）：

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/CLAUDE.md
```

**AGENTS.md**（按项目，供 Codex、OpenCode、Gemini CLI、Amp、Devin、Jules 等使用）：

```bash
curl -o AGENTS.md https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/AGENTS.md
```

**Cursor**（项目规则，始终生效）：

```bash
mkdir -p .cursor/rules && curl -o .cursor/rules/eagleminds-guidelines.mdc https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/.cursor/rules/eagleminds-guidelines.mdc
```

**GitHub Copilot**（仓库指令）：

```bash
mkdir -p .github && curl -o .github/copilot-instructions.md https://raw.githubusercontent.com/shankar4jazz/eagleminds-coding-guidelines/main/.github/copilot-instructions.md
```

已有这些文件？用追加（`curl ... >> CLAUDE.md`）而不是覆盖。这些规则本来就是为了与项目专属指令并存而写的。

## 解决什么问题

LLM 编程代理有几种可预测的失败方式：

- **瞎猜。** 面对模糊的请求，挑一种理解，不说是哪一种，然后一路做下去。不指出不一致，不呈现取舍，请求看起来像个错误时也不反驳。
- **过度设计。** 一个辅助函数长出配置对象、接口和三个没人要的选项。100 行能解决的事写成 1000 行，死代码还留着。
- **乱改不理解的代码。** 注释被改写，`sleep()` 被删掉，import 被重排，全是与任务无关的副作用。
- **过早宣布完成。** 代码从没跑过就说"修好了，应该没问题"，或者测试通过了但需求没满足。

它们擅长的一件事：给一个具体的成功标准，就会循环迭代直到通过。别告诉它怎么做，告诉它"完成"长什么样。

指出失败并不能阻止代理犯错。能阻止它的，是在动念那一刻可以套用的规则：何时该问的阈值、能在自己草稿里识别的坏味道清单、从一个失败的检查开始的循环，以及一套让"应该没问题"说不出口的汇报标准。这就是本仓库的内容。

## 五条规则

| 规则 | 防止什么 |
|---|---|
| **先校准** | 改个错别字也走全套流程，或者改数据库结构却什么都不做 |
| **1. 先弄懂再动手** | 悄悄做错误假设；以及反向失败：不读代码却反复盘问用户 |
| **2. 只做最少的** | 投机性抽象、没人要的选项、100 行能做的事写 1000 行 |
| **3. 只改任务需要的** | 顺手重排格式、改名、删掉自己不理解的代码 |
| **4. 先定义完成，再循环** | 没复现就说"修好了"；测试通过但没满足需求 |
| **5. 只汇报验证过的** | 什么都没跑就说"完成了，应该没问题" |

**先校准。** 显而易见的一行修改不走流程。常规修改：一句话说明假设、跑一次检查、简短汇报。模糊、大型或难以撤销的修改：先读周边代码，写出每步带检查的计划，动手前先摆出取舍。

**先弄懂再动手。** 先看、再决定、然后说。先读代码再提问，大多数"假设"在仓库里就能找到答案。用一句话复述任务。只有当不同理解会导致截然不同的工作、或操作难以撤销时才提问；否则一句话说明假设然后继续。提问时只问一个问题，并给出推荐答案。指出矛盾。有异议就说出来，用户坚持则照做。

**只做最少的。** 解决今天的问题，并附一份过度设计的坏味道清单（没人传的参数、只有一个实现的接口、包着不会失败的代码的 `try/except`、重新造轮子的标准库功能、复述代码的注释），让代理在自己的草稿里认出它们。简单不等于单薄：复用已有的辅助函数，保留边界校验和安全检查。

**只改任务需要的。** 每个改动块都能追溯到请求。不顺手重排格式、改名、加类型标注、加文档字符串、升依赖。遵循文件的现有风格；如果现有风格有害，指出来而不是照抄或悄悄修掉。汇报前重读一遍自己的 diff。

**先定义完成，再循环。** 把任务变成一个可运行的检查，先跑一次看它失败，再改代码，再跑一次。没有测试框架？用最便宜的信号。同一个失败出现三次就停下来汇报。测试通过不等于满足需求。

**只汇报验证过的。** "测试通过"意味着你真的跑了。把已验证、相信如此、跳过了三件事分开说。原样引用失败信息。如果没做完，第一句就说。保持简短。

完整文本见 [`skills/eagleminds-guidelines/SKILL.md`](skills/eagleminds-guidelines/SKILL.md)（约 140 行）。每条规则的前后对比示例见 [`references/examples.md`](skills/eagleminds-guidelines/references/examples.md)。按这些规则审查 diff 的技能见 [`skills/eagleminds-review/SKILL.md`](skills/eagleminds-review/SKILL.md)。

## 真的有效吗

简短回答：模型本来就能写出正确的代码。准则改变的是 diff 里还夹带了什么，以及请求模糊时代理是前进还是停住。

在一个小型 pytest 项目上做了三个任务，每个任务分别在有准则和无准则的情况下各跑一次，仓库副本相互隔离：

| 任务 | 无准则 | 有准则 |
|---|---|---|
| 修复缺少 email 时的崩溃 | 修复正确。但顺手改写了一条已有注释，而且新测试和修复一起提交，测试从未被看到失败过。新增 14 行。 | 同样的修复，注释原封不动，改动前先跑测试并看到它失败。新增 8 行。 |
| 给网络调用加重试 | 正确，但多出两个没人传的关键字参数、一个分类辅助函数和指数退避。新增 73 行。 | 固定 3 次尝试、间隔 1 秒，两个测试，先看到失败再修。新增 50 行。 |
| "我们需要能导出用户"，且用户不在场 | 停下来抛出四个问题的问卷。没有代码。 | 读代码，在已有的 `list` 旁边加了 `export` 命令，排除密码哈希，说明假设，完成验证。 |

两组运行使用相同的模型和提示。每个任务只跑了一次，请视为方向性结论。唯一显现的代价：有准则时的汇报长了大约三分之一，所以规则 5 现在要求保持简短。

## 常见问题

**什么是 CLAUDE.md？** 放在仓库根目录的 Markdown 文件，Claude Code 每次会话开始时读取，作为常驻指令。本仓库的 `CLAUDE.md` 只包含这些规则，可以直接追加到已有文件末尾。

**什么是 AGENTS.md？** CLAUDE.md 的跨工具等价物，OpenAI Codex、OpenCode、Gemini CLI、Amp、Devin、Jules 等都会读取。内容相同，文件名不同。

**这是谁做的？** EagleMinds，作者 [Shankar Venkat](https://github.com/shankar4jazz)。规则、示例、工具和测试均为原创，以 MIT 许可发布，可自由改用。

**小任务会被拖慢吗？** 设计上不会。技能的第一节就是校准表，告诉代理对显而易见的一行修改跳过所有流程。

**我可以加自己的项目规则吗？** 可以。在同一文件末尾追加 `## Project-Specific Guidelines` 段落，写上你的技术栈约定。规则本身刻意与技术栈无关。

**改了技能之后怎么保持各副本同步？** 只编辑 `skills/eagleminds-guidelines/SKILL.md`，然后运行 `python scripts/sync_guidelines.py`。任何生成文件过期，CI 都会失败。

## 许可

MIT，作者 EagleMinds（[Shankar Venkat](https://github.com/shankar4jazz)）。见 [LICENSE](LICENSE)。
