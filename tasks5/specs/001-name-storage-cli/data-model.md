# Data Model: Name Storage CLI

**Feature**: 001-name-storage-cli  
**Phase**: 1 (Design)  
**Date**: 2025-11-19

## Purpose

Define entities, their attributes, validation rules, state transitions, and storage representation for the name storage system.

---

## Entities

### 1. Name (Value Object)

**Description**: A validated, normalized person name ready for storage.

**Attributes**:
- `value: str` — The normalized name (trimmed, non-empty, ≤256 chars)

**Validation Rules**:
- MUST NOT be empty after trimming whitespace
- MUST NOT be whitespace-only (spaces, tabs, newlines)
- MUST NOT exceed 256 characters
- Leading/trailing whitespace MUST be trimmed before storage
- Internal whitespace preserved (e.g., "Mary Ann" remains "Mary Ann")

**Invariants**:
- Once created, a `Name` is immutable and guaranteed valid
- No null or undefined values

**Type Definition** (Python):
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Name:
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Name cannot be empty")
        if len(self.value) > 256:
            raise ValueError("Name too long")
        # Ensure stored value is trimmed
        object.__setattr__(self, 'value', self.value.strip())
```

---

### 2. NameStore (Aggregate Root)

**Description**: The collection of all stored names with persistence responsibility.

**Attributes**:
- `names: list[Name]` — Ordered collection of names (insertion order in storage)
- `storage_path: Path` — Location of JSON file

**Operations**:

1. **add(name: str) -> Name**
   - Validates and normalizes input
   - Appends to in-memory list
   - Persists atomically to JSON
   - Returns the created `Name` object
   - Raises `ValueError` for invalid input
   - Raises `IOError` for storage failures

2. **list() -> list[Name]**
   - Reads from JSON file
   - Returns names sorted case-insensitively (stable)
   - Returns empty list if file doesn't exist or is empty
   - Raises `IOError` for unreadable file or corrupt JSON

3. **_load() -> list[str]**
   - Private: Reads raw strings from JSON
   - Returns empty list if file missing
   - Raises `IOError` for permission errors
   - Raises `ValueError` for corrupt JSON

4. **_save(names: list[str]) -> None**
   - Private: Atomically writes to JSON
   - Creates parent directories if needed
   - Uses temp file + rename for atomicity
   - Raises `IOError` on failure

**State Transitions**:
- Empty → Contains Names (via `add`)
- Contains Names → Contains More Names (via `add`)
- No state transition for `list` (read-only view with sorting applied)

**Invariants**:
- Storage file contains valid JSON array of strings
- All stored strings are non-empty and ≤256 chars (enforced by `Name` validation before storage)
- Duplicate names allowed
- Order in file is insertion order

**Type Definition** (Python):
```python
from pathlib import Path
import json
import tempfile
import os

