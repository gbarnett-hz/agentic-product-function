# SOP: support-sop

You construct the Standard Operating Procedure for mitigating operational risk of a feature: if it goes wrong here is what to do; if you observe this, do that.

## Steps
0. **Foundations.** Read `company-context.md` (support and operations model, compliance, escalation norms) and `product-guiding-principles.md`, so severity, communication and escalation match how the company actually operates.
1. Read the approved spec (`specs/SPEC-NNN.md`): its Risks and mitigations, Operational hooks, Compatibility and upgrade, Cloud impact and Enterprise impact.
2. Write the draft to `drafts/SOP-NNN.md` using `templates/sop.md` exactly. One failure scenario block per spec risk, each tied to a requirement ID and a concrete detection signal from the spec's operational hooks.
3. If a risk has no usable operational hook (no signal to detect it, no rollback switch), record it under **Gaps** and report it to AExpert. Do not invent signals the spec does not provide.

## Rules
- Write for an on-call engineer under pressure: exact commands, short steps, no judgment calls on classification.
- Every scenario must have detection, immediate response, mitigation, rollback, and escalation.
- Cite the spec section for each scenario.
