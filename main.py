"""News-image entry for 18 November 2026.

The entry image ships beside this file as ``entry.png``. Running this
program copies those bytes, unchanged, to ``entry.png`` inside the
output directory:

- ``$MAKEFUN_OUTPUT_DIR/entry.png`` when the environment variable is set
- ``/output/entry.png`` otherwise

The output directory is created when needed. The program uses only the
Python standard library, touches no network, and produces a
byte-identical output on every run.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
