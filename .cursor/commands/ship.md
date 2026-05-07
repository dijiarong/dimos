# /ship - 一句话触发完整交付流程

用法：

`/ship <一句话需求>`

示例：

`/ship 修复登录接口在空参数时的 500 错误`

---

## 执行步骤（必须按顺序）

### 1) 准备与上下文检查

- 确认当前目录是仓库根目录。
- 读取 `AGENTS.md` 与 `.cursor/rules/00-workflow.mdc`。
- 运行 `git status`：
  - 在 `main` 且工作区干净：继续；
  - 在 `main` 且有改动：先与用户确认是否 stash 或新分支承接；
  - 不在 `main`：确认是否继续当前分支。

### 2) 新建工作分支

```bash
git fetch origin
git checkout -b <type>/<topic> origin/main
```

命名规则：

- 功能：`feat/<topic>`
- 修复：`fix/<topic>`
- 文档：`docs/<topic>`
- 工具链：`chore/<topic>`

### 3) 最小改动计划

- 把需求拆成 3-5 个最小任务。
- 仅改必要文件，避免无关重构。
- 若涉及 5+ 文件或跨多个子系统，先询问是否拆分多个 PR。

### 4) 实现

- 按任务顺序逐项完成。
- 每完成一项更新状态并自查影响面。

### 5) 本地验证（强制）

```bash
bash scripts/verify.sh
```

- 通过：进入下一步；
- 失败：进入“读报错 -> 最小修复 -> 重跑 verify”循环。

### 6) 整理改动

- 使用 `git diff --stat` 生成文件改动摘要；
- 只 `git add` 本次相关文件，禁止 `git add -A`。

### 7) 提交

提交信息格式：

```text
<type>: <一句话说明>

<可选：1-3 行，解释为什么改>
```

禁止对已推送提交执行 `--amend`，禁止 `--no-verify`。

### 8) 推送分支

```bash
git push -u origin <branch>
```

失败则立即汇报，不做 force push。

### 9) 创建 PR

```bash
gh pr create \
  --base main \
  --head <branch> \
  --title "<type>: <一句话>" \
  --body-file /tmp/pr-body-<branch>.md
```

PR 描述必须包含：`Summary`、`Test plan`、`Risk`、`Related`。

### 10) 设置自动合并（若仓库支持）

```bash
gh pr merge --auto --squash <pr-url>
```

若失败，记录并提示用户去仓库设置页启用。

### 11) 汇报收尾（固定结构）

- 改动文件及目的；
- 验证命令与结果；
- PR 链接；
- 仍需人工处理的待办。

---

## 中止与失败规则

- 任一步骤失败都先汇报状态，禁止静默重试。
- 用户要求中止时，保留当前分支并等待进一步指令。
- 严禁为了“流程走完”而跳过验证或放宽质量门槛。
