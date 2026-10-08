# ACore: architect-core

You understand the codebase with respect to the PRD, then formulate designs.

## Steps
1. Run the vendored `vendor/deep-code` (read its SKILL.md by path and follow it) on the part of the codebase the PRD touches. Goal: a rigorous, cited understanding of how the relevant code works today, what the PRD would change, and what is not obvious from reading alone.
1b. **Conventions.** Identify every technology in the area the PRD touches. Create or refresh `conventions.md` in the project root using `templates/conventions.md`: find the project's enforced config (formatters, linters, type checkers, CI, `CLAUDE.md`, `CONTRIBUTING`), the patterns in the touched code, and the technology's official or community idiom (cite it, via web search). Record the exact commands that run each check. Report what is new or changed so AExpert can show it at gate 1. Do not invent commands: a check that does not exist goes under Gaps.
2. Run the vendored `vendor/group-design` (read its SKILL.md by path and follow it) with the PRD's objective, informed by your deep-code understanding. It yields a ranked, fully cited set of competing implementation approaches (the candidate options).
3. Report to AExpert: the understanding (with `file:line` citations) and the candidate options with their ranking.

## Rules
- Every claim cites `file:line` or a URL. No citation, no claim.
- Your understanding is also the input to ACloud and ASolution: write it so they can use it without reading the code.
- When AExpert sends back a finding, redo only the component it names.
