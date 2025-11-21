# CLI Contract: Error Handling

**Purpose**: Define unified error handling behavior across all commands

---

## Exit Code Convention

| Code | Meaning | Usage |
|------|---------|-------|
| `0` | Success | Command completed successfully |
| `1` | Validation Error | Invalid input (empty name, too long, etc.) |
| `2` | System Error | Storage unavailable, corrupt file, etc. |

---

## Error Output Format

All errors use:
- **stderr** for message
- **stdout** remains empty
- Emoji prefix `❌`
- Clear, user-friendly message

**Template**:
```
❌ <error_message>
```

---

## Error Catalog

### Validation Errors (Exit Code 1)

#### Empty Name
**Trigger**: Name is empty or whitespace-only after trimming  
**Message**: `❌ Name cannot be empty`  
**Commands**: `add`

#### Name Too Long
**Trigger**: Name exceeds 256 characters  
**Message**: `❌ Name too long`  
**Commands**: `add`

---

### System Errors (Exit Code 2)

#### Storage Unavailable
**Trigger**: File permissions deny read/write, disk full, I/O error  
**Message**: `❌ Storage unavailable`  
**Commands**: `add`, `list`

#### Corrupt Storage
**Trigger**: JSON file is malformed or not an array  
**Message**: `❌ Storage file is corrupt`  
**Commands**: `list`

---

### Invalid Command (Exit Code 1)

#### Unknown Command
**Trigger**: Command not recognized  
**Message**: (usage text shown)
**Example**:
```
usage: names [-h] {add,list} ...
names: error: invalid choice: 'delete' (choose from 'add', 'list')
```

#### Missing Arguments
**Trigger**: Required argument not provided  
**Message**: (usage text shown)
**Example**:
```
usage: names add [-h] name
names add: error: the following arguments are required: name
```

---

## Help/Usage Contract

### Command: `names -h` or `names --help`

**Exit Code**: `0`

**stdout**:
```
usage: names [-h] {add,list} ...

Manage a list of people's names

positional arguments:
  {add,list}
    add       Add a name
    list      List all names

options:
  -h, --help  show this help message and exit
```

### Command: `names add -h`

**Exit Code**: `0`

**stdout**:
```
usage: names add [-h] name

positional arguments:
  name        Name to add

options:
  -h, --help  show this help message and exit
```

### Command: `names list -h`

**Exit Code**: `0`

**stdout**:
```
usage: names list [-h]

options:
  -h, --help  show this help message and exit
```

---

## Contract Tests

```python
def test_unknown_command():
    result = run_cli(['names', 'delete', 'Alice'])
    assert result.returncode != 0
    assert 'invalid choice' in result.stderr.lower()

def test_missing_argument():
    result = run_cli(['names', 'add'])
    assert result.returncode != 0
    assert 'required' in result.stderr.lower()

def test_help_main():
    result = run_cli(['names', '-h'])
    assert result.returncode == 0
    assert 'usage: names' in result.stdout
    assert '{add,list}' in result.stdout

def test_help_add():
    result = run_cli(['names', 'add', '-h'])
    assert result.returncode == 0
    assert 'usage: names add' in result.stdout
```

---

## Error Recovery

- **No automatic retry**: User must fix input and re-run
- **State preservation**: Failed operations leave storage unchanged
- **Clear diagnostics**: Error messages indicate root cause
- **Graceful degradation**: Missing file treated as empty, not error (for `list`)

---

## Notes

- All errors are deterministic (no random behavior)
- Error messages are consistent and actionable
- Emoji improves scannability in terminal output
- System errors distinguish storage problems from validation problems
