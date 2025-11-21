# CLI Contract: names list

**Command**: `names list`

**Purpose**: Display all stored names in alphabetical order (case-insensitive)

---

## Input Specification

### Syntax
```
names list
```

### Arguments

None.

### Examples
```bash
names list
```

---

## Output Specification

### Success Case (Non-Empty)

**Exit Code**: `0`

**stdout**:
```
<name1>
<name2>
<name3>
...
```
(One name per line, sorted alphabetically case-insensitive, preserving original case)

**stderr**: (empty)

**Example**:
```
Alice
Bob
carol
David
```
(Note: "carol" lowercase comes after "Bob" in case-insensitive sort; original case preserved)

### Success Case (Empty Storage)

**Exit Code**: `0`

**stdout**:
```
No names found.
```

**stderr**: (empty)

### Error Cases

#### Storage Unavailable

**Trigger**: Cannot read storage file (permissions, etc.)

**Exit Code**: `2`

**stdout**: (empty)

**stderr**:
```
❌ Storage unavailable
```

#### Corrupt Storage

**Trigger**: JSON file is malformed

**Exit Code**: `2`

**stdout**: (empty)

**stderr**:
```
❌ Storage file is corrupt
```

---

## Behavior Specification

1. **Storage Access**:
   - Read from JSON file
   - Return empty result if file doesn't exist (not an error)
   - Report error if file exists but unreadable or corrupt

2. **Sorting**:
   - Sort names using case-insensitive comparison (`str.lower()`)
   - Preserve original case in output
   - Stable sort (equal names maintain relative order from storage)

3. **Output**:
   - One name per line
   - No decorations (no bullets, numbers, quotes)
   - No trailing newline after list (one newline per name)
   - Empty list shows friendly message

4. **Edge Cases**:
   - Duplicate names: All shown, adjacent due to sorting
   - Mixed case: Sorted together (e.g., "alice", "Alice", "ALICE" adjacent)
   - Special characters: Displayed as-is (Unicode supported)

---

## Sorting Examples

### Input (storage order):
```json
["Zoe", "alice", "Bob", "ALICE", "Carol"]
```

### Output (alphabetical, case-insensitive):
```
alice
ALICE
Bob
Carol
Zoe
```

### Stability Example:
```json
["Alice", "ALICE", "alice"]
```
Output preserves relative order among case-equal names:
```
Alice
ALICE
alice
```

---

## State Changes

- **Before**: Storage file with N names
- **After**: Storage file unchanged (read-only operation)

---

## Contract Tests

```python
def test_list_sorted():
    setup_storage(['Zoe', 'Alice', 'Bob'])
    result = run_cli(['names', 'list'])
    assert result.returncode == 0
    assert result.stdout == 'Alice\nBob\nZoe\n'
    assert result.stderr == ''

def test_list_case_insensitive():
    setup_storage(['bob', 'Alice', 'CAROL'])
    result = run_cli(['names', 'list'])
    assert result.returncode == 0
    assert result.stdout == 'Alice\nbob\nCAROL\n'

def test_list_empty():
    clear_storage()
    result = run_cli(['names', 'list'])
    assert result.returncode == 0
    assert result.stdout == 'No names found.\n'
    assert result.stderr == ''

def test_list_missing_file():
    delete_storage()
    result = run_cli(['names', 'list'])
    assert result.returncode == 0
    assert result.stdout == 'No names found.\n'

def test_list_duplicates():
    setup_storage(['Alice', 'Bob', 'Alice'])
    result = run_cli(['names', 'list'])
    assert result.returncode == 0
    assert result.stdout == 'Alice\nAlice\nBob\n'

def test_list_stable_sort():
    setup_storage(['Alice', 'ALICE', 'alice'])
    result = run_cli(['names', 'list'])
    lines = result.stdout.strip().split('\n')
    # All three present, grouped together
    assert set(lines) == {'Alice', 'ALICE', 'alice'}
    assert len(lines) == 3
```

---

## Notes

- Output is plain text; no JSON or structured format
- Sorting uses Python's `sorted(names, key=str.lower)`
- No pagination (assumes reasonable name count per spec: <10k)
- File missing is not an error (treated as empty)
