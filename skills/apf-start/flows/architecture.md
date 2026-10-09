# Flow: architecture

Owner: AExpert (the main session, after the EM hands over). The only human-facing flow.

Precondition (gate 0): `flows/prd-gap.md` reported `No open gaps.` for the current version of the PRD. The EM does not start this flow otherwise.

| Step | Actor | Input | Output | Next |
|---|---|---|---|---|
| 1 | EM | `prds/PRD-NNN.md` | handover | AExpert |
| 2 | ACore | PRD, repo | understanding + candidate options (apf-deep-code → apf-group-design) | ACloud, ASolution, AExpert |
| 3 | ACloud, ASolution (parallel) | ACore output | cloud impact, enterprise fit (deep-research) | AExpert |
| 4 | AExpert + adversarial agents | all outputs | findings; redo requests (cap 2 rounds) | architects or gate 1 |
| 5 | **Gate 1** (human) | `templates/option-table.md` | chosen option | AExpert |
| 6 | AExpert | chosen option | `drafts/SPEC-NNN.md` | gate 2 |
| 7 | **Gate 2** (human) | draft spec | approval or changes (loop to 6) | `specs/SPEC-NNN.md` |
| 8 | SOP | approved spec | `drafts/SOP-NNN.md` (+ gaps) | gate 3 |
| 9 | **Gate 3** (human) | draft SOP | approval, or scoped re-run of the architecture flow (fresh 2-round cap) | `sops/SOP-NNN.md` |
| 10 | AExpert | spec AND SOP approved | `plans/SPEC-NNN.md` (apf-plan, parallel by default) | EM |

Rules:
- Spec changes caused by SOP feedback need re-approval of the delta only.
- Drafts live in `drafts/`; `specs/` and `sops/` hold only approved artifacts.
- Gate to the EM = spec approved AND SOP approved.
