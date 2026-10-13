# Flow: Requirement Gap

A lighter variant of the architecture flow, for work that does not meet the PRD, spec or SOP. It runs inside the `/apf-dev` command: the EM there spawns a new AExpert for the gap, and the fix is built by the same lane pool.

1. **Verifier** produces `templates/gap-report.md`.
2. **EM** (the `/apf-dev` session) spawns a **new AExpert** for the gap (given the gap report path, the spec and `.agentic-team/arch/PRD-NNN/`) and increments `gap_cycles` for the PRD.
3. **AExpert** runs a scoped flow with **new** architects (fresh agents given the spec, the gap report and `.agentic-team/arch/PRD-NNN/`):
   - ACore runs `apf-deep-code` on the gap only (no apf-group-design unless the gap needs a different design).
   - ACloud and ASolution run only if the gap touches their area.
   - Adversarial review, narrowed to the gap (cap 2 rounds).
   - Gate 2 is skipped: the chosen option stands.
   - If the gap needs a spec or SOP change, that delta goes to the human for re-approval (gates 1 and 3). Otherwise no human gate.
4. **AExpert** runs `apf-plan` (agentic-team mode, gap variant) for only the units that close the gap.
5. **EM** dispatches to idle lanes, merges, and the Verifier checks again.
6. **Cap:** 2 gap cycles. After that, escalate to the human with the remaining gaps and the history.
