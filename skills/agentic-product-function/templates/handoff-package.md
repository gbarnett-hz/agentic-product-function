# Integrator handoff package: PRD-<NNN>, wave <w>

The integrator reads this before touching any worktree.

- **Spec:** `specs/SPEC-NNN.md` (requirement IDs)
- **SOP:** `sops/SOP-NNN.md`
- **Plan:** `plans/SPEC-NNN.md` (ordering constraints, waves)
- **Integration worktree:** `<path>`, branch `prd/<slug>`
- **Base commit:** `<sha>`

## Units merged in this wave
| Unit (plan step) | Lane | Worktree / branch | Owns files | Requirement IDs | Report |
|---|---|---|---|---|---|

## Per-lane report (one per lane)
- What changed, and why
- Interfaces touched (signatures, config keys, schemas)
- Tests added and how to run them
- Assumptions made

## After the merge
1. Run the full suite and the plan's reproducer.
2. Conflicts: resolve using the units' file ownership and requirement IDs. If unresolved, send the hunk, both sides and this package to the owning lane (cap 3), then escalate to the EM.
