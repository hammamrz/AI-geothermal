#!/usr/bin/env python3
"""Tulis sync-manifest.json: daftar file modul (skill) + hash, dibaca oleh sync.py
pada skill claude.ai untuk mengambil versi terbaru dari GitHub.

File KB mentah (references/KB/files/) tidak dicantumkan; sync.py mengunduhnya
sesuai kebutuhan berdasarkan KB_MANIFEST.json. Output deterministik agar commit
hanya terjadi bila isi berubah.

Pemakaian: python scripts/build_sync_manifest.py [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "aigeothermal-pln" / "skills"
OUT = ROOT / "sync-manifest.json"
KB_FILES = Path("geothermal-knowledge") / "references" / "KB" / "files"
SKIP_NAMES = {".gitkeep", ".DS_Store"}


def module_files() -> list[Path]:
    out = []
    for f in sorted(SKILLS.rglob("*")):
        rel = f.relative_to(SKILLS)
        if not f.is_file() or f.name in SKIP_NAMES or "__pycache__" in rel.parts or f.suffix == ".pyc":
            continue
        if rel.parts[: len(KB_FILES.parts)] == KB_FILES.parts:
            continue
        out.append(rel)
    return out


def build() -> str:
    kb = json.loads((SKILLS / "geothermal-knowledge/references/KB/KB_MANIFEST.json").read_text(encoding="utf-8"))
    files = []
    for rel in module_files():
        data = (SKILLS / rel).read_bytes()
        files.append({"path": rel.as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
    manifest = {
        "schema": 1,
        "base_path": SKILLS.relative_to(ROOT).as_posix(),
        "kb_revision": kb.get("kb_revision", 0),
        "kb_updated_at": kb.get("updated_at"),
        "files": files,
    }
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="gagal bila sync-manifest.json belum sesuai")
    args = ap.parse_args()
    text = build()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("sync-manifest.json tidak sesuai; jalankan: python scripts/build_sync_manifest.py", file=sys.stderr)
            sys.exit(1)
        print("sync-manifest.json sesuai")
    else:
        OUT.write_text(text, encoding="utf-8")
        print(f"Tertulis {OUT.name}: {len(json.loads(text)['files'])} file modul")
