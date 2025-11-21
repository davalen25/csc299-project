# CLI Contract: names add

**Command**: `names add <name>`

**Purpose**: Add a validated name to persistent storage

---

## Input Specification

### Syntax
```
names add <name>
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | Name to add; may contain spaces; quotes optional unless name has leading/trailing spaces |

### Examples
```bash
names add Alice
names add "Bob Smith"
names add "  Carol  "  # Will be trimmed to "Carol"
```

---

## Output Specification

### Success Case

**Exit Code**: `0`

**stdout**:
```
✅ Added: <normalized_name>
```

**stderr**: (empty)

**Example**:
```
✅ Added: Alice
```

### Error Cases

#### Empty Name

**Trigger**: Input is empty or whitespace-only after trimming

**Exit Code**: `1`

**stdout**: (empty)

**stderr**:
```
❌ Name cannot be empty
```

#### Name Too Long

**Trigger**: Input exceeds 256 characters

**Exit Code**: `1`

**stdout**: (empty)

**stderr**:
```
❌ Name too long
```

#### Storage Unavailable

**Trigger**: Cannot write to storage file (permissions, disk full, etc.)

**Exit Code**: `2`

**stdout**: (empty)

**stderr**:
```
❌ Storage unavailable
```

---

## Behavior Specification

1. **Input Processing**:
   - Accept `<name>` from command line arguments
   - Trim leading/trailing whitespace
   - Validate against rules (non-empty, ≤256 chars)

2. **Storage**:
   - Append validated name to JSON file
   - Create file if it doesn't exist
   - Use atomic write (temp file + rename)

3. **Output**:
   - Print success message with emoji to stdout
   - Print error message with emoji to stderr on failure
   - Return appropriate exit code

4. **Edge Cases**:
   - Duplicate names: Allowed; stored again
   - Special characters: Preserved (Unicode supported)
   - Internal spaces: Preserved (e.g., "Mary Ann")

---

## State Changes

- **Before**: Storage file contains N names (or doesn't exist)
- **After (success)**: Storage file contains N+1 names
- **After (failure)**: Storage file unchanged

---

## Contract Tests

```python
def test_add_success():
    result = run_cli(['names', 'add', 'Alice'])
    assert result.returncode == 0
    assert result.stdout == '✅ Added: Alice\n'
    assert result.stderr == ''

def test_add_empty():
    result = run_cli(['names', 'add', ''])
    assert result.returncode == 1
    assert result.stdout == ''
    assert result.stderr == '❌ Name cannot be empty\n'

def test_add_whitespace_only():
    result = run_cli(['names', 'add', '   '])
    assert result.returncode == 1
    assert result.stderr == '❌ Name cannot be empty\n'

def test_add_too_long():
    long_name = 'A' * 257
    result = run_cli(['names', 'add', long_name])
    assert result.returncode == 1
    assert result.stderr == '❌ Name too long\n'

def test_add_with_trim():
    result = run_cli(['names', 'add', '  Bob  '])
    assert result.returncode == 0
    assert result.stdout == '✅ Added: Bob\n'
```

---

## Notes

- Emoji characters (✅, ❌) are UTF-8 encoded; terminal must support Unicode
- Exit codes follow convention: 0=success, 1=validation error, 2=system error
- All output must use UTF-8 encoding
