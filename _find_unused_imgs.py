# -*- coding: utf-8 -*-
"""List image files under assets/imgs that are not referenced by the site."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".heic", ".JPG", ".JPEG", ".PNG", ".WEBP", ".GIF", ".SVG", ".HEIC"}

# Collect all text that might reference assets
text_blobs: list[str] = []
for pattern in ("*.html", "*.css", "*.js", "*.json", "*.md"):
    for p in ROOT.rglob(pattern):
        if any(part.startswith(".") for part in p.parts):
            continue
        if "sogra-export" in str(p):
            continue
        if p.name.startswith("_"):
            continue
        try:
            text_blobs.append(p.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            pass

blob = "\n".join(text_blobs).replace("\\", "/")

# Also catch basename-only references
used_names: set[str] = set()
used_rels: set[str] = set()

# paths like assets/imgs/...
for m in re.finditer(r"assets/imgs/([A-Za-z0-9_./\-]+\.(?:png|jpe?g|webp|gif|svg|heic))", blob, re.I):
    rel = m.group(1).replace("\\", "/")
    used_rels.add(rel)
    used_names.add(Path(rel).name.lower())

# url(...) in css without assets/imgs prefix sometimes
for m in re.finditer(r"url\((['\"]?)([^)'\"]+)\1\)", blob, re.I):
    u = m.group(2).replace("\\", "/")
    if "imgs/" in u:
        idx = u.lower().find("imgs/")
        rel = u[idx + 5 :]
        used_rels.add(rel)
        used_names.add(Path(rel).name.lower())

all_files: list[Path] = []
for p in IMGS.rglob("*"):
    if p.is_file() and p.suffix in IMG_EXTS or p.suffix.lower() in {e.lower() for e in IMG_EXTS}:
        all_files.append(p)

unused: list[Path] = []
used: list[Path] = []
for p in all_files:
    rel = p.relative_to(IMGS).as_posix()
    name = p.name.lower()
    # referenced by relative path or by filename
    if rel in used_rels or rel.lower() in {r.lower() for r in used_rels} or name in used_names:
        used.append(p)
    else:
        unused.append(p)

print(f"total={len(all_files)} used={len(used)} unused={len(unused)}")
print("--- UNUSED ---")
for p in sorted(unused, key=lambda x: x.stat().st_size, reverse=True):
    print(f"{p.stat().st_size/1024:8.1f} KB  {p.relative_to(IMGS).as_posix()}")
