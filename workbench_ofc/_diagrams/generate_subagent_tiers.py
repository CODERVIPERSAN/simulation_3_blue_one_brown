"""Three-tier subagent diagrams + refreshed parent medium/tech (light untouched).

Layout matches light: title, role, stage/parent chip, left flow, right tools, footer.
Medium adds: connectors + MCP requirement strip.
Technical adds: tool I/O + schema/MCP contract strip.
Icons: Unicode markers in titles (no dependency on external icon packs).
"""

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
LILAC = "#EDE7F6"


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


# parent, id, name, role, tools[(name, light_sub, med_sub, tech_io)], mcp_req, connectors
SUBS = [
    (
        "triage",
        "data_quality",
        "Data Quality",
        "Validate ServiceNow intake and CI context",
        [
            ("get_incident", "Read one incident", "SN Table API / MCP get", "in: number|sys_id → incident{}"),
            ("validate_required_fields", "Check required fields", "local rules + SN fields", "in: fields[] → {ok, missing[]}"),
            ("enrich_ci_context", "CMDB enrich", "SN CMDB MCP", "in: hints → {ci, service?}"),
            ("update_incident_quality_notes", "Quality work note", "SN write MCP", "in: note → ok  WRITE"),
        ],
        "MCP: servicenow.incident.read, servicenow.cmdb.read, servicenow.incident.write_notes",
        "ServiceNow · Cognitive Bridge",
    ),
    (
        "triage",
        "priority_assessment",
        "Priority Assessment",
        "Recommend P1–P5 from severity and criticality",
        [
            ("score_priority", "Apply matrix", "policy table / Bridge MCP", "in: sev,urg,crit → P1-P5"),
            ("get_service_criticality", "Criticality tier", "Bridge MCP", "in: service_id → tier"),
            ("get_sla_policy", "SLA for priority", "SN SLA MCP", "in: priority → sla{}"),
        ],
        "MCP: bridge.criticality.read, servicenow.sla.read, bridge.policy.read",
        "Cognitive Bridge · ServiceNow",
    ),
    (
        "triage",
        "impact_assessment",
        "Impact Assessment",
        "Business and technical blast radius",
        [
            ("get_service_map", "Upstream/downstream", "Dynatrace MCP", "in: entity,depth → graph"),
            ("get_affected_users_signal", "User impact signal", "Splunk/Azure MCP", "in: service,window → signal"),
            ("list_downstream_services", "Dependents list", "Dynatrace/Bridge MCP", "in: entity → services[]"),
        ],
        "MCP: dynatrace.topology.read, azure.monitor.read, splunk.search, bridge.map.read",
        "Dynatrace · Azure Monitor · Splunk · Bridge",
    ),
    (
        "diagnostic",
        "log_analysis",
        "Log Analysis",
        "Error clusters and spike windows",
        [
            ("search_logs", "Query logs", "Splunk MCP", "in: query,from,to → events[]"),
            ("summarise_error_cluster", "Cluster errors", "local + Splunk", "in: events[] → clusters[]"),
        ],
        "MCP: splunk.search, applogs.query",
        "Splunk · Application logs",
    ),
    (
        "diagnostic",
        "change_analysis",
        "Change Analysis",
        "Correlate recent changes and releases",
        [
            ("list_recent_changes", "Changes in window", "SN/ADO MCP", "in: window → changes[]"),
            ("get_change_risk", "Change risk fields", "SN change MCP", "in: change_id → risk{}"),
        ],
        "MCP: servicenow.change.read, azuredevops.release.read",
        "ServiceNow · Azure DevOps",
    ),
    (
        "diagnostic",
        "infrastructure_analysis",
        "Infrastructure Analysis",
        "Compute, network, storage health",
        [
            ("get_host_metrics", "Host metrics", "Azure/Dynatrace MCP", "in: ids,window → series"),
            ("get_azure_alerts", "Cloud alerts", "Azure Monitor MCP", "in: scope → alerts[]"),
        ],
        "MCP: azure.monitor.metrics, azure.monitor.alerts, dynatrace.metrics.read",
        "Azure Monitor · Dynatrace",
    ),
    (
        "diagnostic",
        "dependency_analysis",
        "Dependency Analysis",
        "Upstream and downstream failures",
        [
            ("get_service_map", "Service graph", "Dynatrace MCP", "in: entity,depth → graph"),
            ("list_failing_dependencies", "Unhealthy neighbors", "Dynatrace MCP", "in: entity → failing[]"),
        ],
        "MCP: dynatrace.topology.read, bridge.map.read",
        "Dynatrace · Cognitive Bridge",
    ),
    (
        "diagnostic",
        "application_analysis",
        "Application Analysis",
        "APM traces and business transactions",
        [
            ("get_apm_traces", "Sample traces", "Dynatrace APM MCP", "in: service,window → traces[]"),
            ("get_transaction_errors", "Txn errors", "Dynatrace MCP", "in: service,window → errors[]"),
        ],
        "MCP: dynatrace.apm.traces, dynatrace.apm.transactions",
        "Dynatrace",
    ),
    (
        "diagnostic",
        "code_analysis",
        "Code Analysis",
        "Suspect commits and deployments",
        [
            ("list_recent_commits", "Commits in window", "GitHub/ADO MCP", "in: repo,window → commits[]"),
            ("diff_suspect_files", "File diffs", "GitHub/ADO MCP", "in: commit → diffs[]"),
        ],
        "MCP: github.commits.read, github.diff.read, azuredevops.git.read",
        "GitHub · Azure DevOps",
    ),
    (
        "resolution",
        "runbook_recommendation",
        "Runbook Recommendation",
        "Match SOP or runbook to diagnosis",
        [
            ("search_sop", "Search SOP library", "Bridge/KB MCP", "in: query → docs[]"),
            ("rank_runbooks", "Rank matches", "local + Bridge", "in: candidates,diagnosis → ranked[]"),
        ],
        "MCP: bridge.sop.search, servicenow.kb.read",
        "Cognitive Bridge · ServiceNow",
    ),
    (
        "resolution",
        "self_healing",
        "Self-Healing",
        "Propose automated fix plan and blast radius",
        [
            ("build_fix_plan", "Structured steps", "local", "in: runbook+ctx → steps[]"),
            ("estimate_blast_radius", "Scope of fix", "Bridge/DT MCP", "in: plan → {scope,risk}"),
        ],
        "MCP: bridge.map.read, dynatrace.topology.read, pagerduty.context.read",
        "Bridge · PagerDuty · Dynatrace",
    ),
    (
        "resolution",
        "automation_execution",
        "Automation Execution",
        "Run approved automation jobs only",
        [
            ("list_automation_jobs", "Jobs for SOP", "Rundeck MCP", "in: sop_id → jobs[]"),
            ("run_approved_job", "Execute job", "Rundeck/Ansible MCP", "in: job+token → exec_id WRITE"),
            ("poll_job_status", "Poll status", "automation MCP", "in: exec_id → status"),
        ],
        "MCP: rundeck.job.read, rundeck.job.execute, ansible.job.execute, azure.automation.execute",
        "Rundeck · Ansible · Azure Automation",
    ),
    (
        "verification",
        "health_verification",
        "Health Verification",
        "Service availability and golden signals",
        [
            ("check_service_health", "Availability", "Dynatrace/Azure MCP", "in: service → health{}"),
            ("check_slo_burn", "SLO burn", "Dynatrace/Azure MCP", "in: slo → burn{}"),
        ],
        "MCP: dynatrace.health.read, azure.monitor.slo.read",
        "Dynatrace · Azure Monitor",
    ),
    (
        "verification",
        "business_validation",
        "Business Validation",
        "Critical business flows still work",
        [
            ("run_synthetic_check", "Synthetic probe", "Dynatrace MCP", "in: check_id → result"),
            ("check_key_transactions", "Key txns", "Dynatrace MCP", "in: txns[] → pass/fail"),
        ],
        "MCP: dynatrace.synthetic.run, dynatrace.apm.transactions, bridge.flows.read",
        "Dynatrace · Bridge",
    ),
    (
        "verification",
        "risk_validation",
        "Risk Validation",
        "Side effects on dependencies",
        [
            ("scan_downstream_health", "Neighbor health", "Dynatrace MCP", "in: service,depth → nodes[]"),
            ("compare_pre_post_metrics", "Pre vs post", "metrics MCP", "in: baseline → deltas[]"),
        ],
        "MCP: dynatrace.topology.read, azure.monitor.metrics, splunk.search",
        "Dynatrace · Azure Monitor · Splunk",
    ),
    (
        "closure_learning",
        "rca_generation",
        "RCA Generation",
        "Draft RCA from evidence timeline",
        [
            ("compose_rca", "Write RCA draft", "local + Bridge", "in: evidence[] → rca_draft"),
            ("attach_timeline", "Attach timeline", "Bridge/SN MCP", "in: events[] → timeline_ref"),
        ],
        "MCP: bridge.evidence.read, servicenow.attachment.write, bridge.rca.write",
        "Bridge · ServiceNow",
    ),
    (
        "closure_learning",
        "problem_creation",
        "Problem Creation",
        "Create or link problem and known error",
        [
            ("create_problem", "Create problem", "SN Problem MCP", "in: fields{} → problem_id WRITE"),
            ("link_known_error", "Link KE", "SN Problem MCP", "in: ids → ok WRITE"),
        ],
        "MCP: servicenow.problem.create, servicenow.problem.link, servicenow.known_error.link",
        "ServiceNow",
    ),
    (
        "closure_learning",
        "knowledge_update",
        "Knowledge Update",
        "Update KB, SOP notes, Cognitive Bridge",
        [
            ("upsert_kb_article", "KB upsert", "SN KB MCP", "in: article{} → kb_id WRITE"),
            ("update_runbook_note", "SOP note", "Bridge MCP", "in: sop_id,note → ok WRITE"),
        ],
        "MCP: servicenow.kb.write, bridge.sop.annotate, bridge.fact.write",
        "ServiceNow · Cognitive Bridge",
    ),
]


