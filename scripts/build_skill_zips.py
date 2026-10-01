#!/usr/bin/env python3
"""Bangun AIGeothermal-PLN.zip: satu skill untuk di-upload di claude.ai
(Customize → Skills → + → Upload a skill), termasuk akun Free/Pro/Max.

Isi ZIP:
  aigeothermal-pln/SKILL.md          router + langkah sinkronisasi
  aigeothermal-pln/config.json       repo/branch sumber (+ token opsional)
  aigeothermal-pln/scripts/sync.py   ambil modul & KB terbaru dari GitHub
  aigeothermal-pln/modules/...       salinan bawaan 4 modul (dipakai bila offline);
                                     file KB mentah tidak dibundel, diunduh saat dibutuhkan

Token baca opsional (hanya bila repo privat): set env AIGEO_READ_TOKEN saat build.
Token itu ikut terbawa ke setiap akun yang menerima ZIP, jadi pakai fine-grained
token read-only yang dibatasi ke repo ini saja.

Pemakaian: python scripts/build_skill_zips.py [--out dist]
"""
from __future__ import annotations

import argparse
import json
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDALONE = ROOT / "standalone" / "aigeothermal-pln"
SKILLS = ROOT / "plugins" / "aigeothermal-pln" / "skills"
KB_FILES = ("geothermal-knowledge", "references", "KB", "files")
SKIP = {"__pycache__", ".DS_Store", ".gitkeep"}
ARC = "aigeothermal-pln"


def skip(rel: Path) -> bool:
    return bool(SKIP & set(rel.parts)) or rel.suffix == ".pyc"


def build(out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    zpath = out / "AIGeothermal-PLN.zip"
    config = json.loads((STANDALONE / "config.json").read_text(encoding="utf-8"))
    if os.environ.get("AIGEO_READ_TOKEN"):
        config["token"] = os.environ["AIGEO_READ_TOKEN"]
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(STANDALONE.rglob("*")):
            rel = f.relative_to(STANDALONE)
            if f.is_file() and not skip(rel) and rel.as_posix() != "config.json":
                z.write(f, f"{ARC}/{rel.as_posix()}")
        z.writestr(f"{ARC}/config.json", json.dumps(config, indent=2) + "\n")
        for f in sorted(SKILLS.rglob("*")):
            rel = f.relative_to(SKILLS)
            if f.is_file() and not skip(rel) and rel.parts[: len(KB_FILES)] != KB_FILES:
                # Hanya boleh ada satu SKILL.md di ZIP skill claude.ai; sync.py memetakannya kembali.
                arc_rel = rel.with_name("MODULE.md") if rel.name == "SKILL.md" else rel
                z.write(f, f"{ARC}/modules/{arc_rel.as_posix()}")
    with zipfile.ZipFile(zpath) as z:
        skill_md = [n for n in z.namelist() if n.rsplit("/", 1)[-1].lower() == "skill.md"]
    if skill_md != [f"{ARC}/SKILL.md"]:
        raise SystemExit(f"ZIP harus berisi tepat satu SKILL.md, ditemukan: {skill_md}")
    print(f"{zpath}\t{zpath.stat().st_size / 1024 / 1024:.2f} MiB" + ("\t(berisi token baca)" if config.get("token") else ""))
    return zpath


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    build(ap.parse_args().out)
