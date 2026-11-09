"""FINAL medium + technical diagrams (parents + subagents).

- Light diagrams are NOT regenerated.
- Same light layout: title, role, stage, left flow, right tools, footer.
- Medium: + connectors + MCP requirements.
- Technical: + full tool description + I/O + MCP + schema path.
- No "Design only" badges.
"""

from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Line, RoundedRectangle, Scene, Text, VGroup, config

config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080

INK = "#1C1917"
MUTED = "#57534E"
LINE = "#44403C"
PAPER = "#F6F3EC"
ACCENT = "#1F4E46"
NAVY = "#E7EEF5"
MINT = "#E4EFEA"
CLAY = "#F3E6D0"
SAND = "#F4EBD6"
CARD = "#FFFCF7"
LILAC = "#EDE7F6"


def box(title, subtitle=None, fill=CARD, width=3.0, height=0.72, title_size=16, sub_size=11):
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.1,
        fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=1.4,
    )
    label = Text(title, font_size=title_size, color=INK)
    if subtitle:
        detail = Text(subtitle, font_size=sub_size, color=MUTED)
        words = VGroup(label, detail).arrange(DOWN, buff=0.03)
        if words.width > width - 0.2:
            words.scale_to_fit_width(width - 0.2)
        words.move_to(rect)
        return VGroup(rect, words)
    if label.width > width - 0.2:
        label.scale_to_fit_width(width - 0.2)
    label.move_to(rect)
    return VGroup(rect, label)


def arrow_v(a, b):
    return Line(a.get_bottom(), b.get_top(), stroke_width=2, color=LINE).add_tip(tip_length=0.12)