class NameStore:
    def __init__(self, storage_path: Path = Path("names.json")):
        self.storage_path = storage_path
    
    def add(self, name_input: str) -> Name:
        """Add a validated name to storage."""
        name = Name(value=name_input)  # Validates
        current = self._load()
        current.append(name.value)
        self._save(current)
        return name
    
    def list(self) -> list[Name]:
        """Return all names sorted case-insensitively."""
        raw_names = self._load()
        sorted_names = sorted(raw_names, key=str.lower)
        return [Name(value=n) for n in sorted_names]
    
    def _load(self) -> list[str]:
        """Load raw names from JSON file."""
        if not self.storage_path.exists():
            return []
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON must be array")
                return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupt JSON: {e}") from e
        except PermissionError as e:
            raise IOError(f"Cannot read {self.storage_path}: {e}") from e
    
    def _save(self, names: list[str]) -> None:
        """Atomically save names to JSON file."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=self.storage_path.parent, 
            suffix='.tmp'
        )
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(names, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self.storage_path)
        except Exception:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise IOError("Failed to write storage file")
```

---

## Relationships

```
┌─────────────┐
│  NameStore  │
│             │
│ - names     │──────┐
│ - path      │      │ contains 0..*
└─────────────┘      │
                     ▼
                ┌─────────┐
                │  Name   │
                │         │
                │ - value │
                └─────────┘
```

- **NameStore** contains zero or more **Name** instances
- **Name** is a value object (immutable, validated)
- **NameStore** is responsible for persistence and ordering

---

## Storage Schema

### JSON File Format (`names.json`)

**Structure**: JSON array of strings

**Example**:
```json
[
  "Alice",
  "Bob",
  "Mary Ann",
  "Carol"
]
```

**Constraints**:
- Array MUST contain only strings
- Strings MUST be non-empty
- Strings MUST be ≤256 characters
- Duplicates allowed
- Order is insertion order

**File Location**: Repository root (configurable via `NameStore` constructor)

**Encoding**: UTF-8

**Atomicity**: Writes use temp file + atomic rename to prevent corruption

---

## Validation Flow

```
User Input (str)
      │
      ▼
┌──────────────────┐
│ Trim whitespace  │
└──────────────────┘
      │
      ▼
┌──────────────────┐
│ Check empty?     │────Yes───▶ ❌ Raise ValueError
└──────────────────┘
      │ No
      ▼
┌──────────────────┐
│ Check length     │────>256──▶ ❌ Raise ValueError
└──────────────────┘
      │ ≤256
      ▼
┌──────────────────┐
│ Create Name      │
└──────────────────┘
      │
      ▼
✅ Valid Name
```

---

## Error Scenarios

| Scenario | Detection | Handling |
|----------|-----------|----------|
| Empty input | `Name.__post_init__` | Raise `ValueError("Name cannot be empty")` |
| Whitespace-only | `Name.__post_init__` | Raise `ValueError("Name cannot be empty")` |
| >256 chars | `Name.__post_init__` | Raise `ValueError("Name too long")` |
| File missing (read) | `NameStore._load()` | Return `[]` (auto-create on next write) |
| File missing (write) | `NameStore._save()` | Create parent dirs + file |
| Permission error (read) | `NameStore._load()` | Raise `IOError` → CLI reports "Storage unavailable" |
| Permission error (write) | `NameStore._save()` | Raise `IOError` → CLI reports "Storage unavailable" |
| Corrupt JSON | `NameStore._load()` | Raise `ValueError` → CLI reports error |

---

## Implementation Notes

1. **Separation of Concerns**: `Name` (value object) handles validation; `NameStore` (aggregate) handles persistence and collection operations.

2. **Immutability**: `Name` is frozen (immutable) to prevent accidental modification.

3. **Atomic Writes**: `NameStore._save()` uses `tempfile` + `os.replace()` to ensure atomic writes (POSIX/Windows compatible).

4. **Case-Insensitive Sort**: Applied at read time in `list()`; storage maintains insertion order for potential future needs (undo, etc.).

5. **Error Mapping**: Domain errors (`ValueError`, `IOError`) will be caught by CLI layer and mapped to user-friendly messages + exit codes.

6. **Testing Hooks**: `NameStore` accepts custom `storage_path` for isolated testing with `tmp_path` fixtures.

---

## Future Considerations (Out of Scope)

- Deletion/update operations
- Search/filter capabilities
- Duplicate suppression
- Migration to database backend
- Concurrency control (file locking)

---

## Validation Against Requirements

| Requirement | Implementation |
|-------------|----------------|
| FR-001: Add command | `NameStore.add(name)` |
| FR-002: List command | `NameStore.list()` |
| FR-003: JSON storage | `_save()` / `_load()` with JSON format |
| FR-004: Trim whitespace | `Name.__post_init__` strips |
| FR-005: Reject empty | `Name` validation raises |
| FR-006: Reject >256 | `Name` validation raises |
| FR-007: Allow duplicates | No uniqueness check |
| FR-008: Auto-create file | `_save()` creates parent dirs |
| FR-009: Separation | `Name` + `NameStore` vs CLI module |
| FR-010: Deterministic output | `sorted()` is deterministic |
| FR-012: Stable case-insensitive | `sorted(key=str.lower)` is stable |

All functional requirements covered.
