"""Light diagrams with simple one-line tool purpose under each tool name.

Same layout as before; only tool subtitles become clear purpose lines.
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


def box(title, subtitle=None, fill=CARD, width=3.0, height=0.72, title_size=17, sub_size=12):
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.1,
        fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=1.4,
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


# left steps + tools with purpose one-liners
PARENTS = {
    "orchestrator": {
        "title": "Master Orchestrator",
        "role": "Incident Commander AI — plans stages, routes agents, holds evidence",
        "stage": "Owns Detect → Close lifecycle",
        "left": [
            ("1  Pick next stage", "Triage → Diagnose → Resolve → Verify → Close", CARD),
            ("2  Invoke agent", "Scoped brief + incident id", CARD),
            ("3  Collect evidence", "Merge agent outputs", MINT),
            ("4  HITL or loop", "Approval gate / investigation / recovery fail", CLAY),
            ("5  Update progress", "ServiceNow + Cognitive Bridge", CARD),
        ],
        "tools": [
            ("invoke_agent", "Starts one specialist agent for this incident"),
            ("collect_evidence", "Saves that agent's findings into the evidence pack"),
            ("request_hitl_approval", "Asks a human to approve a gated decision"),
            ("open_investigation_loop", "Asks Diagnose again when evidence is thin"),
            ("open_recovery_failure_loop", "Stops a failed fix path and escalates"),
            ("update_progress", "Writes the current stage summary to ServiceNow"),
            ("emergency_kill_switch", "Immediately stops all agents and automation"),
        ],
        "note": "Does not diagnose or execute jobs itself — only coordinates.",
    },
    "triage": {
        "title": "Triage Agent",
        "role": "Is it real? How bad? Who owns it?",
        "stage": "Stage 1 — Intake & Triage",
        "left": [
            ("Data Quality", "Validate intake + CI context", CARD),
            ("Priority Assessment", "Recommend P1–P5", CARD),
            ("Impact Assessment", "Business + technical blast radius", CARD),
            ("Propose owner", "Assignment group + on-call", MINT),
            ("Submit triage result", "Packet back to Orchestrator", CLAY),
        ],
        "tools": [
            ("run_data_quality", "Checks the ticket is complete enough to triage"),
            ("run_priority_assessment", "Recommends how urgent the incident is (P1–P5)"),
            ("run_impact_assessment", "Estimates who and what else is affected"),
            ("propose_owner", "Suggests the support group and on-call person"),
            ("submit_triage_result", "Sends the triage packet back to the Orchestrator"),
        ],
        "note": "Does not find root cause or run fixes. HITL on P1/P2 or low confidence.",
    },
    "diagnostic": {
        "title": "Diagnostic Agent",
        "role": "What broke and why?",
        "stage": "Stage 2 — Diagnose & Assess",
        "left": [
            ("Log Analysis", "Error clusters / spike windows", CARD),
            ("Change Analysis", "Recent changes / releases", CARD),
            ("Infra + Dependency", "Health + service map cascade", CARD),
            ("App + Code Analysis", "APM traces + suspect commits", CARD),
            ("Propose root cause", "Ranked hypotheses + evidence", MINT),
        ],
        "tools": [
            ("run_log_analysis", "Finds error patterns in logs for the incident window"),
            ("run_change_analysis", "Checks if a recent change likely caused it"),
            ("run_infra_analysis", "Checks servers and cloud health signals"),
            ("run_dependency_analysis", "Finds failing upstream or downstream services"),
            ("run_app_analysis", "Looks at APM traces and bad transactions"),
            ("run_code_analysis", "Points to suspect commits near the fault time"),
            ("propose_root_cause", "Publishes ranked cause ideas with evidence ids"),
            ("request_more_evidence", "Asks Orchestrator for another investigation pass"),
        ],
        "note": "Never executes remediation. Thin evidence → ask Orchestrator for another loop.",
    },
    "resolution": {
        "title": "Resolution Agent",
        "role": "How do we fix it safely?",
        "stage": "Stage 3 — Resolve",
        "left": [
            ("Runbook Recommendation", "Match SOP to diagnosis", CARD),
            ("Self-Healing proposal", "Fix plan + blast radius", CARD),
            ("HITL approval", "Recovery + automation gates", CLAY),
            ("Automation Execution", "Rundeck / Ansible / Azure", MINT),
        ],
        "tools": [
            ("recommend_runbook", "Finds the best SOP or runbook for this diagnosis"),
            ("propose_self_heal", "Builds a fix plan and estimates blast radius"),
            ("request_recovery_approval", "Asks a human before any automated fix"),
            ("execute_automation", "Runs the approved job in Rundeck/Ansible/etc."),
        ],
        "note": "No job runs without HITL. On failure, stop — Orchestrator opens recovery-failure loop.",
    },
    "verification": {
        "title": "Verification Agent",
        "role": "Is it really recovered?",
        "stage": "Stage 4 — Verify",
        "left": [
            ("Health Verification", "Availability + golden signals", CARD),
            ("Business Validation", "Critical business flows", CARD),
            ("Risk Validation", "Downstream side effects", CARD),
            ("Declare stable / unstable", "Result to Orchestrator", MINT),
        ],
        "tools": [
            ("verify_health", "Checks the service is healthy again"),
            ("verify_business", "Checks critical business flows still work"),
            ("verify_risk", "Looks for side effects on dependent services"),
            ("declare_stable", "Tells Orchestrator the service looks recovered"),
            ("declare_unstable", "Tells Orchestrator recovery failed checks"),
        ],
        "note": "Never closes the incident. Unstable → Orchestrator escalates and reassesses.",
    },
    "closure_learning": {
        "title": "Closure & Learning Agent",
        "role": "Close cleanly and keep the lesson",
        "stage": "Stage 5 — Close & Follow-up",
        "left": [
            ("RCA Generation", "Draft RCA from evidence", CARD),
            ("Problem Creation", "Create / link problem + KE", CARD),
            ("Knowledge Update", "KB / SOP / Cognitive Bridge", CARD),
            ("Close incident", "After Closure HITL gate", MINT),
        ],
        "tools": [
            ("draft_rca", "Writes a root-cause draft from the evidence pack"),
            ("create_or_link_problem", "Creates or links a problem / known error"),
            ("update_knowledge", "Updates KB, runbook notes, or the Bridge"),
            ("close_incident", "Resolves the incident after Closure approval"),
        ],
        "note": "Runs only after stable (or human override). Closure gate is mandatory.",
    },
    "knowledge": {
        "title": "Knowledge Agent",
        "role": "Shared — Cognitive Bridge keeper",
        "stage": "Cross-cutting · all stages",
        "left": [
            ("Query bridge", "Retrieve scoped knowledge", CARD),
            ("Search libraries", "RCA / SOP / automation / arch", CARD),
            ("Write bridge", "Tag source + confidence", MINT),
            ("Governance check", "No silent SOP overwrite", CLAY),
        ],
        "tools": [
            ("query_bridge", "Looks up facts in the Cognitive Bridge"),
            ("search_rca_repo", "Finds similar past root-cause write-ups"),
            ("search_sop_library", "Finds matching SOPs and runbooks"),
            ("search_automation_catalog", "Finds automation jobs linked to an SOP"),
            ("search_architecture", "Finds architecture and dependency notes"),
            ("write_bridge", "Saves a new knowledge fact with source tags"),
        ],
        "note": "Raw get-incident is a connector. This agent decides which knowledge matters.",
    },
    "governance": {
        "title": "Governance Agent",
        "role": "Shared — policy, confidence, audit, kill-switch",
        "stage": "Cross-cutting · brake pedal",
        "left": [
            ("Validate policy", "Action vs org policy pack", CARD),
            ("Score confidence", "0–1 on agent packets", CARD),
            ("Enforce approval", "Block / allow via HITL token", CLAY),
            ("Audit + kill-switch", "Immutable log / halt all", MINT),
        ],
        "tools": [
            ("validate_policy", "Checks whether an action is allowed by policy"),
            ("score_confidence", "Scores how confident an agent packet is"),
            ("enforce_approval", "Blocks or allows based on a human approval token"),
            ("assess_risk", "Rates the risk of a proposed fix"),
            ("write_audit_log", "Writes an immutable audit entry"),
            ("trigger_kill_switch", "Emergency stop for agents and automation"),
        ],
        "note": "Does not triage, diagnose, or fix — only controls and records.",
    },
    "communication": {
        "title": "Communication Agent",
        "role": "Shared — stakeholder updates across the lifecycle",
        "stage": "Cross-cutting · voice of the incident",
        "left": [
            ("Audience fit", "Bridge / exec / customer", CARD),
            ("Draft update", "From evidence only", CARD),
            ("Send channel", "Teams / email / broadcast", MINT),
            ("Recovery rule", "Announce only after Verify", CLAY),
        ],
        "tools": [
            ("post_teams_update", "Posts a status message to the incident Teams channel"),
            ("send_email", "Sends an email update to stakeholders"),
            ("broadcast_status", "Sends a standard status broadcast template"),
            ("draft_executive_summary", "Drafts a short summary for executives"),
            ("draft_customer_update", "Drafts safe wording for external customers"),
        ],
        "note": "Never invents ETA or root cause. Never changes technical state.",
    },
}


class ParentLight(Scene):
    agent_key = "triage"

    def construct(self):
        d = PARENTS[self.agent_key]
        self.camera.background_color = PAPER
        title = Text(d["title"], font_size=32, color=INK).to_edge(UP, buff=0.26)
        role = Text(d["role"], font_size=15, color=MUTED).next_to(title, DOWN, buff=0.1)
        stage = box(d["stage"], fill=NAVY, width=5.4, height=0.52, title_size=14)
        stage.next_to(role, DOWN, buff=0.14)

        left_h = Text("Inside this agent", font_size=15, color=ACCENT)
        chips = VGroup(*[box(t, s, f, 5.2, 0.66) for t, s, f in d["left"]]).arrange(DOWN, buff=0.11)
        left = VGroup(left_h, chips).arrange(DOWN, buff=0.1)
        left.next_to(stage, DOWN, buff=0.22).to_edge(LEFT, buff=0.45)

        right_h = Text("Tools  (what each does)", font_size=15, color=ACCENT)
        tools = VGroup(
            *[box(n, desc, CLAY if i % 2 == 0 else SAND, 5.7, 0.62, 15, 11) for i, (n, desc) in enumerate(d["tools"])]
        ).arrange(DOWN, buff=0.1)
        right = VGroup(right_h, tools).arrange(DOWN, buff=0.1)
        right.next_to(stage, DOWN, buff=0.22).to_edge(RIGHT, buff=0.35)

        content = VGroup(left, right)
        if content.height > 5.4:
            content.scale_to_fit_height(5.4)
            left.next_to(stage, DOWN, buff=0.22).to_edge(LEFT, buff=0.45)
            right.next_to(stage, DOWN, buff=0.22).to_edge(RIGHT, buff=0.35)

        arrows = VGroup(*[arrow_v(chips[i], chips[i + 1]) for i in range(len(chips) - 1)])
        note = Text(d["note"], font_size=13, color=MUTED).to_edge(DOWN, buff=0.26)
        self.add(title, role, stage, left, right, arrows, note)


for _k in PARENTS:
    globals()[f"Light_{_k}"] = type(f"Light_{_k}", (ParentLight,), {"agent_key": _k})


SUBS = [
    ("triage", "data_quality", "Data Quality", "Validate ServiceNow intake and CI context",
     [("get_incident", "Reads the ServiceNow incident record"),
      ("validate_required_fields", "Checks required fields are present"),
      ("enrich_ci_context", "Fills in CI / business service from CMDB"),
      ("update_incident_quality_notes", "Adds a short quality note on the ticket")]),
    ("triage", "priority_assessment", "Priority Assessment", "Recommend P1–P5 from severity and criticality",
     [("score_priority", "Applies the priority matrix to recommend P1–P5"),
      ("get_service_criticality", "Reads how critical the service is"),
      ("get_sla_policy", "Reads the SLA rules for that priority")]),
    ("triage", "impact_assessment", "Impact Assessment", "Business and technical blast radius",
     [("get_service_map", "Loads the service dependency map"),
      ("get_affected_users_signal", "Estimates how many users are impacted"),
      ("list_downstream_services", "Lists services that depend on this one")]),
    ("diagnostic", "log_analysis", "Log Analysis", "Error clusters and spike windows",
     [("search_logs", "Searches logs in the incident time window"),
      ("summarise_error_cluster", "Groups similar errors into clusters")]),
    ("diagnostic", "change_analysis", "Change Analysis", "Correlate recent changes and releases",
     [("list_recent_changes", "Lists recent changes near the incident start"),
      ("get_change_risk", "Reads risk details for a change record")]),
    ("diagnostic", "infrastructure_analysis", "Infrastructure Analysis", "Compute, network, storage health",
     [("get_host_metrics", "Pulls host or cloud health metrics"),
      ("get_azure_alerts", "Lists related Azure Monitor alerts")]),
    ("diagnostic", "dependency_analysis", "Dependency Analysis", "Upstream and downstream failures",
     [("get_service_map", "Loads upstream/downstream service graph"),
      ("list_failing_dependencies", "Lists neighbors that look unhealthy")]),
    ("diagnostic", "application_analysis", "Application Analysis", "APM traces and business transactions",
     [("get_apm_traces", "Pulls APM traces for the service"),
      ("get_transaction_errors", "Lists failing business transactions")]),
    ("diagnostic", "code_analysis", "Code Analysis", "Suspect commits and deployments",
     [("list_recent_commits", "Lists commits around the fault window"),
      ("diff_suspect_files", "Shows what changed in a suspect commit")]),
    ("resolution", "runbook_recommendation", "Runbook Recommendation", "Match SOP or runbook to diagnosis",
     [("search_sop", "Searches the SOP / runbook library"),
      ("rank_runbooks", "Ranks which runbook best matches the diagnosis")]),
    ("resolution", "self_healing", "Self-Healing", "Propose automated fix plan and blast radius",
     [("build_fix_plan", "Builds step-by-step fix actions"),
      ("estimate_blast_radius", "Estimates what else the fix could affect")]),
    ("resolution", "automation_execution", "Automation Execution", "Run approved automation jobs only",
     [("list_automation_jobs", "Lists automation jobs for the chosen SOP"),
      ("run_approved_job", "Runs a job only after human approval"),
      ("poll_job_status", "Checks whether the job succeeded or failed")]),
    ("verification", "health_verification", "Health Verification", "Service availability and golden signals",
     [("check_service_health", "Checks if the service is up and healthy"),
      ("check_slo_burn", "Checks whether SLO burn looks normal")]),
    ("verification", "business_validation", "Business Validation", "Critical business flows still work",
     [("run_synthetic_check", "Runs a synthetic user journey check"),
      ("check_key_transactions", "Checks critical transactions succeed")]),
    ("verification", "risk_validation", "Risk Validation", "Side effects on dependencies",
     [("scan_downstream_health", "Checks dependent services after the fix"),
      ("compare_pre_post_metrics", "Compares metrics before vs after recovery")]),
    ("closure_learning", "rca_generation", "RCA Generation", "Draft RCA from evidence timeline",
     [("compose_rca", "Writes a factual root-cause draft"),
      ("attach_timeline", "Attaches the incident timeline to the RCA")]),
    ("closure_learning", "problem_creation", "Problem Creation", "Create or link problem and known error",
     [("create_problem", "Creates a problem record in ServiceNow"),
      ("link_known_error", "Links a known error to the problem/incident")]),
    ("closure_learning", "knowledge_update", "Knowledge Update", "Update KB, SOP notes, Cognitive Bridge",
     [("upsert_kb_article", "Creates or updates a knowledge article"),
      ("update_runbook_note", "Adds a lesson note to the runbook / SOP")]),
]


class SubLight(Scene):
    meta = SUBS[0]

    def construct(self):
        parent, sid, name, role, tools = self.meta
        self.camera.background_color = PAPER
        title = Text(name, font_size=32, color=INK).to_edge(UP, buff=0.28)
        role_t = Text(role, font_size=15, color=MUTED).next_to(title, DOWN, buff=0.1)
        stage = box(f"Subagent · parent {parent}", fill=NAVY, width=5.4, height=0.52, title_size=14)
        stage.next_to(role_t, DOWN, buff=0.14)

        left_h = Text("Inside this subagent", font_size=15, color=ACCENT)
        steps = VGroup(
            box("1  Receive brief", "Scoped task from parent", CARD, 5.2, 0.7),
            box("2  Use tools", "Call each tool for one job", CARD, 5.2, 0.7),
            box("3  Return result", "Send findings back to parent", MINT, 5.2, 0.7),
        ).arrange(DOWN, buff=0.14)
        left = VGroup(left_h, steps).arrange(DOWN, buff=0.1)
        left.next_to(stage, DOWN, buff=0.28).to_edge(LEFT, buff=0.5)

        right_h = Text("Tools  (what each does)", font_size=15, color=ACCENT)
        right_boxes = VGroup(
            *[box(n, desc, CLAY if i % 2 == 0 else SAND, 5.6, 0.68, 15, 12) for i, (n, desc) in enumerate(tools)]
        ).arrange(DOWN, buff=0.12)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.1)
        right.next_to(stage, DOWN, buff=0.28).to_edge(RIGHT, buff=0.4)

        arrows = VGroup(*[arrow_v(steps[i], steps[i + 1]) for i in range(len(steps) - 1)])
        note = Text("Plain purpose under each tool — no MCP detail in the light view", font_size=13, color=MUTED)
        note.to_edge(DOWN, buff=0.28)
        self.add(title, role_t, stage, left, right, arrows, note)


for meta in SUBS:
    p, s = meta[0], meta[1]
    globals()[f"SLight_{p}_{s}"] = type(f"SLight_{p}_{s}", (SubLight,), {"meta": meta})