# tools: list of (name, medium_desc, tech_desc_with_io)
PARENTS = {
    "orchestrator": {
        "title": "Master Orchestrator",
        "role": "Incident Commander AI — stage routing, evidence, HITL, loops",
        "stage": "Owns Detect → Triage → Diagnose → Resolve → Verify → Close",
        "left_m": [
            ("1  Pick next stage", "Lifecycle order unless policy skip", CARD),
            ("2  Invoke agent", "Scoped brief + incident id", CARD),
            ("3  Collect evidence", "Merge agent payloads", MINT),
            ("4  HITL or loop", "Gates · investigation · recovery-fail", CLAY),
            ("5  Update progress", "ServiceNow + Cognitive Bridge", CARD),
        ],
        "tools": [
            ("invoke_agent", "Start one specialist agent", "Start agent with brief — in: agent_id,incident_id,brief{} → run_id"),
            ("collect_evidence", "Merge outputs into evidence pack", "Append evidence — in: payload{} → evidence_version"),
            ("request_hitl_approval", "Send human approval gate", "HITL request — in: gate,packet{} → approval_request_id"),
            ("open_investigation_loop", "Re-run Diagnose for more proof", "Investigation loop — in: focus[] → loop_id"),
            ("open_recovery_failure_loop", "Stop bad automation path", "Recovery-fail loop — pause jobs + escalate"),
            ("update_progress", "Write stage summary", "Progress write — stage+summary → SN + Bridge"),
            ("emergency_kill_switch", "Halt all agent/automation", "Hard halt — in: reason → halted=true"),
        ],
        "connectors": "ServiceNow · PagerDuty · Cognitive Bridge · Teams/Email · automation cancel APIs",
        "mcp": "servicenow.incident.* · pagerduty.escalate · teams.post · bridge.evidence.write · automation.cancel",
        "schema": "schemas/shared/agent_invoke|result|evidence_pack|hitl_* · orchestrator/progress_update",
        "note_m": "Coordinates only — does not diagnose or execute Rundeck jobs itself.",
        "note_t": "HITL gates: Priority · Recovery · Automation · Confirm · Closure. manual_takeover anytime.",
    },
    "triage": {
        "title": "Triage Agent",
        "role": "Is it real? How bad? Who owns it?",
        "stage": "Stage 1 — Intake & Triage",
        "left_m": [
            ("Data Quality", "Validate intake + CI enrich", CARD),
            ("Priority Assessment", "Recommend P1–P5 + SLA", CARD),
            ("Impact Assessment", "Blast radius + downstream", CARD),
            ("Propose owner", "Assignment group + on-call", MINT),
            ("Submit triage result", "Packet → Orchestrator", CLAY),
        ],
        "tools": [
            ("run_data_quality", "Run Data Quality subagent; hard stop if fail", "Invoke DQA — incident_id → {pass, missing[], ci?}"),
            ("run_priority_assessment", "Recommend priority after quality pass", "Priority subagent — context → {priority, rationale, confidence}"),
            ("run_impact_assessment", "Estimate business/technical impact", "Impact subagent — ci/service → impact + downstream[]"),
            ("propose_owner", "Resolve group + on-call from CI", "Owner lookup — ci → {assignment_group, assigned_to?} READ"),
            ("submit_triage_result", "Hand triage packet to Orchestrator", "Submit packet — triage JSON → evidence_ref"),
        ],
        "connectors": "ServiceNow · PagerDuty · Bridge · Dynatrace · Azure Monitor · Splunk",
        "mcp": "servicenow.incident|cmdb|sla · pagerduty.oncall.read · bridge.criticality|policy · dynatrace.topology · azure.monitor · splunk.search",
        "schema": "schemas/triage/input|output.schema.json · shared agent_invoke|result",
        "note_m": "HITL on P1/P2 or low confidence. No root cause. No fixes.",
        "note_t": "Writes are propose_only; Orchestrator+HITL apply SN assignment. Subagents: DQA, Priority, Impact.",
    },
    "diagnostic": {
        "title": "Diagnostic Agent",
        "role": "What broke and why? Multi-source investigation",
        "stage": "Stage 2 — Diagnose & Assess",
        "left_m": [
            ("Log · Change", "Errors + recent releases", CARD),
            ("Infra · Dependency", "Health + cascade map", CARD),
            ("App · Code", "APM traces + commits", CARD),
            ("Propose root cause", "Ranked hypotheses + evidence", MINT),
            ("Need more evidence?", "Ask Orchestrator for loop", CLAY),
        ],
        "tools": [
            ("run_log_analysis", "Find error clusters in logs", "Log subagent — window → clusters[]  Splunk"),
            ("run_change_analysis", "Correlate changes/releases", "Change subagent — window → changes[]  SN/ADO"),
            ("run_infra_analysis", "Check host/cloud health", "Infra subagent — hosts → anomalies[]  Azure/DT"),
            ("run_dependency_analysis", "Map failing dependencies", "Dependency — service → failing[]  Dynatrace"),
            ("run_app_analysis", "Inspect APM / transactions", "App subagent — service → traces/errors  Dynatrace"),
            ("run_code_analysis", "Find suspect commits", "Code subagent — repo/window → commits/diffs"),
            ("propose_root_cause", "Publish ranked hypotheses", "Publish — findings → hypotheses[{rank,claim,evidence_ids}]"),
            ("request_more_evidence", "Request investigation loop", "Signal Orchestrator — gaps[] → loop_requested"),
        ],
        "connectors": "Splunk · Dynatrace · Azure Monitor · ServiceNow · GitHub/ADO · Bridge",
        "mcp": "splunk.search · dynatrace.* · azure.monitor.* · servicenow.change.read · github.* · azuredevops.*",
        "schema": "schemas/diagnostic/input|output.schema.json",
        "note_m": "Never executes remediation. Thin evidence → investigation loop.",
        "note_t": "Up to 3 parallel subagents. Output hypotheses must cite evidence_ids.",
    },
    "resolution": {
        "title": "Resolution Agent",
        "role": "How do we fix it safely?",
        "stage": "Stage 3 — Resolve",
        "left_m": [
            ("Runbook Recommendation", "Match SOP to diagnosis", CARD),
            ("Self-Healing proposal", "Steps + blast radius", CARD),
            ("HITL gates", "Recovery + Automation", CLAY),
            ("Automation Execution", "Rundeck / Ansible / AA", MINT),
        ],
        "tools": [
            ("recommend_runbook", "Search and rank matching SOPs", "Runbook subagent — diagnosis → runbooks[{id,score}]"),
            ("propose_self_heal", "Build fix plan without executing", "Self-heal — → plan_steps[] + blast_radius  propose-only"),
            ("request_recovery_approval", "Ask human before any job", "HITL — plan → approval_request_id (mandatory)"),
            ("execute_automation", "Run job only with approval token", "Execute — job_id+approval_token → execution_id WRITE"),
        ],
        "connectors": "Bridge · ServiceNow KB · Rundeck · Ansible · Azure Automation · PagerDuty",
        "mcp": "bridge.sop.search · rundeck.job.* · ansible.job.* · azure.automation.* · pagerduty.context.read",
        "schema": "schemas/resolution/input|output.schema.json · shared hitl_request|decision",
        "note_m": "No automation without HITL. Job failure → recovery-failure loop.",
        "note_t": "Subagents: Runbook, Self-Healing, Automation Execution. Token required for WRITE.",
    },
    "verification": {
        "title": "Verification Agent",
        "role": "Is it really recovered?",
        "stage": "Stage 4 — Verify",
        "left_m": [
            ("Health Verification", "Availability + golden signals", CARD),
            ("Business Validation", "Critical business flows", CARD),
            ("Risk Validation", "Downstream side effects", CARD),
            ("Declare stable / unstable", "Result → Orchestrator", MINT),
        ],
        "tools": [
            ("verify_health", "Check service health / SLO", "Health subagent — service → {pass, metrics[]}"),
            ("verify_business", "Check critical business flows", "Business subagent — flows → checks[]"),
            ("verify_risk", "Scan side effects after fix", "Risk subagent — baseline → side_effects[]"),
            ("declare_stable", "Tell Orchestrator recovery OK", "Stable signal — evidence_refs → Orchestrator"),
            ("declare_unstable", "Tell Orchestrator recovery failed", "Unstable — failing[] → open recovery-failure loop"),
        ],
        "connectors": "Dynatrace · Azure Monitor · Splunk · Bridge",
        "mcp": "dynatrace.health|synthetic|apm · azure.monitor.slo|metrics · splunk.search · bridge.flows.read",
        "schema": "schemas/verification/input|output.schema.json",
        "note_m": "Never closes the incident. Unstable → escalate via Orchestrator.",
        "note_t": "All critical checks must pass before declare_stable. Subagents: Health, Business, Risk.",
    },
    "closure_learning": {
        "title": "Closure & Learning Agent",
        "role": "Close cleanly and keep the lesson",
        "stage": "Stage 5 — Close & Follow-up",
        "left_m": [
            ("RCA Generation", "Draft RCA + timeline", CARD),
            ("Problem Creation", "Problem / known error", CARD),
            ("Knowledge Update", "KB / SOP / Bridge", CARD),
            ("Close incident", "After Closure HITL", MINT),
        ],
        "tools": [
            ("draft_rca", "Compose RCA from evidence", "RCA subagent — evidence → rca_draft + timeline_ref"),
            ("create_or_link_problem", "Create/link problem record", "Problem subagent — → problem_id WRITE"),
            ("update_knowledge", "Update KB / runbook / Bridge", "Knowledge subagent — → kb/bridge ids WRITE (gated)"),
            ("close_incident", "Resolve incident after HITL", "Close — approval_token + notes → state Resolved WRITE"),
        ],
        "connectors": "ServiceNow · Cognitive Bridge",
        "mcp": "servicenow.problem|kb|incident.resolve · bridge.rca|sop|fact.write",
        "schema": "schemas/closure_learning/input|output.schema.json · hitl_decision",
        "note_m": "Only after Verify stable (or human override). Closure gate mandatory.",
        "note_t": "Subagents: RCA, Problem Creation, Knowledge Update. No resolve without Closure token.",
    },
    "knowledge": {
        "title": "Knowledge Agent",
        "role": "Shared — Cognitive Bridge keeper",
        "stage": "Cross-cutting · all stages",
        "left_m": [
            ("Query bridge", "Retrieve scoped knowledge", CARD),
            ("Search libraries", "RCA · SOP · automation · arch", CARD),
            ("Write bridge", "Tagged facts + confidence", MINT),
            ("Governance check", "Block silent SOP overwrite", CLAY),
        ],
        "tools": [
            ("query_bridge", "Semantic/keyed Bridge lookup", "Query — query|key → hits[] + citations  READ"),
            ("search_rca_repo", "Find past RCAs", "RCA search — query → rca[]  READ"),
            ("search_sop_library", "Find SOPs / runbooks", "SOP search — query → docs[]  READ"),
            ("search_automation_catalog", "Find jobs mapped to SOPs", "Catalog — sop_id → jobs[]  READ"),
            ("search_architecture", "Architecture / dependency notes", "Arch search — service → notes  READ"),
            ("write_bridge", "Upsert a knowledge fact", "Write fact — fact+source+confidence → fact_id WRITE"),
        ],
        "connectors": "Cognitive Bridge · ServiceNow KB / CMDB notes",
        "mcp": "bridge.query|write · bridge.sop|rca|automation|arch.search · servicenow.kb.read",
        "schema": "schemas/knowledge/input|output.schema.json",
        "note_m": "Chooses which knowledge matters. Raw get-incident stays a connector.",
        "note_t": "write_bridge may require Governance. Never silently overwrite golden SOPs.",
    },
    "governance": {
        "title": "Governance Agent",
        "role": "Shared — policy, confidence, audit, kill-switch",
        "stage": "Cross-cutting · brake pedal",
        "left_m": [
            ("Validate policy", "Action vs policy pack", CARD),
            ("Score confidence", "Packet score 0–1", CARD),
            ("Enforce approval", "HITL token check", CLAY),
            ("Audit + kill-switch", "Immutable log / halt", MINT),
        ],
        "tools": [
            ("validate_policy", "Check action against policy", "Policy — action{} → {allow, violations[]}"),
            ("score_confidence", "Score agent packet 0–1", "Confidence — packet → {score, reasons[]}"),
            ("enforce_approval", "Allow/block by HITL token", "Enforce — gate+token → {allowed}"),
            ("assess_risk", "Qualitative risk of a fix plan", "Risk — plan → {risk_level, notes}"),
            ("write_audit_log", "Append immutable audit entry", "Audit — actor+action → audit_id"),
            ("trigger_kill_switch", "Halt agents and automation", "Kill-switch — reason → halted WRITE"),
        ],
        "connectors": "Bridge policy · Orchestrator approvals · automation cancel · audit sink",
        "mcp": "bridge.policy.read · orchestrator.approval.* · audit.append · automation.cancel",
        "schema": "schemas/governance/input|output.schema.json · hitl_*",
        "note_m": "Does not triage, diagnose, or fix — only controls and records.",
        "note_t": "Called before risky writes. Kill-switch is emergency path for the incident.",
    },
    "communication": {
        "title": "Communication Agent",
        "role": "Shared — stakeholder updates across the lifecycle",
        "stage": "Cross-cutting · voice of the incident",
        "left_m": [
            ("Audience fit", "Bridge / exec / customer", CARD),
            ("Draft from facts", "Evidence only — no invent", CARD),
            ("Send channel", "Teams / email / broadcast", MINT),
            ("Recovery rule", "Announce only after Verify", CLAY),
        ],
        "tools": [
            ("post_teams_update", "Post to incident Teams channel", "Teams post — channel+markdown → message_id WRITE"),
            ("send_email", "Email a distribution list", "Email — to/subject/body → message_id WRITE"),
            ("broadcast_status", "Send status template", "Broadcast — template_id+fields → send"),
            ("draft_executive_summary", "Short exec summary draft", "Exec draft — evidence → {draft}  no send by default"),
            ("draft_customer_update", "External-safe wording draft", "Customer draft — redacted {draft} only"),
        ],
        "connectors": "Microsoft Graph · SMTP · ServiceNow (context read)",
        "mcp": "teams.post · graph.mail.send · bridge.evidence.read",
        "schema": "schemas/communication/input|output.schema.json",
        "note_m": "Never invents ETA or root cause. Never changes technical state.",
        "note_t": "recovery_notice blocked until Verification stable (or human override).",
    },
}