class SubLight(Scene):
    """Light — same template as parent light; no MCP strip."""

    meta = SUBS[0]

    def construct(self):
        parent, sid, name, role, tools, mcp, conns = self.meta
        self.camera.background_color = PAPER

        title = Text(name, font_size=32, color=INK).to_edge(UP, buff=0.28)
        role_t = Text(role, font_size=15, color=MUTED).next_to(title, DOWN, buff=0.1)
        stage = box(f"Subagent · parent {parent}", fill=NAVY, width=5.4, height=0.52, title_size=14)
        stage.next_to(role_t, DOWN, buff=0.14)

        left_h = Text("Inside this subagent", font_size=15, color=ACCENT)
        steps = VGroup(
            box("1  Receive brief", "Scoped task from parent", CARD, 5.2, 0.7),
            box("2  Use tools", "Connector-backed calls", CARD, 5.2, 0.7),
            box("3  Return result", "Structured payload to parent", MINT, 5.2, 0.7),
        ).arrange(DOWN, buff=0.14)
        left = VGroup(left_h, steps).arrange(DOWN, buff=0.1)
        left.next_to(stage, DOWN, buff=0.28).to_edge(LEFT, buff=0.5)

        right_h = Text("Tools", font_size=15, color=ACCENT)
        right_boxes = VGroup(
            *[
                box(f"•  {n}", s, CLAY if i % 2 == 0 else SAND, 5.5, 0.65, 15, 11)
                for i, (n, s, _, __) in enumerate(tools)
            ]
        ).arrange(DOWN, buff=0.12)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.1)
        right.next_to(stage, DOWN, buff=0.28).to_edge(RIGHT, buff=0.4)

        arrows = VGroup(*[arrow_v(steps[i], steps[i + 1]) for i in range(len(steps) - 1)])
        note = Text(f"Connectors: {conns}   ·   Design only — no runtime", font_size=13, color=MUTED)
        note.to_edge(DOWN, buff=0.3)
        self.add(title, role_t, stage, left, right, arrows, note)


