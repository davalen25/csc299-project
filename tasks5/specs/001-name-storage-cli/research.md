# Research: Name Storage CLI

**Feature**: 001-name-storage-cli  
**Phase**: 0 (Outline & Research)  
**Date**: 2025-11-19

## Purpose

Resolve all technical unknowns and document best practices for Python 3.14+, `uv` tooling, JSON storage, CLI design, and testing strategies before design phase.

---

## Research Tasks

### 1. Python 3.14+ Features & Compatibility

**Question**: What Python 3.14 features are relevant and how to ensure compatibility?

**Findings**:
- Python 3.14 is bleeding-edge (pre-release as of Nov 2025); consider 3.12+ stable baseline with 3.14 as aspirational.
- Key features: Enhanced type system (PEP 692+ improvements), pattern matching refinements, performance gains.
- **Decision**: Target Python ≥3.12 for stability; 3.14 compatibility as stretch goal. Use type hints extensively (`str`, `list[str]`, `Path`, etc.).
- **Rationale**: 3.12 is widely available; 3.14 adoption will follow naturally; mypy/ruff support both.

**Alternatives Considered**:
- Python 3.10: Too conservative; missing modern typing features.
- Python 3.11: Good middle ground but 3.12 is now standard.

---

### 2. `uv` Best Practices for CLI Projects

**Question**: How to structure a `uv`-managed Python CLI project?

**Findings**:
- `uv` provides unified workflow: `uv init`, `uv add <dep>`, `uv run <script>`, `uv sync`.
- `pyproject.toml` is central: define `[project.scripts]` for CLI entry points.
- Best practice: Keep `src/` layout with package namespace; `uv` auto-discovers.
- Script entry format: `names = "names.cli:main"` → runs `main()` from `cli.py`.
- Dev dependencies: `uv add --dev pytest ruff mypy` for testing/linting.

**Decision**: Use `uv` for all operations; define `names` CLI script in `pyproject.toml`; single `src/names/` package.

**Rationale**: `uv` unifies venv, pip, and task running; simpler than separate tools.

**Alternatives Considered**:
- Poetry: More mature but heavier; `uv` is faster and simpler for this scope.
- Plain pip + venv: Manual; lacks integrated script management.

---

### 3. JSON File Storage Patterns

**Question**: How to safely read/write JSON with concurrency awareness and error handling?

**Findings**:
- Python `json` module sufficient for simple cases.
- Pattern: Read entire file → modify in-memory → write atomically.
- Atomic write: Write to temp file → `os.replace()` (atomic on POSIX/Windows).
- Error handling: Catch `FileNotFoundError` (create), `PermissionError` (report), `JSONDecodeError` (corrupt file recovery).
- Concurrency: Spec assumes single-user sequential; no file locking needed.

**Decision**: Use `json.load`/`json.dump` with atomic write via temp + replace; handle file errors gracefully.

**Rationale**: Simple, portable, meets spec constraints. Atomic write prevents corruption on interrupt.

**Alternatives Considered**:
- SQLite: Overkill for flat name list; adds dependency.
- File locking (fcntl/msvcrt): Unnecessary given single-user assumption; platform-specific complexity.

**Code Pattern**:
```python
from pathlib import Path
import json
import tempfile
import os

def atomic_write_json(path: Path, data: list[str]) -> None:
    """Atomically write JSON array to file."""
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)
    except Exception:
        os.unlink(tmp_path)
        raise
```

---

### 4. Case-Insensitive Stable Sorting

**Question**: How to sort strings case-insensitively while preserving original case and stable order?

**Findings**:
- Python `sorted()` is stable by default (equal items preserve input order).
- Case-insensitive key: `key=str.lower` or `key=str.casefold` (latter handles Unicode better).
- Example: `sorted(names, key=str.lower)` → `['alice', 'Bob', 'Carol']`.

**Decision**: Use `sorted(names, key=str.lower)` for listing.

**Rationale**: Built-in, efficient, stable, meets spec requirement. `str.lower` sufficient for common Latin names; `casefold` for internationalization if needed.

**Alternatives Considered**:
- Manual sort with tuple keys: Overcomplicates; Python's built-in is optimal.
- Locale-aware sorting (`locale.strxfrm`): Not required by spec; adds complexity.

---

### 5. CLI Argument Parsing

**Question**: Which CLI library balances simplicity and features?

