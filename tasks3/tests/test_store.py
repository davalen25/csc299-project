import pytest
import json
import os
import tempfile
from datetime import datetime
from tasks3.store import load_tasks, save_tasks


@pytest.fixture
def temp_data_file(monkeypatch):
    """Create a temporary data file for testing."""
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_tasks.json")
    
    # Patch the DATA_FILE constant in the store module
    import tasks3.store
    monkeypatch.setattr(tasks3.store, "DATA_FILE", temp_file)
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)
    os.rmdir(temp_dir)


def test_load_tasks_empty(temp_data_file):
    """Test loading tasks when no file exists."""
    tasks = load_tasks()
    assert tasks == []
    assert isinstance(tasks, list)


def test_save_and_load_tasks(temp_data_file):
    """Test saving and loading tasks."""
    test_tasks = [
        {
            "description": "Test task 1",
            "status": "not started",
            "creation_time": datetime.now().isoformat()
        },
        {
            "description": "Test task 2",
            "status": "started",
            "creation_time": datetime.now().isoformat(),
            "due_date": "2025-12-31"
        }
    ]
    
    # Save tasks
    save_tasks(test_tasks)
    
    # Verify file was created
    assert os.path.exists(temp_data_file)
    
    # Load tasks back
    loaded_tasks = load_tasks()
    
    # Verify loaded tasks match saved tasks
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0]["description"] == "Test task 1"
    assert loaded_tasks[0]["status"] == "not started"
    assert loaded_tasks[1]["description"] == "Test task 2"
    assert loaded_tasks[1]["status"] == "started"
    assert loaded_tasks[1]["due_date"] == "2025-12-31"


def test_save_tasks_with_notes(temp_data_file):
    """Test saving tasks with optional notes."""
    test_tasks = [
        {
            "description": "Task with note",
            "status": "not started",
            "creation_time": datetime.now().isoformat(),
            "note": "This is an important note"
        }
    ]
    
    save_tasks(test_tasks)
    loaded_tasks = load_tasks()
    
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0]["note"] == "This is an important note"


def test_save_tasks_preserves_structure(temp_data_file):
    """Test that saving tasks preserves the JSON structure."""
    test_tasks = [
        {
            "description": "Structured task",
            "status": "complete",
            "creation_time": "2025-11-07T10:00:00",
            "due_date": "2025-11-10",
            "note": "Test note"
        }
    ]
    
    save_tasks(test_tasks)
    
    # Read the file directly to verify JSON structure
    with open(temp_data_file, "r") as f:
        file_content = json.load(f)
    
    assert file_content == test_tasks
    assert "description" in file_content[0]
    assert "status" in file_content[0]
    assert "creation_time" in file_content[0]
