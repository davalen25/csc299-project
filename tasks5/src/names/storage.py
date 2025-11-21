"""JSON file storage logic for names."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from names.validation import Name


class NameStore:
    """Collection of stored names with JSON persistence.

    Attributes:
        storage_path: Location of JSON file
    """

    def __init__(self, storage_path: Path = Path("names.json")) -> None:
        """Initialize name storage.

        Args:
            storage_path: Path to JSON storage file
        """
        self.storage_path = storage_path

    def add(self, name_input: str) -> Name:
        """Add a validated name to storage.

        Args:
            name_input: Raw name string to add

        Returns:
            The created Name object

        Raises:
            ValueError: If name is invalid
            IOError: If storage write fails
        """
        name = Name(value=name_input)  # Validates and normalizes
        current = self._load()
        current.append(name.value)
        self._save(current)
        return name

    def get_all(self) -> list[Name]:
        """Return all names sorted case-insensitively.

        Returns:
            List of Name objects in alphabetical order

        Raises:
            IOError: If storage read fails
            ValueError: If JSON is corrupt
        """
        raw_names = self._load()
        sorted_names = sorted(raw_names, key=str.lower)
        return [Name(value=n) for n in sorted_names]

    def _load(self) -> list[str]:
        """Load raw names from JSON file.

        Returns:
            List of name strings, or empty list if file doesn't exist

        Raises:
            IOError: If file is unreadable
            ValueError: If JSON is corrupt
        """
        if not self.storage_path.exists():
            return []

        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON must be array")
                return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupt JSON: {e}") from e
        except PermissionError as e:
            raise OSError(f"Cannot read {self.storage_path}: {e}") from e

    def _save(self, names: list[str]) -> None:
        """Atomically save names to JSON file.

        Args:
            names: List of name strings to save

        Raises:
            IOError: If write fails
        """
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=self.storage_path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(names, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self.storage_path)
        except Exception as e:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise OSError("Failed to write storage file") from e
