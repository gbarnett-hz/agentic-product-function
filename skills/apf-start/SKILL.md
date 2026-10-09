---
name: apf-start
description: Run a product function as a team of agents. An engineering manager watches prds/ for new PRDs, an architect team (AExpert, ACore, ACloud, ASolution) assesses each one, you approve an option, then a spec and an SOP at three human gates, and a fixed pool of developer+tester lanes builds the plan in git worktrees, verifies it against the PRD, spec and SOP, and opens a PR with gh. Use when the user says "apf-start", "start the product team", or wants PRDs dropped into a folder to be assessed, specified and built by an agent team. Also runs a team of researchers. The research/ directory is watched too, and each research request is taken by one researcher lane (researcher, the ResearchJudge, ResearchDocWriter, engineer) and closed with a spike in spikes/. Takes lanes=N researchers=M.
---

# apf-start

Invocation: `/apf-start lanes=N researchers=M`. N engineering lanes (each a developer paired with a tester) and M researcher lanes (each a researcher, ResearchJudge, ResearchDocWriter and ResearchEngineer) are fixed for the session. Each lane owns its own four agents, 1:1 with its researcher like developer:tester, so M researchers give M ResearchDocWriters and M ResearchEngineers with no shared bottleneck. `researchers=0` turns the research function off.

You are the **EM** (main session). Read `roles/engineering-manager.md` and follow it. When a PRD lands (or is modified), you run `flows/prd-gap.md` with **PRDGap** (`roles/prd-gap.md`) until it reports no open gaps, then hand over to **AExpert** (`roles/architect-chief.md`), a role you play, and run `flows/architecture.md`. Then run `flows/engineering.md`, and `flows/requirement-gap.md` when the Verifier reports gaps. When a research request lands in `research/`, run `flows/research.md`. Several PRDs can be in flight; keep the user informed at every transition (chat line plus `.agentic-team/status.md`). The complete picture and rules are in `README.md`.

**Paths.** `<skill dir>` is the folder containing this SKILL.md. Every relative path in `roles/`, `flows/` and `templates/` (e.g. `templates/spec.md`, `vendor/apf-deep-code`) is relative to it. Project artifacts (`prds/`, `research/`, `spikes/`, `specs/`, `sops/`, `plans/`, `drafts/`, `conventions.md`, `.agentic-team/`) are relative to the user's project root.

## Setup
0. **Foundations check.** `product-vision.md`, `product-guiding-principles.md` and `company-context.md` must exist in the project root (created once by the `apf-product-foundations` skill; `AGENTS.md` references them). If any is missing, stop and tell the user to run `/apf-product-foundations` first. Do not proceed without them unless the user explicitly says to.
1. Parse `lanes=N` (positive integer) and `researchers=M` (integer, 0 allowed). Ask once for whichever is missing.
2. `repo` = `git rev-parse --show-toplevel`. Create the knowledge-repo directories if missing: `prds/ specs/ sops/ plans/ drafts/` and `.agentic-team/`; and, if M ≥ 1, `research/ spikes/docs/ spikes/projects/`.
3. Write `.agentic-team/state.json` with N idle lanes and M idle researcher lanes (shape in `roles/engineering-manager.md`), then run `python3 <skill dir>/scripts/render-status.py` to create the dashboard `.agentic-team/status.md`. From here on, announce every state transition (see "Status updates" in the EM role).
4. Arm the PRD watcher with Monitor: `python3 <skill dir>/scripts/watch-dir.py prds .agentic-team/seen.txt PRD edits`.
5. If M ≥ 1, arm the research watcher with a second Monitor: `python3 <skill dir>/scripts/watch-dir.py research .agentic-team/seen-research.txt RESEARCH`.

## Naming running agents
Every subagent you spawn gets a `description` that starts with its label in brackets, then the PRD or request and the unit, so the agent list shows who is doing what: `[PRDGap] PRD-001 analysis`, `[ACore] PRD-001 design`, `[Developer-2] PRD-001 unit 3`, `[Tester-2] PRD-001 unit 3`, `[WaveMerger] PRD-001 wave 1`, `[Verifier] PRD-001 verify`, `[SOP] PRD-001 SOP`, `[Researcher-1] RR-004 angle: pricing`, `[ResearchJudge] RR-004 the ResearchJudge`. Labels: `PRDGap`, `AExpert`, `ACore`, `ACloud`, `ASolution`, `SOP`, `Developer-<lane>`, `Tester-<lane>`, `WaveMerger` (WaveMerger), `Verifier`, `Researcher-<lane>`, `ResearchJudge`, `ResearchDocWriter`, `ResearchEngineer`. The EM and AExpert are the main session. Where an agent can be given a name to message it by, use the same label.

## Dependencies
- Vendored in `vendor/` (read by path, not installed as separate skills): `apf-deep-code`, `apf-group-design`, `apf-plan` (adapted).
- Companion skill `apf-product-foundations` (installed separately, sibling): run once first; creates the three foundation files and references them from `AGENTS.md`.
- Companion skill `apf-research` (installed separately, sibling): the human uses it to write research requests into `research/` with the request template.
- Companion skill `apf-create-prd` (installed separately, sibling of this skill): the human uses it to write PRDs into `prds/` with the PRD template. It runs PRDGap from this skill (`roles/prd-gap.md`, `flows/prd-gap.md`, `templates/prd-gap-report.md`).
- Referenced, not vendored: `deep-research` from Anthropic's `anthropic-skills`. It must be installed.
- `gh` must be installed and authenticated; GitHub is always the host.
- Templates (fixed, always used): `spec.md`, `sop.md`, `conventions.md`, `option-table.md`, `gap-report.md`, `prd-gap-report.md`, `handoff-package.md`, `pr-description.md`, `spike-document.md`, `spike-project-readme.md`. The research-request template lives in the `apf-research` skill.
