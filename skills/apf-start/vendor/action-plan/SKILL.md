---
name: action-plan
description: Turn the current conversation into a detailed, actionable plan document — problem statement, background, design options with a reasoned selection, and an ordered, test-first todo list someone could execute without having read the chat. Two or more planner agents draft competing todo lists (reproducer first, TDD with integration tests, parallel waves), each is validated, and an arbiter agent picks the best and explains why. Use when the user says "action-plan", "turn this into a todo list", "write up a plan for this", "make this actionable", or wants the discussion so far captured as work to do. Works from the existing chat context; do not use at the start of a conversation with nothing to plan.
---

# Action Plan

Distil the current conversation into a plan someone else (or a future session) can pick up cold. The chat is the primary source; the codebase is used to verify and fill gaps, not to start fresh research.

## Agentic-team mode (vendored adaptation)

When AExpert invokes this skill inside apf-start, three things change:
- **Source of context:** the chat is not the source. Build the skeleton from the approved spec (`specs/<id>.md`: Motivation → Problem, Design/MADR → Design options and Selected design, Requirements → Testing and the reproducer) and the approved SOP (`sops/<id>.md`: its operational hooks become steps and tests). Every step must cite the requirement ID(s) it satisfies.
- **Location:** write the plan to `plans/<spec-id>.md` in the project's knowledge repo, not `~/.claude/plans/`. Candidates go beside it as `plans/<spec-id>.candidate-<A|B|C>.md`.
- **Execution mode:** skip section 8's question. Parallel is the default: if N > 1, set `Execution mode: parallel (N agents)`. The EM maps waves onto free lanes.
- **Conventions:** read `conventions.md`. Every step's "Done when" also requires the project's mechanical checks (format, lint, types) to pass, and its Verify line includes the check commands from `conventions.md`. Do not invent commands that file does not list.
- **Requirement Gap runs:** when given a gap report instead of a spec, plan only the units needed to close the listed gaps, and say so in Problem.

## 1. Harvest the context

Re-read the conversation and pull out:
- The goal the user is actually trying to reach (not just the last message).
- Facts already established: files, functions, errors, measurements, constraints, decisions the user has made.
- Open questions and anything left unresolved.

Do not re-litigate decisions the user already made — record them as decided, with the reason they gave.

## 2. Verify and fill gaps

For every file, symbol, or behaviour the plan will reference, confirm it exists and is as described (Grep/Read; `git log` for recent history if relevant). Fix stale claims silently in the plan. Keep this targeted — if the gaps are large enough to need broad research, say so and suggest `deep-code` or `group-design` instead of doing it here.

## 3. Design discussion and selection

- If the chat already settled on a design, state it and summarise the alternatives that were rejected and why.
- Otherwise lay out 2–4 genuinely different options. For each: how it works, files touched, pros, cons, risks (correctness, compatibility/rolling upgrade, performance, effort).
- Pick one and justify it against the others in a few sentences. If the choice hinges on something only the user can decide (product priority, acceptable risk, scope), ask with `AskUserQuestion` before writing the todo list — don't guess.

## 4. Write the plan skeleton

Write to `~/.claude/plans/<YYYY-MM-DD>-<short-slug>.md` using the structure below. You write every section except **Todo**, **Parallel execution**, and **Testing**: leave those as `<pending: candidate plans>`. They come from competing planner agents (step 5) and the arbiter's pick (step 7). The template and Rules below are also the spec the planners and validators work to.

```markdown
# <Title>

## Problem
What is wrong or missing, observable symptoms, who/what is affected. Concrete — include error text, failing tests, ticket IDs if known.

## Background
How the relevant part of the system works today, with `path/to/file:line` references. Constraints and prior decisions from the discussion. Anything a newcomer needs to understand the todo list.

## Design options
### Option A — <name>
How it works · Files touched · Pros · Cons · Risks
### Option B — <name>
...

## Selected design
Which option, why it beats the others, and what we're knowingly giving up.

## Todo
Ordered so each step builds on the last and the tree stays buildable between steps.
TDD gate: every step is test → fail → implement → pass. Do not start step N+1 until step N's test passes and the existing tests still pass. Unit tests cover the logic inside a step; an integration test covers any step whose change crosses a boundary (members, client/server, serialization, persistence, network, config wiring).

- [ ] 1. Write the reproducer
  - What: one end-to-end test or runnable program that exercises the objective exactly as a user/caller would (real cluster, real config, real API), and asserts the outcome the plan exists to deliver. It encodes the plan's definition of done.
  - Where: `path/to/ReproducerTest` (or script)
  - Fails now because: <the observable symptom from Problem, as the expected failure message>
  - Done when: it compiles/runs and fails for that reason. It stays red until the final step; mark it so it doesn't break the per-step "existing tests still pass" check (e.g. excluded from the default suite or tracked as the one expected failure).
  - Verify: exact command that runs it
- [ ] 2. <Imperative action>
  - Test first: `path/to/TestFile:testName`, what it asserts, and why it fails before the change
  - Integration test (if the step crosses a boundary): `path/to/ITFile:testName`, which components it wires together, what it asserts
  - Where: `path/to/file:line` (or new file)
  - What: specific change, enough detail to do without the chat
  - Done when: the test above passes and the module's existing tests still pass
  - Verify: exact command that runs that test (e.g. `mvn -pl <module> test -Dtest=<Class>#<method>`)
