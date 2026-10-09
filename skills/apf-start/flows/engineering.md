# Flow: engineering

Owner: EM. Capacity = number of lanes, fixed at invocation. A lane is a developer paired with a tester.

Every transition below is announced by the EM (chat line, `state.json`, `.agentic-team/status.md`; see "Status updates" in `roles/engineering-manager.md`). On the plan arriving the EM sets the totals: P = number of Todo steps, W = number of waves.

## Dispatch
1. The EM receives `plans/SPEC-NNN.md` (steps, waves, ordering constraints, N).
2. For each wave, the EM assigns units to **idle** lanes only. No idle lane means the units queue, even if the plan is ready.
3. The EM creates one worktree per unit, each with its own isolation key, port block and `$TMPDIR` (`roles/engineering-manager.md`, "Test isolation"), so tests in one worktree never affect another; a unit marked `Exclusive:` waits for its resource. Worktrees live outside `prds/` (e.g. `../<repo>.worktrees/`) and branch from the PRD integration branch `prd/PRD-NNN`.
4. The EM spawns a **new** developer and a **new** tester for the unit (never the previous unit's agents) and gives each the paths to the spec, the SOP and the plan and a **unit brief** (the plan step numbers, their `Cites:` lines with requirement IDs, SOP scenario IDs and spec sections, and the files owned), plus the context-hygiene contract (`SKILL.md`). Developer and tester read only what is relevant to their unit, not the whole spec, SOP and plan.

## Lane loop
developer works in the worktree, following `conventions.md` and running its mechanical checks (format, lint, types, tests) until clean → sends to tester (SendMessage), who re-runs the checks and reviews idiom → tester comments → developer addresses → … **cap 3 rounds**, then escalate to the EM (then the human). When the tester is satisfied it declares the unit complete and tells the EM which plan steps are complete and "I am done, I am now free." The EM adds them to the PRD's done count and reports `step N/P`. The unit's two agents are now finished. The EM marks the lane idle and dispatches the next queued unit to it with a fresh pair.

A crashed or stalled lane: the EM reassigns its unit to another idle lane. Work sent back after a unit is complete (a WaveMerger conflict or a red merged suite) goes to a **new** developer, with a fix brief (the hunk or failing output, the lane report path, the branch), not to the finished agent.

## Merge
- Plan split across lanes: after a wave completes, the EM spawns a new **WaveMerger** with `templates/handoff-package.md` (paths and branches, not diffs). It merges into `prd/PRD-NNN`, resolves conflicts, runs the full suite and the reproducer. The next wave branches from the result.
- Plan taken by one lane: no WaveMerger; that worktree is the output.

## Finish
1. The EM spawns a new **Verifier** on the output worktree (a new one for every cycle).
2. `CONFORMS` → the EM pushes `prd/PRD-NNN` and opens a PR with `gh pr create` using `templates/pr-description.md`.
3. Gaps → `flows/requirement-gap.md`.
