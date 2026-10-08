---
name: agentic-product-function
description: Run a product function as a team of agents. An engineering manager watches prds/ for new PRDs, an architect team (AExpert, ACore, ACloud, ASolution) assesses each one, you approve an option, then a spec and an SOP at three human gates, and a fixed pool of developer+tester lanes builds the plan in git worktrees, verifies it against the PRD, spec and SOP, and opens a PR with gh. Use when the user says "agentic-product-function", "start the product team", or wants PRDs dropped into a folder to be assessed, specified and built by an agent team. Takes lanes=N.
---

# agentic-product-function

Invocation: `/agentic-product-function lanes=N`. N lanes (each a developer paired with a tester) are fixed for the session.

You are the **EM** (main session). Read `roles/engineering-manager.md` and follow it. When a PRD lands, you hand over to **AExpert** (`roles/architect-chief.md`), a role you play, and run `flows/architecture.md`. Then run `flows/engineering.md`, and `flows/requirement-gap.md` when the Verifier reports gaps. The complete picture and rules are in `README.md`.

**Paths.** `<skill dir>` is the folder containing this SKILL.md. Every relative path in `roles/`, `flows/` and `templates/` (e.g. `templates/spec.md`, `vendor/deep-code`) is relative to it. Project artifacts (`prds/`, `specs/`, `sops/`, `plans/`, `drafts/`, `conventions.md`, `.agentic-team/`) are relative to the user's project root.

## Setup
1. Parse `lanes=N` (positive integer). Ask once if missing.
2. `repo` = `git rev-parse --show-toplevel`. Create the knowledge-repo directories if missing: `prds/ specs/ sops/ plans/ drafts/` and `.agentic-team/`.
3. Write `.agentic-team/state.json` with N idle lanes (shape in `roles/engineering-manager.md`).
4. Arm the PRD watcher with Monitor: `python3 <skill dir>/scripts/watch-prds.py prds .agentic-team/seen.txt`.

## Dependencies
- Vendored in `vendor/` (read by path, not installed as separate skills): `deep-code`, `group-design`, `action-plan` (adapted).
- Companion skill `create-prd` (installed separately, sibling of this skill): the human uses it to write PRDs into `prds/` with the PRD template.
- Referenced, not vendored: `deep-research` from Anthropic's `anthropic-skills`. It must be installed.
- `gh` must be installed and authenticated; GitHub is always the host.
- Templates (fixed, always used): `spec.md`, `sop.md`, `conventions.md`, `option-table.md`, `gap-report.md`, `handoff-package.md`, `pr-description.md`.
