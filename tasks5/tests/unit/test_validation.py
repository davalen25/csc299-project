"""Unit tests for Name validation."""

import pytest

from names.validation import Name


class TestNameValidation:
    """Test Name value object validation rules."""

    def test_valid_name(self) -> None:
        """Test creating a valid name."""
        name = Name(value="Alice")
        assert name.value == "Alice"

    def test_empty_string_raises(self) -> None:
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Name(value="")

    def test_whitespace_only_raises(self) -> None:
        """Test that whitespace-only string raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Name(value="   ")

    def test_tab_only_raises(self) -> None:
        """Test that tab-only string raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Name(value="\t")

    def test_newline_only_raises(self) -> None:
        """Test that newline-only string raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Name(value="\n")

    def test_mixed_whitespace_only_raises(self) -> None:
        """Test that mixed whitespace raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Name(value="  \t\n  ")

    def test_too_long_raises(self) -> None:
        """Test that names >256 chars raise ValueError."""
        long_name = "A" * 257
        with pytest.raises(ValueError, match="Name too long"):
            Name(value=long_name)

    def test_exactly_256_chars_ok(self) -> None:
        """Test that exactly 256 chars is acceptable."""
        name = Name(value="A" * 256)
        assert len(name.value) == 256

    def test_leading_whitespace_trimmed(self) -> None:
        """Test that leading whitespace is trimmed."""
        name = Name(value="  Alice")
        assert name.value == "Alice"

    def test_trailing_whitespace_trimmed(self) -> None:
        """Test that trailing whitespace is trimmed."""
        name = Name(value="Alice  ")
        assert name.value == "Alice"

    def test_both_sides_whitespace_trimmed(self) -> None:
        """Test that whitespace on both sides is trimmed."""
        name = Name(value="  Bob  ")
        assert name.value == "Bob"

    def test_internal_whitespace_preserved(self) -> None:
        """Test that internal spaces are preserved."""
        name = Name(value="Mary Ann")
        assert name.value == "Mary Ann"

    def test_internal_whitespace_with_trim(self) -> None:
        """Test internal spaces preserved while ends trimmed."""
        name = Name(value="  Mary Ann  ")
        assert name.value == "Mary Ann"

    def test_name_is_immutable(self) -> None:
        """Test that Name is frozen and cannot be modified."""
        name = Name(value="Alice")
        with pytest.raises(AttributeError):
            name.value = "Bob"  # type: ignore[misc]
