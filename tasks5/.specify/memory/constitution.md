<!--
Sync Impact Report
- Version change: N/A → 1.0.0
- Modified principles: N/A (initial adoption)
- Added sections: Core Principles (4), Quality Gates, Development Workflow
- Removed sections: Unused Principle 5 template slot
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md (Constitution Check gates aligned)
	- ✅ .specify/templates/spec-template.md (UX/testing alignment cues added)
	- ✅ .specify/templates/tasks-template.md (tests required; gates added)
	- ⚠ .specify/templates/commands/*.md (no commands directory present)
	- ⚠ README.md (not present; no references to update)
- Deferred TODOs: None
-->

# Names Constitution

## Core Principles

### I. Clarity & Simplicity (NON-NEGOTIABLE)
Every solution MUST favor straightforward, readable code over cleverness. Keep
APIs minimal, functions small, names descriptive, and data flow explicit. Avoid
premature abstractions and speculative generality. Any intentional complexity
requires a justification entry in the plan's Complexity Tracking table.

Rationale: Simple, explicit code reduces cognitive load, accelerates reviews,
and lowers defect rates.

### II. Code Quality
Quality gates are enforced on every change:
- Linting/formatting: MUST pass with zero errors on main.
- Static analysis/type checks (where supported): MUST pass in CI.
- No new warnings: New code MUST NOT introduce warnings; suppressions require
	justification and scope minimization.
- Style: Follow the project language conventions; consistent patterns across
	modules.
- Documentation: Public APIs and non-obvious logic MUST be documented inline or
	in the spec/quickstart as appropriate.

Rationale: Consistent quality controls produce reliable software and predictable
maintenance costs.

### III. Testing Standards
Testing is mandatory and outcome-driven:
- Test-first preferred: Write failing tests before implementation when feasible.
- Coverage: New/changed code MUST be covered by unit tests; critical paths and
	defect fixes MUST include targeted tests. Aim for ≥80% unit coverage overall;
	exceptions require written rationale.
- Integration/contract tests: Required at external boundaries (APIs/CLIs,
	storage, services) and for cross-module behaviors.
- Determinism and speed: Tests MUST be deterministic and fast; avoid external
	flakiness. Use fakes/mocks where appropriate.
- CI: All tests MUST run and pass in CI before merge.

Rationale: Tests document behavior, prevent regressions, and enable safe change.

### IV. UX Consistency
User experience MUST be consistent across interfaces:
- Terminology, behaviors, and error handling MUST be uniform across CLI/API/UI.
- I/O contracts: Inputs, outputs, status/exit codes, and error schemas MUST be
	documented in specs and honored by implementations.
- Accessibility and defaults: Sensible defaults, clear messages, and accessible
	interactions are required where applicable.
- Consistency checklist: Each feature spec MUST include UX acceptance criteria
	covering success, error, and edge cases using consistent patterns.

Rationale: Consistency reduces user friction and support burden.

### V. Use Emojis in Output

Add emojis in program output when possible.

## Quality Gates
All work MUST pass these gates before merge. Document any temporary waivers with
an expiration and remediation plan.

- Simplicity Gate: No unnecessary abstractions; complexity justification present
	if applicable; API surface minimal.
- Quality Gate: Linters/formatters clean; static analysis/type checks passing;
	no new warnings on main.
- Testing Gate: Required tests exist and pass in CI; coverage goals met; tests
	are deterministic.
- UX Gate: Spec includes UX acceptance criteria; I/O contracts documented and
	verified; error handling consistent.

- Documentation Gate: User-facing documentation MUST be created or updated and
	kept up to date when changes are merged into the `main` or `master` branch.
	Documentation must cover user workflows, installation/quickstart, and
	I/O/contracts where applicable. PRs for user-facing changes MUST include a
	link to the updated docs and a brief verification that the docs build or the
	examples run (if applicable).

## Development Workflow
- Planning: Each feature uses the plan/spec/templates; include Constitution
	Check results and Complexity Tracking if applicable.
- Branching/PRs: Keep changes scoped. PR description MUST reference which
	principles guided key decisions and how gates were satisfied.
- Reviews: Reviewers verify gate compliance; non-compliance blocks merge unless
	a time-bound waiver is approved by maintainers.
- Commit hygiene: Meaningful messages; link to spec/tasks where relevant.
- Decision records: Non-trivial trade-offs MUST note the impacted principles and
	rationale in the plan/spec or PR description.

- Documentation: For any user-facing change, author or update user documentation
	(README, quickstart, docs site, or in-repo guides) as part of the change. The
	PR must include the documentation changes and references; maintainers should
	verify that user docs are present and accurate before merging to `main` or
	`master`.

## Governance
The Constitution governs technical decisions and implementation choices. It is
authoritative over templates and conventions.

- Authority: Principles are mandatory. When principles appear to conflict, favor
	Clarity & Simplicity, then Safety/Quality, then Performance unless the spec
	explicitly states otherwise.
- Amendments: Propose changes via PR updating this file with a summary,
	rationale, impact assessment, and migration plan if needed. Approval requires
	at least one maintainer review. Minor wording clarifications require one
	approval; principle changes require two approvals.
- Versioning: Semantic versioning of the Constitution:
	- MAJOR: Backward-incompatible changes to principles or governance.
	- MINOR: New principles/sections or materially expanded guidance.
	- PATCH: Clarifications and non-semantic refinements.
- Compliance: PRs MUST include a Constitution Check. Periodic audits may be
	conducted. Temporary waivers MUST include scope, duration, and remediation.

 - Compliance: PRs MUST include a Constitution Check AND a Documentation Check
	 for user-facing changes (docs present, linked in the PR, and up-to-date).
	 Periodic audits may be conducted. Temporary waivers MUST include scope,
	 duration, and remediation.
- Dispute Resolution: Maintainers adjudicate by referencing principles and
	documented rationale; unresolved disputes defer to simplicity and user impact.

**Version**: 1.0.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->

