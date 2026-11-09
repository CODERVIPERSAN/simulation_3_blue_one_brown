# Risk Validation Agent — Design

![Light overview](diagram.png)

![Medium — tools + MCP](diagram_medium.png)

![Technical — I/O + MCP + schemas](diagram_technical.png)

## Role
Look for side effects on dependencies after the fix.

## Parent
Verification Agent

## Tools
- `scan_downstream_health`
- `compare_pre_post_metrics`
