# APSO Agentic AI Operations — Workbench Index

This folder is the first design layer for the APSO future-state architecture
shown in the two OFC diagrams. It is organised the same way the runtime will run:

1. **Orchestrator** plans and routes.
2. **Lifecycle agents** own one stage each.
3. **Shared agents** sit beside every stage.
4. **Connectors** are APIs and MCP servers — not agents.

```
Detect → Triage → Diagnose → Resolve → Verify → Close & Learn
```

---

## Folder map

```
workbench_ofc/
├── INDEX.md                          ← you are here
├── AVAILABILITY.md                   ← what exists vs not implemented
├── schemas/                          ← hard tier: JSON Schema for every communication
├── _diagrams/                        ← Manim generator for tier diagrams
├── connectors/                       ← APIs + MCP (no LLM when a call is enough)
├── orchestrator/                     ← Master Orchestrator (Incident Commander AI)
└── agents/
    ├── triage/                       ← Stage 1 — Intake & Triage
    ├── diagnostic/                   ← Stage 2 — Diagnose & Assess
    ├── resolution/                   ← Stage 3 — Resolve
    ├── verification/                 ← Stage 4 — Verify
    ├── closure_learning/             ← Stage 5 — Close & Follow-up
    ├── knowledge/                    ← Shared — Cognitive Bridge keeper
    ├── governance/                   ← Shared — policy, HITL, kill-switch
    └── communication/                ← Shared — stakeholder updates
```

**Availability:** see [`AVAILABILITY.md`](AVAILABILITY.md) — design docs and diagrams are present; no live runtime/MCP wiring.

Each **parent agent** (and the orchestrator) folder has:

| File | Purpose |
|------|---------|
| `diagram.png` | Light overview (flow + tool names) |
| `diagram_medium.png` | Medium technical (structure + tool groups + connectors) |
| `diagram_technical.png` | Large technical (tool I/O + write/read; design-only badge) |
| `SPEC.md` | **Canonical detailed design** — all **15 sections** (see standard below) |
| `DESIGN.md` | Short plain-language overview (embeds all three diagrams) |
| `system_prompt.md` | System prompt for the parent agent |
| `config.yaml` | Runtime config (model, confidence, HITL gates, connectors) |
| `tools.md` | Tool catalogue with Technical (inputs/outputs/connector/side-effects) |
| `subagents/<name>/` | Subagent `SPEC.md` + **3 diagrams** (`diagram.png` / `_medium` / `_technical`) + prompt + config |

**0 → 100 technical ladder**

| Level | Artifacts |
|------:|-----------|
| 0 (light) | `diagram.png` |
| 50 (medium) | `diagram_medium.png` + `DESIGN.md` |
| 100 (hard) | `diagram_technical.png` + `tools.md` Technical column + [`schemas/`](schemas/README.md) JSON Schema + examples |

JSON contracts for invoke/result/HITL/evidence and each agent’s `input.schema.json` / `output.schema.json` live under [`schemas/`](schemas/README.md).

### SPEC.md standard (15 sections)

Every parent agent and the orchestrator **must** include all of these headings in `SPEC.md`. Subagents use the same 15 headings in a shorter form.

1. Agent Identity  
2. Purpose & Goals  
3. Personality  
4. Intelligence  
5. Memory  
6. Knowledge  
7. Capabilities  
8. Tools & Integrations  
9. Autonomy Level  
10. Planning & Execution  
11. Communication  
12. Permissions & Control  
13. Trust & Safety  
14. Error & Recovery  
15. Performance Metrics  

**Worked example (fullest):** `agents/triage/SPEC.md`

---

## Layer 0 — Orchestrator

| Item | Detail |
|------|--------|
| **Name** | Master Orchestrator Agent (Incident Commander AI) |
| **Job** | Own the whole incident. Pick the next stage. Invoke agents. Hold evidence. Ask a human when a gate needs approval. Open investigation or recovery-failure loops. |
| **Does not** | Read raw logs itself, execute rundeck jobs itself, or invent a priority without Triage. |
| **Folder** | `orchestrator/` |

