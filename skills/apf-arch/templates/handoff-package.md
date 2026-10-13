# WaveMerger handoff package: PRD-<NNN>, wave <w>

The WaveMerger reads this before touching any worktree.

- **Spec:** `specs/SPEC-NNN.md` (requirement IDs)
- **SOP:** `sops/SOP-NNN.md`
- **Plan:** `plans/SPEC-NNN.md` (ordering constraints, waves)
- **Integration worktree:** `<path>`, branch `prd/<slug>`
- **Base commit:** `<sha>`

## Units merged in this wave
| Unit (plan step) | Lane | Worktree / branch (read its diff with `git diff`) | Owns files | Requirement IDs | Report (path) |
|---|---|---|---|---|---|

## Per-lane report (one file per unit, `.agentic-team/reports/PRD-NNN/unit-<steps>.md`; referenced here, not pasted)
- What changed, and why
- Interfaces touched (signatures, config keys, schemas)
- Tests added and how to run them
- Assumptions made

## After the merge
1. Run the full suite and the plan's reproducer.
2. Conflicts: resolve using the units' file ownership and requirement IDs. If unresolved, send the hunk, both sides and this package to the EM for a new developer on that unit (cap 3), then escalate to the EM.
