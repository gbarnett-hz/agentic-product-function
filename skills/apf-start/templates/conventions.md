# Conventions

Project-level, written by ACore and refreshed when the stack changes. Developers follow it, testers check it, the WaveMerger and Verifier enforce it.

**Authority order** (higher wins):
1. The project's own enforced configuration (formatter, linter, type checker, CI, `CLAUDE.md`, `CONTRIBUTING`).
2. The patterns already in the code being touched.
3. The technology's official or community idiom (cite it).

## Test isolation (project-wide)

Many worktrees run tests at the same time, from different lanes and different PRDs. Running tests in one worktree must never affect tests in another, and every resource a test uses is isolated the same way.

**Rules (fixed):**
1. **Key.** Each worktree has an isolation key, `APF_KEY` (its directory name), and a 100-port block starting at `APF_PORT_BASE`, both given by the EM. Everything below derives from them.
2. **Files.** Tests write only inside their worktree. Temp files go to `$TMPDIR`, which is `<worktree>/.apf-tmp`. No fixed paths such as `/tmp/x`, `~/...` or a shared data directory.
3. **Network.** Bind port 0 (ephemeral) where possible; otherwise a port inside the worktree's block. Never a hard-coded port.
4. **Services and data.** Databases, schemas, queues, topics, containers, networks and volumes are created by test setup with `APF_KEY` in their name (for example `docker compose -p $APF_KEY`) and removed by teardown.
5. **Process state.** Configuration comes from per-process environment variables or files in the worktree; never edit global or user-level config. Build outputs, virtual environments and dependency installs live in the worktree. Shared caches are fine only if safe for concurrent use.
6. **Exclusive resources.** A resource that cannot be namespaced (a shared staging environment, a licensed or single-instance service, a hardware device) is listed below. Units that need one are marked `Exclusive: <resource>` in the plan, and the EM never runs two of them at the same time, across all PRDs.
7. **Teardown.** Tests clean up what they create. The EM also runs the teardown command below when it removes a worktree.

**This project:**

| Resource | How it is isolated here | Teardown | Source (config file or doc) |
|---|---|---|---|
| Ports | | | |
| Temp files | | | |
| Database / queue / container | | | |

- **Exclusive resources:** none / list.
- **Gaps:** places where today's tests violate the rules (for example a hard-coded port in `path:line`). A unit that touches such a test makes it compliant as part of that unit; reviewers check it.

Repeat the block below once per technology in the project.

## <Technology, e.g. Java 21 / Python 3.12 / Go 1.23 / Terraform>

- **Where it is used:** paths.
- **Idiom standard(s):** name and URL (e.g. PEP 8, Effective Go, Google Java Style Guide, Rust API Guidelines).
- **Mechanical checks (run before handoff, all must pass):**

  | Check | Command | Source (config file or doc) |
  |---|---|---|
  | Format | | |
  | Lint | | |
  | Types / static analysis | | |
  | Tests | | |

- **Project-specific rules** (from config, CLAUDE.md, CONTRIBUTING, review history): naming, error handling, logging, concurrency, dependency policy, test layout, commit/PR rules.
- **Patterns to copy:** `path/file:line` examples of the idiom in this codebase.
- **Where project and general idiom differ:** which one wins and why.
- **Gaps:** checks that do not exist (e.g. no linter configured), so reviewers cover them by hand.
