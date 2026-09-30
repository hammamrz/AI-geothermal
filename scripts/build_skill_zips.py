#!/usr/bin/env python3
"""Bangun ZIP per-skill untuk upload manual ke Claude (Settings → Capabilities → Skills,
atau Organization settings → Plugins & skills → Upload a skill).

Jalur utama distribusi tetap sinkronisasi plugin dari GitHub; ZIP ini hanya untuk akun
yang tidak bisa memakai sinkronisasi (mis. paket individual). ZIP tidak ter-update otomatis.

Pemakaian: python scripts/build_skill_zips.py [--out dist]
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "geothermal-review" / "skills"
# File lintas-skill yang dirujuk dengan path relatif ../ dan harus ikut dibundel
# bila skill diinstal sendiri-sendiri.
EXTRA = {
    "geothermal-review-presentation": [
        (SKILLS / "geothermal-comment-sheet-report" / "references" / "REPORT_STRUCTURE.md", "references/REPORT_STRUCTURE.md"),
    ],
}
SKIP = {"__pycache__", ".DS_Store", ".gitkeep"}


def build(out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    built = []
    for skill in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()):
        zpath = out / f"{skill.name}.zip"
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(skill.rglob("*")):
                if f.is_file() and not (SKIP & set(f.relative_to(skill).parts)) and f.suffix != ".pyc":
                    z.write(f, f"{skill.name}/{f.relative_to(skill).as_posix()}")
            for src, arc in EXTRA.get(skill.name, []):
                z.write(src, f"{skill.name}/{arc}")
        built.append(zpath)
        print(f"{zpath.relative_to(ROOT) if zpath.is_relative_to(ROOT) else zpath}\t{zpath.stat().st_size / 1024 / 1024:.2f} MiB")
    return built


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    build(ap.parse_args().out)
