"""Contract tests for CLI commands.

These tests verify the CLI adheres to the contracts specified in:
- specs/001-name-storage-cli/contracts/add.md
- specs/001-name-storage-cli/contracts/list.md
- specs/001-name-storage-cli/contracts/error-handling.md
"""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def clean_storage(tmp_path: Path) -> Path:
    """Provide clean temporary storage location."""
    storage_file = tmp_path / "names.json"
    return storage_file


@pytest.fixture
def cli_env(clean_storage: Path, monkeypatch):
    """Set up environment for CLI testing."""
    monkeypatch.setenv("NAMES_STORAGE_PATH", str(clean_storage))
    return clean_storage


class TestAddCommandContract:
    """Contract tests for 'names add' command."""

    def test_add_success_exit_code(self, cli_env: Path) -> None:
        """Contract: add command returns exit code 0 on success."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "add", "Alice"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 0, f"Expected exit 0, got {result.returncode}"

    def test_add_success_message_format(self, cli_env: Path) -> None:
        """Contract: add command outputs '✅ Added: {name}' on success."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "add", "Alice"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert "✅ Added: Alice" in result.stdout

    def test_add_persists_to_storage(self, cli_env: Path) -> None:
        """Contract: add command persists name to storage file."""
        subprocess.run(
            [sys.executable, "-m", "names.cli", "add", "Alice"],
            capture_output=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert cli_env.exists()
        content = cli_env.read_text()
        assert "Alice" in content

    def test_add_empty_name_error(self, cli_env: Path) -> None:
        """Contract: add command with empty name returns exit code 1."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "add", ""],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 1
        assert "❌ Error:" in result.stderr
        assert "empty" in result.stderr.lower()

    def test_add_whitespace_only_error(self, cli_env: Path) -> None:
        """Contract: add command with whitespace-only name returns exit code 1."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "add", "   "],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 1
        assert "❌ Error:" in result.stderr
        assert "empty" in result.stderr.lower()

    def test_add_too_long_error(self, cli_env: Path) -> None:
        """Contract: add command with too-long name returns exit code 1."""
        long_name = "A" * 257
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "add", long_name],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 1
        assert "❌ Error:" in result.stderr
        assert "too long" in result.stderr.lower()

    def test_add_trims_whitespace(self, cli_env: Path) -> None:
        """Contract: add command trims leading/trailing whitespace."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "add", "  Alice  "],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 0
        assert "✅ Added: Alice" in result.stdout
        content = cli_env.read_text()
        assert '"Alice"' in content
        assert '"  Alice  "' not in content

    def test_add_duplicate_allowed(self, cli_env: Path) -> None:
        """Contract: add command allows duplicate names."""
        subprocess.run(
            [sys.executable, "-m", "names.cli", "add", "Alice"],
            capture_output=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "add", "Alice"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 0
        assert "✅ Added: Alice" in result.stdout


class TestListCommandContract:
    """Contract tests for 'names list' command."""

    def test_list_empty_storage(self, cli_env: Path) -> None:
        """Contract: list command shows 'No names found.' for empty storage."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "list"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 0
        assert "No names found." in result.stdout

    def test_list_single_name(self, cli_env: Path) -> None:
        """Contract: list command displays single name."""
        subprocess.run(
            [sys.executable, "-m", "names.cli", "add", "Alice"],
            capture_output=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "list"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 0
        assert "Alice" in result.stdout

    def test_list_alphabetical_order(self, cli_env: Path) -> None:
        """Contract: list command displays names in alphabetical order."""
        for name in ["Zoe", "Alice", "Bob"]:
            subprocess.run(
                [sys.executable, "-m", "names.cli", "add", name],
                capture_output=True,
                env={"NAMES_STORAGE_PATH": str(cli_env)},
            )
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "list"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        output = result.stdout
        alice_pos = output.find("Alice")
        bob_pos = output.find("Bob")
        zoe_pos = output.find("Zoe")
        assert alice_pos < bob_pos < zoe_pos, f"Names not in alphabetical order: {output}"

    def test_list_case_insensitive_sort(self, cli_env: Path) -> None:
        """Contract: list command sorts case-insensitively."""
        for name in ["bob", "Alice", "CAROL"]:
            subprocess.run(
                [sys.executable, "-m", "names.cli", "add", name],
                capture_output=True,
                env={"NAMES_STORAGE_PATH": str(cli_env)},
            )
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "list"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        output = result.stdout
        alice_pos = output.find("Alice")
        bob_pos = output.find("bob")
        carol_pos = output.find("CAROL")
        assert alice_pos < bob_pos < carol_pos, f"Case-insensitive sort failed: {output}"


class TestErrorHandlingContract:
    """Contract tests for error handling."""

    def test_missing_command(self, cli_env: Path) -> None:
        """Contract: missing command returns exit code 2 (usage error)."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 2

    def test_unknown_command(self, cli_env: Path) -> None:
        """Contract: unknown command returns exit code 2 (usage error)."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "invalid"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 2

    def test_add_missing_name_argument(self, cli_env: Path) -> None:
        """Contract: add without name argument returns exit code 2."""
        result = subprocess.run(
            [sys.executable, "-m", "names.cli", "add"],
            capture_output=True,
            text=True,
            env={"NAMES_STORAGE_PATH": str(cli_env)},
        )
        assert result.returncode == 2
