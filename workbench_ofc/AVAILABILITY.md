# Availability — what exists vs what does not

This workbench is a **design pack**. It documents agents, tools, prompts, configs, and diagrams. It is **not** a running APSO system.

## Available now (in this repo)

| Item | Where |
|------|--------|
| Architecture index (orchestrator → agents → subagents → tools) | [`INDEX.md`](INDEX.md) |
| 15-section SPECs for orchestrator + 8 parent agents | `orchestrator/SPEC.md`, `agents/*/SPEC.md` |
| Shorter SPECs for 18 subagents | `agents/*/subagents/*/SPEC.md` |
| System prompts + YAML configs | `system_prompt.md`, `config.yaml` |
| Tool catalogues with technical I/O notes | `tools.md` (all parents) |
| Light overview diagrams | `diagram.png` (9 parents) |
| Medium technical diagrams | `diagram_medium.png` (9 parents) |
| Large technical diagrams | `diagram_technical.png` (9 parents) |
| Subagent diagrams (3 tiers each) | `subagents/*/diagram.png` + `_medium` + `_technical` (18×3) |
| Connector / MCP design catalogue | [`connectors/CONNECTIONS.md`](connectors/CONNECTIONS.md) |
| Why-not-an-agent image | `connectors/connectors-why-no-agent.png` |
| Diagram generator script | [`_diagrams/generate_tier_diagrams.py`](_diagrams/generate_tier_diagrams.py) |
| JSON Schema contracts (invoke/result/HITL/evidence + per-agent I/O) | [`schemas/`](schemas/README.md) |
| Example JSON messages | `schemas/*/examples/` |

## Not available

| Item | Status |
|------|--------|
| Runnable Master Orchestrator / agent runtime | **Not implemented** |
| Live MCP servers for ServiceNow, PagerDuty, Dynatrace, Splunk, etc. | **Not wired** |
| Real REST credentials or API clients | **None in this folder** |
| Executable Rundeck / Ansible / Azure Automation jobs | **Not present** |
| Working HITL UI, approval tokens, or kill-switch service | **Design only** |
| Cognitive Bridge as a live data store | **Described only** |
| End-to-end incident execution against a real ticket | **Cannot run from these docs alone** |
| Runtime JSON Schema validation against live traffic | **Schemas are design-only until a runtime exists** |

## How to read the diagrams

| File | Meaning |
|------|---------|
| `diagram.png` | Light — flow a human can skim (do not change) |
| `diagram_medium.png` | Same layout + tool descriptions + connectors + MCP requirements |
| `diagram_technical.png` | Same layout + full tool description with I/O + MCP + JSON schema paths |

Runtime status (what is/isn't implemented) lives only in this file — not as a badge on diagrams.
