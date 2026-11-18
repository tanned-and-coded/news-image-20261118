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
import sys
import tempfile
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_IMAGE_BYTES = 1024 * 1024  # the gate accepts at most 1 MiB


def load_entry_image(source: Path) -> bytes:
    """Read the shipped image, checking that it is a PNG within limits."""
    if not source.is_file():
        raise SystemExit(f"error: entry image not found: {source}")
    data = source.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit(f"error: {source.name} is not a PNG image")
    if len(data) > MAX_IMAGE_BYTES:
        raise SystemExit(
            f"error: {source.name} is {len(data)} bytes, over the 1 MiB limit"
        )
    return data


def write_atomically(destination: Path, data: bytes) -> None:
    """Write via a temp file in the same directory, then rename over the
    destination, so a reader never sees a half-written entry.png and an
    interrupted run leaves any previous output untouched."""
    fd, tmp_name = tempfile.mkstemp(
        dir=destination.parent, prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(data)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_name, destination)
        # mkstemp creates the temp file with mode 0600; relax the finished
        # output to the usual 0644 so a later process running as a
        # different user can still read entry.png.
        os.chmod(destination, 0o644)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    data = load_entry_image(source)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    write_atomically(destination, data)
    written = destination.stat().st_size
    if written != len(data):
        raise SystemExit(
            f"error: wrote {written} bytes to {destination}, expected {len(data)}"
        )
    print(f"wrote {destination} ({written} bytes)", file=sys.stdout)


if __name__ == "__main__":
    main()
