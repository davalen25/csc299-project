"""Make names package executable with python -m names."""

import sys

from names.cli import main

if __name__ == "__main__":
    sys.exit(main())
