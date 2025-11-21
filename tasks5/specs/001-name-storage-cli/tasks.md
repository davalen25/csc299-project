---

description: "Task list template for feature implementation"
---

# Tasks: Name Storage CLI

**Input**: Design documents from `/specs/001-name-storage-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per the Testing Standards. Include unit tests for new logic and integration/contract tests at boundaries as defined in the spec.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize uv project with `uv init` and configure pyproject.toml
- [X] T002 [P] Add dev dependencies: `uv add --dev pytest ruff mypy`
- [X] T003 [P] Create src/names/ package with __init__.py
- [X] T004 [P] Create tests/ directories (unit/, integration/, contract/)
- [X] T005 Configure CLI script entry point in pyproject.toml: `names = "names.cli:main"`
- [X] T006 [P] Configure ruff in pyproject.toml (linter + formatter settings)
- [X] T007 [P] Configure mypy in pyproject.toml (strict type checking)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 [P] Implement Name value object in src/names/validation.py with trim, empty check, length validation
- [X] T009 [P] Create unit tests for Name validation in tests/unit/test_validation.py
- [X] T010 [P] Implement NameStore._load() method in src/names/storage.py (JSON read with error handling)
- [X] T011 [P] Implement NameStore._save() method in src/names/storage.py (atomic write with temp file)
- [X] T012 Define Constitution Gates checklist for feature: Simplicity, Quality, Testing, UX, Documentation
- [X] T013 [P] Create .gitignore to exclude names.json, .venv/, __pycache__, .pytest_cache

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a Name (Priority: P1) 🎯 MVP

**Goal**: Enable users to add validated names to persistent storage via CLI

**Independent Test**: Run `names add "Alice"` and verify storage file contains the name and exit code is 0

### Tests for User Story 1 (REQUIRED) ⚠️

> Write these tests FIRST and ensure they FAIL before implementation

- [ ] T014 [P] [US1] Contract test for `add` command success case in tests/contract/test_cli_contract.py
- [ ] T015 [P] [US1] Contract test for `add` command empty name error in tests/contract/test_cli_contract.py
- [ ] T016 [P] [US1] Contract test for `add` command too-long name error in tests/contract/test_cli_contract.py
- [ ] T017 [P] [US1] Integration test for end-to-end add flow in tests/integration/test_add_flow.py

### Implementation for User Story 1

- [ ] T018 [US1] Implement NameStore.add() method in src/names/storage.py (validate, append, persist)
- [ ] T019 [US1] Create unit tests for NameStore.add() in tests/unit/test_storage.py
- [ ] T020 [US1] Implement CLI argument parser with argparse in src/names/cli.py (subcommand structure)
- [ ] T021 [US1] Implement `add` command handler in src/names/cli.py (call NameStore.add, format output with emoji)
- [ ] T022 [US1] Add error handling in cli.py: map ValueError → exit code 1, IOError → exit code 2
- [ ] T023 [US1] Create unit tests for CLI add command parsing in tests/unit/test_cli.py
- [ ] T024 [US1] Verify all US1 contract tests pass

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - List All Names Alphabetically (Priority: P2)

**Goal**: Enable users to view all stored names in alphabetical order (case-insensitive)

**Independent Test**: Add names in non-sorted order, run `names list`, verify alphabetical output

### Tests for User Story 2 (REQUIRED) ⚠️

- [ ] T025 [P] [US2] Contract test for `list` command with sorted output in tests/contract/test_cli_contract.py
- [ ] T026 [P] [US2] Contract test for `list` command with empty storage in tests/contract/test_cli_contract.py
- [ ] T027 [P] [US2] Contract test for `list` with case-insensitive sorting in tests/contract/test_cli_contract.py
- [ ] T028 [P] [US2] Integration test for end-to-end list flow in tests/integration/test_list_flow.py

### Implementation for User Story 2

- [ ] T029 [P] [US2] Implement NameStore.list() method in src/names/storage.py (load, sort case-insensitive, return)
- [ ] T030 [P] [US2] Create unit tests for NameStore.list() and sorting in tests/unit/test_storage.py
- [ ] T031 [US2] Implement `list` command handler in src/names/cli.py (call NameStore.list, format output)
- [ ] T032 [US2] Add empty list handling: print "No names found." for zero names
- [ ] T033 [US2] Create unit tests for CLI list command in tests/unit/test_cli.py
- [ ] T034 [US2] Verify all US2 contract tests pass

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Prevent Invalid Names (Priority: P3)

**Goal**: Provide clear feedback for invalid inputs (already partially covered by US1, this phase ensures complete coverage)

**Independent Test**: Attempt invalid additions (empty, whitespace-only, too-long); verify rejection and unchanged storage

### Tests for User Story 3 (REQUIRED) ⚠️

- [ ] T035 [P] [US3] Contract test for whitespace-only name rejection in tests/contract/test_cli_contract.py
- [ ] T036 [P] [US3] Contract test for trimming behavior in tests/contract/test_cli_contract.py
- [ ] T037 [P] [US3] Integration test for invalid input scenarios in tests/integration/test_add_flow.py

### Implementation for User Story 3

- [ ] T038 [US3] Verify Name validation handles all edge cases (whitespace-only, tabs, newlines)
- [ ] T039 [US3] Add unit tests for edge case validation in tests/unit/test_validation.py
- [ ] T040 [US3] Verify error messages match UX contracts (emoji, specific wording)
- [ ] T041 [US3] Test storage remains unchanged after failed add attempts

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T042 [P] Add help text customization in cli.py argparse (descriptions, examples)
- [ ] T043 [P] Create README.md at repository root with overview and link to quickstart
- [ ] T044 [P] Verify ruff formatting passes: `uv run ruff format --check src/ tests/`
- [ ] T045 [P] Verify ruff linting passes: `uv run ruff check src/ tests/`
- [ ] T046 [P] Verify mypy type checking passes: `uv run mypy src/`
- [ ] T047 Run full test suite with coverage: `uv run pytest --cov=src/names --cov-report=term`
- [ ] T048 Verify coverage meets ≥80% threshold
- [ ] T049 [P] Add docstrings to public methods (Name, NameStore.add, NameStore.list, main)
- [ ] T050 Run quickstart.md validation: execute all example commands and verify outputs
- [ ] T051 Final Constitution Check: verify all gates pass (Simplicity, Quality, Testing, UX, Documentation)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - No dependencies on US1 (storage layer independent)
  - User Story 3 (P3): Depends on US1 completion (builds on add validation)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable (reads don't depend on write implementation details)
- **User Story 3 (P3)**: Minimal dependency on US1 (validation already in place; this phase ensures comprehensive edge case coverage)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Foundational components (Name, NameStore methods) before CLI
- CLI parsing before command handlers
- Error handling after core logic
- Contract test verification after implementation complete

### Parallel Opportunities

- **Setup (Phase 1)**: T002, T003, T004, T006, T007 can run in parallel
- **Foundational (Phase 2)**: T008+T009, T010, T011, T013 can run in parallel
- **User Story 1 Tests**: T014, T015, T016, T017 can run in parallel
- **User Story 1 Implementation**: T018+T019 parallel with T020+T023 (storage vs CLI)
- **User Story 2 Tests**: T025, T026, T027, T028 can run in parallel
- **User Story 2 Implementation**: T029+T030 parallel with T031+T033 (storage vs CLI)
- **User Story 3 Tests**: T035, T036, T037 can run in parallel
- **Polish**: T042, T043, T044, T045, T046, T049 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
# Terminal 1:
Task: "Contract test for add command success case in tests/contract/test_cli_contract.py"

# Terminal 2:
Task: "Contract test for add command empty name error in tests/contract/test_cli_contract.py"

# Terminal 3:
Task: "Contract test for add command too-long name error in tests/contract/test_cli_contract.py"

# Terminal 4:
Task: "Integration test for end-to-end add flow in tests/integration/test_add_flow.py"

# After tests written, launch parallel implementation:
# Terminal 1:
Task: "Implement NameStore.add() + unit tests" (T018 + T019)

# Terminal 2:
Task: "Implement CLI argument parser + unit tests" (T020 + T023)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Run: `uv run names add "Alice"` and `uv run names list` to verify basic flow
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Validate add command works
3. Add User Story 2 → Test independently → Validate alphabetical listing
4. Add User Story 3 → Test independently → Validate comprehensive error handling
5. Polish → Final quality checks
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (tests → implementation)
   - Developer B: User Story 2 (tests → implementation, can proceed independently)
   - Developer C: Prepares Polish tasks (README, documentation)
3. After US1 complete:
   - Developer A moves to US3
   - Developer B completes US2
   - Developer C continues Polish
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution Gates MUST pass before merging to main

---

## Task Count Summary

- **Total Tasks**: 51
- **Setup (Phase 1)**: 7 tasks
- **Foundational (Phase 2)**: 6 tasks (CRITICAL PATH)
- **User Story 1 (P1)**: 11 tasks (4 tests + 7 implementation)
- **User Story 2 (P2)**: 10 tasks (4 tests + 6 implementation)
- **User Story 3 (P3)**: 7 tasks (3 tests + 4 implementation)
- **Polish (Phase 6)**: 10 tasks
- **Parallel Opportunities**: 23 tasks marked [P]
- **MVP Scope**: Phases 1-3 (24 tasks)

---

## Suggested Execution Order (Sequential)

1. T001-T007 (Setup)
2. T008-T013 (Foundational - MUST COMPLETE BEFORE STORIES)
3. T014-T024 (User Story 1 - MVP)
4. Validate MVP: `uv run pytest tests/integration/test_add_flow.py`
5. T025-T034 (User Story 2)
6. Validate: `uv run pytest tests/integration/test_list_flow.py`
7. T035-T041 (User Story 3)
8. T042-T051 (Polish)
9. Final: `uv run pytest --cov=src/names --cov-fail-under=80`
10. Merge to main after Constitution Check passes
