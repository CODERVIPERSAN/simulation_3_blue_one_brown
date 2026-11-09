# Communication JSON schemas (hard / 100 technical)

These schemas define **exactly which fields** agents send and receive. They sit at the top of the technical ladder:

| Level | What you get | Audience |
|------:|--------------|----------|
| **0** | `diagram.png` — boxes and arrows | Anyone |
| **50** | `diagram_medium.png` + plain `DESIGN.md` | Engineers learning the system |
| **100** | `diagram_technical.png` + `tools.md` Technical column + **these JSON schemas** | Implementers / API builders |

Yes — generating light → medium → hard (schemas) from one architecture is how a non-technical design becomes implementable without guessing field names.

## Folder layout

```
schemas/
├── README.md                 ← you are here
├── shared/                   ← envelopes used by everyone
├── orchestrator/
├── triage/ … communication/  ← per-agent request/response
└── */examples/               ← sample JSON that validates against the schema
```

## Shared envelopes (always wrap agent payloads)

| Schema | Purpose |
|--------|---------|
| `shared/agent_invoke.schema.json` | Orchestrator → agent brief |
| `shared/agent_result.schema.json` | Agent → Orchestrator result wrapper |
| `shared/evidence_pack.schema.json` | Accumulated incident evidence |
| `shared/hitl_request.schema.json` | Approval request to a human |
| `shared/hitl_decision.schema.json` | Human yes/no + token |
| `shared/error.schema.json` | Standard tool/agent error |

## Per-agent payload schemas

Each agent folder has:

- `input.schema.json` — fields inside `brief.payload` when invoked
- `output.schema.json` — fields inside `result.payload` when finished

Tool-level I/O is documented in that agent’s `tools.md` Technical column; schemas here cover **agent-to-agent / orchestrator communication**, not every low-level connector call.

## Status

Schemas are **design contracts**. Nothing in this repo validates them at runtime yet (see `../AVAILABILITY.md`).
