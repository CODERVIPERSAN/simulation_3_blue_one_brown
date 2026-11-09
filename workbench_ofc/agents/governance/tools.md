# Governance Agent — tools

| Tool | Description | Technical | Use when | Do not use when | Error |
|------|-------------|-----------|----------|-----------------|-------|
| `validate_policy` | Check action against org policy pack | **In:** `action{}`, `policy_pack_id?`. **Out:** `{allow, violations[]}`. **Connector:** Bridge policy store. **Side effect:** read-only. | Before risky writes / automation | Cosmetic drafts | `Policy pack missing` |
| `score_confidence` | Score an agent packet 0–1 | **In:** packet{}, rubric?. **Out:** `{score, reasons[]}`. **Connector:** local rules + optional model. **Side effect:** none. | Before HITL / stage advance | Empty packet | `Malformed packet` |
| `write_audit_log` | Immutable audit entry | **In:** actor, action, payload_ref. **Out:** `audit_id`. **Connector:** Bridge / SIEM sink. **Side effect:** append-only write. | Every gated decision | High-volume chatter | `Audit sink down` |
| `enforce_approval` | Block or allow based on HITL token | **In:** `gate`, `approval_token`. **Out:** `{allowed}`. **Connector:** Orchestrator approval store. **Side effect:** none (gate). | Before execute / close / escalate | Informational messages | `Token invalid/expired` |
| `assess_risk` | Qualitative risk of a proposed fix | **In:** plan{}, blast_radius{}. **Out:** `{risk_level, notes}`. **Connector:** Bridge + maps (read). **Side effect:** read-only. | Before Recovery HITL | After job already ran | `Insufficient context` |
| `trigger_kill_switch` | Halt automation + agents for the incident | **In:** `incident_id`, `reason`. **Out:** `halted`. **Connector:** Orchestrator + automation cancel APIs. **Side effect:** **hard stop**. | Unsafe / runaway | Routine pause | `Already halted` |
