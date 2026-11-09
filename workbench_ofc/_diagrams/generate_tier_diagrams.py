"""Medium + technical diagrams in the same visual language as light diagram.png."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Line,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
    config,
)

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
ROSE = "#F5E6E6"


def box(title, subtitle=None, fill=CARD, width=3.0, height=0.72, title_size=17, sub_size=12):
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.1,
        fill_color=fill,
        fill_opacity=1,
        stroke_color=INK,
        stroke_width=1.4,
    )
    label = Text(title, font_size=title_size, color=INK)
    if subtitle:
        detail = Text(subtitle, font_size=sub_size, color=MUTED)
        words = VGroup(label, detail).arrange(DOWN, buff=0.04)
        if words.width > width - 0.22:
            words.scale_to_fit_width(width - 0.22)
        words.move_to(rect)
        return VGroup(rect, words)
    if label.width > width - 0.22:
        label.scale_to_fit_width(width - 0.22)
    label.move_to(rect)
    return VGroup(rect, label)


def arrow_v(a, b):
    return Line(a.get_bottom(), b.get_top(), stroke_width=2, color=LINE).add_tip(tip_length=0.12)


# Same shape as light diagrams: title, role, stage chip, left flow, right tools, footer.
# Medium adds connector strip; technical adds I/O lines + schema footer.

PARENTS = {
    "orchestrator": {
        "title": "Master Orchestrator",
        "role": "Incident Commander AI — plans stages, routes agents, holds evidence",
        "stage": "Owns Detect → Close lifecycle",
        "medium_left": [
            ("1  Pick next stage", "Triage → Diagnose → Resolve → Verify → Close", CARD),
            ("2  Invoke agent", "Scoped brief + incident id", CARD),
            ("3  Collect evidence", "Merge agent JSON into pack", MINT),
            ("4  HITL or loop", "Approval · investigation · recovery-fail", CLAY),
            ("5  Update progress", "ServiceNow + Cognitive Bridge", CARD),
        ],
        "medium_right": [
            ("invoke_agent", "Start one specialist"),
            ("collect_evidence", "Append evidence_version"),
            ("request_hitl_approval", "Gate packet → Teams"),
            ("open_*_loop", "Re-diagnose / stop automation"),
            ("emergency_kill_switch", "Hard halt"),
        ],
        "medium_connectors": "ServiceNow · PagerDuty · Bridge · Teams/Email · automation cancel",
        "medium_note": "Does not diagnose or execute jobs — only coordinates.",
        "tech_left": [
            ("Invoke", "agent_invoke.schema → run_id", CARD),
            ("Evidence", "collect → evidence_pack.version++", MINT),
            ("HITL", "hitl_request ↔ hitl_decision + token", CLAY),
            ("Loops", "investigation / recovery_failure budgets", CARD),
            ("Progress", "progress_update.schema → SN write", NAVY),
        ],
        "tech_right": [
            ("invoke_agent", "in: agent_id, brief{}  out: run_id"),
            ("collect_evidence", "in: payload{}  out: evidence_version"),
            ("request_hitl_approval", "in: gate, packet{}  out: request_id"),
            ("open_investigation_loop", "in: focus[]  out: loop_id"),
            ("emergency_kill_switch", "in: reason  out: halted=true"),
        ],
        "tech_schema": "schemas/shared/* · schemas/orchestrator/progress_update.schema.json",
        "tech_note": "Design only — no runtime. Write mode via connectors after HITL.",
    },
    "triage": {
        "title": "Triage Agent",
        "role": "Is it real? How bad? Who owns it?",
        "stage": "Stage 1 — Intake & Triage",
        "medium_left": [
            ("Data Quality", "Validate intake + CI enrich", CARD),
            ("Priority Assessment", "P1–P5 from matrix + SLA", CARD),
            ("Impact Assessment", "Blast radius + downstream", CARD),
            ("Propose owner", "Assignment group + on-call", MINT),
            ("Submit triage result", "Packet → Orchestrator", CLAY),
        ],
        "medium_right": [
            ("run_data_quality", "Hard stop if fail"),
            ("run_priority_assessment", "After quality pass"),
            ("run_impact_assessment", "Parallel with priority"),
            ("propose_owner", "CMDB + PagerDuty"),
            ("submit_triage_result", "Evidence packet"),
        ],
        "medium_connectors": "ServiceNow · PagerDuty · Bridge · Dynatrace · Azure Monitor · Splunk",
        "medium_note": "HITL on P1/P2 or low confidence. No root cause, no fixes.",
        "tech_left": [
            ("Quality gate", "pass|fail + missing[]", CARD),
            ("Priority", "enum P1–P5 + confidence", CARD),
            ("Impact", "summary + downstream[]", CARD),
            ("Owner", "group + assigned_to?", MINT),
            ("Output schema", "triage/output.schema.json", CLAY),
        ],
        "tech_right": [
            ("run_data_quality", "incident_id → {pass, missing[], ci?}"),
            ("run_priority_assessment", "context → {priority, confidence}"),
            ("run_impact_assessment", "ci → impact + downstream[]"),
            ("propose_owner", "ci → group + on-call  (read)"),
            ("submit_triage_result", "packet → evidence_ref"),
        ],
        "tech_schema": "schemas/triage/input|output.schema.json · shared agent_invoke/result",
        "tech_note": "Design only — propose_only writes; HITL applies SN assign.",
    },
    "diagnostic": {
        "title": "Diagnostic Agent",
        "role": "What broke and why?",
        "stage": "Stage 2 — Diagnose & Assess",
        "medium_left": [
            ("Log · Change", "Errors + recent releases", CARD),
            ("Infra · Dependency", "Health + cascade map", CARD),
            ("App · Code", "APM traces + commits", CARD),
            ("Propose root cause", "Ranked hypotheses", MINT),
            ("Need more evidence?", "Investigation loop", CLAY),
        ],
        "medium_right": [
            ("run_log_analysis", "Splunk / app logs"),
            ("run_change_analysis", "ServiceNow / ADO"),
            ("run_infra / dependency", "Azure / Dynatrace"),
            ("run_app / code", "APM + GitHub"),
            ("propose_root_cause", "evidence_ids[]"),
        ],
        "medium_connectors": "Splunk · Dynatrace · Azure Monitor · ServiceNow · GitHub/ADO · Bridge",
        "medium_note": "Never executes remediation. Thin evidence → Orchestrator loop.",
        "tech_left": [
            ("Subagents ×6", "parallel up to 3", CARD),
            ("Hypothesis", "rank, claim, confidence", MINT),
            ("Evidence ids", "cite connector refs", CARD),
            ("Gaps", "needs_more_evidence bool", CLAY),
            ("Output schema", "diagnostic/output.schema.json", NAVY),
        ],
        "tech_right": [
            ("run_log_analysis", "window → clusters[]"),
            ("run_change_analysis", "window → changes[]"),
            ("run_infra_analysis", "hosts → anomalies[]"),
            ("run_*_analysis", "service → traces/commits"),
            ("propose_root_cause", "findings → hypotheses[]"),
        ],
        "tech_schema": "schemas/diagnostic/input|output.schema.json",
        "tech_note": "Design only — read-only connectors; no fix execution.",
    },
    "resolution": {
        "title": "Resolution Agent",
        "role": "How do we fix it safely?",
        "stage": "Stage 3 — Resolve",
        "medium_left": [
            ("Runbook Recommendation", "Match SOP to diagnosis", CARD),
            ("Self-Healing proposal", "Steps + blast radius", CARD),
            ("HITL gates", "Recovery + Automation", CLAY),
            ("Automation Execution", "Rundeck / Ansible / AA", MINT),
        ],
        "medium_right": [
            ("recommend_runbook", "search + rank SOPs"),
            ("propose_self_heal", "plan only"),
            ("request_recovery_approval", "Mandatory HITL"),
            ("execute_automation", "Token required"),
            ("poll_job_status", "queued→succeeded"),
        ],
        "medium_connectors": "Bridge · ServiceNow KB · Rundeck · Ansible · Azure Automation · PagerDuty",
        "medium_note": "No job without HITL. Failure → recovery-failure loop.",
        "tech_left": [
            ("mode", "plan_only | awaiting | executed", CARD),
            ("fix_plan", "steps[] + risk_level", CARD),
            ("approval_token", "from hitl_decision", CLAY),
            ("execution", "job_id + execution_id", MINT),
            ("Output schema", "resolution/output.schema.json", NAVY),
        ],
        "tech_right": [
            ("recommend_runbook", "diagnosis → runbooks[{id,score}]"),
            ("propose_self_heal", "→ plan_steps + blast_radius"),
            ("request_recovery_approval", "plan → approval_request_id"),
            ("execute_automation", "job_id+token → execution_id WRITE"),
            ("poll_job_status", "execution_id → status"),
        ],
        "tech_schema": "schemas/resolution/input|output.schema.json · hitl_*",
        "tech_note": "Design only — WRITE only after approval_token present.",
    },
    "verification": {
        "title": "Verification Agent",
        "role": "Is it really recovered?",
        "stage": "Stage 4 — Verify",
        "medium_left": [
            ("Health Verification", "Availability + golden signals", CARD),
            ("Business Validation", "Critical business flows", CARD),
            ("Risk Validation", "Downstream side effects", CARD),
            ("Declare stable / unstable", "Result → Orchestrator", MINT),
        ],
        "medium_right": [
            ("verify_health", "SLO / service health"),
            ("verify_business", "Synthetics / key txns"),
            ("verify_risk", "Pre/post compare"),
            ("declare_stable", "All critical green"),
            ("declare_unstable", "Open failure loop"),
        ],
        "medium_connectors": "Dynatrace · Azure Monitor · Splunk · Bridge",
        "medium_note": "Never closes the incident. Unstable → escalate.",
        "tech_left": [
            ("checks[]", "health | business | risk", CARD),
            ("stable bool", "all critical passed", MINT),
            ("open_recovery_failure_loop", "when unstable", CLAY),
            ("Output schema", "verification/output.schema.json", NAVY),
        ],
        "tech_right": [
            ("verify_health", "service → {pass, metrics[]}"),
            ("verify_business", "flows → checks[]"),
            ("verify_risk", "baseline → side_effects[]"),
            ("declare_stable", "evidence → Orchestrator"),
            ("declare_unstable", "failing[] → loop signal"),
        ],
        "tech_schema": "schemas/verification/input|output.schema.json",
        "tech_note": "Design only — read-mostly; synthetics may run checks.",
    },
    "closure_learning": {
        "title": "Closure & Learning Agent",
        "role": "Close cleanly and keep the lesson",
        "stage": "Stage 5 — Close & Follow-up",
        "medium_left": [
            ("RCA Generation", "Draft + timeline", CARD),
            ("Problem Creation", "Problem / known error", CARD),
            ("Knowledge Update", "KB / SOP / Bridge", CARD),
            ("Close incident", "After Closure HITL", MINT),
        ],
        "medium_right": [
            ("draft_rca", "compose + attach"),
            ("create_or_link_problem", "ServiceNow write"),
            ("update_knowledge", "Gated write"),
            ("close_incident", "Token + resolve"),
        ],
        "medium_connectors": "ServiceNow · Cognitive Bridge",
        "medium_note": "Runs after stable (or human override). Closure gate mandatory.",
        "tech_left": [
            ("mode", "drafted | awaiting | closed", CARD),
            ("rca.draft", "string + timeline_ref", CARD),
            ("problem_id", "optional KE link", CARD),
            ("Closure HITL", "approval_token required", CLAY),
            ("Output schema", "closure_learning/output.schema.json", MINT),
        ],
        "tech_right": [
            ("draft_rca", "evidence → rca_draft"),
            ("create_or_link_problem", "→ problem_id WRITE"),
            ("update_knowledge", "→ kb/bridge ids WRITE"),
            ("close_incident", "token → state Resolved WRITE"),
        ],
        "tech_schema": "schemas/closure_learning/input|output.schema.json · hitl_decision",
        "tech_note": "Design only — no close without Closure gate token.",
    },
    "knowledge": {
        "title": "Knowledge Agent",
        "role": "Shared — Cognitive Bridge keeper",
        "stage": "Cross-cutting · all stages",
        "medium_left": [
            ("Query bridge", "Retrieve scoped knowledge", CARD),
            ("Search libraries", "RCA · SOP · automation · arch", CARD),
            ("Write bridge", "Tagged facts + confidence", MINT),
            ("Governance check", "No silent SOP overwrite", CLAY),
        ],
        "medium_right": [
            ("query_bridge", "hits + citations"),
            ("search_rca / sop / …", "Library reads"),
            ("search_automation_catalog", "Job ↔ SOP map"),
            ("write_bridge", "Upsert fact_id"),
        ],
        "medium_connectors": "Cognitive Bridge · ServiceNow KB / CMDB notes",
        "medium_note": "Raw get-incident is a connector. This agent chooses knowledge.",
        "tech_left": [
            ("operation", "query | search_* | write", CARD),
            ("hits[]", "id, summary, score?", MINT),
            ("written_fact_id", "when write succeeds", CARD),
            ("blocked_by_governance", "bool", CLAY),
            ("Output schema", "knowledge/output.schema.json", NAVY),
        ],
        "tech_right": [
            ("query_bridge", "query/key → hits[]"),
            ("search_rca_repo", "→ rca[]"),
            ("search_sop_library", "→ docs[]"),
            ("write_bridge", "fact+source → fact_id WRITE"),
        ],
        "tech_schema": "schemas/knowledge/input|output.schema.json",
        "tech_note": "Design only — writes may require Governance approval.",
    },
    "governance": {
        "title": "Governance Agent",
        "role": "Shared — policy, confidence, kill-switch",
        "stage": "Cross-cutting · brake pedal",
        "medium_left": [
            ("Validate policy", "Action vs policy pack", CARD),
            ("Score confidence", "Packet 0–1", CARD),
            ("Enforce approval", "HITL token check", CLAY),
            ("Audit + kill-switch", "Immutable log / halt", MINT),
        ],
        "medium_right": [
            ("validate_policy", "allow / violations[]"),
            ("score_confidence", "score + reasons"),
            ("enforce_approval", "gate + token"),
            ("trigger_kill_switch", "Hard stop"),
        ],
        "medium_connectors": "Bridge policy · Orchestrator approvals · automation cancel · audit sink",
        "medium_note": "Does not triage, diagnose, or fix — only controls.",
        "tech_left": [
            ("action", "validate | score | enforce | kill", CARD),
            ("allowed", "boolean gate result", CLAY),
            ("confidence_score", "0–1 optional", CARD),
            ("kill_switch_active", "bool", MINT),
            ("Output schema", "governance/output.schema.json", NAVY),
        ],
        "tech_right": [
            ("validate_policy", "action{} → allow/violations[]"),
            ("score_confidence", "packet → score"),
            ("enforce_approval", "gate+token → allowed"),
            ("write_audit_log", "→ audit_id append-only"),
            ("trigger_kill_switch", "reason → halted WRITE"),
        ],
        "tech_schema": "schemas/governance/input|output.schema.json · hitl_*",
        "tech_note": "Design only — kill-switch is the emergency path.",
    },
    "communication": {
        "title": "Communication Agent",
        "role": "Shared — stakeholder updates",
        "stage": "Cross-cutting · voice of the incident",
        "medium_left": [
            ("Audience fit", "Bridge / exec / customer", CARD),
            ("Draft from facts", "Evidence only — no invent", CARD),
            ("Send channel", "Teams / email / broadcast", MINT),
            ("Recovery rule", "Announce only after Verify", CLAY),
        ],
        "medium_right": [
            ("post_teams_update", "Graph message_id"),
            ("send_email", "SMTP / Graph"),
            ("broadcast_status", "Template send"),
            ("draft_executive_summary", "Draft unless auto-send"),
            ("draft_customer_update", "Redacted draft"),
        ],
        "medium_connectors": "Microsoft Graph · SMTP · ServiceNow (context read)",
        "medium_note": "Never invents ETA or root cause. Never changes technical state.",
        "tech_left": [
            ("audience + intent", "enums in input schema", CARD),
            ("facts{}", "verified fields only", CARD),
            ("draft", "subject + body_markdown", MINT),
            ("sent", "bool + message_ids[]", CARD),
            ("Output schema", "communication/output.schema.json", NAVY),
        ],
        "tech_right": [
            ("post_teams_update", "channel+md → message_id WRITE"),
            ("send_email", "to/subject/body → message_id"),
            ("broadcast_status", "template_id+fields → send"),
            ("draft_*", "evidence → draft (no send default)"),
        ],
        "tech_schema": "schemas/communication/input|output.schema.json",
        "tech_note": "Design only — recovery_notice blocked until Verify stable.",
    },
}


class MediumDiagram(Scene):
    agent_key = "triage"

    def construct(self):
        d = PARENTS[self.agent_key]
        self.camera.background_color = PAPER

        title = Text(d["title"] + "  ·  medium", font_size=30, color=INK).to_edge(UP, buff=0.26)
        role = Text(d["role"], font_size=15, color=MUTED).next_to(title, DOWN, buff=0.1)
        stage = box(d["stage"], fill=NAVY, width=5.2, height=0.52, title_size=14)
        stage.next_to(role, DOWN, buff=0.14)

        left_h = Text("Inside this agent", font_size=15, color=ACCENT)
        left_boxes = VGroup(*[box(t, s, f, 5.3, 0.68) for t, s, f in d["medium_left"]]).arrange(DOWN, buff=0.1)
        left = VGroup(left_h, left_boxes).arrange(DOWN, buff=0.08)
        left.next_to(stage, DOWN, buff=0.22).to_edge(LEFT, buff=0.45)

        right_h = Text("Tools", font_size=15, color=ACCENT)
        right_boxes = VGroup(
            *[box(t, s, CLAY if i % 2 == 0 else SAND, 5.5, 0.62, 15, 11) for i, (t, s) in enumerate(d["medium_right"])]
        ).arrange(DOWN, buff=0.1)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.08)
        right.next_to(stage, DOWN, buff=0.22).to_edge(RIGHT, buff=0.4)

        arrows = VGroup(*[arrow_v(left_boxes[i], left_boxes[i + 1]) for i in range(len(left_boxes) - 1)])

        conn = box("Connectors", d["medium_connectors"], NAVY, 14.8, 0.58, 14, 11)
        note = Text(d["medium_note"], font_size=13, color=MUTED)
        foot = VGroup(conn, note).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.22)

        self.add(title, role, stage, left, right, arrows, foot)


class TechnicalDiagram(Scene):
    agent_key = "triage"

    def construct(self):
        d = PARENTS[self.agent_key]
        self.camera.background_color = PAPER

        title = Text(d["title"] + "  ·  technical", font_size=30, color=INK).to_edge(UP, buff=0.24)
        role = Text(d["role"], font_size=15, color=MUTED).next_to(title, DOWN, buff=0.08)
        stage = box(d["stage"], fill=NAVY, width=5.2, height=0.5, title_size=14)
        stage.next_to(role, DOWN, buff=0.12)

        badge = box("Design only — no runtime", "schemas are contracts; MCP/API not wired", ROSE, 8.5, 0.55, 13, 11)
        badge.next_to(stage, DOWN, buff=0.12)

        left_h = Text("Contracts / state", font_size=15, color=ACCENT)
        left_boxes = VGroup(*[box(t, s, f, 5.3, 0.64, 15, 11) for t, s, f in d["tech_left"]]).arrange(DOWN, buff=0.09)
        left = VGroup(left_h, left_boxes).arrange(DOWN, buff=0.07)
        left.next_to(badge, DOWN, buff=0.16).to_edge(LEFT, buff=0.4)

        right_h = Text("Tool I/O", font_size=15, color=ACCENT)
        right_boxes = VGroup(
            *[box(t, s, CLAY if i % 2 == 0 else SAND, 5.7, 0.64, 14, 11) for i, (t, s) in enumerate(d["tech_right"])]
        ).arrange(DOWN, buff=0.09)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.07)
        right.next_to(badge, DOWN, buff=0.16).to_edge(RIGHT, buff=0.35)

        arrows = VGroup(*[arrow_v(left_boxes[i], left_boxes[i + 1]) for i in range(len(left_boxes) - 1)])

        schema = box("JSON Schema", d["tech_schema"], MINT, 14.8, 0.55, 13, 11)
        note = Text(d["tech_note"], font_size=13, color=MUTED)
        foot = VGroup(schema, note).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.2)

        self.add(title, role, stage, badge, left, right, arrows, foot)


def _mk(base, key, prefix):
    class C(base):
        agent_key = key

    C.__name__ = f"{prefix}_{key}"
    return C


for _k in PARENTS:
    globals()[f"Medium_{_k}"] = _mk(MediumDiagram, _k, "Medium")
    globals()[f"Tech_{_k}"] = _mk(TechnicalDiagram, _k, "Tech")


# ---------- Subagents (same light style, single column + tools) ----------
SUBAGENTS = [
    ("triage", "data_quality", "Data Quality", "Validate intake + CI", "get_incident · validate_required_fields · enrich_ci_context · update_incident_quality_notes", "ServiceNow · Bridge"),
    ("triage", "priority_assessment", "Priority Assessment", "Recommend P1–P5", "score_priority · get_service_criticality · get_sla_policy", "Bridge · ServiceNow"),
    ("triage", "impact_assessment", "Impact Assessment", "Blast radius", "get_service_map · get_affected_users_signal · list_downstream_services", "Dynatrace · Azure · Splunk · Bridge"),
    ("diagnostic", "log_analysis", "Log Analysis", "Error clusters", "search_logs · summarise_error_cluster", "Splunk · app logs"),
    ("diagnostic", "change_analysis", "Change Analysis", "Correlate changes", "list_recent_changes · get_change_risk", "ServiceNow · ADO"),
    ("diagnostic", "infrastructure_analysis", "Infrastructure Analysis", "Host/cloud health", "get_host_metrics · get_azure_alerts", "Azure Monitor · Dynatrace"),
    ("diagnostic", "dependency_analysis", "Dependency Analysis", "Cascade map", "get_service_map · list_failing_dependencies", "Dynatrace · Bridge"),
    ("diagnostic", "application_analysis", "Application Analysis", "APM / txns", "get_apm_traces · get_transaction_errors", "Dynatrace"),
    ("diagnostic", "code_analysis", "Code Analysis", "Suspect commits", "list_recent_commits · diff_suspect_files", "GitHub · ADO"),
    ("resolution", "runbook_recommendation", "Runbook Recommendation", "Match SOP", "search_sop · rank_runbooks", "Bridge · ServiceNow"),
    ("resolution", "self_healing", "Self-Healing", "Fix plan + blast radius", "build_fix_plan · estimate_blast_radius", "Bridge · PagerDuty"),
    ("resolution", "automation_execution", "Automation Execution", "Run approved job", "list_automation_jobs · run_approved_job · poll_job_status", "Rundeck · Ansible · Azure Automation"),
    ("verification", "health_verification", "Health Verification", "Golden signals", "check_service_health · check_slo_burn", "Dynatrace · Azure Monitor"),
    ("verification", "business_validation", "Business Validation", "Critical flows", "run_synthetic_check · check_key_transactions", "Dynatrace · Bridge"),
    ("verification", "risk_validation", "Risk Validation", "Side effects", "scan_downstream_health · compare_pre_post_metrics", "Dynatrace · Azure · Splunk"),
    ("closure_learning", "rca_generation", "RCA Generation", "Draft RCA", "compose_rca · attach_timeline", "Bridge · ServiceNow"),
    ("closure_learning", "problem_creation", "Problem Creation", "Problem / KE", "create_problem · link_known_error", "ServiceNow"),
    ("closure_learning", "knowledge_update", "Knowledge Update", "KB / SOP notes", "upsert_kb_article · update_runbook_note", "ServiceNow · Bridge"),
]


class SubagentDiagram(Scene):
    parent = "triage"
    name = "Data Quality"
    role = ""
    tools = ""
    connectors = ""

    def construct(self):
        self.camera.background_color = PAPER
        title = Text(self.name, font_size=32, color=INK).to_edge(UP, buff=0.32)
        role = Text(self.role, font_size=16, color=MUTED).next_to(title, DOWN, buff=0.1)
        parent = box(f"Parent · {self.parent}", "subagent under lifecycle / shared agent", NAVY, 7.0, 0.7)
        parent.next_to(role, DOWN, buff=0.2)

        tool_names = [t.strip() for t in self.tools.split("·")]
        left_h = Text("Inside this subagent", font_size=15, color=ACCENT)
        steps = VGroup(
            box("1  Receive brief", "From parent agent", CARD, 5.2, 0.65),
            box("2  Call tools", "Connector-backed reads/writes", CARD, 5.2, 0.65),
            box("3  Return result", "Structured payload to parent", MINT, 5.2, 0.65),
        ).arrange(DOWN, buff=0.12)
        left = VGroup(left_h, steps).arrange(DOWN, buff=0.1)
        left.next_to(parent, DOWN, buff=0.28).to_edge(LEFT, buff=0.5)

        right_h = Text("Tools", font_size=15, color=ACCENT)
        tool_boxes = VGroup(
            *[box(n, "see parent tools.md", CLAY if i % 2 == 0 else SAND, 5.4, 0.62, 15, 11) for i, n in enumerate(tool_names)]
        ).arrange(DOWN, buff=0.1)
        right = VGroup(right_h, tool_boxes).arrange(DOWN, buff=0.1)
        right.next_to(parent, DOWN, buff=0.28).to_edge(RIGHT, buff=0.45)

        arrows = VGroup(*[arrow_v(steps[i], steps[i + 1]) for i in range(len(steps) - 1)])
        conn = box("Connectors", self.connectors, NAVY, 14.5, 0.6, 14, 12)
        note = Text("Design only — no runtime", font_size=13, color=MUTED)
        foot = VGroup(conn, note).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.25)
        self.add(title, role, parent, left, right, arrows, foot)


for p, sid, name, role, tools, conn in SUBAGENTS:
    cls = type(
        f"Sub_{p}_{sid}",
        (SubagentDiagram,),
        {"parent": p, "name": name, "role": role, "tools": tools, "connectors": conn},
    )
    globals()[cls.__name__] = cls
