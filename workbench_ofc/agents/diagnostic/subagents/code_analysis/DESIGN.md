# Code Analysis Agent — Design

![Light overview](diagram.png)

![Medium — tools + MCP](diagram_medium.png)

![Technical — I/O + MCP + schemas](diagram_technical.png)

## Role
Identify suspect commits or deployments near the fault window.

## Parent
Diagnostic Agent

## Tools
- `list_recent_commits`
- `diff_suspect_files`