class ParentMedium(Scene):
    agent_key = "triage"

    def construct(self):
        d = PARENTS[self.agent_key]
        self.camera.background_color = PAPER
        title = Text(d["title"] + "  ·  medium", font_size=28, color=INK).to_edge(UP, buff=0.2)
        role = Text(d["role"], font_size=14, color=MUTED).next_to(title, DOWN, buff=0.08)
        stage = box(d["stage"], fill=NAVY, width=min(6.5, 0.42 * len(d["stage"]) + 2), height=0.48, title_size=13)
        stage.next_to(role, DOWN, buff=0.1)

        left_h = Text("Inside this agent", font_size=14, color=ACCENT)
        left_boxes = VGroup(*[box(f"•  {t}", s, f, 5.2, 0.58, 14, 10) for t, s, f in d["left_m"]]).arrange(DOWN, buff=0.08)
        left = VGroup(left_h, left_boxes).arrange(DOWN, buff=0.06)
        left.next_to(stage, DOWN, buff=0.14).to_edge(LEFT, buff=0.35)

        right_h = Text("Tools  (what each does)", font_size=14, color=ACCENT)
        right_boxes = VGroup(
            *[
                box(f"•  {n}", desc, CLAY if i % 2 == 0 else SAND, 5.8, 0.55, 13, 10)
                for i, (n, desc, _) in enumerate(d["tools"])
            ]
        ).arrange(DOWN, buff=0.07)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.06)
        right.next_to(stage, DOWN, buff=0.14).to_edge(RIGHT, buff=0.3)

        # scale if too tall
        content = VGroup(left, right)
        if content.height > 5.0:
            content.scale_to_fit_height(5.0)
            left.next_to(stage, DOWN, buff=0.14).to_edge(LEFT, buff=0.35)
            right.next_to(stage, DOWN, buff=0.14).to_edge(RIGHT, buff=0.3)

        arrows = VGroup(*[arrow_v(left_boxes[i], left_boxes[i + 1]) for i in range(len(left_boxes) - 1)])
        conn = box("Connectors", d["connectors"], NAVY, 14.8, 0.48, 12, 10)
        mcp = box("MCP requirements", d["mcp"], LILAC, 14.8, 0.52, 11, 9)
        note = Text(d["note_m"], font_size=12, color=MUTED)
        foot = VGroup(conn, mcp, note).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.12)
        self.add(title, role, stage, left, right, arrows, foot)


