---
name: apf-research
description: Interview the user and write a research request in the fixed spike-request template to research/, ready for /apf-spike to hand it to a team of researchers. The result is a spike (a document or a small project) in spikes/. Use when the user says "/apf-research", "research this", "run a spike", "investigate X", "I need a spike on", or wants the agentic team's researchers to look into a question thoroughly, adversarially and objectively. Nothing runs on its own: the request waits until the user runs /apf-spike.
---

# apf-research

You help the human write a research request good enough for a researcher to take in its entirety and close with a document or a small project. Nothing watches `research/`, so publishing the file starts nothing by itself; the request must be complete first, because `/apf-spike` hands it whole to one researcher lane.

Template: `templates/research-request.md` in this skill's directory. Use it exactly; do not add or drop sections.

## 1. Orient
- `research/` existing files: the next ID is the highest `RR-NNN` + 1 (start at `RR-001`). Create `research/` and `drafts/` if missing.
- Read `product-vision.md`, `product-guiding-principles.md` and `company-context.md` if present (created by `/apf-product-foundations`). Skim `prds/`, `specs/` and `spikes/` for related work, so you do not request research that already exists. If a matching spike exists, show it to the user and ask whether to extend it.
- If the user brought notes, a ticket, or a rough idea, start from that.

## 2. Interview
Ask in small batches (`AskUserQuestion` for choices, plain questions for open answers), only for what is missing. Cover, in order:
1. The objective: what decision or work this research informs, and for whom. Link a PRD or spec if there is one.
2. The research questions: specific and answerable. Push back on vague ones ("is X good?") and turn them into questions with a checkable answer (compared against what, measured how, under which constraints).
3. Context: what is already known, tried or decided; links.
4. Scope and non-goals.
5. Sources to consult (repo, web, papers, industry standards, other) and any to exclude or distrust.
6. Depth: `quick`, `standard` or `deep` (see the template).
7. Exit criteria: what must be true to close the request.
8. Deliverable: a document, a project, or `ResearchJudge decides`. Default to `ResearchJudge decides`.
9. Constraints: hard constraints (HC-n) the investigation or any prototype must respect, and anything else.

Rules while interviewing:
- Do not invent facts, context or sources. Unknown goes in Open questions.
- A request asks for knowledge, not a decision made for the user: the spike will recommend, the human decides.
- Each question gets an ID (`Q-1`, `Q-2`, ...). Exit criteria refer to question IDs.
- Keep one request to one coherent objective. If the user's ask is really two investigations, offer to write two requests.

## 3. Draft
Write the draft to `drafts/RR-NNN.md` (not `research/`). Show it to the user and edit it in place for requested changes. Status stays `Draft`.

## 4. Publish
Only when the user says it is ready:
1. Set Status to `Ready`, set the date.
2. Write it to `research/RR-NNN-<short-slug>.md` in a single write. Remove the draft.
3. Tell the user the path and that nothing picks it up on its own: run `/apf-spike RR-NNN researchers=M` when ready (or `/apf-spike researchers=M` to run every pending request in `research/`).
4. Say where the result will appear: `spikes/docs/RR-NNN-<slug>.md` or `spikes/projects/RR-NNN-<slug>/`.
