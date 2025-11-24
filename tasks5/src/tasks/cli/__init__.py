"""CLI interface for task management."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from tasks.ai import get_task_advice, suggest_priority, summarize_task
from tasks.storage import Task, TaskStore


def get_storage_path() -> Path:
    """Get storage path from environment or use default."""
    env_path = os.getenv("TASKS_STORAGE_PATH")
    if env_path:
        return Path(env_path)
    return Path.home() / ".local" / "share" / "tasks" / "tasks.json"


def format_task(task: Task, number: int) -> str:
    """Format a task for display.

    Args:
        task: Task to format
        number: Task number

    Returns:
        Formatted task string
    """
    lines = [f"{number}. [{task.status.upper()}] {task.description}"]
    if task.priority:
        priority_display = task.priority.upper()
        lines.append(f"   Priority: {priority_display}")
    if task.estimate_hours is not None:
        lines.append(f"   Estimate: {task.estimate_hours}h")
    if task.due_date:
        lines.append(f"   Due: {task.due_date}")
    if task.note:
        lines.append(f"   Note: {task.note}")
    return "\n".join(lines)


def cmd_add(args: argparse.Namespace) -> int:
    """Handle 'add' command."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    description = args.description

    # AI: Summarize if requested and description is long
    if args.summarize and len(description) > 50:
        print("🤖 Generating summary...")
        summary = summarize_task(description)
        if summary and "unavailable" not in summary.lower() and "api key" not in summary.lower():
            print(f"   Original: {description}")
            print(f"   Summary: {summary}")
            use_summary = input("   Use summary as task description? (y/n): ").strip().lower()
            if use_summary == "y":
                description = summary

    # AI: Auto-suggest priority if requested
    priority = None
    estimate_hours = None
    if args.auto_priority:
        print("🤖 Analyzing task priority...")
        priority_data = suggest_priority(description, args.due)
        priority = priority_data.get("priority")
        estimate_hours = priority_data.get("estimate_hours")
        reason = priority_data.get("reason", "")
        if priority and "error" not in reason.lower():
            print(f"   Suggested priority: {priority.upper()}")
            print(f"   Estimated time: {estimate_hours}h")
            print(f"   Reason: {reason}")

    try:
        task = store.add(
            description=description,
            due_date=args.due,
            note=args.note,
            priority=priority,
            estimate_hours=estimate_hours,
        )
        print(f"✅ Task added: {task.description}")
        if task.priority:
            print(f"   Priority: {task.priority.upper()}")
        if task.estimate_hours is not None:
            print(f"   Estimate: {task.estimate_hours}h")
        if task.due_date:
            print(f"   Due date: {task.due_date}")
        if task.note:
            print(f"   Note: {task.note}")
        return 0
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_list(args: argparse.Namespace) -> int:
    """Handle 'list' command."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    tasks = store.get_all()
    if not tasks:
        print("No tasks found.")
    else:
        for i, task in enumerate(tasks, 1):
            print(format_task(task, i))

    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Handle 'search' command."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    tasks = store.search(args.term)
    if not tasks:
        print("No matching tasks found.")
    else:
        for i, task in enumerate(tasks, 1):
            print(format_task(task, i))

    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    """Handle 'delete' command."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    try:
        task = store.delete(args.number)
        print(f"✅ Task {args.number} deleted: {task.description}")
        return 0
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    """Handle 'status' command."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    try:
        task = store.update_status(args.number, args.status)
        print(f"✅ Task {args.number} status updated to: {task.status}")
        print(f"   Task: {task.description}")
        return 0
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_update(args: argparse.Namespace) -> int:
    """Handle 'update' command."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    try:
        task = store.update_metadata(
            task_number=args.number,
            due_date=args.due,
            note=args.note,
        )
        print(f"✅ Task {args.number} updated: {task.description}")
        if args.due:
            print(f"   Due date: {task.due_date}")
        if args.note:
            print(f"   Note: {task.note}")
        return 0
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_sort(args: argparse.Namespace) -> int:
    """Handle 'sort' command."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    try:
        tasks = store.sort_tasks(sort_by=args.by, reverse=args.reverse)
        if not tasks:
            print("No tasks found.")
        else:
            sort_name = {"alpha": "alphabetically", "recent": "by most recent", "due": "by due date"}
            print(f"Tasks sorted {sort_name.get(args.by, args.by)}:")
            for i, task in enumerate(tasks, 1):
                print(format_task(task, i))
        return 0
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_swap(args: argparse.Namespace) -> int:
    """Handle 'swap' command."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    try:
        tasks = store.swap_tasks(args.pos1, args.pos2)
        print(f"✅ Swapped tasks at positions {args.pos1} and {args.pos2}:")
        for i, task in enumerate(tasks, 1):
            print(format_task(task, i))
        return 0
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_summarize(args: argparse.Namespace) -> int:
    """Handle 'summarize' command - summarize a task description."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    try:
        tasks = store.get_all()
        if not tasks:
            print("No tasks found.")
            return 1

        if args.number < 1 or args.number > len(tasks):
            print(f"❌ Error: Task number must be between 1 and {len(tasks)}", file=sys.stderr)
            return 1

        task = tasks[args.number - 1]
        print(f"Original: {task.description}")
        print("🤖 Generating summary...")

        summary = summarize_task(task.description)
        print(f"Summary: {summary}")

        if "unavailable" not in summary.lower() and "api key" not in summary.lower():
            update = input("\nUpdate task with this summary? (y/n): ").strip().lower()
            if update == "y":
                task.description = summary
                store.save_tasks(tasks)
                print("✅ Task updated with summary")

        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_analyze_priority(args: argparse.Namespace) -> int:
    """Handle 'analyze-priority' command - suggest priority for a task."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    try:
        tasks = store.get_all()
        if not tasks:
            print("No tasks found.")
            return 1

        if args.number < 1 or args.number > len(tasks):
            print(f"❌ Error: Task number must be between 1 and {len(tasks)}", file=sys.stderr)
            return 1

        task = tasks[args.number - 1]
        print(f"Task: {task.description}")
        print("🤖 Analyzing priority...")

        priority_data = suggest_priority(task.description, task.due_date)
        priority = priority_data.get("priority", "medium")
        estimate = priority_data.get("estimate_hours", 1.0)
        reason = priority_data.get("reason", "")

        print(f"\n📊 Analysis Results:")
        print(f"   Priority: {priority.upper()}")
        print(f"   Estimated time: {estimate}h")
        print(f"   Reason: {reason}")

        if "error" not in reason.lower():
            update = input("\nApply this priority to the task? (y/n): ").strip().lower()
            if update == "y":
                task.priority = priority
                task.estimate_hours = estimate
                store.save_tasks(tasks)
                print("✅ Task priority updated")

        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_advice(args: argparse.Namespace) -> int:
    """Handle 'advice' command - get AI advice for completing a task."""
    storage_path = get_storage_path()
    store = TaskStore(storage_path=storage_path)

    try:
        tasks = store.get_all()
        if not tasks:
            print("No tasks found.")
            return 1

        if args.number < 1 or args.number > len(tasks):
            print(f"❌ Error: Task number must be between 1 and {len(tasks)}", file=sys.stderr)
            return 1

        task = tasks[args.number - 1]
        print(f"Task: {task.description}")
        print(f"Status: {task.status}")
        print("\n🤖 Getting advice...\n")

        advice = get_task_advice(
            description=task.description,
            status=task.status,
            due_date=task.due_date,
            note=task.note,
        )

        print("💡 Advice:")
        print(f"   {advice}")

        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="tasks",
        description="Task management system with persistent storage",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", help="Task description")
    parser_add.add_argument("--due", help="Due date (YYYY-MM-DD)")
    parser_add.add_argument("--note", help="Additional note")
    parser_add.add_argument(
        "--summarize",
        action="store_true",
        help="Use AI to summarize long descriptions",
    )
    parser_add.add_argument(
        "--auto-priority",
        action="store_true",
        help="Use AI to suggest priority and estimate",
    )
    parser_add.set_defaults(func=cmd_add)

    # List command
    parser_list = subparsers.add_parser("list", help="List all tasks")
    parser_list.set_defaults(func=cmd_list)

    # Search command
    parser_search = subparsers.add_parser("search", help="Search tasks by keyword")
    parser_search.add_argument("term", help="Search term")
    parser_search.set_defaults(func=cmd_search)

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("number", type=int, help="Task number to delete")
    parser_delete.set_defaults(func=cmd_delete)

    # Status command
    parser_status = subparsers.add_parser("status", help="Update task status")
    parser_status.add_argument("number", type=int, help="Task number")
    parser_status.add_argument(
        "status",
        choices=["not started", "started", "complete"],
        help="New status",
    )
    parser_status.set_defaults(func=cmd_status)

    # Update command
    parser_update = subparsers.add_parser("update", help="Update task metadata")
    parser_update.add_argument("number", type=int, help="Task number")
    parser_update.add_argument("--due", help="Update due date (YYYY-MM-DD)")
    parser_update.add_argument("--note", help="Update note")
    parser_update.set_defaults(func=cmd_update)

    # Sort command
    parser_sort = subparsers.add_parser("sort", help="Sort tasks")
    parser_sort.add_argument(
        "--by",
        choices=["alpha", "recent", "due"],
        default="alpha",
        help="Sort by field (default: alpha)",
    )
    parser_sort.add_argument(
        "--reverse",
        action="store_true",
        help="Reverse sort order",
    )
    parser_sort.set_defaults(func=cmd_sort)

    # Swap command
    parser_swap = subparsers.add_parser("swap", help="Swap two tasks")
    parser_swap.add_argument("pos1", type=int, help="First task position")
    parser_swap.add_argument("pos2", type=int, help="Second task position")
    parser_swap.set_defaults(func=cmd_swap)

    # AI: Summarize command
    parser_summarize = subparsers.add_parser(
        "summarize",
        help="Use AI to summarize a task description",
    )
    parser_summarize.add_argument("number", type=int, help="Task number to summarize")
    parser_summarize.set_defaults(func=cmd_summarize)

    # AI: Analyze priority command
    parser_priority = subparsers.add_parser(
        "analyze-priority",
        help="Use AI to analyze and suggest task priority",
    )
    parser_priority.add_argument("number", type=int, help="Task number to analyze")
    parser_priority.set_defaults(func=cmd_analyze_priority)

    # AI: Advice command
    parser_advice = subparsers.add_parser(
        "advice",
        help="Get AI-powered advice for completing a task",
    )
    parser_advice.add_argument("number", type=int, help="Task number to get advice for")
    parser_advice.set_defaults(func=cmd_advice)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 2

    if not hasattr(args, "func"):
        parser.print_help()
        return 2

    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
