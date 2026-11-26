#!/usr/bin/env python3
"""Make.fun entry: what the elevator would say (one-liner).

Writes the entry byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.txt:
one line, 57 characters, no trailing newline.
"""

import os
import sys

ENTRY = "Weight limit reached. The buffet was your idea, not mine."


def main() -> int:
    for ch in ENTRY:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            print(f"entry REJECTED: control character U+{ord(ch):04X} "
                  f"not allowed", file=sys.stderr)
            return 1
    out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    expected_size = len(ENTRY.encode("utf-8"))
    actual_size = os.path.getsize(path)
    if actual_size != expected_size:
        print(f"entry FAILED: on-disk size {actual_size} != "
              f"expected {expected_size}", file=sys.stderr)
        return 1
    return 0


def verify() -> int:
    """Read entry.txt back from disk and check bytes, length, newline."""
    out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "rb") as f:
        data = f.read()
    expected = ENTRY.encode("utf-8")
    if data != expected:
        print(f"verify FAILED: bytes differ: {data!r} != {expected!r}",
              file=sys.stderr)
        return 1
    if not (1 <= len(data) <= 120):
        print(f"verify FAILED: length {len(data)} outside 1-120",
              file=sys.stderr)
        return 1
    if data.endswith(b"\n"):
        print("verify FAILED: trailing newline present", file=sys.stderr)
        return 1
    print(f"verify OK: {len(data)} bytes, no trailing newline")
    return 0


if __name__ == "__main__":
    rc = main()
    if rc != 0:
        sys.exit(rc)
    sys.exit(verify())
