# Agent Team Setup

[中文](README.md) | **English**

A Codex skill for configuring multi-agent teams: choose member models and reasoning effort, define responsibilities, dependencies, and file scopes, and preserve project handoffs and acceptance records.

Author: Glock

This is a workflow carried out by the main agent, not a standalone multi-agent service. Configuration, persistence, and execution are separate stages. By default, the agent shows the work split and waits for you to say "start" before executing.

## Features

- **Eight team presets** for small changes, everyday development, architecture, diagnosis, research checks, and critical reviews.
- **Two configuration interfaces**: an interactive in-conversation panel and a standalone HTML page for offline browser use.
- **Editable members**: roles, models, reasoning effort, tasks, write scopes, dependencies, and concurrency; choose automatic task decomposition or manual assignment.
- **Reusable custom presets**: save named member configurations and load them across projects, without carrying over project tasks or execution history.
- **Durable project records**: retain member identifiers, task ledgers, escalation and retry history, handoff summaries, and version-bound acceptance evidence.

## Installation

You need Git and a Codex environment that can load local skills. These commands use the default skill directory. If you set `CODEX_HOME`, use its `skills/agent-team-setup` directory instead.

### macOS / Linux

```bash
git clone https://github.com/Glock019/agent-team-setup.git "$HOME/.codex/skills/agent-team-setup"
```

### Windows PowerShell

```powershell
git clone https://github.com/Glock019/agent-team-setup.git (Join-Path $HOME '.codex\skills\agent-team-setup')
```

If the destination already exists, inspect it first and preserve local changes. Invoke `$agent-team-setup` on your next turn after installation. If the client has not discovered the skill, reopen the conversation or restart the client.

## Quick Start

Send this in your conversation:

```text
Use $agent-team-setup and open the in-conversation configuration panel.
Choose G, the everyday development team, with automatic task decomposition
and a maximum concurrency of 2. Show the work split and wait for "start".
```

1. Choose a preset and provide a project name, goal, and input location. Adjust members as needed.
2. Click "完成配置" (Complete configuration). After local validation, the page immediately displays a team-table preview. When the host supports submission, it sends the configuration to the main agent for verification and persistence.
3. After a successful save, the main agent returns the team table and a brief save result. Member assignment prompts are available on request.
4. Once you provide a concrete task, review the work split and say "start" to execute it.

Submission may trigger the application's own confirmation dialog. A preview or a "submission initiated" status is not proof of a saved file; rely on the main agent's save result. When the host interface is unavailable, or when using the offline browser page, import the configuration manually.

If your environment cannot display the interactive panel, use the text-only workflow:

```text
Use $agent-team-setup to configure preset G in text only.
The goal is to implement a login form in this project. Decompose the work
automatically, use a maximum concurrency of 2, and wait for "start".
```

## Team Presets

These configurations describe subagents. The main agent keeps its current model and owns requirements, decomposition, shared files, integration, and final acceptance.

| Short name | Full model ID |
|---|---|
| Sol | `gpt-6.1-sol` |
| Luna | `gpt-6-luna` |
| Astra | `gpt-6-astra` |

Each entry below is "model / reasoning effort / responsibility". The order corresponds to members 1, 2, and 3.

| Preset | Member configuration | Use case |
|---|---|---|
| A Lightweight pair | Luna / medium / scan; Luna / high / item-by-item checks | Scoped inspections and batch checks |
| B Implementation and review | Sol / high / implementation; Luna / high / review | Small changes and localized fixes |
| C Architecture and modules | Astra / high / architecture; Sol / high / core module; Luna / high / supporting module | Cross-module features and refactoring |
| D Diagnosis and repair | Astra / high / root cause; Luna / high / evidence; Sol / high / repair | Difficult failures, reproduction, and diagnosis |
| E Research consistency | Astra / high / methodology; Sol / high / code workflow; Luna / high / formulas and values | Manuscript, code, and experiment consistency |
| F Adversarial design review | Sol / high / proposal; Astra / xhigh / counterexamples; Luna / high / acceptance cases | Important designs and algorithm decisions |
| G Everyday development | Sol / high / implementation; Luna / high / independent review; Luna / medium / tests and reproduction | Recommended starting point for routine development |
| H Critical-change review | Sol / high / implementation; Astra / high / critical review; Luna / high / tests and reproduction | Critical interfaces, concurrency logic, and important algorithms |

