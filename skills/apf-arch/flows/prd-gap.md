# Flow: PRD gap analysis

Owner: the `apf-create-prd` skill while drafting; the `/apf-arch` command when a published PRD was edited. Purpose: close the human-answerable questions **before** architecture, so nothing after the spec gate has to stop and ask the human about the PRD.

It runs after **every** modification of the PRD, with no exceptions: a gap answer is itself a modification, so the loop repeats until a round finds nothing.

| Step | Actor | Input | Output |
|---|---|---|---|
| 1 | caller | a new draft or modified PRD | spawns PRDGap |
| 2 | PRDGap | PRD, foundations, knowledge repo, code and git, web | `drafts/PRD-NNN.gaps.md` (open gaps only, max 10) |
| 3 | caller | the report | zero gaps: done. Otherwise show each gap with its proposed answer |
| 4 | **you** | each gap | `accepted`, `edited` or `waived` (`needs-human` gaps get an answer or a waiver) |
| 5 | caller | decisions | PRD updated (accepted/edited answers into the sections they affect; waivers under §8). This is a modification: back to step 1 |

Done = a round with **No open gaps**. Only then may the PRD be published, and only then does architecture start on it: a published PRD whose content still matches the recorded clean hash goes straight to AExpert; any later edit must pass a clean round before the change reaches AExpert.

## Triggers
- `apf-create-prd`: after every draft change, including the user's own edits. The PRD is published only when the last round is clean, and the publish step records that version's hash in `.agentic-team/state.json`.
- `/apf-arch`, before spawning AExpert: if the PRD file's hash does not match the last recorded clean hash (the PRD was edited after it was published or after an earlier clean round), run the flow on the new version and record the new hash when a round is clean. Only then does AExpert start.
- If a published PRD changes while or after it has already been architected, the clean round is still the precondition: AExpert is told to re-run scoped to the change (see `flows/architecture.md`).

## Rules
- PRDGap reports; it never edits the PRD and never talks to the user. The caller does both.
- Keep PR-n IDs stable. A new requirement from an accepted answer takes the next free number.
- A waived gap is not re-raised unless a later change invalidates its default.
- Gap questions to the user are about the PRD, not architecture, so the caller may ask them directly, before AExpert is spawned (or, for a later edit, is only told afterwards).
