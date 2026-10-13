---
name: apf-create-prd
description: Interview the user and write a PRD in the fixed PRD template (`templates/prd.md` in this skill) to prds/, ready for /apf-arch PRD-NNN to take into architecture. Use when the user says "apf-create-prd", "write a PRD", "new PRD", "I want to spec a feature for the agentic team", or wants to start with a new product requirement. Nothing runs on its own: the published PRD waits until the user runs /apf-arch.
---

# apf-create-prd

You help the human write a PRD good enough for the architecture team to act on. Nothing watches `prds/`, so publishing the file starts nothing by itself; the PRD must be complete and gap-clean first, because `/apf-arch PRD-NNN` takes it straight to the architect team.

Template: `templates/prd.md` in this skill's directory. Use it exactly; do not add or drop sections.

## 1. Orient
- `prds/` existing files: the next ID is the highest `PRD-NNN` + 1 (start at `PRD-001`). Create `prds/` and `drafts/` if missing.
- Read `product-vision.md`, `product-guiding-principles.md` and `company-context.md` if present (created by `/apf-product-foundations`; if absent, suggest running it first, but do not block). Skim `spikes/` (completed research: `docs/` and `projects/`), `market-analysis` and related PRDs; if the PRD needs research that does not exist yet, suggest `/apf-research` first. Ask only what they do not answer.
- Keep the PRD consistent with them. If a requirement the user wants conflicts with the vision or a hard constraint (HC-n), say so and let the user decide; record the conflict under Risks and open questions.
- If the user brought notes, a ticket or a rough idea, start from that.

## 2. Interview
Ask in small batches (use `AskUserQuestion` for choices, plain questions for open answers), only for what is missing. Cover, in order:
1. The problem: what is wrong or missing, for whom, evidence.
2. Goals and non-goals.
3. Users and the key scenarios.
4. Requirements, each with a priority (Must/Should/Could) and acceptance criteria.
5. Success metrics, with a target and how it is measured.
6. Constraints and dependencies, risks, open questions, references.

Rules while interviewing:
- Push back on vague requirements ("fast", "scalable", "easy"). Ask for a measurable criterion, or record it as an open question.
- A requirement states what, never how. Move design ideas into Constraints or References, or drop them; the architects decide the design.
- One requirement per row, each testable. IDs are `PR-1`, `PR-2`, ... and stay stable once written.
- Do not invent facts, metrics or evidence. Unknown goes in Open questions.

## 3. Draft
Write the draft to `drafts/PRD-NNN.md` (not `prds/`). Show it to the user and edit it in place for requested changes. Status stays `Draft`.

## 3b. Gap analysis (after every change to the draft)
Run the PRD gap flow from the sibling `apf-arch` skill (`../apf-arch/flows/prd-gap.md`, role `../apf-arch/roles/prd-gap.md`, report template `../apf-arch/templates/prd-gap-report.md`; if `apf-arch` is not installed, tell the user to install it and stop). The goal is that the team needs no questions after the spec and SOP sign-off.
1. Spawn a subagent with description `[PRDGap] PRD-NNN analysis` and the role file; it writes `drafts/PRD-NNN.gaps.md`.
2. For each open gap, ask the user with `AskUserQuestion`: the proposed answer (with its evidence) as the recommended option, plus "edit" and "waive". `needs-human` gaps get an open question or a waiver.
3. Apply the decisions: accepted or edited answers go into the sections they affect (keep PR-n IDs stable; a new requirement takes the next free number); a waiver goes under section 8 as `Waived G-n: <gap>. Default assumed: <default or "architects decide">`.
4. That edit is a modification, so run the analysis again. Repeat until a round reports `No open gaps.` The same applies to any edit the user makes to the draft at any time.

## 4. Publish
Only when the user says it is ready **and the last gap analysis round reported `No open gaps.`** (if the draft changed since, run it again first):
1. Set Status to `Ready`, set the date.
2. Write it to `prds/PRD-NNN-<short-slug>.md` in a single write. Remove the draft.
3. Record the clean version in `.agentic-team/state.json` (create `.agentic-team/` and the file if missing; keep every existing entry): under `prds["PRD-NNN"]` set `path`, `title`, `phase: "queued"`, `gap_clean_hash` = the file's SHA-1 (`shasum -a 1 <path>`), and `updated`. This records that the published version passed a clean gap round; `/apf-arch` checks it before spawning AExpert and re-runs the gap analysis if the file changes later.
4. Tell the user the path and that nothing picks it up on its own: run `/apf-arch PRD-NNN` when ready.