class SubMedium(Scene):
    """Medium — light layout + connector strip + MCP requirements."""

    meta = SUBS[0]

    def construct(self):
        parent, sid, name, role, tools, mcp, conns = self.meta
        self.camera.background_color = PAPER

        title = Text(f"{name}  ·  medium", font_size=30, color=INK).to_edge(UP, buff=0.24)
        role_t = Text(role, font_size=15, color=MUTED).next_to(title, DOWN, buff=0.08)
        stage = box(f"Subagent · parent {parent}", fill=NAVY, width=5.4, height=0.5, title_size=14)
        stage.next_to(role_t, DOWN, buff=0.12)

        left_h = Text("Inside this subagent", font_size=15, color=ACCENT)
        steps = VGroup(
            box("1  Receive brief", "From parent agent invoke", CARD, 5.2, 0.62),
            box("2  Call tools", "One job per tool", CARD, 5.2, 0.62),
            box("3  MCP / API hop", "Via connector layer", CLAY, 5.2, 0.62),
            box("4  Return result", "Payload + confidence notes", MINT, 5.2, 0.62),
        ).arrange(DOWN, buff=0.1)
        left = VGroup(left_h, steps).arrange(DOWN, buff=0.08)
        left.next_to(stage, DOWN, buff=0.18).to_edge(LEFT, buff=0.45)

        right_h = Text("Tools  +  where they run", font_size=15, color=ACCENT)
        right_boxes = VGroup(
            *[
                box(f"•  {n}", med, CLAY if i % 2 == 0 else SAND, 5.6, 0.58, 14, 11)
                for i, (n, _, med, __) in enumerate(tools)
            ]
        ).arrange(DOWN, buff=0.09)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.08)
        right.next_to(stage, DOWN, buff=0.18).to_edge(RIGHT, buff=0.35)

        arrows = VGroup(*[arrow_v(steps[i], steps[i + 1]) for i in range(len(steps) - 1)])

        conn = box("Connectors", conns, NAVY, 14.8, 0.52, 13, 11)
        mcp_box = box("MCP requirements", mcp, LILAC, 14.8, 0.58, 12, 10)
        note = Text("Extra vs light: connector strip + MCP requirement names", font_size=12, color=MUTED)
        foot = VGroup(conn, mcp_box, note).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.16)
        self.add(title, role_t, stage, left, right, arrows, foot)


