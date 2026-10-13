# Agent Team Setup

**中文** | [English](README.en.md)

为 Codex 配置多智能体团队的 Skill：选择成员模型与思考程度，安排职责、任务依赖和文件范围，并保存项目交接与验收记录。

作者：Glock

这是由主 Agent 执行的协作工作流，不是独立运行的多 Agent 服务。配置、保存和启动是不同阶段；默认先展示分工，等你说“开始”再执行。

## 功能概览

- **八套团队方案**：覆盖小改、日常开发、架构、故障诊断、科研核对和关键审查。
- **两种配置入口**：对话内交互页面，以及可离线打开的浏览器 HTML。
- **可编辑成员**：角色、模型、思考程度、任务、修改范围、依赖和并发数；支持自动拆分或手动派活。
- **可复用自定义方案**：命名保存成员组合，跨项目加载；不携带原项目的任务和运行历史。
- **持续项目记录**：保留成员编号、任务台账、升级与重试记录、交接摘要和版本绑定的验收证据。

## 安装

需要 Git，以及能够加载本地 Skill 的 Codex 环境。以下命令使用默认 Skill 目录；设置了 `CODEX_HOME` 时，请把目标改为该目录下的 `skills/agent-team-setup`。

### macOS / Linux

```bash
git clone https://github.com/Glock019/agent-team-setup.git "$HOME/.codex/skills/agent-team-setup"
```

### Windows PowerShell

```powershell
git clone https://github.com/Glock019/agent-team-setup.git (Join-Path $HOME '.codex\skills\agent-team-setup')
```

已有同名目录时，先检查其内容，不覆盖本地修改。安装后在下一轮对话中调用 `$agent-team-setup`；如果客户端尚未识别该 Skill，重新打开会话或重启客户端。

## 快速开始

在对话中输入：

```text
使用 $agent-team-setup，打开对话内配置。
采用 G 日常开发三岗位，主 Agent 自动拆分，最大并发2。
先展示分工，等我说“开始”再执行。
```

1. 选择团队方案，填写项目名称、目标与材料位置，按需调整成员。
2. 点击“完成配置”。页面校验通过后立即显示团队表预览；支持宿主提交接口时，将配置交给主 Agent 核对并保存。
3. 主 Agent 保存成功后返回团队表与保存结果，派活提示词按需查看。
4. 提供具体任务后检查分工，再说“开始”启动执行。

页面提交可能触发应用自身的发送确认。预览或“已发起提交”不代表文件已经保存，以主 Agent 的保存结果为准。宿主接口缺失或使用离线浏览器版时，需要手动导入配置。

如果环境不能显示交互页面，可使用纯文字入口：

```text
使用 $agent-team-setup，以纯文字配置 G。
目标是为当前项目实现登录表单，自动拆分，最大并发2，等待“开始”。
```

## 团队方案

以下均为子成员配置，主 Agent 保持当前模型，负责需求、任务拆分、公共文件、集成和最终验收。

| 简称 | 完整模型 ID |
|---|---|
| Sol | `gpt-6.1-sol` |
| Luna | `gpt-6-luna` |
| Astra | `gpt-6-astra` |

表中每项格式为“模型 · 思考程度 · 职责”，排列顺序对应成员1、成员2、成员3。

| 方案 | 成员配置 | 适用场景 |
|---|---|---|
| A 轻量双人协作 | Luna · medium · 扫描；Luna · high · 逐项核对 | 小范围检查、批量核对 |
| B 实现与独立审查 | Sol · high · 实现；Luna · high · 审查 | 小改、局部缺陷修复 |
| C 架构与模块开发 | Astra · high · 架构；Sol · high · 核心模块；Luna · high · 配套模块 | 跨模块功能、重构 |
| D 故障定位与修复 | Astra · high · 根因；Luna · high · 证据；Sol · high · 修复 | 疑难故障、复现与诊断 |
| E 科研代码与稿件核对 | Astra · high · 方法；Sol · high · 代码流程；Luna · high · 公式与数值 | 论文、代码和实验一致性 |
| F 对抗式方案审查 | Sol · high · 方案；Astra · xhigh · 反例；Luna · high · 验收用例 | 重要设计和算法论证 |
| G 日常开发三岗位 | Sol · high · 实现；Luna · high · 独立审查；Luna · medium · 测试与复现 | 常规开发推荐起点 |
| H 关键改动审查 | Sol · high · 实现；Astra · high · 关键审查；Luna · high · 测试与复现 | 关键接口、并发逻辑、重要算法 |

