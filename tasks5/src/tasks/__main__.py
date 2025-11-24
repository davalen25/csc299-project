"""Allow running as python -m tasks."""

from __future__ import annotations

import sys

from tasks.cli import main

if __name__ == "__main__":
    sys.exit(main())