class SubTech(Scene):
    """Technical — light layout + I/O + MCP + schema note."""

    meta = SUBS[0]

    def construct(self):
        parent, sid, name, role, tools, mcp, conns = self.meta
        self.camera.background_color = PAPER

        title = Text(f"{name}  ·  technical", font_size=28, color=INK).to_edge(UP, buff=0.2)
        role_t = Text(role, font_size=14, color=MUTED).next_to(title, DOWN, buff=0.06)
        stage = box(f"Subagent · parent {parent}", fill=NAVY, width=5.4, height=0.48, title_size=13)
        stage.next_to(role_t, DOWN, buff=0.1)
        badge = box("Design only — no runtime", "tool I/O + MCP contracts; not wired", ROSE, 8.2, 0.5, 12, 10)
        badge.next_to(stage, DOWN, buff=0.1)

        left_h = Text("Contracts / flow", font_size=14, color=ACCENT)
        steps = VGroup(
            box("1  Parent brief", f"agent_invoke → {parent}", CARD, 5.2, 0.55, 14, 10),
            box("2  Tool calls", "see Tool I/O →", CARD, 5.2, 0.55, 14, 10),
            box("3  MCP servers", "required capabilities below", CLAY, 5.2, 0.55, 14, 10),
            box("4  Result to parent", "structured JSON payload", MINT, 5.2, 0.55, 14, 10),
            box("5  Side effects", "READ unless marked WRITE", SAND, 5.2, 0.55, 14, 10),
        ).arrange(DOWN, buff=0.07)
        left = VGroup(left_h, steps).arrange(DOWN, buff=0.06)
        left.next_to(badge, DOWN, buff=0.12).to_edge(LEFT, buff=0.4)

        right_h = Text("Tool I/O", font_size=14, color=ACCENT)
        right_boxes = VGroup(
            *[
                box(f"•  {n}", io, CLAY if i % 2 == 0 else SAND, 5.8, 0.55, 13, 10)
                for i, (n, _, __, io) in enumerate(tools)
            ]
        ).arrange(DOWN, buff=0.07)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.06)
        right.next_to(badge, DOWN, buff=0.12).to_edge(RIGHT, buff=0.32)

        arrows = VGroup(*[arrow_v(steps[i], steps[i + 1]) for i in range(len(steps) - 1)])

        conn = box("Connectors", conns, NAVY, 14.8, 0.48, 12, 10)
        mcp_box = box("MCP requirements", mcp, LILAC, 14.8, 0.55, 11, 10)
        schema = box(
            "Schemas",
            f"shared/agent_invoke|result · parent schemas/{parent}/ · tools.md Technical",
            MINT,
            14.8,
            0.48,
            11,
            10,
        )
        note = Text("Extra vs medium: tool I/O signatures + WRITE flags + schema pointers", font_size=11, color=MUTED)
        foot = VGroup(conn, mcp_box, schema, note).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.12)
        self.add(title, role_t, stage, badge, left, right, arrows, foot)