**Orchestrator tools**

| Tool | One job |
|------|---------|
| `invoke_agent` | Start one lifecycle or shared agent with a scoped brief |
| `collect_evidence` | Merge agent outputs into the incident evidence pack |
| `open_investigation_loop` | Re-run Diagnose when evidence is thin |
| `open_recovery_failure_loop` | Stop automation, escalate, reassess after a failed fix |
| `request_hitl_approval` | Route Priority / Recovery / Automation / Confirm / Closure to a human |
| `manual_takeover` | Hand the incident to an engineer and pause agents |
| `update_progress` | Write stage status to ServiceNow + Cognitive Bridge |
| `emergency_kill_switch` | Halt all agent and automation activity for this incident |

---

## Layer 1 — Lifecycle agents

### 1. Triage Agent — *is it real, how bad, who owns it?*

| Subagent | Job |
|----------|-----|
| Data Quality Agent | Validate ServiceNow intake fields and context |
| Priority Assessment Agent | Recommend P1–P5 from severity + impact signals |
| Impact Assessment Agent | Business + technical blast radius |

| Parent tools | Subagent tools |
|--------------|----------------|
| `run_data_quality` | `get_incident`, `validate_required_fields`, `enrich_ci_context`, `update_incident_quality_notes` |
| `run_priority_assessment` | `score_priority`, `get_service_criticality`, `get_sla_policy` |
| `run_impact_assessment` | `get_service_map`, `get_affected_users_signal`, `list_downstream_services` |
| `propose_owner` | `find_assignment_group`, `find_on_call` |
| `submit_triage_result` | — |

→ Detail: `agents/triage/`

---

### 2. Diagnostic Agent — *what broke and why?*

| Subagent | Job |
|----------|-----|
| Log Analysis Agent | Patterns, errors, spike windows in Splunk / app logs |
| Change Analysis Agent | Correlate recent changes / releases |
| Infrastructure Analysis Agent | Compute, network, storage health |
| Dependency Analysis Agent | Service map / upstream-downstream |
| Application Analysis Agent | APM traces, business transactions |
| Code Analysis Agent | Commits / deployments likely linked to the fault |

| Parent tools | Subagent tools (examples) |
|--------------|---------------------------|
| `run_log_analysis` | `search_logs`, `summarise_error_cluster` |
| `run_change_analysis` | `list_recent_changes`, `get_change_risk` |
| `run_infra_analysis` | `get_host_metrics`, `get_azure_alerts` |
| `run_dependency_analysis` | `get_service_map`, `list_failing_dependencies` |
| `run_app_analysis` | `get_apm_traces`, `get_transaction_errors` |
| `run_code_analysis` | `list_recent_commits`, `diff_suspect_files` |
| `propose_root_cause` | — |
| `request_more_evidence` | — |

→ Detail: `agents/diagnostic/`

---

### 3. Resolution Agent — *how do we fix it safely?*

| Subagent | Job |
|----------|-----|
| Runbook Recommendation Agent | Match SOP / runbook to the diagnosis |
| Self-Healing Agent | Propose automated fix steps |
| Automation Execution Agent | Invoke Rundeck / Ansible / Azure Automation after approval |

| Parent tools | Subagent tools |
|--------------|----------------|
| `recommend_runbook` | `search_sop`, `rank_runbooks` |
| `propose_self_heal` | `build_fix_plan`, `estimate_blast_radius` |
| `execute_automation` | `list_automation_jobs`, `run_approved_job`, `poll_job_status` |
| `request_recovery_approval` | — |

→ Detail: `agents/resolution/`

---

### 4. Verification Agent — *is it really recovered?*

| Subagent | Job |
|----------|-----|
| Health Verification Agent | Service availability and golden signals |
| Business Validation Agent | Critical business flows still work |
| Risk Validation Agent | Side effects on dependencies |

| Parent tools | Subagent tools |
|--------------|----------------|
| `verify_health` | `check_service_health`, `check_slo_burn` |
| `verify_business` | `run_synthetic_check`, `check_key_transactions` |
| `verify_risk` | `scan_downstream_health`, `compare_pre_post_metrics` |
| `declare_stable` / `declare_unstable` | — |

