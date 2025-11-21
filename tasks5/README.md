# Names CLI

A simple command-line tool to store and list people's names with persistent JSON storage.

## Features

- ✅ Add names with automatic validation and trimming
- ✅ List all names in alphabetical order (case-insensitive)
- ✅ Persistent JSON storage
- ✅ Clear error messages with emoji indicators
- ✅ Duplicate names allowed
- ✅ Unicode support

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <repository-url>
cd names

# Install dependencies
uv sync

# Run the CLI
uv run names --help
```

## Usage

### Add a Name

Add a new name to storage:

```bash
uv run names add "Alice Smith"
# ✅ Added: Alice Smith

uv run names add "Bob Jones"
# ✅ Added: Bob Jones
```

**Features:**
- Names are automatically trimmed (leading/trailing whitespace removed)
- Empty names are rejected
- Names longer than 256 characters are rejected
- Duplicate names are allowed

### List All Names

Display all stored names in alphabetical order (case-insensitive):

```bash
uv run names list
# Alice Smith
# Bob Jones
# Zoe Williams
```

If no names are stored:

```bash
uv run names list
# No names found.
```

**Sorting behavior:**
- Case-insensitive alphabetical order (alice < Bob < Carol)
- Original case is preserved in output
- Stable sort for names that are equal when case-folded

### Error Handling

The CLI provides clear error messages for invalid inputs:

```bash
# Empty name
uv run names add ""
# ❌ Error: Name cannot be empty

# Whitespace-only name
uv run names add "   "
# ❌ Error: Name cannot be empty

# Name too long (>256 characters)
uv run names add "A very long name..."
# ❌ Error: Name too long (max 256 chars)
```

### Exit Codes

- `0`: Success
- `1`: Validation error (empty name, too long, etc.)
- `2`: Usage error (missing command, invalid arguments)

## Storage

Names are stored in a JSON file at:
- Default: `~/.local/share/names/names.json`
- Custom location: Set `NAMES_STORAGE_PATH` environment variable

```bash
# Use custom storage location
export NAMES_STORAGE_PATH=/path/to/custom/names.json
uv run names add "Alice"
```

The storage file is created automatically on first use with proper parent directories.

## Development

### Prerequisites

- Python 3.12 or later
- uv package manager

### Setup Development Environment

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/names --cov-report=term-missing

# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Type check
uv run mypy src/
```

### Project Structure

```
names/
├── src/
│   └── names/
│       ├── __init__.py
│       ├── __main__.py         # Package entry point
│       ├── cli/                # CLI interface
│       │   ├── __init__.py
│       │   └── __main__.py
│       ├── validation.py       # Name validation logic
│       └── storage.py          # JSON persistence layer
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── contract/               # Contract/end-to-end tests
├── specs/                      # Feature specifications
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

### Testing

The project uses a 3-layer testing strategy:

1. **Unit tests**: Test individual components in isolation
   - `tests/unit/test_validation.py`: Name validation rules
   - `tests/unit/test_storage.py`: Storage operations

2. **Contract tests**: Verify CLI contracts match specifications
   - `tests/contract/test_cli_contract.py`: End-to-end CLI behavior

3. **Integration tests**: Test component interactions (planned)

Run all tests:

```bash
uv run pytest -v
```

Run specific test suite:

```bash
uv run pytest tests/unit/ -v
uv run pytest tests/contract/ -v
```

### Code Quality

The project enforces strict code quality standards:

- **Linting**: ruff with PEP 8 compliance
- **Formatting**: ruff formatter (line length: 100)
- **Type checking**: mypy in strict mode
- **Test coverage**: Target ≥80%

Check all quality gates:

```bash
# All checks pass = ready to merge
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
uv run pytest --cov=src/names
```

### Architecture

The project follows separation of concerns:

- **Validation layer** (`validation.py`): Input validation and normalization
  - `Name` value object with immutable, validated data

- **Storage layer** (`storage.py`): Data persistence
  - `NameStore` aggregate with JSON file operations
  - Atomic writes using temp files + os.replace()

- **CLI layer** (`cli/`): User interface
  - Command parsing with argparse
  - Error handling with emoji feedback
  - Exit code management

## Specifications

See `specs/001-name-storage-cli/` for detailed feature specifications:

- `spec.md`: User stories and requirements
- `plan.md`: Technical implementation plan
- `data-model.md`: Entity and relationship definitions
- `contracts/`: Input/output contracts
- `quickstart.md`: Integration guide
- `tasks.md`: Implementation task breakdown

## Constitution

This project follows the principles defined in `.specify/memory/constitution.md`:

1. **Clarity & Simplicity** (NON-NEGOTIABLE): Favor readable code over cleverness
2. **Code Quality**: Strict linting, formatting, and type checking
3. **Testing Standards**: Comprehensive tests required, ≥80% coverage target
4. **UX Consistency**: Uniform error handling and output formatting
5. **Documentation**: User-facing docs required for all features

## License

[Specify your license here]

## Contributing

[Add contribution guidelines]

## Support

[Add support contact information]