# Register 18 × 3 scenes
for meta in SUBS:
    parent, sid = meta[0], meta[1]

    def _bind(base, m, prefix):
        class C(base):
            meta = m

        C.__name__ = f"{prefix}_{m[0]}_{m[1]}"
        return C

    globals()[f"SubLight_{parent}_{sid}"] = _bind(SubLight, meta, "SubLight")
    globals()[f"SubMed_{parent}_{sid}"] = _bind(SubMedium, meta, "SubMed")
    globals()[f"SubTech_{parent}_{sid}"] = _bind(SubTech, meta, "SubTech")


# ---- Parent medium/tech refresh (icons + MCP); do NOT regenerate light ----
PARENT_MCP = {
    "orchestrator": "MCP: servicenow.incident.write_notes, pagerduty.escalate, teams.post, bridge.evidence.write, automation.cancel",
    "triage": "MCP: servicenow.*, pagerduty.oncall.read, bridge.criticality.read, dynatrace.topology.read, azure.monitor.read, splunk.search",
    "diagnostic": "MCP: splunk.search, dynatrace.*, azure.monitor.*, servicenow.change.read, github.*, azuredevops.*",
    "resolution": "MCP: bridge.sop.search, rundeck.job.*, ansible.job.*, azure.automation.*, pagerduty.context.read",
    "verification": "MCP: dynatrace.health|synthetic|apm, azure.monitor.slo|metrics, splunk.search, bridge.flows.read",
    "closure_learning": "MCP: servicenow.problem|kb|incident.resolve, bridge.rca|sop|fact.write",
    "knowledge": "MCP: bridge.query|write, bridge.sop|rca|automation|arch.search, servicenow.kb.read",
    "governance": "MCP: bridge.policy.read, orchestrator.approval.*, audit.append, automation.cancel",
    "communication": "MCP: teams.post, graph.mail.send, bridge.evidence.read (facts only)",
}

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_tier_diagrams import PARENTS  # noqa: E402


