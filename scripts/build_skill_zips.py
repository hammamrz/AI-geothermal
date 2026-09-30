#!/usr/bin/env python3
"""Bangun ZIP untuk upload manual ke Claude:

- geothermal-review-plugin.zip : plugin utuh (4 skill) untuk Organization settings →
  Plugins & skills → upload plugin.
- <skill>.zip                  : per-skill untuk Settings → Capabilities → Skills.

Jalur utama distribusi tetap sinkronisasi plugin dari GitHub; ZIP ini hanya cadangan
dan tidak ter-update otomatis.

Pemakaian: python scripts/build_skill_zips.py [--out dist]
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "geothermal-review"
SKILLS = PLUGIN / "skills"
# File lintas-skill yang dirujuk dengan path relatif ../ dan harus ikut dibundel
# bila skill diinstal sendiri-sendiri.
EXTRA = {
    "geothermal-review-presentation": [
        (SKILLS / "geothermal-comment-sheet-report" / "references" / "REPORT_STRUCTURE.md", "references/REPORT_STRUCTURE.md"),
    ],
}
SKIP = {"__pycache__", ".DS_Store", ".gitkeep"}


def skip(rel: Path) -> bool:
    return bool(SKIP & set(rel.parts)) or rel.suffix == ".pyc"


def report(zpath: Path) -> None:
    print(f"{zpath.name}\t{zpath.stat().st_size / 1024 / 1024:.2f} MiB")


def build(out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    plugin_zip = out / "geothermal-review-plugin.zip"
    with zipfile.ZipFile(plugin_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(PLUGIN.rglob("*")):
            if f.is_file() and not skip(f.relative_to(PLUGIN)):
                z.write(f, f"geothermal-review/{f.relative_to(PLUGIN).as_posix()}")
    report(plugin_zip)
    built = [plugin_zip]
    for skill in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()):
        zpath = out / f"{skill.name}.zip"
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(skill.rglob("*")):
                if f.is_file() and not skip(f.relative_to(skill)):
                    z.write(f, f"{skill.name}/{f.relative_to(skill).as_posix()}")
            for src, arc in EXTRA.get(skill.name, []):
                z.write(src, f"{skill.name}/{arc}")
        built.append(zpath)
        report(zpath)
    return built


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    build(ap.parse_args().out)
