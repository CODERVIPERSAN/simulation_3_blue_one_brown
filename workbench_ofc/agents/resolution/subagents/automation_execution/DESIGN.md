# Automation Execution Agent — Design

![Light overview](diagram.png)

![Medium — tools + MCP](diagram_medium.png)

![Technical — I/O + MCP + schemas](diagram_technical.png)

## Role
Execute only an approved automation job and report status.

## Parent
Resolution Agent

## Tools
- `list_automation_jobs`
- `run_approved_job`
- `poll_job_status`
