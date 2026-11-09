# Verification Agent — tools

## Parent tools

| Tool | Description | Technical | Use when | Do not use when | Error |
|------|-------------|-----------|----------|-----------------|-------|
| `verify_health` | Invoke Health Verification | **In:** `service_id`, window. **Out:** `{pass, metrics[]}`. **Connector:** Dynatrace / Azure Monitor. **Side effect:** read-only. | After fix / always before declare | No service id | `Health API error` |
| `verify_business` | Invoke Business Validation | **In:** `service_id`, critical_flows[]. **Out:** `{pass, checks[]}`. **Connector:** Dynatrace synthetics / Bridge. **Side effect:** may trigger synthetic (read-ish). | After health lean-green | No flow catalog | `Synthetic failed to run` |
| `verify_risk` | Invoke Risk Validation | **In:** `service_id`, pre_baseline?. **Out:** `{pass, side_effects[]}`. **Connector:** Dynatrace / Azure / Splunk. **Side effect:** read-only. | After health+business | No baseline | `Compare unavailable` |
| `declare_stable` | Tell Orchestrator recovery looks good | **In:** evidence refs. **Out:** `stable=true`. **Connector:** Orchestrator. **Side effect:** evidence append. | All critical checks green | Any critical fail | `Checks incomplete` |
| `declare_unstable` | Tell Orchestrator recovery failed checks | **In:** failing checks[]. **Out:** `stable=false`. **Connector:** Orchestrator (may open recovery-failure loop). **Side effect:** evidence + loop signal. | Any critical fail | Soft warnings only | — |

## Subagent tools

| Tool | Description | Technical | Connector |
|------|-------------|-----------|-----------|
| `check_service_health` | Availability / golden signals | **In:** service_id, window. **Out:** health snapshot. **Side effect:** read-only. | Dynatrace / Azure Monitor |
| `check_slo_burn` | SLO burn rate | **In:** slo_id / service. **Out:** burn metrics. **Side effect:** read-only. | Dynatrace / Azure Monitor |
| `run_synthetic_check` | Trigger/read synthetic | **In:** check_id. **Out:** result. **Side effect:** may run check. | Dynatrace / Bridge |
| `check_key_transactions` | Critical txn success | **In:** service, txns[]. **Out:** pass/fail per txn. **Side effect:** read-only. | Dynatrace |
| `scan_downstream_health` | Neighbor health after fix | **In:** service, depth. **Out:** node health[]. **Side effect:** read-only. | Dynatrace |
| `compare_pre_post_metrics` | Pre vs post metrics | **In:** baseline_id, window. **Out:** deltas[]. **Side effect:** read-only. | Dynatrace / Azure / Splunk |
