---
name: apf-arch
description: "Run the architecture phase for one PRD, on demand. Spawns an architect team (AExpert, ACore, ACloud, ASolution) that drafts a spec you approve first (gate 1), assesses the code and proposes options (gate 2), completes the spec, drafts the SOP you approve (gate 3), and then writes the plan. Use when the user says \"apf-arch\", \"architecture for PRD-001\", \"turn this PRD into a spec and plan\", or has a PRD in prds/ published by apf-create-prd and wants it specified and planned. Takes the PRD id (e.g. PRD-001). Nothing runs on its own: without this command no PRD is picked up. Ends with plans/SPEC-NNN.md ready; the user runs /apf-dev next."
---

# apf-arch

Invocation: `/apf-arch PRD-NNN`. This session runs the **architecture phase** for that one PRD: spec draft (gate 1) → assessment (gate 2) → completed spec → SOP (gate 3) → plan. It ends when the plan is written, and then the session stops. Nothing watches any directory: the command does exactly this one PRD's architecture, and only when the user invokes it.

You are the **EM** (main session). Read `roles/engineering-manager.md` and follow its **"Command: apf-arch"** section (and the shared sections it points to). You never plan, design or write code yourself: **AExpert** (`roles/architect-chief.md`) owns the architecture flow, and you relay its gates to the user exactly as the EM role describes. The complete picture and rules are in `README.md`.

**Paths.** `<skill dir>` is the folder containing this SKILL.md. Every relative path in `roles/`, `flows/` and `templates/` (e.g. `templates/spec.md`, `vendor/apf-deep-code`) is relative to it. Project artifacts (`prds/`, `research/`, `spikes/`, `specs/`, `sops/`, `plans/`, `drafts/`, `conventions.md`, `.agentic-team/`) are relative to the user's project root.

## Setup
1. **Foundations check.** `product-vision.md`, `product-guiding-principles.md` and `company-context.md` must exist in the project root (created once by the `apf-product-foundations` skill; `AGENTS.md` references them). If any is missing, stop and tell the user to run `/apf-product-foundations` first. Do not proceed without them unless the user explicitly says to.
2. Resolve the PRD from the argument: `prds/PRD-NNN-*.md`. If the argument is missing or matches nothing, list the PRDs in `prds/` and ask which one. There is no queue: one command, one PRD.
3. `repo` = `git rev-parse --show-toplevel`. Create the knowledge-repo directories if missing: `specs/ sops/ plans/ drafts/ .agentic-team/`. Initialize or update `.agentic-team/state.json` (see the EM role for its shape; keep existing data, you are its only writer **in this session**).
4. Base branch: the PRD's `Base: <branch>` line if it has one, otherwise `master`.
5. **Gap-clean precondition.** `apf-create-prd` publishes only after a `No open gaps.` round and records that clean version's hash in `state.json`. If the recorded hash does not match the PRD file, the PRD was edited after publication: run the PRD gap flow (`flows/prd-gap.md`) with PRDGap (`roles/prd-gap.md`) until a round reports no open gaps, applying the user's decisions, then record the new hash. Only then does architecture start.
6. Run `python3 <skill dir>/scripts/render-status.py` to create/refresh `.agentic-team/status.md` (the dashboard is still useful while this command runs; the user can `watch cat .agentic-team/status.md` in another terminal).

## Run the architecture phase
Spawn **AExpert** for the PRD (description `[AExpert] PRD-NNN architecture`, prompt = `roles/architect-chief.md`, the PRD path, the base branch and the context-hygiene contract) and run it per `flows/architecture.md` and the EM role's "Command: apf-arch". The EM role has the message protocol: `STAGE <what>`, `GATE <n> <path>`, `SPAWN ...`, `PLAN <path> steps <P> waves <W>`.

- At each gate, set `waiting_on: you` and present it to the user; answer AExpert **verbatim** (approve, chosen option, or requested changes). Never answer a gate yourself.
- If the PRD already has a spec, SOP or plan (this is a re-run after an edit), tell AExpert to run **scoped to what changed**, with the existing artifacts as input, instead of starting over.
- On `PLAN <path> steps <P> waves <W>`: record the plan, steps and waves in `state.json`, set the PRD `planned`, create the integration branch `prd/PRD-NNN` from the base (without checking it out), and stop. AExpert is finished; never message it again. Tell the user in one line that the plan is ready and to run `/apf-dev PRD-NNN` (the TeamSizer will pick the team size from the plan and report it).

## Rules
- One command, one PRD: no watcher, no queue, nothing runs on its own. To architecture another PRD, run `/apf-arch` again (a new session); run one command at a time, because `.agentic-team/state.json` has a single writer.
- Never start architecture on a PRD whose last gap round is not clean (step 5).
- Gates are always the user's: the spec (1), the option (2) and the SOP (3) are approved by the user, never by an agent.
- The plan is not reviewed by the user; it goes straight to `plans/SPEC-NNN.md` and is built by `/apf-dev`.

## Dependencies
- Vendored in `vendor/` (read by path, not installed as separate skills): `apf-deep-code`, `apf-group-design`, `apf-deep-research`, `apf-plan` (adapted).
- Companion skills (installed separately, siblings in the same skills folder): `apf-product-foundations` (run once first), `apf-create-prd` (writes PRDs into `prds/` and runs PRDGap from this skill), `apf-research` (writes research requests), `apf-dev` (builds a plan produced here), `apf-spike` (runs research requests).
- `gh` must be installed and authenticated; GitHub is always the host.
- Templates (fixed, always used): `spec.md`, `sop.md`, `conventions.md`, `option-table.md`, `gap-report.md`, `prd-gap-report.md`, `handoff-package.md`, `pr-description.md`, `spike-document.md`, `spike-project-readme.md`. The research-request template lives in the `apf-research` skill.
