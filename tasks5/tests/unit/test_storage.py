"""Unit tests for NameStore storage operations."""

import json
from pathlib import Path

import pytest

from names.storage import NameStore
from names.validation import Name


class TestNameStoreLoad:
    """Test NameStore._load() method."""

    def test_load_missing_file_returns_empty(self, tmp_path: Path) -> None:
        """Test loading from non-existent file returns empty list."""
        store = NameStore(storage_path=tmp_path / "nonexistent.json")
        result = store._load()
        assert result == []

    def test_load_valid_json(self, tmp_path: Path) -> None:
        """Test loading valid JSON array."""
        path = tmp_path / "names.json"
        path.write_text('["Alice", "Bob"]', encoding="utf-8")
        store = NameStore(storage_path=path)
        result = store._load()
        assert result == ["Alice", "Bob"]

    def test_load_empty_array(self, tmp_path: Path) -> None:
        """Test loading empty JSON array."""
        path = tmp_path / "names.json"
        path.write_text("[]", encoding="utf-8")
        store = NameStore(storage_path=path)
        result = store._load()
        assert result == []

    def test_load_corrupt_json_raises(self, tmp_path: Path) -> None:
        """Test loading corrupt JSON raises ValueError."""
        path = tmp_path / "names.json"
        path.write_text("{not valid json", encoding="utf-8")
        store = NameStore(storage_path=path)
        with pytest.raises(ValueError, match="Corrupt JSON"):
            store._load()

    def test_load_non_array_raises(self, tmp_path: Path) -> None:
        """Test loading non-array JSON raises ValueError."""
        path = tmp_path / "names.json"
        path.write_text('{"name": "Alice"}', encoding="utf-8")
        store = NameStore(storage_path=path)
        with pytest.raises(ValueError, match="JSON must be array"):
            store._load()


class TestNameStoreSave:
    """Test NameStore._save() method."""

    def test_save_creates_file(self, tmp_path: Path) -> None:
        """Test save creates file if it doesn't exist."""
        path = tmp_path / "names.json"
        store = NameStore(storage_path=path)
        store._save(["Alice"])
        assert path.exists()

    def test_save_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Test save creates parent directories."""
        path = tmp_path / "subdir" / "names.json"
        store = NameStore(storage_path=path)
        store._save(["Alice"])
        assert path.exists()

    def test_save_valid_json(self, tmp_path: Path) -> None:
        """Test save writes valid JSON."""
        path = tmp_path / "names.json"
        store = NameStore(storage_path=path)
        store._save(["Alice", "Bob"])

        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        assert data == ["Alice", "Bob"]

    def test_save_overwrites_existing(self, tmp_path: Path) -> None:
        """Test save overwrites existing file."""
        path = tmp_path / "names.json"
        path.write_text('["Old"]', encoding="utf-8")
        store = NameStore(storage_path=path)
        store._save(["New"])

        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        assert data == ["New"]

    def test_save_preserves_unicode(self, tmp_path: Path) -> None:
        """Test save preserves Unicode characters."""
        path = tmp_path / "names.json"
        store = NameStore(storage_path=path)
        store._save(["Zoë", "José"])

        content = path.read_text(encoding="utf-8")
        assert "Zoë" in content
        assert "José" in content


class TestNameStoreAdd:
    """Test NameStore.add() method."""

    def test_add_to_empty_storage(self, tmp_path: Path) -> None:
        """Test adding first name to empty storage."""
        path = tmp_path / "names.json"
        store = NameStore(storage_path=path)
        result = store.add("Alice")

        assert isinstance(result, Name)
        assert result.value == "Alice"
        assert json.loads(path.read_text()) == ["Alice"]

    def test_add_to_existing_storage(self, tmp_path: Path) -> None:
        """Test adding name to existing storage."""
        path = tmp_path / "names.json"
        path.write_text('["Alice"]', encoding="utf-8")
        store = NameStore(storage_path=path)
        store.add("Bob")

        assert json.loads(path.read_text()) == ["Alice", "Bob"]

    def test_add_trims_whitespace(self, tmp_path: Path) -> None:
        """Test add trims whitespace from input."""
        path = tmp_path / "names.json"
        store = NameStore(storage_path=path)
        result = store.add("  Carol  ")

        assert result.value == "Carol"
        assert json.loads(path.read_text()) == ["Carol"]

    def test_add_empty_raises(self, tmp_path: Path) -> None:
        """Test adding empty name raises ValueError."""
        store = NameStore(storage_path=tmp_path / "names.json")
        with pytest.raises(ValueError, match="Name cannot be empty"):
            store.add("")

    def test_add_too_long_raises(self, tmp_path: Path) -> None:
        """Test adding too-long name raises ValueError."""
        store = NameStore(storage_path=tmp_path / "names.json")
        with pytest.raises(ValueError, match="Name too long"):
            store.add("A" * 257)

    def test_add_duplicate_allowed(self, tmp_path: Path) -> None:
        """Test duplicate names are allowed."""
        path = tmp_path / "names.json"
        store = NameStore(storage_path=path)
        store.add("Alice")
        store.add("Alice")

        assert json.loads(path.read_text()) == ["Alice", "Alice"]


class TestNameStoreList:
    """Test NameStore.get_all() method."""

    def test_list_empty_storage(self, tmp_path: Path) -> None:
        """Test listing empty storage returns empty list."""
        store = NameStore(storage_path=tmp_path / "nonexistent.json")
        result = store.get_all()
        assert result == []

    def test_list_single_name(self, tmp_path: Path) -> None:
        """Test listing single name."""
        path = tmp_path / "names.json"
        path.write_text('["Alice"]', encoding="utf-8")
        store = NameStore(storage_path=path)
        result = store.get_all()

        assert len(result) == 1
        assert result[0].value == "Alice"

    def test_list_sorts_alphabetically(self, tmp_path: Path) -> None:
        """Test list sorts names alphabetically."""
        path = tmp_path / "names.json"
        path.write_text('["Zoe", "Alice", "Bob"]', encoding="utf-8")
        store = NameStore(storage_path=path)
        result = store.get_all()

        values = [n.value for n in result]
        assert values == ["Alice", "Bob", "Zoe"]

    def test_list_case_insensitive_sort(self, tmp_path: Path) -> None:
        """Test list sorts case-insensitively."""
        path = tmp_path / "names.json"
        path.write_text('["bob", "Alice", "CAROL"]', encoding="utf-8")
        store = NameStore(storage_path=path)
        result = store.get_all()

        values = [n.value for n in result]
        assert values == ["Alice", "bob", "CAROL"]

    def test_list_preserves_original_case(self, tmp_path: Path) -> None:
        """Test list preserves original case in output."""
        path = tmp_path / "names.json"
        path.write_text('["alice", "ALICE", "Alice"]', encoding="utf-8")
        store = NameStore(storage_path=path)
        result = store.get_all()

        values = [n.value for n in result]
        # All present, stable sort among equal lowercase
        assert set(values) == {"alice", "ALICE", "Alice"}
        assert len(values) == 3

    def test_list_stable_sort(self, tmp_path: Path) -> None:
        """Test list uses stable sort for equal names."""
        path = tmp_path / "names.json"
        path.write_text('["Alice1", "alice2", "Alice3"]', encoding="utf-8")
        store = NameStore(storage_path=path)
        result = store.get_all()

        values = [n.value for n in result]
        # All start with same letter (case-insensitive), order should be stable
        assert values[0] == "Alice1"
        assert values[1] == "alice2"
        assert values[2] == "Alice3"