**Findings**:
- `argparse` (stdlib): Fully capable for two commands; no external dependency.
- `click`: Popular, decorator-based, but adds dependency.
- `typer`: Modern, type-hint driven, wraps `click`.

**Decision**: Use `argparse` for minimal dependencies; two subcommands (`add`, `list`) straightforward.

**Rationale**: Stdlib solution; no extra dependency; sufficient expressiveness for simple CLI.

**Alternatives Considered**:
- `click`/`typer`: Better for complex CLIs; unnecessary here; violates simplicity principle.

**Pattern**:
```python
import argparse

def main():
    parser = argparse.ArgumentParser(prog='names')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    add_parser = subparsers.add_parser('add', help='Add a name')
    add_parser.add_argument('name', help='Name to add')
    
    subparsers.add_parser('list', help='List all names')
    
    args = parser.parse_args()
    # dispatch to handlers
```

---

### 6. Testing Strategy with pytest

**Question**: How to structure unit/integration/contract tests for this CLI?

**Findings**:
- pytest conventions: `tests/` mirror `src/` structure; `test_*.py` files; `test_*()` functions.
- Unit tests: Direct function calls; mock file I/O with `tmp_path` fixture.
- Integration tests: Invoke CLI via `subprocess.run(['uv', 'run', 'names', ...])` or direct `main()` call with `sys.argv` patching.
- Contract tests: Assert exact output strings and exit codes.
- Coverage: `pytest --cov=src/names --cov-report=term`.

**Decision**: Three test directories (unit/integration/contract); use `tmp_path` for isolation; aim for ≥80% coverage.

**Rationale**: Matches Constitution's testing requirement; pytest is standard; clear separation aids focus.

**Alternatives Considered**:
- unittest (stdlib): More verbose; pytest is community standard.
- Single test directory: Harder to isolate concerns; violates Constitution's layered testing principle.

---

### 7. Linting & Type Checking

**Question**: Which tools for quality gate compliance?

**Findings**:
- `ruff`: Fast linter + formatter (replaces flake8, black, isort); single tool.
- `mypy`: Type checker; enforces type hints.
- Configuration: `pyproject.toml` sections for both.

**Decision**: Use `ruff check` and `ruff format` for linting/formatting; `mypy` for type checking; CI runs both.

**Rationale**: `ruff` is fastest and most comprehensive single tool; `mypy` is standard for types. Meets Constitution Quality Gate.

**Alternatives Considered**:
- black + flake8 + isort: Multiple tools; slower; `ruff` consolidates.

**CI commands**:
```bash
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/
uv run pytest --cov=src/names --cov-fail-under=80
```

---

### 8. Emoji Support in Output

**Question**: How to include emojis in CLI output per Constitution Principle V?

**Findings**:
- Python 3 handles Unicode natively; emoji literals safe in strings.
- Terminal compatibility: Modern terminals support emoji; fallback not required by spec.
- Example: `print("✅ Added: Alice")`, `print("❌ Name cannot be empty")`.

**Decision**: Use emoji literals in success/error messages; no fallback mechanism (simplicity).

**Rationale**: Constitution mandates emoji; modern environment assumption; enhances UX.

**Pattern**:
```python
SUCCESS = "✅"
ERROR = "❌"
INFO = "ℹ️"

print(f"{SUCCESS} Added: {name}")
print(f"{ERROR} Name cannot be empty")
```

---

## Consolidated Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Python Version | ≥3.12 (3.14+ compatible) | Stability + modern features |
| Dependency Manager | `uv` | Unified, fast, simple |
| Storage Format | JSON (atomic write) | Simple, portable, safe |
| Sorting | `sorted(key=str.lower)` | Built-in stable sort |
| CLI Framework | `argparse` (stdlib) | No extra deps, sufficient |
| Testing | pytest (unit/int/contract) | Standard, clear separation |
| Linter/Formatter | `ruff` | Fast, comprehensive |
| Type Checker | `mypy` | Standard for Python |
| Emoji | Native Unicode literals | Constitution requirement |

---

## Open Questions (None)

All technical unknowns resolved. Ready for Phase 1 design.

---

## References

- `uv` docs: https://github.com/astral-sh/uv
- Python 3.12 release notes: https://docs.python.org/3.12/whatsnew/
- `ruff` docs: https://docs.astral.sh/ruff/
- pytest best practices: https://docs.pytest.org/