class ParentMediumMCP(Scene):
    agent_key = "triage"

    def construct(self):
        d = PARENTS[self.agent_key]
        self.camera.background_color = PAPER
        title = Text(d["title"] + "  ·  medium", font_size=30, color=INK).to_edge(UP, buff=0.22)
        role = Text(d["role"], font_size=15, color=MUTED).next_to(title, DOWN, buff=0.08)
        stage = box(d["stage"], fill=NAVY, width=5.2, height=0.5, title_size=14)
        stage.next_to(role, DOWN, buff=0.12)

        left_h = Text("Inside this agent", font_size=15, color=ACCENT)
        left_boxes = VGroup(*[box(f"•  {t}", s, f, 5.3, 0.62) for t, s, f in d["medium_left"]]).arrange(DOWN, buff=0.09)
        left = VGroup(left_h, left_boxes).arrange(DOWN, buff=0.08)
        left.next_to(stage, DOWN, buff=0.16).to_edge(LEFT, buff=0.4)

        right_h = Text("Tools", font_size=15, color=ACCENT)
        right_boxes = VGroup(
            *[box(f"•  {t}", s, CLAY if i % 2 == 0 else SAND, 5.5, 0.58, 14, 11) for i, (t, s) in enumerate(d["medium_right"])]
        ).arrange(DOWN, buff=0.09)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.08)
        right.next_to(stage, DOWN, buff=0.16).to_edge(RIGHT, buff=0.35)

        arrows = VGroup(*[arrow_v(left_boxes[i], left_boxes[i + 1]) for i in range(len(left_boxes) - 1)])
        conn = box("Connectors", d["medium_connectors"], NAVY, 14.8, 0.5, 13, 11)
        mcp = box("MCP requirements", PARENT_MCP[self.agent_key], LILAC, 14.8, 0.55, 11, 10)
        note = Text(d["medium_note"], font_size=12, color=MUTED)
        foot = VGroup(conn, mcp, note).arrange(DOWN, buff=0.07).to_edge(DOWN, buff=0.14)
        self.add(title, role, stage, left, right, arrows, foot)


class ParentTechMCP(Scene):
    agent_key = "triage"

    def construct(self):
        d = PARENTS[self.agent_key]
        self.camera.background_color = PAPER
        title = Text(d["title"] + "  ·  technical", font_size=28, color=INK).to_edge(UP, buff=0.18)
        role = Text(d["role"], font_size=14, color=MUTED).next_to(title, DOWN, buff=0.06)
        stage = box(d["stage"], fill=NAVY, width=5.2, height=0.48, title_size=13)
        stage.next_to(role, DOWN, buff=0.1)
        badge = box("Design only — no runtime", "I/O + MCP + schemas; not wired", ROSE, 8.5, 0.48, 12, 10)
        badge.next_to(stage, DOWN, buff=0.08)

        left_h = Text("Contracts / state", font_size=14, color=ACCENT)
        left_boxes = VGroup(*[box(f"•  {t}", s, f, 5.3, 0.55, 14, 10) for t, s, f in d["tech_left"]]).arrange(DOWN, buff=0.07)
        left = VGroup(left_h, left_boxes).arrange(DOWN, buff=0.06)
        left.next_to(badge, DOWN, buff=0.1).to_edge(LEFT, buff=0.35)

        right_h = Text("Tool I/O", font_size=14, color=ACCENT)
        right_boxes = VGroup(
            *[box(f"•  {t}", s, CLAY if i % 2 == 0 else SAND, 5.8, 0.55, 13, 10) for i, (t, s) in enumerate(d["tech_right"])]
        ).arrange(DOWN, buff=0.07)
        right = VGroup(right_h, right_boxes).arrange(DOWN, buff=0.06)
        right.next_to(badge, DOWN, buff=0.1).to_edge(RIGHT, buff=0.3)

        arrows = VGroup(*[arrow_v(left_boxes[i], left_boxes[i + 1]) for i in range(len(left_boxes) - 1)])
        schema = box("JSON Schema", d["tech_schema"], MINT, 14.8, 0.45, 11, 10)
        mcp = box("MCP requirements", PARENT_MCP[self.agent_key], LILAC, 14.8, 0.52, 10, 9)
        note = Text(d["tech_note"], font_size=11, color=MUTED)
        foot = VGroup(schema, mcp, note).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.1)
        self.add(title, role, stage, badge, left, right, arrows, foot)


for _k in PARENT_MCP:
    globals()[f"PMed_{_k}"] = type(f"PMed_{_k}", (ParentMediumMCP,), {"agent_key": _k})
    globals()[f"PTech_{_k}"] = type(f"PTech_{_k}", (ParentTechMCP,), {"agent_key": _k})
