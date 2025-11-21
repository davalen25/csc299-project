"""CLI interface for name storage application."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from names.storage import NameStore


def get_storage_path() -> Path:
    """Get storage path from environment or use default."""
    env_path = os.getenv("NAMES_STORAGE_PATH")
    if env_path:
        return Path(env_path)
    return Path.home() / ".local" / "share" / "names" / "names.json"


def cmd_add(args: argparse.Namespace) -> int:
    """Handle 'add' command.

    Args:
        args: Parsed command arguments with 'name' attribute

    Returns:
        Exit code (0=success, 1=validation error)
    """
    storage_path = get_storage_path()
    store = NameStore(storage_path=storage_path)

    try:
        name = store.add(args.name)
        print(f"✅ Added: {name.value}")
        return 0
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_list(args: argparse.Namespace) -> int:
    """Handle 'list' command.

    Args:
        args: Parsed command arguments (unused)

    Returns:
        Exit code (always 0)
    """
    storage_path = get_storage_path()
    store = NameStore(storage_path=storage_path)

    names = store.get_all()
    if not names:
        print("No names found.")
    else:
        for name in names:
            print(name.value)

    return 0


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code (0=success, 1=validation error, 2=usage error)
    """
    parser = argparse.ArgumentParser(
        prog="names",
        description="Store and list names",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a name to storage")
    parser_add.add_argument("name", help="Name to add")
    parser_add.set_defaults(func=cmd_add)

    # List command
    parser_list = subparsers.add_parser("list", help="List all names alphabetically")
    parser_list.set_defaults(func=cmd_list)

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
