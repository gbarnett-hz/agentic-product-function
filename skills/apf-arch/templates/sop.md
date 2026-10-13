# SOP-<NNN>: <Feature> operations

Format: incident runbook. Written for an on-call engineer under pressure: short steps, exact commands, no judgment calls on classification.

| | |
|---|---|
| Status | Draft / Approved |
| Author | SOP |
| Spec | <link to specs/SPEC-NNN.md> |
| Date | <YYYY-MM-DD> |

## 1. Overview
What the feature does operationally, and the one-sentence blast radius if it fails.

## 2. Severity definitions
| Severity | Criteria | Response target | Who is paged |
|---|---|---|---|
| SEV-1 | | | |
| SEV-2 | | | |
| SEV-3 | | | |
| SEV-4 | | | |

## 3. Failure scenarios
One block per scenario, from the spec's Risks and Operational hooks. Repeat this block.

### Scenario S-<n>: <name>
- **Spec risk / requirement:** <ID>
- **Severity:** SEV-<n>
- **Detection:** the signal (metric/log/alert, with threshold). Cite the spec's operational hook.
- **Immediate response (first 15 minutes):** exact steps and commands.
- **Investigation:** where to look, diagnostic commands, what each result means.
- **Mitigation:** steps to restore service.
- **Rollback:** how to undo the feature (flag, config, version), and how to confirm it worked.
- **Communication:** who to notify, when, with what template.
- **Escalation:** who, after how long.
- **Post-incident:** follow-ups, data to preserve for the post-mortem.

## 4. Routine operations
Deploy, enable/disable, scale, upgrade, health checks.

## 5. Contacts and escalation path

## 6. Gaps
Spec operational hooks that are missing or too weak for this SOP to work. These go back to AExpert.