G/H 中，实现和测试准备可以并行；验证新代码必须等待实现产物，最终审查再结合代码与同版本测试证据。三名成员可在并发上限为2时分阶段工作；没有独立测试任务时不启动空岗位。

这些是工作流建议，不是经过基准测试的最优配方。模型与思考程度需按实际工具能力核对；不可用时明确说明，不静默换模型。完整执行边界见 [团队预设](references/team-presets.md)。

## 常用指令

以下是对话提示词，不是终端命令。

| 目的 | 示例 |
|---|---|
| 浏览器版 | `使用 $agent-team-setup，打开浏览器配置。` |
| 自动拆分 | `沿用当前团队，目标是修复这个问题，材料在 src/；自动拆分，展示分工后等我说“开始”。` |
| 查看提示词 | `展示当前团队每位成员的派活提示词。` |
| 保存方案 | `将当前团队保存为自定义方案“日常开发”。` |
| 加载方案 | `使用自定义方案“日常开发”，展示分工后等待“开始”。` |
| 恢复项目 | `使用 $agent-team-setup 恢复 ./agent-team，展示交接摘要，等待“开始”。` |
| 查看进度 | `汇报当前团队进度，区分已完成、待验收和阻塞事项。` |

## 项目记录与协作规则

项目记录默认放在项目的 `agent-team/`，也可指定其他持久位置；不会写入 Skill 自身目录。

| 文件 | 用途 |
|---|---|
| `team.json` | 项目标识、配置版本、成员与协作策略 |
| `tasks.json` | 任务编号、依赖、状态、重试与验收条件 |
| `events.jsonl` | 追加式配置、授权、升级、失败与重试事件 |
| `tasks/Txxx.md` | 单项任务的交接、证据与验收清单 |
| `handoff.md` | 最新配置、进展、阻碍与下一步 |

恢复项目时先核对原记录、展示交接摘要，再按默认规则等待“开始”。修改配置不重置已有任务、升级计数或验收状态。记录中的成员编号可延续，实际执行进程不保证跨对话存活。

成员自报完成先进入待验收，由主 Agent 检查具体版本与证据后确认。每个根任务失败后默认最多自动重试两次，且须有新证据或具体修正。同模型提高思考程度遵循告知与升级阈值规则；更换模型需单独授权，除非已有明确适用的许可。详见 [项目生命周期](references/project-lifecycle.md)。

## 运行要求与边界

- 真正启动成员需要宿主提供子 Agent 工具；没有该工具时，只能由主 Agent 顺序处理。
- 对话内页面需要宿主支持交互显示；直接提交还需要对应的宿主接口。离线浏览器页不会调用模型服务或自动保存项目记录。
- 页面主要使用中文标签；英文 README 提供等效使用说明。
- Python 3 用于页面渲染、方案管理和仓库测试，这些脚本使用标准库。
- 文件访问、模型可用性、并发和授权边界由实际环境决定，Skill 不增加权限、不保证金额封顶，也不会自动发布或推送项目。
- 多人写入应使用独立 worktree 或互不重叠的文件范围；团队记录不是文件锁。

## 仓库结构与验证

```text
agent-team-setup/
|-- README.md
|-- README.en.md
|-- SKILL.md
|-- agents/openai.yaml
|-- assets/icon.svg
|-- assets/team-config.html
|-- references/
|-- scripts/render_config.py
|-- scripts/manage_presets.py
`-- tests/test_config.py
```

从仓库根目录运行标准库测试：

```bash
python -B tests/test_config.py
```

测试覆盖推荐方案的模型与强度、两种渲染模式的上下文一致性和嵌入数据转义，不等于完整浏览器或真实宿主端到端验证。

维护者可在核实环境能力、准备上下文 JSON 后生成浏览器页：

```bash
python scripts/render_config.py --context verified-context.json --mode browser --output agent-team-browser.html
```

上下文格式及交互验证要求见 [配置页面](references/config-panel.md)；自定义方案的保存规则见 [自定义方案](references/custom-presets.md)。
