"""Task storage and persistence."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class Task:
    """Represents a single task."""

    def __init__(
        self,
        description: str,
        status: str = "not started",
        creation_time: str | None = None,
        due_date: str | None = None,
        note: str | None = None,
        priority: str | None = None,
        estimate_hours: float | None = None,
    ) -> None:
        """Initialize a task.

        Args:
            description: Task description
            status: Task status (not started, started, complete)
            creation_time: ISO format timestamp
            due_date: Due date in YYYY-MM-DD format
            note: Optional note
            priority: Priority level (low, medium, high)
            estimate_hours: Estimated hours to complete
        """
        self.description = description
        self.status = status
        self.creation_time = creation_time or datetime.now().isoformat()
        self.due_date = due_date
        self.note = note
        self.priority = priority
        self.estimate_hours = estimate_hours

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        result: dict[str, Any] = {
            "description": self.description,
            "status": self.status,
            "creation_time": self.creation_time,
        }
        if self.due_date:
            result["due_date"] = self.due_date
        if self.note:
            result["note"] = self.note
        if self.priority:
            result["priority"] = self.priority
        if self.estimate_hours is not None:
            result["estimate_hours"] = self.estimate_hours
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        """Create task from dictionary."""
        return cls(
            description=data["description"],
            status=data.get("status", "not started"),
            creation_time=data.get("creation_time"),
            due_date=data.get("due_date"),
            note=data.get("note"),
            priority=data.get("priority"),
            estimate_hours=data.get("estimate_hours"),
        )


class TaskStore:
    """Manages task storage and retrieval."""

    VALID_STATUSES = ["not started", "started", "complete"]

    def __init__(self, storage_path: Path) -> None:
        """Initialize task store.

        Args:
            storage_path: Path to JSON storage file
        """
        self.storage_path = storage_path

    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load_tasks(self) -> list[Task]:
        """Load all tasks from storage."""
        if not self.storage_path.exists():
            return []

        with open(self.storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task.from_dict(task_dict) for task_dict in data]

    def save_tasks(self, tasks: list[Task]) -> None:
        """Save tasks to storage."""
        self._ensure_storage_dir()
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)

    def add(
        self,
        description: str,
        due_date: str | None = None,
        note: str | None = None,
        priority: str | None = None,
        estimate_hours: float | None = None,
    ) -> Task:
        """Add a new task.

        Args:
            description: Task description
            due_date: Optional due date
            note: Optional note
            priority: Optional priority level
            estimate_hours: Optional estimated hours

        Returns:
            The created task

        Raises:
            ValueError: If description is empty
        """
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")

        tasks = self.load_tasks()
        task = Task(
            description=description.strip(),
            due_date=due_date,
            note=note,
            priority=priority,
            estimate_hours=estimate_hours,
        )
        tasks.append(task)
        self.save_tasks(tasks)
        return task

    def get_all(self) -> list[Task]:
        """Get all tasks."""
        return self.load_tasks()

    def search(self, term: str) -> list[Task]:
        """Search tasks by description.

        Args:
            term: Search term

        Returns:
            List of matching tasks
        """
        tasks = self.load_tasks()
        term_lower = term.lower()
        return [task for task in tasks if term_lower in task.description.lower()]

    def delete(self, task_number: int) -> Task:
        """Delete a task by its number (1-indexed).

        Args:
            task_number: Task number to delete

        Returns:
            The deleted task

        Raises:
            ValueError: If task number is invalid
        """
        tasks = self.load_tasks()

        if not tasks:
            raise ValueError("No tasks found")

        if task_number < 1 or task_number > len(tasks):
            raise ValueError(f"Task number must be between 1 and {len(tasks)}")

        deleted_task = tasks.pop(task_number - 1)
        self.save_tasks(tasks)
        return deleted_task

    def update_status(self, task_number: int, status: str) -> Task:
        """Update task status.

        Args:
            task_number: Task number to update (1-indexed)
            status: New status

        Returns:
            The updated task

        Raises:
            ValueError: If task number or status is invalid
        """
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(self.VALID_STATUSES)}"
            )

        tasks = self.load_tasks()

        if not tasks:
            raise ValueError("No tasks found")

        if task_number < 1 or task_number > len(tasks):
            raise ValueError(f"Task number must be between 1 and {len(tasks)}")

        tasks[task_number - 1].status = status
        self.save_tasks(tasks)
        return tasks[task_number - 1]

    def update_metadata(
        self,
        task_number: int,
        due_date: str | None = None,
        note: str | None = None,
    ) -> Task:
        """Update task metadata (due date or note).

        Args:
            task_number: Task number to update (1-indexed)
            due_date: New due date (optional)
            note: New note (optional)

        Returns:
            The updated task

        Raises:
            ValueError: If task number is invalid or no updates provided
        """
        if due_date is None and note is None:
            raise ValueError("You must specify at least due_date or note")

        tasks = self.load_tasks()

        if not tasks:
            raise ValueError("No tasks found")

        if task_number < 1 or task_number > len(tasks):
            raise ValueError(f"Task number must be between 1 and {len(tasks)}")

        task = tasks[task_number - 1]
        if due_date is not None:
            task.due_date = due_date
        if note is not None:
            task.note = note

        self.save_tasks(tasks)
        return task

    def sort_tasks(self, sort_by: str, reverse: bool = False) -> list[Task]:
        """Sort tasks by specified field.

        Args:
            sort_by: Field to sort by (alpha, recent, due)
            reverse: Whether to reverse the sort order

        Returns:
            Sorted list of tasks

        Raises:
            ValueError: If sort_by is invalid
        """
        tasks = self.load_tasks()

        if not tasks:
            return []

        if sort_by == "alpha":
            sorted_tasks = sorted(tasks, key=lambda t: t.description.lower(), reverse=reverse)
        elif sort_by == "recent":
            sorted_tasks = sorted(tasks, key=lambda t: t.creation_time, reverse=not reverse)
        elif sort_by == "due":
            # Tasks with due dates first, sorted by date
            with_due = [t for t in tasks if t.due_date]
            without_due = [t for t in tasks if not t.due_date]
            with_due_sorted = sorted(with_due, key=lambda t: t.due_date or "", reverse=reverse)
            sorted_tasks = with_due_sorted + without_due
        else:
            raise ValueError(f"Invalid sort option: {sort_by}")

        self.save_tasks(sorted_tasks)
        return sorted_tasks

    def swap_tasks(self, pos1: int, pos2: int) -> list[Task]:
        """Swap two tasks by their positions.

        Args:
            pos1: First task position (1-indexed)
            pos2: Second task position (1-indexed)

        Returns:
            Updated task list

        Raises:
            ValueError: If positions are invalid
        """
        tasks = self.load_tasks()

        if not tasks:
            raise ValueError("No tasks found")

        if pos1 < 1 or pos1 > len(tasks) or pos2 < 1 or pos2 > len(tasks):
            raise ValueError(f"Task positions must be between 1 and {len(tasks)}")

        if pos1 == pos2:
            raise ValueError("Cannot swap a task with itself")

        # Convert to 0-indexed
        idx1, idx2 = pos1 - 1, pos2 - 1
        tasks[idx1], tasks[idx2] = tasks[idx2], tasks[idx1]

        self.save_tasks(tasks)
        return tasks
