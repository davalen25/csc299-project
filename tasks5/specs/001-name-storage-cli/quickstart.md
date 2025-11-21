# Quickstart: Name Storage CLI

**Feature**: 001-name-storage-cli  
**Last Updated**: 2025-11-19

## Overview

A simple CLI tool to store and list people's names. Names are stored locally in a JSON file and listed alphabetically (case-insensitive).

**Features**:
- ✅ Add names with validation (non-empty, ≤256 chars)
- ✅ List names alphabetically
- ✅ Persistent local storage (JSON)
- ✅ Emoji-enhanced output
- ✅ Comprehensive error handling

---

## Prerequisites

- **Python**: 3.12 or higher (3.14+ recommended)
- **uv**: Package manager (see installation below)

---

## Installation

### 1. Install `uv` (if not already installed)

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:
```bash
uv --version
```

### 2. Clone or Navigate to Project

```bash
cd /path/to/names
```

### 3. Initialize Project (First Time)

```bash
uv sync
```

This command:
- Creates a virtual environment
- Installs all dependencies
- Sets up the `names` CLI command

---

## Usage

### Add a Name

```bash
uv run names add Alice
```

**Output**:
```
✅ Added: Alice
```

**With spaces**:
```bash
uv run names add "Bob Smith"
```

**With trimming**:
```bash
uv run names add "  Carol  "
```
Output: `✅ Added: Carol`

---

### List All Names

```bash
uv run names list
```

**Output** (alphabetical, case-insensitive):
```
Alice
Bob Smith
Carol
```

**Empty list**:
```
No names found.
```

---

## Examples

### Complete Workflow

```bash
# Add some names
uv run names add Zoe
uv run names add Alice
uv run names add "Mary Ann"
uv run names add bob

# List them (sorted alphabetically)
uv run names list
```

**Output**:
```
✅ Added: Zoe
✅ Added: Alice
✅ Added: Mary Ann
✅ Added: bob
Alice
bob
Mary Ann
Zoe
```

Note: Lowercase "bob" sorts correctly with uppercase names (case-insensitive).

---

### Error Handling

#### Empty Name
```bash
uv run names add ""
```
**Output**:
```
❌ Name cannot be empty
```
**Exit Code**: 1

#### Name Too Long
```bash
uv run names add "$(python -c 'print("A" * 257)')"
```
**Output**:
```
❌ Name too long
```
**Exit Code**: 1

#### Help
```bash
uv run names --help
uv run names add --help
uv run names list --help
```

---

## Storage

### Location
Names are stored in `names.json` at the repository root.

### Format
```json
[
  "Alice",
  "Bob Smith",
  "Carol"
]
```

### Manual Inspection
```bash
cat names.json
```

### Reset Storage
```bash
rm names.json
```

---

## Development

### Run Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src/names --cov-report=term

# Specific test category
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/contract/
```

### Linting & Formatting

```bash
# Check code
uv run ruff check src/ tests/

# Format code
uv run ruff format src/ tests/

# Type checking
uv run mypy src/
```

### Run Without `uv run` Prefix (Optional)

Activate the virtual environment:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

Then use `names` directly:
```bash
names add Alice
names list
```

---

## Troubleshooting

### `uv: command not found`
- Ensure `uv` is installed and in PATH
- Restart terminal after installation
- See: https://github.com/astral-sh/uv

### `names: command not found`
- Always use `uv run names ...` unless virtual environment is activated
- Run `uv sync` to ensure project is set up

### Permission Errors
```
❌ Storage unavailable
```
- Check file permissions for `names.json`
- Ensure write access to project directory

### Corrupt JSON
```
❌ Storage file is corrupt
```
- Inspect `names.json` for syntax errors
- Delete file to reset (or fix JSON manually)

---

## Architecture

```
┌─────────────────┐
│   CLI Layer     │  (cli.py)
│  - Parse args   │
│  - Format output│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Storage Layer   │  (storage.py)
│  - Load/save    │
│  - Sort names   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validation      │  (validation.py)
│  - Trim         │
│  - Check rules  │
└─────────────────┘
```

**Separation of Concerns**: CLI logic never touches file I/O directly; storage module encapsulates JSON operations.

---

## Next Steps

- See [spec.md](./spec.md) for detailed requirements
- See [data-model.md](./data-model.md) for entity design
- See [contracts/](./contracts/) for API contracts
- Run tests to verify installation: `uv run pytest`

---

## Support

For issues or questions:
1. Check contract documents in `specs/001-name-storage-cli/contracts/`
2. Review error messages (they're designed to be self-explanatory)
3. Inspect `names.json` for storage issues
4. Run tests to diagnose: `uv run pytest -v`
