---
name: apf-group-design
description: Turn one architectural objective into a short, ranked, fully-cited set of competing implementation approaches. Spawns 5+ subagents that each argue a genuinely different way to achieve the objective, then a final agent ranks them by risk, complexity, rolling-upgrade impact, and backwards compatibility. Use whenever the user wants an architecture/design decision explored from multiple angles rather than a single recommendation — phrases like "how should we approach X", "give me some design options for X", "what's the best way to build X", "group design", or "I need an architecture review before we commit to an approach". Every claim in every agent's output must cite a file:line or URL — do not use this for quick lookups, single-obvious-answer questions, or non-architectural coding tasks.
---

# Group Plan

Triangulate an architecture decision instead of committing to the first idea. One objective goes in; 5+ independently-reasoned approaches come out, each grounded in citations, followed by a short ranked verdict that calls out the subtleties (rolling upgrades, backwards compatibility, operational risk) a single pass tends to skip.

## 1. Frame the objective

Restate the user's objective as a concrete, scoped engineering problem. If it's too vague to hand to independent agents (no target system, no rough boundary of what's in/out of scope), ask one clarifying question rather than guessing.

## 2. Build focused context

Before spawning the opposing-view agents, ground them in the actual codebase — otherwise they'll all independently re-discover the same files and burn time doing it, or worse, hallucinate structure. Do a quick focused review yourself (Grep/Glob/Read the relevant modules, `git log` on the relevant paths for recent history) and write up a short context brief: what exists today, the key files/interfaces involved, and any constraints you already know about (e.g. this is a clustered system, this path is on the rolling-upgrade wire protocol, etc).

If the objective spans an area you don't know well enough to scope quickly, it's fine to delegate this step to a single `Explore` agent instead — just make sure its findings (with file:line citations) get folded into the brief every subsequent agent receives. Don't skip the brief entirely; agents with zero shared context tend to converge on the same generic answer instead of genuinely diverging.

## 3. Launch 5+ opposing-view agents in parallel

Use the `Agent` tool with `subagent_type: "general-purpose"`, and send all of them in **one message** with multiple tool calls so they run concurrently.

Each agent gets the same objective and the same context brief from step 2, but a distinct angle to argue for. Pick angles that would actually disagree with each other given the objective — not cosmetic variations of the same plan. Depending on the objective, draw from things like:

- **Minimal-diff approach**: smallest change that satisfies the objective within the existing architecture, even if it's not the "cleanest" long-term shape.
- **Clean-slate/idiomatic approach**: how you'd build this if starting from the current codebase's own conventions with no legacy constraint, favoring maintainability over minimal diff.
- **Performance/scalability-first approach**: optimizes for throughput, memory, or cluster-scale behavior even at the cost of complexity.
- **Operational-safety-first approach**: optimizes for rolling upgrades, backwards compatibility, rollback safety, and minimizing blast radius, even at the cost of elegance or speed.
- **Alternative-technology approach**: solves it with a different existing dependency, library, or pattern already present in the codebase (or a well-established external one) rather than hand-rolling it.
- **Adversarial/"why not to do this at all" approach**: actively argues for the simplest possible non-solution (config change, existing feature, doing nothing) or surfaces the strongest reason the objective itself is the wrong ask.

Use whichever 5+ of these (or other genuinely opposing angles) fit the objective — the requirement is real disagreement, not a fixed list.

Each agent's prompt must state, verbatim in substance:
- The objective, restated concretely.
- The context brief from step 2.
- Its specific angle to argue, and that it should optimize its proposal for that angle even where it trades off against the others.
- It may ground its proposal in the source code, `git log`/`git blame` history, and/or web search (docs, specs, issues, blog posts) — its choice how to mix them, appropriate to the claim being made.
- **Every factual or architectural claim must carry a citation**: `path/to/file:line` for source code, or a URL for external material. No citation, no claim — drop anything it can't source rather than asserting it unsourced.
- Report as: a short proposal description, then a flat list of cited claims supporting it (including known risks/tradeoffs of its own approach — don't let it only cite in its own favor).

## 4. Launch the ranking agent

Once all opposing-view agents report back, launch one more `general-purpose` agent (or do this synthesis yourself if the proposals are simple enough that delegating loses more context than it saves — use judgment) whose only job is to rank the proposals.

Give it all 5+ proposals verbatim, with their citations intact. Its job:
- Rank the approaches by risk, complexity, and any other criteria that clearly matter for this objective — state the criteria it used.
- Specifically call out rolling-upgrade impact and backwards compatibility for each approach where the objective touches a system where that matters (clustered/distributed components, wire protocols, persisted formats, public APIs) — don't skip this even if no input agent raised it; if none of them addressed it, say so explicitly rather than silently omitting it.
- Keep every claim cited, same rule as step 3 — it can reuse the input agents' citations or add its own, but nothing uncited survives into the final ranking.
- Adopt an objective critical view when ranking: take into account idiomatic codebase extension, architectural and design best practices. Your objective is to be an expert in the codebase, distributed system design and subtleties that arise from under specified design.
- Produce a short, succinct architectural/design impact review, not a restatement of all 5 proposals in full.

## 5. Output format

Keep the final answer short and scannable — a decision aid, not a report:

```
## Objective
<restated concretely>

## Approaches considered
1. <name/angle> — <one-line summary> [key citations]
2. ...

## Ranking (risk / complexity / rolling-upgrade & compatibility impact)
1. <approach> — <why it ranks here, cited>
   - Rolling upgrade impact: <cited assessment, or "not addressed by any proposal">
   - Backwards compatibility: <cited assessment>
2. ...

## Recommendation
<1-3 sentences, built only from the cited findings above>
```

Drop any bullet that has no citation backing it rather than smoothing it over with judgment-only prose — the whole point of this workflow is that nothing in the final answer is a single agent's unsupported opinion.
