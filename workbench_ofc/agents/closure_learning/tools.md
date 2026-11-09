# Closure & Learning Agent — tools

## Parent tools

| Tool | Description | Technical | Use when | Do not use when | Error |
|------|-------------|-----------|----------|-----------------|-------|
| `draft_rca` | Invoke RCA Generation | **In:** `incident_id`, evidence pack. **Out:** `{rca_draft, timeline_ref}`. **Connector:** Bridge + ServiceNow. **Side effect:** draft only until approved. | After stable / human override | Before Verify | `Evidence incomplete` |
| `create_or_link_problem` | Invoke Problem Creation | **In:** RCA summary, known_error?. **Out:** `{problem_id, linked}`. **Connector:** ServiceNow Problem. **Side effect:** **create/link write**. | Recurring / major / policy says so | One-off with no problem need | `ACL deny` |
| `update_knowledge` | Invoke Knowledge Update | **In:** lessons{}, sop_notes?. **Out:** `{kb_ids[], bridge_ids[]}`. **Connector:** ServiceNow KB + Bridge. **Side effect:** write (may need Governance). | After RCA draft | Overwriting golden SOP without approval | `Governance block` |
| `close_incident` | Propose / apply resolution + resolve after HITL | **In:** resolution_code, notes, `approval_token`. **Out:** `{state}`. **Connector:** ServiceNow. **Side effect:** **resolve write** after Closure HITL. | Closure gate approved | Unstable verification | `Approval required` |

## Subagent tools

| Tool | Description | Technical | Connector |
|------|-------------|-----------|-----------|
| `compose_rca` | Build RCA narrative | **In:** evidence[]. **Out:** markdown/structured RCA. **Side effect:** none. | local + Bridge |
| `attach_timeline` | Attach chronological timeline | **In:** events[]. **Out:** timeline_ref. **Side effect:** Bridge/ServiceNow attach. | Bridge / ServiceNow |
| `create_problem` | Create problem record | **In:** fields{}. **Out:** problem_id. **Side effect:** write. | ServiceNow |
| `link_known_error` | Link KE to problem/incident | **In:** ids. **Out:** ok. **Side effect:** write. | ServiceNow |
| `upsert_kb_article` | Create/update KB | **In:** article{}. **Out:** kb_id. **Side effect:** write. | ServiceNow |
| `update_runbook_note` | Annotate runbook/SOP | **In:** sop_id, note. **Out:** ok. **Side effect:** write (gated). | Bridge / ServiceNow |
| `update_resolution_notes` | Set resolution notes | **In:** incident_id, notes. **Out:** ok. **Side effect:** write. | ServiceNow |
| `set_incident_resolved` | Set state Resolved/Closed | **In:** incident_id, code. **Out:** state. **Side effect:** write. | ServiceNow |
