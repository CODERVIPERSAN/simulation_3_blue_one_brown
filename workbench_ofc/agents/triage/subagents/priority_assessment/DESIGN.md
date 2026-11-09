# Priority Assessment Agent — Design

![Light overview](diagram.png)

![Medium — tools + MCP](diagram_medium.png)

![Technical — I/O + MCP + schemas](diagram_technical.png)

## Role

Recommend incident priority (P1–P5) using severity signals, service criticality, and SLA policy.

## Inputs

- Incident severity / urgency fields
- Service criticality from Cognitive Bridge
- Active user or executive impact hints from Impact (if already available)

## Tools

`score_priority`, `get_service_criticality`, `get_sla_policy`