class ParentTech(Scene):
    agent_key = "triage"

    def construct(self):
        d = PARENTS[self.agent_key]
        self.camera.background_color = PAPER
        title = Text(d["title"] + "  ·  technical", font_size=26, color=INK).to_edge(UP, buff=0.16)
        role = Text(d["role"], font_size=13, color=MUTED).next_to(title, DOWN, buff=0.05)
        stage = box(d["stage"], fill=NAVY, width=6.2, height=0.45, title_size=12)
        stage.next_to(role, DOWN, buff=0.08)

        left_h = Text("Inside / contracts", font_size=13, color=ACCENT)
        left_boxes = VGroup(*[box(f"•  {t}", s, f, 5.1, 0.52, 13, 9) for t, s, f in d["left_m"]]).arrange(DOWN, buff=0.06)
        left = VGroup(left_h, left_boxes).arrange(DOWN, buff=0.05)
        left.next_to(stage, DOWN, buff=0.1).to_edge(LEFT, buff=0.3)

        right_h = Text("Tools — description + I/O", font_size=13, color=ACCENT)
        right_boxes = VGroup(
            *[
                box(f"•  {n}", tech, CLAY if i % 2 == 0 else SAND, 6.0, 0.52, 12, 9)
                for i, (n, _, tech) in enumerate(d["tools"])
            ]
        ).arrange(DOWN, buff=0.055)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.05)
        right.next_to(stage, DOWN, buff=0.1).to_edge(RIGHT, buff=0.25)

        content = VGroup(left, right)
        if content.height > 4.8:
            content.scale_to_fit_height(4.8)
            left.next_to(stage, DOWN, buff=0.1).to_edge(LEFT, buff=0.3)
            right.next_to(stage, DOWN, buff=0.1).to_edge(RIGHT, buff=0.25)

        arrows = VGroup(*[arrow_v(left_boxes[i], left_boxes[i + 1]) for i in range(len(left_boxes) - 1)])
        schema = box("JSON Schema", d["schema"], MINT, 14.8, 0.42, 11, 9)
        mcp = box("MCP requirements", d["mcp"], LILAC, 14.8, 0.48, 10, 8)
        note = Text(d["note_t"], font_size=11, color=MUTED)
        foot = VGroup(schema, mcp, note).arrange(DOWN, buff=0.05).to_edge(DOWN, buff=0.08)
        self.add(title, role, stage, left, right, arrows, foot)


