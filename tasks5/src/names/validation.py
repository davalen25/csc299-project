"""Input validation for names."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Name:
    """A validated, normalized person name.

    Attributes:
        value: The normalized name (trimmed, non-empty, ≤256 chars)

    Raises:
        ValueError: If name is empty, whitespace-only, or too long
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the name after initialization."""
        if not self.value or not self.value.strip():
            raise ValueError("Name cannot be empty")
        if len(self.value) > 256:
            raise ValueError("Name too long")
        # Ensure stored value is trimmed
        object.__setattr__(self, "value", self.value.strip())
