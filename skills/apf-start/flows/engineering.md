# Flow: engineering

Owner: EM. Capacity = number of lanes, fixed at invocation. A lane is a developer paired with a tester.

## Dispatch
1. The EM receives `plans/SPEC-NNN.md` (steps, waves, ordering constraints, N).
2. For each wave, the EM assigns units to **idle** lanes only. No idle lane means the units queue, even if the plan is ready.
3. The EM creates one worktree per unit (outside `prds/`, e.g. `../<repo>.worktrees/`), branching from the PRD integration branch `prd/PRD-NNN`.
4. The EM spawns the lane's developer and tester as subagents and gives each the spec, the SOP, the whole plan and its unit.

## Lane loop
developer works in the worktree, following `conventions.md` and running its mechanical checks (format, lint, types, tests) until clean → sends to tester (SendMessage), who re-runs the checks and reviews idiom → tester comments → developer addresses → … **cap 3 rounds**, then escalate to the EM (then the human). When the tester is satisfied it declares the unit complete and tells the EM: "I am done, I am now free." The EM marks the lane idle and dispatches the next queued unit.

A crashed or stalled lane: the EM reassigns its unit to another idle lane.

## Merge
- Plan split across lanes: after a wave completes, the EM spawns the **WaveMerger** with `templates/handoff-package.md`. It merges into `prd/PRD-NNN`, resolves conflicts, runs the full suite and the reproducer. The next wave branches from the result.
- Plan taken by one lane: no WaveMerger; that worktree is the output.

## Finish
1. The EM spawns the **Verifier** on the output worktree.
2. `CONFORMS` → the EM pushes `prd/PRD-NNN` and opens a PR with `gh pr create` using `templates/pr-description.md`.
3. Gaps → `flows/requirement-gap.md`.