for _k in PARENTS:
    globals()[f"PMed_{_k}"] = type(f"PMed_{_k}", (ParentMedium,), {"agent_key": _k})
    globals()[f"PTech_{_k}"] = type(f"PTech_{_k}", (ParentTech,), {"agent_key": _k})


# ---- Subagents ----
# (parent, id, name, role, tools[(name, med_desc, tech_desc)], mcp, connectors)
SUBS = [
    ("triage", "data_quality", "Data Quality", "Validate ServiceNow intake and CI context",
     [("get_incident", "Read one SN incident", "Read incident — number|sys_id → fields  READ"),
      ("validate_required_fields", "Check mandatory intake fields", "Validate — fields+rules → {ok, missing[]}"),
      ("enrich_ci_context", "Enrich CI from CMDB", "CMDB enrich — hints → {ci, service?}  READ"),
      ("update_incident_quality_notes", "Append quality work note", "Work note — note → ok  WRITE")],
     "servicenow.incident.read · servicenow.cmdb.read · servicenow.incident.write_notes",
     "ServiceNow · Cognitive Bridge"),
    ("triage", "priority_assessment", "Priority Assessment", "Recommend P1–P5 from severity and criticality",
     [("score_priority", "Apply priority matrix", "Score — sev,urg,crit → P1-P5"),
      ("get_service_criticality", "Get service criticality tier", "Criticality — service_id → tier  READ"),
      ("get_sla_policy", "Get SLA for priority", "SLA — priority → sla{}  READ")],
     "bridge.criticality.read · bridge.policy.read · servicenow.sla.read",
     "Cognitive Bridge · ServiceNow"),
    ("triage", "impact_assessment", "Impact Assessment", "Business and technical blast radius",
     [("get_service_map", "Pull service dependency map", "Map — entity,depth → graph  READ"),
      ("get_affected_users_signal", "Estimate user impact signal", "Users — service,window → signal  READ"),
      ("list_downstream_services", "List dependent services", "Downstream — entity → services[]  READ")],
     "dynatrace.topology.read · azure.monitor.read · splunk.search · bridge.map.read",
     "Dynatrace · Azure Monitor · Splunk · Bridge"),
    ("diagnostic", "log_analysis", "Log Analysis", "Error clusters and spike windows",
     [("search_logs", "Query logs for incident window", "Search — query,from,to → events[]  READ"),
      ("summarise_error_cluster", "Cluster similar errors", "Cluster — events[] → clusters[]")],
     "splunk.search · applogs.query", "Splunk · Application logs"),
    ("diagnostic", "change_analysis", "Change Analysis", "Correlate recent changes and releases",
     [("list_recent_changes", "List changes in window", "Changes — window → changes[]  READ"),
      ("get_change_risk", "Read change risk metadata", "Risk — change_id → risk{}  READ")],
     "servicenow.change.read · azuredevops.release.read", "ServiceNow · Azure DevOps"),
    ("diagnostic", "infrastructure_analysis", "Infrastructure Analysis", "Compute, network, storage health",
     [("get_host_metrics", "Pull host/resource metrics", "Metrics — ids,window → series  READ"),
      ("get_azure_alerts", "List Azure Monitor alerts", "Alerts — scope → alerts[]  READ")],
     "azure.monitor.metrics · azure.monitor.alerts · dynatrace.metrics.read",
     "Azure Monitor · Dynatrace"),
    ("diagnostic", "dependency_analysis", "Dependency Analysis", "Upstream and downstream failures",
     [("get_service_map", "Get dependency graph", "Map — entity,depth → graph  READ"),
      ("list_failing_dependencies", "List unhealthy neighbors", "Failing — entity → failing[]  READ")],
     "dynatrace.topology.read · bridge.map.read", "Dynatrace · Cognitive Bridge"),
    ("diagnostic", "application_analysis", "Application Analysis", "APM traces and business transactions",
     [("get_apm_traces", "Sample APM traces", "Traces — service,window → traces[]  READ"),
      ("get_transaction_errors", "Get transaction errors", "Txn errors — service,window → errors[]  READ")],
     "dynatrace.apm.traces · dynatrace.apm.transactions", "Dynatrace"),
    ("diagnostic", "code_analysis", "Code Analysis", "Suspect commits and deployments",
     [("list_recent_commits", "List commits in window", "Commits — repo,window → commits[]  READ"),
      ("diff_suspect_files", "Diff suspect commit/PR", "Diff — commit → file diffs  READ")],
     "github.commits.read · github.diff.read · azuredevops.git.read", "GitHub · Azure DevOps"),
    ("resolution", "runbook_recommendation", "Runbook Recommendation", "Match SOP or runbook to diagnosis",
     [("search_sop", "Search SOP / runbook library", "Search — query → docs[]  READ"),
      ("rank_runbooks", "Rank SOPs against diagnosis", "Rank — candidates+diagnosis → ranked[]")],
     "bridge.sop.search · servicenow.kb.read", "Cognitive Bridge · ServiceNow"),
    ("resolution", "self_healing", "Self-Healing", "Propose automated fix plan and blast radius",
     [("build_fix_plan", "Build structured fix steps", "Plan — runbook+ctx → steps[]  propose-only"),
      ("estimate_blast_radius", "Estimate who/what fix touches", "Blast — plan → {scope,risk}  READ")],
     "bridge.map.read · dynatrace.topology.read · pagerduty.context.read",
     "Bridge · PagerDuty · Dynatrace"),
    ("resolution", "automation_execution", "Automation Execution", "Run approved automation jobs only",
     [("list_automation_jobs", "List jobs mapped to SOP", "List — sop_id → jobs[]  READ"),
      ("run_approved_job", "Execute approved job", "Run — job_id+token+params → execution_id WRITE"),
      ("poll_job_status", "Poll job execution status", "Poll — execution_id → status  READ")],
     "rundeck.job.read|execute · ansible.job.execute · azure.automation.execute",
     "Rundeck · Ansible · Azure Automation"),
    ("verification", "health_verification", "Health Verification", "Service availability and golden signals",
     [("check_service_health", "Check service availability", "Health — service → health{}  READ"),
      ("check_slo_burn", "Check SLO burn rate", "SLO — slo_id → burn{}  READ")],
     "dynatrace.health.read · azure.monitor.slo.read", "Dynatrace · Azure Monitor"),
    ("verification", "business_validation", "Business Validation", "Critical business flows still work",
     [("run_synthetic_check", "Run/read synthetic check", "Synthetic — check_id → result"),
      ("check_key_transactions", "Validate key transactions", "Txns — list → pass/fail  READ")],
     "dynatrace.synthetic.run · dynatrace.apm.transactions · bridge.flows.read",
     "Dynatrace · Bridge"),
    ("verification", "risk_validation", "Risk Validation", "Side effects on dependencies",
     [("scan_downstream_health", "Scan neighbor health", "Downstream — service,depth → nodes[]  READ"),
      ("compare_pre_post_metrics", "Compare pre vs post metrics", "Compare — baseline → deltas[]  READ")],
     "dynatrace.topology.read · azure.monitor.metrics · splunk.search",
     "Dynatrace · Azure Monitor · Splunk"),
    ("closure_learning", "rca_generation", "RCA Generation", "Draft RCA from evidence timeline",
     [("compose_rca", "Compose factual RCA draft", "Compose — evidence[] → rca_draft"),
      ("attach_timeline", "Attach chronological timeline", "Timeline — events[] → timeline_ref")],
     "bridge.evidence.read · servicenow.attachment.write · bridge.rca.write",
     "Bridge · ServiceNow"),
    ("closure_learning", "problem_creation", "Problem Creation", "Create or link problem and known error",
     [("create_problem", "Create problem record", "Create — fields{} → problem_id WRITE"),
      ("link_known_error", "Link known error record", "Link KE — ids → ok WRITE")],
     "servicenow.problem.create · servicenow.problem.link · servicenow.known_error.link",
     "ServiceNow"),
    ("closure_learning", "knowledge_update", "Knowledge Update", "Update KB, SOP notes, Cognitive Bridge",
     [("upsert_kb_article", "Create or update KB article", "KB upsert — article{} → kb_id WRITE"),
      ("update_runbook_note", "Annotate runbook / SOP", "SOP note — sop_id+note → ok WRITE")],
     "servicenow.kb.write · bridge.sop.annotate · bridge.fact.write",
     "ServiceNow · Cognitive Bridge"),
]


