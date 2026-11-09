# Communication Agent — tools

| Tool | Description | Technical | Use when | Do not use when | Error |
|------|-------------|-----------|----------|-----------------|-------|
| `post_teams_update` | Post to the incident Teams channel | **In:** `channel_id`, `markdown`. **Out:** `message_id`. **Connector:** Microsoft Graph + MCP. **Side effect:** post message. | Bridge updates | Customer-only wording needed | `Channel not found` / `Graph deny` |
| `send_email` | Send email to a distribution list | **In:** `to[]`, `subject`, `body`. **Out:** `message_id`. **Connector:** Graph / SMTP + MCP. **Side effect:** send mail. | Formal stakeholder mail | Unverified recovery claim | `SMTP/Graph error` |
| `broadcast_status` | Standard status broadcast template | **In:** `template_id`, fields{}. **Out:** `message_id`. **Connector:** Teams / email. **Side effect:** send. | Cadence status ticks | Ad-hoc custom narrative | `Template missing` |
| `draft_executive_summary` | Short exec summary | **In:** evidence refs, audience=exec. **Out:** `{draft}`. **Connector:** none (LLM). **Side effect:** draft only unless auto-send allowed. | Exec ask / major incident | Before triage packet exists | `Insufficient facts` |
| `draft_customer_update` | External-safe wording draft | **In:** evidence refs, redaction rules. **Out:** `{draft}`. **Connector:** none (LLM) + policy. **Side effect:** draft only. | External comms needed | Internal bridge chat | `Policy redaction fail` |
