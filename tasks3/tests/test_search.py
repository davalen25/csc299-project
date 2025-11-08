import pytest
import os
import tempfile
from tasks3.store import save_tasks
from tasks3.search import load_tasks


@pytest.fixture
def temp_data_file(monkeypatch):
    """Create a temporary data file for testing with sample tasks."""
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_tasks.json")
    
    # Patch the DATA_FILE constant in both modules
    import tasks3.search
    import tasks3.store
    monkeypatch.setattr(tasks3.search, "DATA_FILE", temp_file)
    monkeypatch.setattr(tasks3.store, "DATA_FILE", temp_file)
    
    # Create sample tasks for testing
    sample_tasks = [
        {
            "description": "Write Python tests",
            "status": "started",
            "creation_time": "2025-11-07T10:00:00"
        },
        {
            "description": "Review code documentation",
            "status": "not started",
            "creation_time": "2025-11-07T11:00:00"
        },
        {
            "description": "Deploy to production",
            "status": "not started",
            "creation_time": "2025-11-07T12:00:00",
            "due_date": "2025-11-15"
        },
        {
            "description": "Write unit tests for API",
            "status": "complete",
            "creation_time": "2025-11-06T09:00:00"
        }
    ]
    
    save_tasks(sample_tasks)
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)
    os.rmdir(temp_dir)


def test_search_finds_matching_tasks(temp_data_file):
    """Test that search correctly finds tasks containing the search term."""
    tasks = load_tasks()
    
    # Search for tasks containing "write"
    search_term = "write"
    found = [task for task in tasks if search_term in task['description'].lower()]
    
    assert len(found) == 2
    descriptions = [task['description'] for task in found]
    assert "Write Python tests" in descriptions
    assert "Write unit tests for API" in descriptions


def test_search_case_insensitive(temp_data_file):
    """Test that search is case insensitive."""
    tasks = load_tasks()
    
    # Search with different cases
    search_term_lower = "python"
    search_term_upper = "PYTHON"
    search_term_mixed = "PyThOn"
    
    found_lower = [task for task in tasks if search_term_lower in task['description'].lower()]
    found_upper = [task for task in tasks if search_term_upper.lower() in task['description'].lower()]
    found_mixed = [task for task in tasks if search_term_mixed.lower() in task['description'].lower()]
    
    # All should find the same task
    assert len(found_lower) == 1
    assert len(found_upper) == 1
    assert len(found_mixed) == 1
    assert found_lower == found_upper == found_mixed


def test_search_no_matches(temp_data_file):
    """Test that search returns empty list when no matches found."""
    tasks = load_tasks()
    
    search_term = "nonexistent"
    found = [task for task in tasks if search_term in task['description'].lower()]
    
    assert len(found) == 0
    assert found == []


def test_search_partial_match(temp_data_file):
    """Test that search finds partial matches."""
    tasks = load_tasks()
    
    # Search for partial word
    search_term = "test"
    found = [task for task in tasks if search_term in task['description'].lower()]
    
    assert len(found) == 2
    # Should find both "Write Python tests" and "Write unit tests for API"
    

def test_search_multiple_word_term(temp_data_file):
    """Test searching with multiple words."""
    tasks = load_tasks()
    
    search_term = "unit tests"
    found = [task for task in tasks if search_term in task['description'].lower()]
    
    assert len(found) == 1
    assert found[0]['description'] == "Write unit tests for API"


def test_search_preserves_task_metadata(temp_data_file):
    """Test that search results preserve all task metadata."""
    tasks = load_tasks()
    
    search_term = "production"
    found = [task for task in tasks if search_term in task['description'].lower()]
    
    assert len(found) == 1
    task = found[0]
    assert task['description'] == "Deploy to production"
    assert task['status'] == "not started"
    assert 'creation_time' in task
    assert 'due_date' in task
    assert task['due_date'] == "2025-11-15"