class SubMedium(Scene):
    meta = SUBS[0]

    def construct(self):
        parent, sid, name, role, tools, mcp, conns = self.meta
        self.camera.background_color = PAPER
        title = Text(f"{name}  ·  medium", font_size=28, color=INK).to_edge(UP, buff=0.22)
        role_t = Text(role, font_size=14, color=MUTED).next_to(title, DOWN, buff=0.08)
        stage = box(f"Subagent · parent {parent}", fill=NAVY, width=5.4, height=0.48, title_size=13)
        stage.next_to(role_t, DOWN, buff=0.1)

        left_h = Text("Inside this subagent", font_size=14, color=ACCENT)
        steps = VGroup(
            box("1  Receive brief", "Scoped task from parent", CARD, 5.1, 0.58, 14, 10),
            box("2  Call tools", "One job per tool", CARD, 5.1, 0.58, 14, 10),
            box("3  MCP / API hop", "Via connector layer", CLAY, 5.1, 0.58, 14, 10),
            box("4  Return result", "Payload back to parent", MINT, 5.1, 0.58, 14, 10),
        ).arrange(DOWN, buff=0.09)
        left = VGroup(left_h, steps).arrange(DOWN, buff=0.07)
        left.next_to(stage, DOWN, buff=0.14).to_edge(LEFT, buff=0.4)

        right_h = Text("Tools  (what each does)", font_size=14, color=ACCENT)
        right_boxes = VGroup(
            *[box(f"•  {n}", d, CLAY if i % 2 == 0 else SAND, 5.7, 0.58, 13, 10) for i, (n, d, _) in enumerate(tools)]
        ).arrange(DOWN, buff=0.09)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.07)
        right.next_to(stage, DOWN, buff=0.14).to_edge(RIGHT, buff=0.35)

        arrows = VGroup(*[arrow_v(steps[i], steps[i + 1]) for i in range(len(steps) - 1)])
        conn = box("Connectors", conns, NAVY, 14.8, 0.48, 12, 10)
        mcp_b = box("MCP requirements", mcp, LILAC, 14.8, 0.52, 11, 9)
        note = Text(f"Parent: {parent}  ·  returns structured result for parent evidence pack", font_size=12, color=MUTED)
        foot = VGroup(conn, mcp_b, note).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.14)
        self.add(title, role_t, stage, left, right, arrows, foot)


