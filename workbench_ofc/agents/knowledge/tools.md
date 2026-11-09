# Knowledge Agent — tools

| Tool | Description | Technical | Do not use for | Error |
|------|-------------|-----------|----------------|-------|
| `query_bridge` | Semantic + keyed lookup across Cognitive Bridge | **In:** `query` or `key`, filters{}. **Out:** `{hits[], citations[]}`. **Connector:** Cognitive Bridge. **Side effect:** read-only. | Direct ServiceNow field update | `Bridge unavailable` |
| `write_bridge` | Upsert a knowledge fact with source tags | **In:** `fact{}`, `source_incident`, `confidence`. **Out:** `fact_id`. **Connector:** Cognitive Bridge. **Side effect:** write (Governance may require). | Silent overwrite of approved SOPs | `Governance block` |
| `search_rca_repo` | Find past RCAs | **In:** query / service. **Out:** rca[]. **Connector:** Bridge / ServiceNow. **Side effect:** read-only. | Creating a new problem record | `No matches` |
| `search_automation_catalog` | Find automation jobs mapped to SOPs | **In:** sop_id / tags. **Out:** jobs[]. **Connector:** Bridge automation catalogue. **Side effect:** read-only. | Executing a job | `Catalog empty` |
| `search_sop_library` | Find SOPs / runbooks | **In:** query / tags. **Out:** docs[]. **Connector:** Bridge / KB. **Side effect:** read-only. | Editing production runbooks without approval | `No matches` |
| `search_architecture` | Dependency / architecture notes | **In:** service / CI. **Out:** notes / graph refs. **Connector:** Bridge / CMDB notes. **Side effect:** read-only. | Live APM queries (use Dynatrace via Diagnostic) | `No architecture doc` |
