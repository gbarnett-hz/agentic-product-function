# Flow: research

Owner: EM. Capacity = number of researcher lanes (`researchers=M`), independent of the engineering lanes. A researcher lane is four role agents: **researcher**, **ResearchJudge**, **ResearchDocWriter** and **ResearchEngineer**. Each lane owns its own four agents (1:1 with its researcher, like developer:tester), so `researchers=M` gives M of each and the producers are never a shared bottleneck. One request occupies a whole lane, from start to finish, and is never split across lanes.

```
research/RR-NNN-slug.md ─(NEW_RESEARCH)─► EM ─► idle researcher lane Rk

  Researcher ─ findings.md ─► ResearchJudge ─ judgement.md ─┬─► ResearchDocWriter ─► spikes/docs/RR-NNN-slug.md
      ▲                            │                        │
      └─ gaps, cap 2 rounds ───────┘                        └─► ResearchEngineer ──► spikes/projects/RR-NNN-slug/

  the ResearchDocWriter or ResearchEngineer tells the EM: "RR-NNN done, I am now free"
```

## Dispatch
1. The watcher prints `NEW_RESEARCH <path>`. The EM tells the user in one line and adds the request to `.agentic-team/state.json` as `queued`.
2. The EM assigns it to an **idle** researcher lane. If none is idle, it queues, even when other work is waiting. Researcher capacity is separate from the engineering lanes.
3. The EM spawns **new** agents for the lane (researcher, ResearchJudge and the producer; never agents from a previous request) and gives each its role file and the request path. They share the request only through `.agentic-team/research/RR-NNN/`. Intermediate artifacts live in `.agentic-team/research/RR-NNN/`.

## Stages
1. **researcher:** researches the request using `roles/researcher.md` (multi-agent, adversarial), and writes `findings.md`.
2. **ResearchJudge:** checks the findings against the request's exit criteria (sending gaps back to the researcher, cap 2 rounds), decides `document` or `project`, writes `judgement.md`, and routes to exactly one producer.
3. **ResearchDocWriter** (document) writes `spikes/docs/RR-NNN-<slug>.md`, or **ResearchEngineer** (project) builds and runs `spikes/projects/RR-NNN-<slug>/`.
4. The producer tells the EM "RR-NNN done, I am now free". The EM marks the lane idle, tells the user the artifact path in one line, and dispatches the next queued request.

## Rules
- No human gate in this flow. If a request is ambiguous the researcher records its assumption and continues; the spike lists assumptions and gaps. The user reads the result and decides.
- A crashed or stalled lane: the EM reassigns the request to another idle researcher lane.
- Spikes recommend; they never make decisions for the human.
- Architects, `apf-create-prd` and `/apf-research` read `spikes/` as research context.
- Spikes are left in the working tree; committing them is up to the user.
