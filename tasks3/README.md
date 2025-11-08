# Tasks3 - Personal Knowledge Management System (PKMS)

A command-line task management system built with Python, designed for efficient task tracking and organization.

## Features

- **Task Management**: Create, list, search, update, and delete tasks
- **Status Tracking**: Track task progress (not started, started, complete)
- **Due Dates**: Set and track task deadlines
- **Notes**: Add additional context to tasks
- **Search**: Find tasks quickly with keyword search
- **Sorting**: Organize tasks by status, due date, or creation time

## Installation

This project uses `uv` for dependency management. Make sure you have `uv` installed.

```bash
# Install dependencies
uv sync
```

## Usage

The application provides a unified CLI interface through the main entry point:

```bash
uv run tasks3 <command> [arguments]
```

### Available Commands

#### Add a Task
```bash
uv run tasks3 add "Task description" [--due YYYY-MM-DD] [--note "note text"]
```
Example:
```bash
uv run tasks3 add "Write documentation" --due 2025-11-15 --note "Include examples"
```

#### List All Tasks
```bash
uv run tasks3 list
```

#### Search for Tasks
```bash
uv run tasks3 search <search term>
```
Example:
```bash
uv run tasks3 search "documentation"
```

#### Delete a Task
```bash
uv run tasks3 delete <task_number>
```
Example:
```bash
uv run tasks3 delete 1
```

#### Update Task Status
```bash
uv run tasks3 status <task_number> <status>
```
Status options: `not started`, `started`, `complete`

Example:
```bash
uv run tasks3 status 1 started
```

#### Update Task Description
```bash
uv run tasks3 update <task_number> <new_description>
```
Example:
```bash
uv run tasks3 update 1 "Updated task description"
```

#### Sort Tasks
```bash
uv run tasks3 sort [--by field] [--reverse]
```
Sort fields: `status`, `due_date`, `creation_time`

Example:
```bash
uv run tasks3 sort --by due_date
```

#### Help
```bash
uv run tasks3 help
```

## Project Structure

```
tasks3/
├── src/
│   └── tasks3/
│       ├── __init__.py         # Main entry point with CLI interface
│       ├── store.py            # Task storage and persistence
│       ├── list.py             # List tasks functionality
│       ├── search.py           # Search functionality
│       ├── delete.py           # Delete tasks
│       ├── update_status.py    # Update task status
│       ├── update_task.py      # Update task descriptions
│       └── sort_tasks.py       # Sort tasks by various fields
├── tests/
│   ├── test_store.py           # Tests for storage functionality
│   ├── test_search.py          # Tests for search functionality
│   └── test_inc.py             # Basic utility tests
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## New Implementations (November 2025)

### Unified CLI Interface
- **Main Entry Point**: Updated `__init__.py` to provide a unified command-line interface
- **Command Router**: Single `uv run tasks3` command routes to all functionality
- **Help System**: Comprehensive help documentation accessible via `uv run tasks3 help`

### Comprehensive Test Suite
Added pytest-based testing framework with two main test files:

#### `test_store.py` - Storage Functionality Tests
- **test_load_tasks_empty**: Verifies behavior when no tasks file exists
- **test_save_and_load_tasks**: Tests saving and loading multiple tasks with various fields
- **test_save_tasks_with_notes**: Validates tasks with optional notes
- **test_save_tasks_preserves_structure**: Ensures JSON structure integrity

#### `test_search.py` - Search Functionality Tests
- **test_search_finds_matching_tasks**: Verifies correct task matching
- **test_search_case_insensitive**: Tests case-insensitive search
- **test_search_no_matches**: Handles no results scenarios
- **test_search_partial_match**: Tests partial word matching
- **test_search_multiple_word_term**: Multi-word search validation
- **test_search_preserves_task_metadata**: Ensures all task data is preserved

### Testing Features
- **Fixtures**: Use of pytest fixtures for test isolation
- **Temporary Files**: Tests use temporary files to avoid affecting actual data
- **Monkeypatching**: Clean testing environment without side effects
- **Comprehensive Coverage**: Tests cover core functionality including edge cases

## Running Tests

Run all tests:
```bash
uv run pytest tests/ -v
```

Run specific test file:
```bash
uv run pytest tests/test_store.py -v
uv run pytest tests/test_search.py -v
```

Run with coverage:
```bash
uv run pytest tests/ --cov=tasks3 --cov-report=html
```

## Data Storage

Tasks are stored in `tasks.json` in the current working directory. Each task contains:
- `description`: Task description (required)
- `status`: Current status (not started, started, complete)
- `creation_time`: ISO format timestamp
- `due_date`: Optional due date (YYYY-MM-DD)
- `note`: Optional additional notes

Example task structure:
```json
{
  "description": "Write documentation",
  "status": "started",
  "creation_time": "2025-11-07T10:00:00",
  "due_date": "2025-11-15",
  "note": "Include examples"
}
```

## Development

### Requirements
- Python >= 3.13
- pytest >= 8.4.2

### Contributing
1. Make changes to the source code
2. Add tests for new functionality
3. Run tests to ensure everything passes
4. Update documentation as needed

## Author

David Valencia (davalencia102@gmail.com)

## License

This project is part of CSC 299 coursework.