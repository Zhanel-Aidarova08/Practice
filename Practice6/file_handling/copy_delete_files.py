# copy_delete_files.py
# Demonstrates: shutil.copy, shutil.copy2, shutil.move, safe delete

import shutil
from pathlib import Path

src = Path("sample_data.txt")

# Ensure source exists
if not src.exists():
    src.write_text(
        "Line 1: Hello, World!\nLine 2: Python file handling\nLine 3: Practice 6\n",
        encoding="utf-8",
    )

# ── 1. Copy file (preserves content only) ───────────────────────────────────
copy1 = Path("sample_copy.txt")
shutil.copy(src, copy1)
print(f"[COPY] '{src}' → '{copy1}'")

# ── 2. Copy file with metadata (timestamps, permissions) ────────────────────
copy2 = Path("sample_backup.txt")
shutil.copy2(src, copy2)
print(f"[COPY2] '{src}' → '{copy2}' (metadata preserved)")

# ── 3. Backup into a subdirectory ───────────────────────────────────────────
backup_dir = Path("backup")
backup_dir.mkdir(exist_ok=True)
shutil.copy2(src, backup_dir / src.name)
print(f"[BACKUP] Copied to '{backup_dir / src.name}'")

# ── 4. Move / rename a file ──────────────────────────────────────────────────
moved = Path("moved_copy.txt")
shutil.move(str(copy1), str(moved))
print(f"[MOVE] '{copy1}' → '{moved}'")

# ── 5. Safe delete (check existence first) ───────────────────────────────────
for target in [moved, copy2]:
    if target.exists():
        target.unlink()
        print(f"[DELETE] Removed '{target}'")
    else:
        print(f"[SKIP] '{target}' not found")

print("\nDone. Backup still exists at:", backup_dir / src.name)
