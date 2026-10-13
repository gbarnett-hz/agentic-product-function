---
name: apf-spike
description: "Run research requests with a team of researcher lanes, on demand. Each request written by /apf-research is taken whole by one lane (researcher, ResearchJudge, ResearchDocWriter, ResearchEngineer) and closed with a spike: a document in spikes/docs/ or a small project in spikes/projects/. Use when the user says \"apf-spike\", \"run the research\", \"run RR-001 with 2 researchers\", or has research requests in research/ and wants them answered. Takes an optional request id (default: every pending request) and researchers=M. Nothing runs on its own: without this command no request is picked up."
---

# apf-spike

Invocation: `/apf-spike [RR-NNN] researchers=M`. This session runs the **research phase**: M researcher lanes close research requests with spikes. A researcher lane is four role agents (researcher, ResearchJudge, ResearchDocWriter, ResearchEngineer), one lane per request, never shared. It ends when every selected request is done. Nothing watches any directory: requests sit in `research/` until the user invokes this command.

You are the **EM** (main session). Read `roles/engineering-manager.md` and follow its **"Command: apf-spike"** section (and the shared sections it points to). You never do the research yourself: the lanes do.

**Paths.** This skill's assets live in the sibling `apf-arch` skill: `<arch dir>` = `../apf-arch` (relative to this skill's folder). Every relative path below (`roles/`, `flows/`, `templates/`, `scripts/`) is relative to `<arch dir>`. Project artifacts (`research/`, `spikes/`, `.agentic-team/`) are relative to the user's project root.

## Setup
1. Parse `researchers=M` (integer ≥ 1; ask once if missing). The number of lanes is fixed for the session: `R1`..`RM`.
2. Select the requests: the `RR-NNN` argument if given; otherwise every `research/*.md` that has no spike yet (no matching artifact under `spikes/` and not recorded as done in `.agentic-team/state.json`). If none, tell the user there is nothing pending and stop.
3. `repo` = `git rev-parse --show-toplevel`. Create the knowledge-repo directories if missing: `research/ spikes/docs/ spikes/projects/ .agentic-team/`. Update `.agentic-team/state.json`: write M idle researcher lanes, keep every other slice untouched (the EM role has the shape).
4. Run `python3 <arch dir>/scripts/render-status.py` to create/refresh `.agentic-team/status.md`, the dashboard the user can `watch cat`.

## Run the research phase
Run `flows/research.md` and the EM role's "Command: apf-spike": assign each request to an idle lane, spawn the lane's four agents with their role files and the request path, and keep the state and dashboard current at every stage (researching, judging, producing). When the producer reports "done, I am now free", tell the user the artifact path in one line and dispatch the next queued request. When every selected request is done and every lane is idle, stop.

## Rules
- No human gate, no review: the spike lists its assumptions and gaps; you read it and decide.
- One request occupies one lane from start to finish; it is never split across lanes.
- Researcher capacity is `researchers=M`; if all lanes are busy, later requests queue until a lane frees.

## Dependencies
- Companion skills (installed separately, siblings in the same skills folder): `apf-arch` (must be installed; it holds the roles, flows, templates and scripts this command uses), `apf-research` (writes the requests), `apf-product-foundations` (run once first), `apf-create-prd` and `apf-dev` (the PRD-to-PR flow).
- `python3` for the status dashboard.
