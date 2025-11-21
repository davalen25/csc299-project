"""Make cli module executable with python -m names.cli."""

import sys

from . import main

if __name__ == "__main__":
    sys.exit(main())
