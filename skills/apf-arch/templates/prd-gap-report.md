# PRD gap report: PRD-<NNN> (round <n>)

Produced by PRDGap after a change to the PRD. Each row is something a downstream agent would otherwise have to ask the human. Open gaps only.

| ID | Where in the PRD | Gap | Why it matters downstream | Proposed answer | Evidence | Kind |
|---|---|---|---|---|---|---|
| G-1 | §5 PR-2 | "fast" has no target | Tester cannot write an assertion | p99 < 200 ms at 500 rps | `docs/slo.md:12` | evidence |
| G-2 | §7 | Does it need EU data residency? | SOP and cloud design differ | none | | needs-human |

**Kind:** `evidence` (proposed answer is supported by a cited source), `assumption` (conservative default, thin evidence), `needs-human` (no proposal).

**Decision per gap (recorded by the caller):** `accepted` / `edited` / `waived`. Accepted and edited answers are written into the PRD sections they affect. A waived gap is recorded under PRD §8 as `Waived G-n: <gap>. Default assumed: <default or "architects decide">`.

**Open gaps:** <n> (or `No open gaps.`)
