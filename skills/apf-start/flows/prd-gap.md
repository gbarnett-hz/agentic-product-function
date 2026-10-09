# Flow: PRD gap analysis

Owner: whoever holds the PRD (the `apf-create-prd` skill while drafting, the EM once the PRD is in `prds/`). Purpose: close the human-answerable questions **before** architecture, so everything after gates 2 and 3 can run without asking the human.

It runs after **every** modification of the PRD, with no exceptions: a gap answer is itself a modification, so the loop repeats until a round finds nothing.

| Step | Actor | Input | Output |
|---|---|---|---|
| 1 | caller | a new or modified PRD | spawns PRDGap |
| 2 | PRDGap | PRD, foundations, knowledge repo, code and git, web | `drafts/PRD-NNN.gaps.md` (open gaps only, max 10) |
| 3 | caller | the report | zero gaps: done. Otherwise show each gap with its proposed answer |
| 4 | **you** | each gap | `accepted`, `edited` or `waived` (`needs-human` gaps get an answer or a waiver) |
| 5 | caller | decisions | PRD updated (accepted/edited answers into the sections they affect; waivers under §8). This is a modification: back to step 1 |

Done = a round with **No open gaps**. Only then may the PRD be published (`apf-create-prd`) or handed to the EM to spawn AExpert.

## Triggers
- `apf-create-prd`: after every draft change, including the user's own edits. The PRD is published only when the last round is clean.
- EM, `NEW_PRD`: before architecture. The PRD may have been written without the skill.
- EM, `MOD_PRD` (the watcher reports an edited PRD): run the flow on the new version, ignoring changes the EM made itself (`own_write` in `state.json`). Then:
  - while AExpert is still running (before it hands over the plan): send it the new PRD to re-run scoped to what changed;
  - after the plan was handed over: tell the user in one line and ask whether to spawn a new AExpert for a scoped re-run.

## Rules
- PRDGap reports; it never edits the PRD and never talks to the user. The caller does both.
- Keep PR-n IDs stable. A new requirement from an accepted answer takes the next free number.
- A waived gap is not re-raised unless a later change invalidates its default.
- Gap questions to the user are about the PRD, not architecture, so the EM may ask them directly. AExpert is not spawned yet (or, for a later edit, is only told afterwards).
