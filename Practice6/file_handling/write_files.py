# write_files.py
# Demonstrates: creating files, writing, appending

from pathlib import Path

# ── 1. Create a new file and write sample data ──────────────────────────────
data_path = Path("sample_data.txt")

with open(data_path, "w", encoding="utf-8") as f:
    f.write("Line 1: Hello, World!\n")
    f.write("Line 2: Python file handling\n")
    f.write("Line 3: Practice 6\n")

print(f"[WRITE] Created '{data_path}' and wrote 3 lines.")

# ── 2. Append new lines ──────────────────────────────────────────────────────
with open(data_path, "a", encoding="utf-8") as f:
    f.write("Line 4: Appended line #1\n")
    f.write("Line 5: Appended line #2\n")

print(f"[APPEND] Added 2 more lines to '{data_path}'.")

# ── 3. Verify full content ───────────────────────────────────────────────────
print("\n[VERIFY] Current file contents:")
with open(data_path, "r", encoding="utf-8") as f:
    print(f.read())

# ── 4. Exclusive creation (mode 'x') ────────────────────────────────────────
new_path = Path("exclusive_file.txt")
if new_path.exists():
    new_path.unlink()                          # remove if leftover from prev run

with open(new_path, "x", encoding="utf-8") as f:
    f.write("Created with mode 'x' — fails if file already exists.\n")

print(f"[CREATE-X] '{new_path}' created with exclusive mode.")
