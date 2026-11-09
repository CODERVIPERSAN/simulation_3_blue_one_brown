# Connectors — APIs, MCP, and when NOT to use an agent

Agents reason. Connectors fetch and write. If an existing API or MCP server already returns a fact or performs a single deterministic write, **do not invent an agent for that call**. Put it on a connector and let an agent call it as a tool.

```
Sources / tools  →  Connector (API or MCP)  →  Agent tool wrapper  →  Agent reasoning
```

---

## Idea of the connector layer

| Piece | Job |
|-------|-----|
| **REST / Graph / Query API** | Native vendor interface (ServiceNow Table API, PagerDuty REST, Splunk SPL, Dynatrace API, …) |
| **MCP server** | Same capability exposed as Model Context Protocol tools the agent runtime can discover |
| **Tool wrapper** | Thin description the LLM sees: one job, when to use, when not to, error text |
| **Cognitive Bridge** | Unified knowledge fabric that *indexes* connector data; Knowledge Agent reasons over it |

One physical system can appear as both REST and MCP. Prefer MCP for agent runtimes; keep REST for automation jobs and HITL scripts.

---

## Connector catalogue

### ITSM — ServiceNow

| Capability | Mode | Typical tools | Needs an agent? |
|------------|------|---------------|-----------------|
| Get / update incident | REST + MCP | `get_incident`, `update_resolution_notes`, `set_incident_resolved` | **No** — CRUD is the API |
| CMDB CI / service | REST + MCP | `enrich_ci_context`, `find_assignment_group` | **No** for lookup |
| Change records | REST + MCP | `list_recent_changes`, `get_change_risk` | Lookup = connector; *correlation* = Change Analysis Agent |
| Problem / known error | REST + MCP | `create_problem`, `link_known_error` | Write = connector; *whether* to create = Closure Agent |
| SLA / assignment | REST + MCP | `get_sla_policy` | **No** |

### Alerting — PagerDuty

| Capability | Mode | Tools | Needs an agent? |
|------------|------|-------|-----------------|
| On-call lookup | REST + MCP | `find_on_call` | **No** |
| Acknowledge / page | REST + MCP | acknowledge / escalate APIs | **No** for the call; **yes** for “should we escalate?” (Triage + Governance) |
| Trigger ingest | webhook → Orchestrator | — | Ingest is plumbing, not an agent |

### Observability

| System | Mode | Tools | Needs an agent? |
|--------|------|-------|-----------------|
| Dynatrace | REST + MCP | `get_service_map`, `get_apm_traces`, `check_service_health` | Fetch = connector; interpret = Diagnostic / Verification |
| Splunk | Query + MCP | `search_logs`, `summarise_error_cluster` (summarise may be LLM *inside* Log Analysis Agent) | Raw search = connector |
| Azure Monitor | REST + MCP | `get_host_metrics`, `get_azure_alerts`, `check_slo_burn` | **No** for metrics pull |
| Application logs | file / API + MCP | same as Splunk pattern | **No** for retrieval |

### Source & change

| System | Mode | Tools | Needs an agent? |
|--------|------|-------|-----------------|
| GitHub | REST + MCP | `list_recent_commits`, `diff_suspect_files` | Diff fetch = connector; blame hypothesis = Code Analysis Agent |
| Azure DevOps | REST + MCP | commits, releases | Same split |

### Automation (execution layer)

| System | Mode | Tools | Needs an agent? |
|--------|------|-------|-----------------|
| Rundeck | REST + MCP | `list_automation_jobs`, `run_approved_job`, `poll_job_status` | Run = connector; *choose + approve* = Resolution + HITL |
| Ansible | REST / AWX + MCP | same pattern | Same |
| Azure Automation | REST + MCP | same pattern | Same |
| Jenkins | REST + MCP | trigger / status | Prefer for build pipelines; incident fix jobs prefer Rundeck/Ansible |

### Communication

| System | Mode | Tools | Needs an agent? |
|--------|------|-------|-----------------|
| Microsoft Teams | Graph + MCP | `post_teams_update`, `broadcast_status` | Send = connector; wording = Communication Agent |
| Email | SMTP / Graph + MCP | `send_email` | Same |

### Cognitive Bridge (knowledge fabric)

| Store | Behind Bridge | Used by |
|-------|---------------|---------|
| Incidents & problems | ServiceNow | Knowledge, Closure |
| Changes | ServiceNow / ADO | Diagnostic |
| Code / commits | GitHub / ADO | Code Analysis |
| Logs & metrics | Splunk / Dynatrace / Azure | Diagnostic, Verification |
| Architecture | CMDB / wiki | Dependency, Knowledge |
| SOPs & runbooks | KB / Bridge | Resolution |
| Automation catalogue | SOP → Rundeck map | Resolution, Knowledge |

Bridge **reads/writes** are connectors. Choosing *what* to remember is Knowledge Agent work.

---

## Why these things do **not** need an agent

| Capability | Why a connector is enough |
|------------|---------------------------|
| Get incident by number | Deterministic CRUD; ACL already on ServiceNow |
| List on-call for a schedule | Single PagerDuty lookup |
| Pull CPU / error rate for a window | Metrics query; no judgement |
| Run job X after approval token exists | Automation API; judgement already happened at HITL |
| Post a pre-approved status template | Transport only |
| Fetch CMDB support group | Field lookup |
| Poll Rundeck job status | State machine, not reasoning |

## What **does** need an agent

| Capability | Why |
|------------|-----|
| Priority from conflicting signals | Judgement across severity, criticality, user impact |
| Root-cause hypothesis | Multi-source synthesis |
| Which runbook fits this failure | Ranking + context |
| Whether to open a problem record | Policy + pattern matching |
| Stakeholder wording for a half-known outage | Audience-aware drafting |
| When to kill-switch | Risk and policy reasoning |

**Rule of thumb:** if one API call with fixed inputs is the whole answer, it is a **connector**. If several facts must be weighed, it is an **agent** (calling connectors as tools).

---

## MCP packing suggestion

Expose one MCP server (or one server per vendor) with tools named exactly like the agent tool catalogues:

```
mcp://servicenow   → get_incident, update_*, create_problem, ...
mcp://pagerduty    → find_on_call, acknowledge_incident, ...
mcp://dynatrace    → get_service_map, get_apm_traces, check_service_health, ...
mcp://splunk       → search_logs, ...
mcp://azure_monitor→ get_host_metrics, get_azure_alerts, check_slo_burn, ...
mcp://github       → list_recent_commits, diff_suspect_files, ...
mcp://rundeck      → list_automation_jobs, run_approved_job, poll_job_status, ...
mcp://teams        → post_teams_update, broadcast_status, ...
mcp://bridge       → query_bridge, write_bridge, search_*, ...
```

Agents never hold vendor credentials; the connector runtime does.

---

## Image

See `connectors-why-no-agent.png` in this folder (and project root copy) for the visual: Agent vs Connector split.