→ Detail: `agents/verification/`

---

### 5. Closure & Learning Agent — *close cleanly and keep the lesson*

| Subagent | Job |
|----------|-----|
| RCA Generation Agent | Draft root-cause write-up from evidence |
| Problem Creation Agent | Create / link problem + known error |
| Knowledge Update Agent | Update KB / SOP / Cognitive Bridge |

| Parent tools | Subagent tools |
|--------------|----------------|
| `draft_rca` | `compose_rca`, `attach_timeline` |
| `create_or_link_problem` | `create_problem`, `link_known_error` |
| `update_knowledge` | `upsert_kb_article`, `update_runbook_note` |
| `close_incident` | `update_resolution_notes`, `set_incident_resolved` |

→ Detail: `agents/closure_learning/`

---

## Layer 2 — Shared agents (cross-cutting)

| Agent | Job | Key tools |
|-------|-----|-----------|
| **Knowledge Agent** | Keep the Cognitive Bridge current | `query_bridge`, `write_bridge`, `search_rca_repo`, `search_automation_catalog` |
| **Governance Agent** | Policy, confidence, audit, kill-switch | `validate_policy`, `score_confidence`, `write_audit_log`, `enforce_approval`, `trigger_kill_switch` |
| **Communication Agent** | Stakeholder updates across the life of the incident | `post_teams_update`, `send_email`, `broadcast_status`, `draft_executive_summary` |

→ Detail: `agents/knowledge/`, `agents/governance/`, `agents/communication/`

---

## Layer 3 — Connectors (not agents)

These are **connections**. If an existing API or MCP server already returns the fact, do **not** invent an agent for that call. Agents reason; connectors fetch and write.

| Connector family | Examples | Mode |
|------------------|----------|------|
| ITSM | ServiceNow Incidents, Changes, Problems, CMDB | REST + MCP |
| Alerting | PagerDuty | REST + MCP |
| Observability | Dynatrace, Splunk, Azure Monitor, app logs | REST / Query + MCP |
| Source & change | Azure DevOps, GitHub | REST + MCP |
| Automation | Rundeck, Ansible, Azure Automation, Jenkins | REST + MCP |
| Comms | Microsoft Teams, Email | Graph / SMTP + MCP |

→ Full catalogue and “when not to use an agent”: `connectors/CONNECTIONS.md`

---

## HITL gates (always human)

1. Priority & escalation  
2. Recovery approach  
3. Automation execution  
4. Recovery confirmation  
5. Closure  

Manual takeover is available at any stage.

---

## Design layers in this workbench

| Layer | What it is | Where |
|-------|------------|-------|
| **First** | Index of orchestrator → agents → subagents → tools | this file |
| **Second** | Per-agent **SPEC.md** (15 sections), prompts, configs, tools | `agents/*`, `orchestrator/` |
| **Diagrams** | Light / medium / technical per parent **and** per subagent | `diagram*.png`, `subagents/*/diagram*.png` |
| **Schemas** | Hard-tier JSON Schema for every agent communication | [`schemas/`](schemas/README.md) |
| **Connectors** | APIs + MCP + why some things do **not** need an agent | `connectors/CONNECTIONS.md` + `connectors/connectors-why-no-agent.png` |
| **Availability** | What is in-repo vs not implemented | [`AVAILABILITY.md`](AVAILABILITY.md) |

---

## Suggested reading order

1. This `INDEX.md` (including SPEC standard) + [`AVAILABILITY.md`](AVAILABILITY.md)
2. `orchestrator/` (SPEC + three diagrams)
3. `agents/triage/` (worked example — fullest SPEC, tools Technical column, three diagrams, subagent diagrams)
4. Remaining lifecycle agents (`SPEC.md` + diagrams first)
5. Shared agents: knowledge, governance, communication
6. `connectors/CONNECTIONS.md` + `connectors/connectors-why-no-agent.png`
