# AGENTS Workflow Contract

## 1) 仓库目标 / Definition of Done

本仓库通过 PR 驱动交付，目标是让每次改动都满足以下条件：

- 功能或修复需求在对应 PR 中有清晰描述；
- 本地与 CI 都执行同一套验证入口；
- CI 通过后才允许合并到 `main`；
- 不引入明文 secret、破坏性 git 操作或绕过流程行为。

只有当 PR 的 `Summary`、`Test plan`、`Risk` 填写完整且验证通过，才视为 Done。

## 2) 唯一验证命令

唯一权威验证入口：

```bash
bash scripts/verify.sh
```

本地自测和 GitHub Actions 必须运行同一个命令，不允许并行维护另一套“CI 专用”校验逻辑。

## 3) 强制规则（Hard Rules）

1. 禁止直推 `main`，一律走 feature/fix 分支 + PR。
2. 禁止 `git push --force` 到任何受保护或协作分支。
3. 禁止跳过 `scripts/verify.sh` 或弱化其校验来“放水”。
4. 禁止提交任何 secret（如 `.env`、token、私钥、密码）。
5. 禁止在本任务中混入无关重构，保持“一次 PR 一件事”。

## 4) PR 规则

- **分支命名**：`feat/<topic>`、`fix/<topic>`、`chore/<topic>`。
- **标题格式**：`type(scope): summary`（例如 `fix(verify): handle missing pyproject in bootstrap`）。
- **PR 描述必填三段**：
  - `Summary`：说明改动目的与结果；
  - `Test plan`：列出已执行命令与结果；
  - `Risk`：说明潜在影响与回滚策略。

## 5) 角色分工

- **你（仓库维护者）**：提供需求、处理必须网页交互的配置项、最终确认合并策略。
- **Cursor 本地 Agent**：实现代码、运行验证、提交分支、创建并维护 PR。
- **Codex GitHub App**：在 PR 打开后自动 review（comment/reaction），辅助发现风险。

## 6) Codex Review Guidelines（P0/P1/P2/P3）

### P0（阻断，必须修复）

- 明文 secret 入库（token、私钥、凭据）；
- 破坏分支安全流程（绕过 PR、force push 受保护分支）；
- 命令注入 / 代码执行风险（不安全 shell 拼接、未转义外部输入）；
- 关键校验被删除或强行短路导致“假绿”。

### P1（高优先，合并前应修复）

- 影响兼容性的行为变化且未说明迁移策略；
- 核心参数或默认行为出现显著变化（约 >=30%）且无验证；
- 测试被注释、删除或被跳过且缺少替代验证。

### P2（建议改进，可后续处理）

- 可读性、重复代码、日志和错误信息质量改进；
- 小规模结构优化，不影响当前正确性。

### P3（不建议拦截）

- 纯风格、拼写、排版等非功能性细节。

Codex 在 P3 级别问题上应倾向不阻断，避免噪音评论。