- [ ] 3. ...
- [ ] N. Confirm the objective
  - Run the step 1 reproducer unmodified; remove any exclusion added in step 1 so it joins the normal suite
  - Done when: it passes and the full suite is green
  - Verify: reproducer command + full-suite command

## Parallel execution
Recommended agents: N
Why N: <one or two sentences: width of the widest wave, any steps folded together>
Waves:
- Wave 1: steps 1, 2 (sequential prerequisite / why)
- Wave 2: steps 3, 4, 5, 6 — independent because <...>
- ...
Ordering constraints: <step X before step Y because ...>
Worktree isolation needed for: <steps, or "none">
Execution mode: <parallel (N agents) | single agent>

## Plan selection
Which candidate won, the arbiter's reasoning, and links to the losing candidate files.

## Testing
The reproducer (step 1) and what passing it proves. Then the unit and integration tests the Todo steps add, grouped by level, plus the full-suite command to run at the end.

## Risks and open questions
Unresolved items, assumptions made, things to check with someone.

## Out of scope
Things discussed but deliberately deferred.
```

Rules:
- Every todo item must be independently actionable: a specific location, a specific change, a check that proves it's done. "Refactor X" or "handle edge cases" is not an item.
- TDD is a strict gate for every step. The step's test is written first and must fail for the right reason before any implementation. The step is done only when that test passes. Test and implementation stay in the same step; never split them, and never put all tests in a final "add tests" step. If a step changes no behaviour (pure refactor, rename, build/config), its test is a named existing test that covers the touched code and must stay green. If no such test exists, write a characterization test first.
- Step 1 is always the reproducer; the last step is always running it to green. The reproducer is the acceptance test for the whole plan, so it must exercise the real entry point, not a mocked slice, and must not be edited to pass. If the objective can't be reproduced end-to-end (e.g. a pure refactor), say so in step 1 and name the existing tests that define "unchanged behaviour" instead.
- Integration tests are part of the TDD gate, not an afterthought. A step that changes how components interact names an integration test in its "Test first" alongside (or instead of) a unit test. Mocks alone don't satisfy the gate for such a step.
- Parallel execution: two steps share a wave only if neither needs the other's output (new class, method, config, schema, generated code), they edit no files in common, and neither changes an API, build file, or shared test fixture the other relies on — confirmed against the cited files, not guessed from titles. The reproducer is in the first wave; "Confirm the objective" is alone in the last. N is normally the widest wave, fewer if some steps in it are too small to be worth an agent. Steps that are independent but would collide in one working tree (concurrent builds of a module, shared generated sources) need `isolation: "worktree"`. If every wave has one step, N = 1 and say why.
- Cite `file:line` for every code claim. No citation, no claim.
- Omit a section only if it is genuinely empty (e.g. no options when the fix is unambiguous) — say so in one line rather than padding.

## 5. Competing candidate plans

Spawn **at least two** fresh `general-purpose` planner agents in one message so they run concurrently (not forks: they must work from the skeleton alone, which proves it's self-sufficient). Use three when the Selected design spans three or more modules or has a risky cross-boundary change. Give each a different strategy so the candidates genuinely differ:

- **A — Lean critical path:** fewest steps, smallest diffs, simplest ordering; parallelism only where it falls out naturally.
- **B — Maximum safe parallelism:** decompose by module/file ownership so the widest waves are as wide as possible without breaking the parallel rule.
- **C — Risk first** (third agent): prove the riskiest boundary or integration point as early as possible so a wrong design fails fast.

Prompt for each:

> Read the plan skeleton at `<plan path>` and the action-plan spec (the SKILL.md you were launched from: `<path to this action-plan/SKILL.md>`, resolved to the vendored copy under `vendor/action-plan/`) (section 4: the Todo, Parallel execution and Testing formats, and the Rules). Your strategy: `<strategy text>`. Using the codebase to confirm every reference, write a candidate containing only `## Todo`, `## Parallel execution` (leave Execution mode blank), and `## Testing` to `<plan path minus .md>.candidate-<A|B|C>.md`. Follow every Rule: reproducer first, "Confirm the objective" last, TDD gate per step, integration tests for cross-boundary steps, `file:line` citations, and wave analysis checked against the actual files. Do not edit the skeleton or any source files. Reply with the candidate path, step count, N, and widest wave.

