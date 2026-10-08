---
name: deep-code
description: Deep research into a specific area of a codebase, augmenting source-of-truth reading with web context (docs, specs, issues, blog posts, papers). Spawns multiple agents that each attack the target area from a different angle — implementation, history, tests, external docs/standards, prior art/alternatives — then reconciles their findings into one rigorously cited report. Use when the user asks to "deeply understand", "do deep research on", "deep-code", or "really dig into" a part of the codebase, especially when they want more than a summary of what the code does — they want why it's shaped that way, how it compares to the wider ecosystem, and what's not obvious from reading it alone. Do not use for quick lookups, single-file questions, or when a plain Explore/Read pass already answers the question.
---

# Deep Code

Turn "go deeply understand X part of the codebase" into a short, rigorously cited dossier: what the code does, why it's shaped that way, and how it holds up against external context (specs, docs, prior art, known pitfalls). No single pass — several agents attack the same target from different angles in parallel, every claim carries a citation, and nothing uncited survives into the final report.

## 1. Scope the target

Restate the user's target as a concrete area: a package, module, subsystem, or feature (e.g. "the CP subsystem's session heartbeat handling", not "CP subsystem" writ large — narrow it to something a handful of agents can actually cover in depth). If it's too broad to scope in one pass, do a quick `Explore`/Grep pass yourself first to find the real boundary (entry points, key classes, package layout) before delegating.

If genuinely ambiguous (multiple unrelated areas could match), ask one clarifying question rather than guessing.

## 2. Build a shared context brief

Before spawning angle agents, do a quick pass yourself (Glob/Grep/Read, `git log --oneline` on the relevant paths) to identify:
- The key files/classes/interfaces in scope, with paths.
- Any obvious recent history worth flagging (recent refactor, open TODO, a linked issue/ticket in a commit message).
- Related OS vs. enterprise counterparts if this repo's `CLAUDE.md` structure applies (check both `hazelcast/` and `hazelcast-enterprise/` for the same package).

Fold this into a short brief every agent receives — it stops every agent from re-discovering the same file layout and burning its budget on orientation instead of depth.

## 3. Launch angle agents in parallel

Use the `Agent` tool with `subagent_type: "general-purpose"` (or `"Explore"` for a pure code-mapping angle), all in **one message** with multiple tool calls so they run concurrently. Use 4+ angles; pick whichever genuinely fit the target from:

- **Implementation agent**: reads the actual code path end to end — entry point to effect, main branches, concurrency/locking, error handling. Cites `path/to/file:line`.
- **History/intent agent**: `git log -p`/`git blame` on the key files, commit messages, linked issues/PRs — why the code is shaped this way, not just what it does. Cites commit hashes and `path:line`.
- **Test/behavior agent**: reads the test suite for the area to determine actual guaranteed behavior, edge cases, and regressions being guarded against. Cites `path/to/test:line`.
- **External-context agent**: grounds the area in outside material — official docs, JEPs/specs/RFCs it implements, upstream library docs, known issues/CVEs, blog posts or conference talks about the same mechanism. Cites URLs with the specific section/quote.
- **Prior-art/comparison agent**: how do other systems (or other parts of this same codebase, OS vs. enterprise) solve the same problem — surfaces alternatives considered/rejected, or gaps. Cites `path:line` and/or URLs.
- **Adversarial agent**: actively hunts for what's fragile, under-tested, or contradicts the docs/comments — a second, skeptical read rather than a confirming one.

Each agent's prompt must state, verbatim in substance:
- The scoped target and the context brief from step 2.
- Its specific angle, and that it should go deep on that angle rather than surveying everything.
- It may use source reading, `git log`/`git blame`, and web search/fetch as fits its angle.
- **Every claim must carry a citation** — `path/to/file:line` for source, commit hash for history, URL + section/quote for web material. No citation, no claim.
- Report as a flat list of cited findings, not prose narrative — including things that surprised it or contradict assumptions, not just confirming detail.

## 4. Reconcile

Do this yourself once all agents report (don't delegate — reconciliation needs the full cross-agent picture):
- Findings independently confirmed by multiple agents → state once, with all supporting citations.
- Findings from a single agent → keep if cited, flagged as single-sourced only if load-bearing to the conclusion.
- Contradictions (e.g. docs say X, code does Y) → state explicitly as a discrepancy, both citations, don't silently resolve it.
- Drop anything uncited. Don't patch gaps with your own unsourced knowledge.
- If coverage is thin or agents disagree on something central, it's fine to launch one more targeted agent rather than paper over it.

## 5. Output format

```
## Target
<the scoped area, concretely>

## What it does
<short, cited summary of mechanism — not a restatement of the code>

## Why it's shaped this way
<cited history/intent findings, or "no history found — inferred from structure only">

## External context
<cited standards/docs/prior-art findings>

## Discrepancies / risks
<cited contradictions, under-tested paths, fragile assumptions — omit section if none>

## Sources
<flat list of every path:line and URL cited above>
```

Keep it a dossier, not an essay — every section should be scannable, and every non-trivial sentence should trace to a citation in the Sources list.
