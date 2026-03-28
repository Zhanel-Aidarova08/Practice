# create_list_dirs.py
# Demonstrates: mkdir, makedirs, listdir, getcwd, chdir, rmdir, pathlib

import os
import shutil
from pathlib import Path

# ── 1. Current working directory ────────────────────────────────────────────
print("CWD:", os.getcwd())

# ── 2. Create a single directory ────────────────────────────────────────────
single_dir = Path("test_dir")
single_dir.mkdir(exist_ok=True)
print(f"[MKDIR] Created '{single_dir}'")

# ── 3. Create nested directories in one call ────────────────────────────────
nested = Path("project/src/utils")
nested.mkdir(parents=True, exist_ok=True)          # os.makedirs equivalent
print(f"[MAKEDIRS] Created nested path '{nested}'")

# Create some sample files for listing
(nested / "helper.py").write_text("# helper\n")
(nested.parent / "main.py").write_text("# main\n")
(nested.parent.parent / "README.md").write_text("# Project\n")

# ── 4. List directory contents ───────────────────────────────────────────────
print("\n[LISTDIR] Contents of 'project/':")
for item in os.listdir("project"):
    print(" ", item)

# ── 5. Recursive listing with pathlib ────────────────────────────────────────
print("\n[RGLOB] All files under 'project/':")
for path in Path("project").rglob("*"):
    print(" ", path)

# ── 6. Find files by extension ───────────────────────────────────────────────
print("\n[FIND .py] Python files under 'project/':")
for py_file in Path("project").rglob("*.py"):
    print(" ", py_file)

# ── 7. Change directory and back ─────────────────────────────────────────────
original = os.getcwd()
os.chdir(single_dir)
print(f"\n[CHDIR] Moved into: {os.getcwd()}")
os.chdir(original)
print(f"[CHDIR] Back to:    {os.getcwd()}")

# ── 8. Remove directories (cleanup) ─────────────────────────────────────────
single_dir.rmdir()                      # only works on empty dir
shutil.rmtree("project")               # removes non-empty tree
print("\n[CLEANUP] Removed 'test_dir' and 'project/'")
