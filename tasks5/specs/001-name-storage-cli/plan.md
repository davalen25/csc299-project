# Implementation Plan: Name Storage CLI

**Branch**: `001-name-storage-cli` | **Date**: 2025-11-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-name-storage-cli/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a CLI tool to add and list people's names with persistent JSON file storage. Core requirements: (1) `names add <name>` validates and appends to JSON; (2) `names list` outputs names alphabetically (case-insensitive); (3) CLI and storage logic separated into distinct modules. Technical approach: Python 3.14+ managed with `uv`, JSON file backend, case-insensitive stable sorting, comprehensive testing (unit/integration/contract).

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.14+  
**Primary Dependencies**: `uv` (project/dependency management, script running)  
**Storage**: Local JSON file (`names.json` by default)  
**Testing**: pytest (unit, integration, contract tests)  
**Target Platform**: Cross-platform (macOS/Linux/Windows with Python 3.14+)
**Project Type**: Single project (CLI tool with storage module)  
**Performance Goals**: List 10,000 names alphabetically in under 2 seconds  
**Constraints**: Single-user sequential usage; no concurrency; offline-only; plain JSON (no DB)  
**Scale/Scope**: Expected usage: <10k names; minimal external dependencies; two modules (CLI + storage)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Initial Assessment (Pre-Research):**

- ✅ **Simplicity Gate**: Two-module design (CLI + storage); minimal API (`add`, `list`); no premature abstractions; JSON for simplicity over database.
- ✅ **Quality Gate**: Will use `ruff` (linter/formatter) and `mypy` (type checker); Python 3.14 type hints enforced; zero warnings target.
- ✅ **Testing Gate**: Comprehensive test plan defined in spec: unit tests (validation, sorting logic), integration tests (CLI commands), contract tests (output formats); target ≥80% coverage; CI execution required.
- ✅ **UX Gate**: I/O contracts fully specified in spec (UX-001 through UX-006); exit codes, error messages, output formats documented; emoji support per Constitution Principle V.
- ✅ **Documentation Gate**: Quickstart.md will document installation (uv), usage (add/list), examples; README at repo root will link to quickstart.

**No gate violations.** Complexity Tracking table not required.

---

**Post-Design Re-Evaluation (Phase 1 Complete):**

- ✅ **Simplicity Gate**: Design confirmed: 3 focused modules (`cli.py`, `storage.py`, `validation.py`); `Name` value object and `NameStore` aggregate; stdlib `argparse`; no ORM or unnecessary layers. API surface: 2 public methods (`add`, `list`).
- ✅ **Quality Gate**: `ruff` + `mypy` configured in research; type hints throughout data model; atomic write pattern for safety; error handling explicit.
- ✅ **Testing Gate**: Contracts generated (`add-command.md`, `list-command.md`, `error-handling.md`) with pytest examples; data model includes validation test hooks (`tmp_path` support); 3-layer test structure matches Constitution requirement.
- ✅ **UX Gate**: Contracts confirm exit codes (0/1/2), error messages (with emoji), output formats (plain text, sorted); deterministic behavior documented; help text specified.
- ✅ **Documentation Gate**: Quickstart.md generated with installation, usage, troubleshooting, architecture diagram; ready for repo-root README linkage.

**Final Verdict: ALL GATES PASS.** No complexity justifications needed. Ready for Phase 2 (task breakdown).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── names/
│   ├── __init__.py
│   ├── cli.py           # CLI entry point and command handlers
│   ├── storage.py       # JSON file storage logic (add, list)
│   └── validation.py    # Input validation (trim, empty check, length)

tests/
├── contract/
│   └── test_cli_contract.py  # CLI output format contracts
├── integration/
│   ├── test_add_flow.py      # End-to-end add command
│   └── test_list_flow.py     # End-to-end list with sorting
└── unit/
    ├── test_validation.py    # Validation logic
    ├── test_storage.py       # Storage add/list/sort
    └── test_cli.py           # CLI command parsing

pyproject.toml                # uv project config, dependencies, scripts
README.md                     # Project overview, link to quickstart
names.json                    # Storage file (created on first add)
```

**Structure Decision**: Single project structure chosen. Python package `names` in `src/` with three focused modules: `cli.py` (command interface), `storage.py` (JSON persistence + sorting), `validation.py` (input rules). Tests mirror Constitution's three-layer requirement (unit/integration/contract). `uv` manages dependencies and provides script entry point via `pyproject.toml`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
