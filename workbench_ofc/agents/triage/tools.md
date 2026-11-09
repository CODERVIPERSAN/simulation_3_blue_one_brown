# Triage Agent — tools

## Parent tools

| Tool | Description | Technical | Use when | Do not use when | Error |
|------|-------------|-----------|----------|-----------------|-------|
| `run_data_quality` | Runs Data Quality subagent; returns pass/fail + enriched context | **In:** `incident_id`. **Out:** `{pass, missing[], ci?, notes}`. **Connector:** ServiceNow + Bridge via subagent. **Side effect:** optional quality work note (propose/write per config). | Always first | After hard fail without new intake data | `Subagent timeout` |
| `run_priority_assessment` | Runs Priority subagent; returns P1–P5 + rationale | **In:** `incident_id`, `quality_context{}`. **Out:** `{priority, rationale, confidence}`. **Connector:** Bridge policy + ServiceNow SLA. **Side effect:** read-only. | After quality pass | When quality failed | `Missing severity or service` |
| `run_impact_assessment` | Runs Impact subagent; returns blast-radius summary | **In:** `incident_id`, `ci_or_service`. **Out:** `{impact_summary, downstream[], confidence}`. **Connector:** Dynatrace / Azure Monitor / Splunk / Bridge. **Side effect:** read-only. | After quality pass | When no service/CI exists | `Service map unavailable` |
| `propose_owner` | Resolves assignment group and on-call from CI / service | **In:** `ci_id` or `service_id`. **Out:** `{assignment_group, assigned_to?}`. **Connector:** ServiceNow CMDB + PagerDuty. **Side effect:** read-only (propose only). | After priority/impact | When quality failed | `No support group on CI` |
| `submit_triage_result` | Posts the triage packet to Orchestrator evidence | **In:** triage packet YAML/JSON. **Out:** `evidence_ref`. **Connector:** Orchestrator / Bridge. **Side effect:** evidence append. | When all required fields ready | Mid-flight while subagent running | `Incomplete packet` |

## Shared connector helpers (used by subagents)

| Tool | Description | Technical | Connector |
|------|-------------|-----------|-----------|
| `get_incident` | Read one ServiceNow incident | **In:** `number` or `sys_id`. **Out:** incident fields. **Side effect:** read-only. | ServiceNow API / MCP |
| `update_incident_quality_notes` | Append quality notes only | **In:** `incident_id`, `note`. **Out:** `ok`. **Side effect:** work-note write. | ServiceNow API / MCP |
| `validate_required_fields` | Check mandatory intake fields | **In:** incident dict + required list. **Out:** `{ok, missing[]}`. **Side effect:** none. | local rule + ServiceNow |
| `enrich_ci_context` | Pull CI + business service from CMDB | **In:** name/hints. **Out:** `{ci, business_service}` or empty. **Side effect:** read-only. | ServiceNow CMDB / Bridge |
| `score_priority` | Apply priority matrix | **In:** severity, urgency, criticality. **Out:** `P1–P5`. **Side effect:** none. | policy table / Bridge |
| `get_service_criticality` | Criticality tier of the service | **In:** `service_id`. **Out:** tier enum. **Side effect:** read-only. | Cognitive Bridge |
| `get_sla_policy` | SLA clock for the priority | **In:** `priority`. **Out:** SLA definition. **Side effect:** read-only. | ServiceNow |
| `get_service_map` | Upstream/downstream map | **In:** `entity_id`, `depth`. **Out:** graph nodes/edges. **Side effect:** read-only. | Dynatrace / Bridge |
| `get_affected_users_signal` | Rough user-impact signal | **In:** `service_id`, time window. **Out:** `{signal, sample}`. **Side effect:** read-only. | Splunk / Azure Monitor / Bridge |
| `list_downstream_services` | Dependents of the CI/service | **In:** `entity_id`. **Out:** service list. **Side effect:** read-only. | Dynatrace / Bridge |
| `find_assignment_group` | Support group for CI | **In:** `ci_id`. **Out:** group. **Side effect:** read-only. | ServiceNow |
| `find_on_call` | Current on-call for the group | **In:** `group` or schedule id. **Out:** user. **Side effect:** read-only. | PagerDuty |
