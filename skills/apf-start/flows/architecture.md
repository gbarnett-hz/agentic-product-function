# Flow: architecture

Owner: AExpert, a spawned agent per PRD. The human-facing flow: AExpert writes each gate to a file and the EM relays it to the user and the answer back. **Lifetime:** the architecture function for a PRD exists from the EM's spawn of AExpert (PRD gap-clean) until AExpert hands the plan to the EM; then AExpert and every architecture agent are finished. Later work (Requirement Gap, PRD change after the plan) gets a new AExpert given the files.

Each step is announced by the EM as a status update (`roles/engineering-manager.md`, "Status updates"); at gates the PRD is `waiting_on: you`.

Precondition (gate 0): `flows/prd-gap.md` reported `No open gaps.` for the current version of the PRD. The EM does not start this flow otherwise.

| Step | Actor | Input | Output | Next |
|---|---|---|---|---|
| 1 | EM | `prds/PRD-NNN.md` | spawns AExpert | AExpert |
| 2 | AExpert | PRD, foundations, knowledge repo | `drafts/SPEC-NNN.md`: given-when-then scenarios for every PRD requirement, sections 1-4 only (no code analysis yet) | gate 1 |
| 3 | **Gate 1** (human, via the EM) | draft spec | approval, or changes (loop to 2) | `specs/SPEC-NNN.md` |
| 4 | ACore | approved spec, PRD, repo | understanding + candidate options (apf-deep-code → apf-group-design) | ACloud, ASolution, AExpert |
| 5 | ACloud, ASolution (parallel) | ACore output | cloud impact, enterprise fit (apf-deep-research) | AExpert |
| 6 | AExpert + adversarial agents | all outputs | findings; redo requests (cap 2 rounds) | architects or gate 2 |
| 7 | **Gate 2** (human, via the EM) | `templates/option-table.md` | chosen option | AExpert |
| 8 | AExpert | chosen option | completes the spec's sections 5-12 in `specs/SPEC-NNN.md` (no re-approval) | SOP |
| 9 | SOP | completed spec | `drafts/SOP-NNN.md` (+ gaps) | gate 3 |
| 10 | **Gate 3** (human, via the EM) | draft SOP | approval, or scoped re-run of the architecture flow (fresh 2-round cap) | `sops/SOP-NNN.md` |
| 11 | AExpert | spec AND SOP approved | `plans/SPEC-NNN.md` (apf-plan, parallel by default); AExpert replies `PLAN` and is shut down | EM |

Rules:
- The spec is approved before any code analysis: its scenarios are design-independent (no implementation, technology or file paths). Sections 5-12 (design, cloud, enterprise, decision record) are completed after the option choice with no further approval. If the analysis forces a change to an approved scenario (sections 1-4), that delta needs re-approval through gate 1.
- Spec changes caused by SOP feedback need re-approval of the delta only.
- Drafts live in `drafts/`; `specs/` and `sops/` hold only approved artifacts.
- Gate to the EM = spec approved AND SOP approved.
