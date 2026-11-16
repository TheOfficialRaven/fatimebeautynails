# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMGS = ROOT / "assets" / "imgs"
IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".heic"}

text_blobs: list[str] = []
for pattern in ("*.html", "*.css", "*.js", "*.json"):
    for p in ROOT.rglob(pattern):
        if any(part.startswith(".") for part in p.parts):
            continue
        if p.name.startswith("_"):
            continue
        try:
            text_blobs.append(p.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            pass

blob = "\n".join(text_blobs).replace("\\", "/")

used_rels: set[str] = set()
for m in re.finditer(
    r"assets/imgs/([A-Za-z0-9_./\-]+\.(?:png|jpe?g|webp|gif|svg|heic))",
    blob,
    re.I,
):
    used_rels.add(m.group(1).replace("\\", "/").lower())

for m in re.finditer(r"url\((['\"]?)([^)'\"]+)\1\)", blob, re.I):
    u = m.group(2).replace("\\", "/")
    if "imgs/" in u.lower():
        idx = u.lower().find("imgs/")
        used_rels.add(u[idx + 5 :].lower())

# Prefer path-based matching only (avoid basename false positives for deletion)
unused: list[Path] = []
for p in IMGS.rglob("*"):
    if not p.is_file():
        continue
    if p.suffix.lower() not in IMG_EXTS:
        continue
    rel = p.relative_to(IMGS).as_posix().lower()
    if rel not in used_rels:
        unused.append(p)

freed = 0
deleted = 0
errors = 0
for p in sorted(unused, key=lambda x: x.as_posix().lower()):
    try:
        size = p.stat().st_size
        rel = p.relative_to(IMGS).as_posix()
        p.unlink()
        freed += size
        deleted += 1
        print("deleted", rel)
    except OSError as e:
        errors += 1
        print("FAIL", p, e)

print(f"DONE deleted={deleted} errors={errors} freed_MB={freed/1024/1024:.1f}")
