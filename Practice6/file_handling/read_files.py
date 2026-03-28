# read_files.py
# Demonstrates: read(), readline(), readlines(), context manager

from pathlib import Path

sample = Path("sample_data.txt")

# Ensure the file exists (run write_files.py first, or create it here)
if not sample.exists():
    sample.write_text(
        "Line 1: Hello, World!\n"
        "Line 2: Python file handling\n"
        "Line 3: Practice 6\n",
        encoding="utf-8",
    )

# ── 1. read() — entire file as one string ───────────────────────────────────
print("=== read() ===")
with open(sample, "r", encoding="utf-8") as f:
    content = f.read()
print(content)

# ── 2. readline() — one line at a time ──────────────────────────────────────
print("=== readline() ===")
with open(sample, "r", encoding="utf-8") as f:
    line = f.readline()
    while line:
        print(repr(line))
        line = f.readline()

# ── 3. readlines() — list of all lines ──────────────────────────────────────
print("\n=== readlines() ===")
with open(sample, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines, start=1):
    print(f"  [{i}] {line.rstrip()}")

# ── 4. Iterating line by line (memory-efficient) ─────────────────────────────
print("\n=== Iterating line by line ===")
with open(sample, "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
