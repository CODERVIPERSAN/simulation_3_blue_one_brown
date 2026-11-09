# Resolution Agent — tools

## Parent tools

| Tool | Description | Technical | Use when | Do not use when | Error |
|------|-------------|-----------|----------|-----------------|-------|
| `recommend_runbook` | Invoke Runbook Recommendation subagent | **In:** `diagnosis{}`, `service_id`. **Out:** `{runbooks[{id, score, summary}]}`. **Connector:** Bridge / ServiceNow KB. **Side effect:** read-only. | After Diagnostic hypothesis | No diagnosis packet | `No matching SOP` |
| `propose_self_heal` | Invoke Self-Healing subagent | **In:** `diagnosis{}`, preferred runbook?. **Out:** `{plan_steps[], blast_radius, confidence}`. **Connector:** Bridge + PagerDuty context. **Side effect:** propose only. | Automation candidate exists | Policy forbids auto-heal | `Cannot estimate blast radius` |
| `execute_automation` | Invoke Automation Execution after approval | **In:** `job_id`, `approval_token`, `params{}`. **Out:** `{execution_id, status}`. **Connector:** Rundeck / Ansible / Azure Automation. **Side effect:** **runs job**. | HITL Automation gate approved | Missing/expired token | `Approval required` / `Job failed` |
| `request_recovery_approval` | Ask Orchestrator for Recovery / Automation HITL | **In:** `plan{}`, `gate`. **Out:** `approval_request_id`. **Connector:** Orchestrator → Teams. **Side effect:** blocks until decision. | Before any execute | Already approved for this plan | `Gate not configured` |

## Subagent tools

| Tool | Description | Technical | Connector |
|------|-------------|-----------|-----------|
| `search_sop` | Search SOP / runbook library | **In:** query / tags. **Out:** docs[]. **Side effect:** read-only. | Cognitive Bridge / ServiceNow |
| `rank_runbooks` | Rank matches to diagnosis | **In:** candidates[], diagnosis. **Out:** ranked[]. **Side effect:** none. | local + Bridge |
| `build_fix_plan` | Structured fix steps | **In:** runbook + context. **Out:** steps[]. **Side effect:** none. | local |
| `estimate_blast_radius` | Who/what the fix can touch | **In:** plan, service map. **Out:** `{scope, risk}`. **Side effect:** read-only lookups. | Bridge / Dynatrace |
| `list_automation_jobs` | Jobs mapped to SOP | **In:** sop_id / tags. **Out:** jobs[]. **Side effect:** read-only. | Rundeck / Ansible / Azure Automation |
| `run_approved_job` | Execute one approved job | **In:** job_id, token, params. **Out:** execution_id. **Side effect:** **write/execute**. | Rundeck / Ansible / Azure Automation |
| `poll_job_status` | Poll execution status | **In:** execution_id. **Out:** `{status, logs?}`. **Side effect:** read-only. | same automation APIs |
