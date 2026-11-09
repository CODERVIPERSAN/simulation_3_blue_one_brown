# Diagnostic Agent — tools

## Parent tools

| Tool | Description | Technical | Use when | Do not use when | Error |
|------|-------------|-----------|----------|-----------------|-------|
| `run_log_analysis` | Invoke Log Analysis subagent | **In:** `incident_id`, `window`, `service?`. **Out:** `{clusters[], confidence}`. **Connector:** Splunk / app logs MCP. **Side effect:** read-only. | Errors / latency symptoms | No time window | `Query failed` |
| `run_change_analysis` | Invoke Change Analysis subagent | **In:** `incident_id`, `window`. **Out:** `{changes[], correlation}`. **Connector:** ServiceNow / Azure DevOps. **Side effect:** read-only. | Suspect recent deploy | No change source linked | `No changes in window` |
| `run_infra_analysis` | Invoke Infrastructure Analysis subagent | **In:** `hosts[]` / `resource_ids[]`. **Out:** `{signals[], anomalies[]}`. **Connector:** Azure Monitor / Dynatrace. **Side effect:** read-only. | Saturation / infra alerts | App-only symptom with no hosts | `Metrics unavailable` |
| `run_dependency_analysis` | Invoke Dependency Analysis subagent | **In:** `service_id`, `depth`. **Out:** `{upstream[], downstream[], failing[]}`. **Connector:** Dynatrace / Bridge. **Side effect:** read-only. | Cascade suspected | Service map missing | `Map unavailable` |
| `run_app_analysis` | Invoke Application Analysis subagent | **In:** `service_id`, `window`. **Out:** `{traces[], txn_errors[]}`. **Connector:** Dynatrace APM. **Side effect:** read-only. | App / txn failures | Infra-only outage | `APM empty` |
| `run_code_analysis` | Invoke Code Analysis subagent | **In:** `repos[]`, `window`. **Out:** `{commits[], suspects[]}`. **Connector:** GitHub / Azure DevOps. **Side effect:** read-only. | Deploy-correlated fault | No repo mapping | `No commits` |
| `propose_root_cause` | Publish ranked hypotheses + evidence ids | **In:** findings[]. **Out:** `{hypotheses[{rank, claim, evidence_ids, confidence}]}`. **Connector:** Orchestrator evidence. **Side effect:** evidence append. | Enough findings | Zero subagent results | `Empty findings` |
| `request_more_evidence` | Ask Orchestrator for another investigation pass | **In:** `gaps[]`, `focus`. **Out:** `loop_requested`. **Connector:** Orchestrator. **Side effect:** may open investigation loop. | Confidence below threshold | Loop budget exhausted | `Loop budget exceeded` |

## Subagent connector tools

| Tool | Description | Technical | Connector |
|------|-------------|-----------|-----------|
| `search_logs` | Run log query for window | **In:** query, from, to. **Out:** events / aggregations. **Side effect:** read-only. | Splunk / app logs |
| `summarise_error_cluster` | Cluster similar errors | **In:** events[]. **Out:** clusters with counts. **Side effect:** none (LLM+rules). | local + Splunk |
| `list_recent_changes` | Changes/releases in window | **In:** window, CI/service. **Out:** change list. **Side effect:** read-only. | ServiceNow / ADO |
| `get_change_risk` | Risk metadata for a change | **In:** `change_id`. **Out:** risk fields. **Side effect:** read-only. | ServiceNow |
| `get_host_metrics` | Host/resource golden metrics | **In:** ids, window. **Out:** timeseries. **Side effect:** read-only. | Azure Monitor / Dynatrace |
| `get_azure_alerts` | Active Azure alerts | **In:** scope, window. **Out:** alerts[]. **Side effect:** read-only. | Azure Monitor |
| `get_service_map` | Dependency graph | **In:** entity, depth. **Out:** graph. **Side effect:** read-only. | Dynatrace / Bridge |
| `list_failing_dependencies` | Unhealthy neighbors | **In:** entity. **Out:** failing nodes. **Side effect:** read-only. | Dynatrace |
| `get_apm_traces` | Sample traces | **In:** service, window. **Out:** traces[]. **Side effect:** read-only. | Dynatrace |
| `get_transaction_errors` | Business txn errors | **In:** service, window. **Out:** errors[]. **Side effect:** read-only. | Dynatrace |
| `list_recent_commits` | Commits in window | **In:** repo, window. **Out:** commits[]. **Side effect:** read-only. | GitHub / ADO |
| `diff_suspect_files` | Diff for a commit/PR | **In:** commit/PR id. **Out:** file diffs. **Side effect:** read-only. | GitHub / ADO |