## 6. Validate each candidate

For each candidate, spawn one fresh `general-purpose` validator (all in one message). Give it the skeleton path, the candidate path, and these instructions:

> Read the plan skeleton at `<plan path>` and the candidate at `<candidate path>`. Do not change any files. Walk the candidate's Todo in order, as if executing it, and check:
> 1. **References** — every `file:line`, class, method, and config key cited exists and says what the candidate claims (Grep/Read to confirm).
> 2. **Sequence** — no step depends on something created or changed in a later step; the build and existing tests would still pass after each step; migrations, interface changes, and callers are ordered so nothing is half-wired.
> 3. **Completeness** — together the steps fully implement the skeleton's Selected design; nothing in Selected design or Testing is missing a step; no step does something outside the design or listed as Out of scope.
> 4. **Actionability** — each step has a concrete location, change, done-when criterion, and a verify command that would actually run in this repo.
> 5. **TDD gate** — every step names its test first (file, test name, assertion) and that test would fail before the step's change and pass after it. Its Verify command runs that specific test. No step defers its testing to a later step. A non-behavioural step names an existing test that covers the touched code, and that test really does cover it.
> 6. **Reproducer** — step 1 is a reproducer that drives the real entry point and asserts the plan's objective; it would fail today for the reason stated; the final step runs it unmodified. Passing it would genuinely show the Problem is solved, not just that the units work.
> 7. **Integration coverage** — every step that changes behaviour across a boundary (members, client/server, serialization, persistence, network, config) names an integration test, not only mocked unit tests.
> 8. **Parallelism** — every pair of steps sharing a wave really is independent (no shared files, symbols, build files, or fixtures — check the cited files); each wave boundary is forced by a named dependency; worktree isolation is listed wherever steps would collide; N matches the waves.
>
> Report one line per problem: step number, which check failed, evidence (`file:line` or quote), and the fix (reorder, split, add, remove a step, or regroup waves). If a step is fine, say nothing about it. End with `VALID` if there are no problems.

Send each report to the planner that wrote the candidate (`SendMessage`) and have it revise its file. If the revision reordered, added, or removed steps, validate it once more; stop after two rounds. Problems still open after that stay in the candidate under an `Unresolved` line — the arbiter weighs them.

## 7. Arbiter

Spawn one fresh `general-purpose` arbiter with the skeleton path, every candidate path, and each candidate's final validator report:

> Read the plan skeleton at `<plan path>`, the candidates at `<paths>`, and their validator reports below. Do not change any files. Judge which candidate an engineer should execute. Weigh, in this order: correctness and completeness against the Selected design (unresolved validator problems count heavily); strength of the reproducer and integration coverage; risk — how early a wrong assumption would surface; parallel speed-up that is actually safe (wide waves that collide or need heavy worktree juggling score lower); size and clarity of steps. Spot-check claims against the codebase where candidates disagree.
>
> Report: the winner; a ranking of all candidates; **why the winner is best**, comparing it head-to-head with each loser on the criteria above with concrete evidence (step numbers, `file:line`); what the winner gives up relative to the others; and any specific step from a loser that is strictly better and could be swapped in without changing the winner's sequence or waves (or "none").

Copy the winner's Todo, Parallel execution, and Testing into the plan file. Apply a suggested swap only if the arbiter says it leaves sequence and waves intact. Fill **Plan selection** with the winner, the arbiter's "why best" and "gives up" reasoning, and the paths of the losing candidates (keep those files). Add the winner's `Unresolved` items, if any, to Risks and open questions.

## 8. Execution mode

If the winner's N > 1, use `AskUserQuestion` to ask a single yes/no question: "Use N parallel agents for this plan?" Put the "Why N" line and the wave summary in the question so the choice is informed. Options: **Yes**, which runs N agents, one per step in each wave, wave by wave, with the listed steps in worktrees. **No**, which runs one agent through the steps in order. Write the answer into `Execution mode`. If N = 1, skip the question and set `Execution mode: single agent`.

The skill stops after planning. Execution mode tells whoever runs the plan, including a later request in this session, how to run it. In either mode the TDD gate holds: each agent writes the step's test, confirms it fails, implements, confirms it passes, and only then marks the step done. A wave finishes only when every step in it has passed its gate.

## 9. Report

Reply with the file path, the selected design in one sentence, the reproducer (file and what it asserts), which candidate won and the arbiter's reasons it beat each of the others (a few lines, kept specific), the number of todo items, what validation changed across candidates (one line), the execution mode with N and the widest wave, and any open questions that block starting. Do not paste the whole plan back into chat.
