---
name: apf-dev
description: Build a PRD's plan with an auto-sized pool of developer+tester lanes, on demand. Run it after /apf-arch has produced plans/SPEC-NNN.md: a TeamSizer agent reads the plan and picks the optimal team size, reporting its number and reasoning, and the EM dispatches the plan's units to idle lanes in git worktrees wave by wave; a tester signs off each unit, a WaveMerger merges each wave, a Verifier checks the result against the PRD, spec and SOP, and the branch is pushed and a GitHub PR opened with gh. Use when the user says "apf-dev", "build the plan", "take the plan and pick a team size", or has a plan ready and wants the development team to execute it. Takes the PRD id (optional when only one plan is ready); the team size is always chosen by the TeamSizer. Nothing runs on its own: without this command no plan is built. For the spec/SOP/plan phase use /apf-arch.
---

# apf-dev

Invocation: `/apf-dev [PRD-NNN]`. This session runs the **engineering phase** for one PRD whose plan already exists (`plans/SPEC-NNN.md`, written by `/apf-arch`): a **TeamSizer** agent picks the team size from the plan, and a fixed pool of that many developer+tester lanes builds it in worktrees, merges it wave by wave, verifies it against the PRD, spec and SOP, pushes the branch and opens the PR. It ends when the PR is open. Nothing watches any directory: the work starts only when the user invokes this command.

The team size is never asked of you: a **TeamSizer** agent reads the plan (waves, per-step size, `Exclusive:` resources) and picks it. Its number and reasoning are printed in the chat before work starts, and the full analysis is written to `.agentic-team/reports/PRD-NNN/team-size.md`.

You are the **EM** (main session). Read `roles/engineering-manager.md` and follow its **"Command: apf-dev"** section (and the shared sections it points to). You never write code yourself: the lanes do the work, wave by wave.

**Paths.** This skill's assets live in the sibling `apf-arch` skill: `<arch dir>` = `../apf-arch` (relative to this skill's folder). Every relative path below (`roles/`, `flows/`, `templates/`, `scripts/`) is relative to `<arch dir>`. Project artifacts (`prds/`, `specs/`, `sops/`, `plans/`, `conventions.md`, `.agentic-team/`) are relative to the user's project root.

## Setup
1. **Foundations check.** `product-vision.md`, `product-guiding-principles.md` and `company-context.md` must exist in the project root. If any is missing, stop and tell the user to run `/apf-product-foundations` first.
2. Resolve the PRD: the argument if given; otherwise the PRD(s) with a `plans/SPEC-NNN.md` and no PR yet in `.agentic-team/state.json`. If there is more than one, list them and ask. The plan must exist: if it does not, stop and tell the user to run `/apf-arch PRD-NNN` first.
3. **Team size.** Spawn a new **TeamSizer** (`<arch dir>/roles/team-sizer.md`) on the plan and `conventions.md`, per the EM role's "Team size": it replies `LANES <n>` and its reasoning, and writes `.agentic-team/reports/PRD-NNN/team-size.md`. Print the number and the reasoning in the chat (a short block, plus the report path). N is now fixed for the session: lanes are named `L1`..`LN`.
4. `repo` = `git rev-parse --show-toplevel`. Create the knowledge-repo directories if missing (`prds/ specs/ sops/ plans/ drafts/ .agentic-team/`). Update `.agentic-team/state.json`: write N idle lanes `L1`..`LN`, record `team_size`, keep every other slice untouched (the EM role has the shape). Worktrees go under `<repo>/../<name>.worktrees/`.
5. Run `python3 <arch dir>/scripts/render-status.py` to create/refresh `.agentic-team/status.md`, the dashboard the user can `watch cat`.

## Run the engineering phase
Run `flows/engineering.md` and the EM role's "Command: apf-dev" + "Test isolation" + "Context hygiene" sections: dispatch the plan's waves to idle lanes with a new developer and tester per unit, merge each wave with a WaveMerger, run the Requirement Gap flow when the Verifier reports gaps (cap 2 cycles), and on `CONFORMS` push `prd/PRD-NNN` and open the PR with `gh pr create` using `templates/pr-description.md`. Keep the state and the dashboard current at every transition; the user can walk away and read the chat line or the dashboard.

## Stop conditions
- The PR is open: record the URL, tell the user in one line, stop. Review and merge the PR yourself.
- A cap escalates to the user (dev-test rounds, WaveMerger conflicts, Requirement Gap cycles): stop the affected work, put the question to the user, and continue what is not blocked.
- The Verifier still reports gaps after 2 gap cycles: tell the user with the history and stop.

## Dependencies
- Companion skills (installed separately, siblings in the same skills folder): `apf-arch` (must be installed; it holds the roles, flows, templates and scripts this command uses), `apf-product-foundations` (run once first), `apf-create-prd` (writes the PRDs), `apf-research` and `apf-spike` (research).
- `gh` must be installed and authenticated; GitHub is always the host.
- `python3` for the status dashboard.