For G/H, implementation and test preparation can run in parallel. Validation of new code must wait for the implementation artifact; final review then uses the code and same-version test evidence. Three members can work in stages under a concurrency limit of 2. A member with no independent testing task is not started merely to fill the team.

These are workflow recommendations, not benchmark-proven optimal combinations. Model and effort availability must be checked against the actual tools. Unsupported settings are reported rather than silently replaced. See [team presets](references/team-presets.md) for execution boundaries.

## Common Requests

These are conversational prompts, not shell commands.

| Purpose | Example |
|---|---|
| Browser interface | `Use $agent-team-setup and open the browser configuration page.` |
| Automatic decomposition | `Use the current team to fix this issue. Inputs are in src/. Decompose the work, show the assignments, and wait for "start".` |
| Assignment prompts | `Show the assignment prompt for each member of the current team.` |
| Save a preset | `Save the current team as a custom preset named "Everyday development".` |
| Load a preset | `Use the custom preset "Everyday development", show the assignments, and wait for "start".` |
| Restore a project | `Use $agent-team-setup to restore ./agent-team, show the handoff summary, and wait for "start".` |
| Progress | `Report team progress, separating completed work, pending acceptance, and blocked tasks.` |

## Project Records and Coordination

Project records normally live in the project's `agent-team/` directory, or another explicitly chosen durable location, rather than inside the installed skill.

| File | Purpose |
|---|---|
| `team.json` | Project identity, configuration revision, members, and coordination policies |
| `tasks.json` | Task IDs, dependencies, states, retries, and acceptance conditions |
| `events.jsonl` | Append-only configuration, authorization, escalation, failure, and retry events |
| `tasks/Txxx.md` | Per-task handoffs, evidence, and acceptance checklists |
| `handoff.md` | Latest configuration, progress, blockers, and next steps |

Restoration checks the existing records and displays a handoff summary, then waits for "start" by default. Configuration changes preserve existing tasks, escalation counts, and acceptance states. Member identifiers can persist across conversations; actual execution processes are not guaranteed to survive.

A member's completion report enters pending acceptance until the main agent checks the specific version and evidence. Each root task allows at most two automatic retries after the initial attempt, supported by new evidence or a concrete correction. Same-model effort increases follow notification and escalation-threshold rules. Model changes need separate authorization unless an explicit applicable permission already exists. See [project lifecycle](references/project-lifecycle.md).

## Requirements and Boundaries

- Executing members requires host-provided subagent tools. Without them, the main agent can only handle the work sequentially.
- The in-conversation panel requires an interactive host surface; direct submission also requires the corresponding host interface. The offline browser page does not call model services or automatically persist project records.
- The panel primarily uses Chinese labels. This English README provides equivalent usage guidance.
- Python 3 is used for rendering, preset management, and repository tests. These scripts use the standard library.
- File access, model availability, concurrency, and approval boundaries depend on the actual environment. The skill does not grant permissions, guarantee a monetary cap, or automatically publish or push projects.
- Concurrent writers should use separate worktrees or non-overlapping file scopes. Team records are not file locks.

## Repository Layout and Validation

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

Run the standard-library tests from the repository root:

```bash
python -B tests/test_config.py
```

The tests cover recommended model/effort combinations, context equivalence between render modes, and embedded-data escaping. They are not a full browser or real-host end-to-end test suite.

Maintainers can render a browser page after verifying environment capabilities and preparing a context JSON file:

```bash
python scripts/render_config.py --context verified-context.json --mode browser --output agent-team-browser.html
```

See [configuration panel](references/config-panel.md) for the context format and interaction checks, and [custom presets](references/custom-presets.md) for persistence rules. The detailed references are currently written in Chinese.
