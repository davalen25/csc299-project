import sys
from tasks3 import store, list, search, delete, update_status, update_task, sort_tasks


def inc(n: int) -> int:
    return n + 1


def print_help():
    """Print help message showing available commands."""
    help_text = """
Task Management System (tasks3)
================================

Usage: uv run tasks3 <command> [arguments]

Available commands:

  add <description> [--due YYYY-MM-DD] [--note "note text"]
      Add a new task with optional due date and note
      Example: uv run tasks3 add "Write documentation" --due 2025-11-15

  list
      List all tasks with their status
      Example: uv run tasks3 list

  search <term>
      Search for tasks containing the search term
      Example: uv run tasks3 search "documentation"

  delete <task_number>
      Delete a task by its number
      Example: uv run tasks3 delete 1

  status <task_number> <status>
      Update task status (not started, started, complete)
      Example: uv run tasks3 status 1 started

  update <task_number> <new_description>
      Update task description
      Example: uv run tasks3 update 1 "New description"

  sort [--by field] [--reverse]
      Sort tasks by field (status, due_date, creation_time)
      Example: uv run tasks3 sort --by due_date

  help
      Show this help message

"""
    print(help_text)


def main() -> None:
    """Main entry point for the task management system."""
    if len(sys.argv) < 2:
        print("Error: No command specified.")
        print("Use 'uv run tasks3 help' for usage information.")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "help" or command == "--help" or command == "-h":
        print_help()
    elif command == "add":
        # Pass arguments to store module
        sys.argv = ["store.py"] + sys.argv[2:]
        store.main()
    elif command == "list":
        list.main()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Search term required")
            print("Usage: uv run tasks3 search <term>")
            sys.exit(1)
        sys.argv = ["search.py"] + sys.argv[2:]
        search.main()
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Task number required")
            print("Usage: uv run tasks3 delete <task_number>")
            sys.exit(1)
        sys.argv = ["delete.py"] + sys.argv[2:]
        delete.main()
    elif command == "status":
        if len(sys.argv) < 4:
            print("Error: Task number and status required")
            print("Usage: uv run tasks3 status <task_number> <status>")
            sys.exit(1)
        sys.argv = ["update_status.py"] + sys.argv[2:]
        update_status.main()
    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: Task number and new description required")
            print("Usage: uv run tasks3 update <task_number> <new_description>")
            sys.exit(1)
        sys.argv = ["update_task.py"] + sys.argv[2:]
        update_task.main()
    elif command == "sort":
        sys.argv = ["sort_tasks.py"] + sys.argv[2:]
        sort_tasks.main()
    else:
        print(f"Error: Unknown command '{command}'")
        print("Use 'uv run tasks3 help' for usage information.")
        sys.exit(1)