class SubTech(Scene):
    meta = SUBS[0]

    def construct(self):
        parent, sid, name, role, tools, mcp, conns = self.meta
        self.camera.background_color = PAPER
        title = Text(f"{name}  ·  technical", font_size=26, color=INK).to_edge(UP, buff=0.18)
        role_t = Text(role, font_size=13, color=MUTED).next_to(title, DOWN, buff=0.06)
        stage = box(f"Subagent · parent {parent}", fill=NAVY, width=5.4, height=0.45, title_size=12)
        stage.next_to(role_t, DOWN, buff=0.08)

        left_h = Text("Inside / contracts", font_size=13, color=ACCENT)
        steps = VGroup(
            box("1  Parent brief", f"Via {parent} invoke", CARD, 5.1, 0.52, 13, 9),
            box("2  Tool calls", "See Tool I/O →", CARD, 5.1, 0.52, 13, 9),
            box("3  MCP servers", "Required capabilities below", CLAY, 5.1, 0.52, 13, 9),
            box("4  Result to parent", "Structured JSON payload", MINT, 5.1, 0.52, 13, 9),
            box("5  Side effects", "READ unless marked WRITE", SAND, 5.1, 0.52, 13, 9),
        ).arrange(DOWN, buff=0.06)
        left = VGroup(left_h, steps).arrange(DOWN, buff=0.05)
        left.next_to(stage, DOWN, buff=0.1).to_edge(LEFT, buff=0.35)

        right_h = Text("Tools — description + I/O", font_size=13, color=ACCENT)
        right_boxes = VGroup(
            *[box(f"•  {n}", t, CLAY if i % 2 == 0 else SAND, 6.0, 0.52, 12, 9) for i, (n, _, t) in enumerate(tools)]
        ).arrange(DOWN, buff=0.06)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.05)
        right.next_to(stage, DOWN, buff=0.1).to_edge(RIGHT, buff=0.28)

        arrows = VGroup(*[arrow_v(steps[i], steps[i + 1]) for i in range(len(steps) - 1)])
        conn = box("Connectors", conns, NAVY, 14.8, 0.42, 11, 9)
        mcp_b = box("MCP requirements", mcp, LILAC, 14.8, 0.48, 10, 8)
        schema = box("Schemas", f"shared/agent_invoke|result · schemas/{parent}/ · parent tools.md", MINT, 14.8, 0.42, 10, 8)
        note = Text("Architecture aligned: subagent tools only; parent owns stage decision", font_size=11, color=MUTED)
        foot = VGroup(conn, mcp_b, schema, note).arrange(DOWN, buff=0.05).to_edge(DOWN, buff=0.1)
        self.add(title, role_t, stage, left, right, arrows, foot)


for meta in SUBS:
    p, s = meta[0], meta[1]
    globals()[f"SMed_{p}_{s}"] = type(f"SMed_{p}_{s}", (SubMedium,), {"meta": meta})
    globals()[f"STech_{p}_{s}"] = type(f"STech_{p}_{s}", (SubTech,), {"meta": meta})
