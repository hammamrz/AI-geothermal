#!/usr/bin/env python3
"""Bangun dua ZIP untuk claude.ai, keduanya berisi skill pemuat yang sama:

- AIGeothermal-PLN.zip         skill  -> Customize → Skills → + → Upload a skill (akun Free)
- AIGeothermal-PLN-plugin.zip  plugin -> Customize → Plugins → Add → Upload plugin (Pro/Max)

Plugin dibuat "tipis" seperti skill: modul dan KB diambil dari GitHub saat dipakai, jadi plugin
tidak perlu diunggah ulang ketika KB atau modul berubah, dan tidak bergantung pada ukuran repo
(marketplace claude.ai menolak repo besar).

Isi skill pemuat:
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
PLUGIN_JSON = ROOT / "plugins" / "aigeothermal-pln" / ".claude-plugin" / "plugin.json"
KB_FILES = ("geothermal-knowledge", "references", "KB", "files")
SKIP = {"__pycache__", ".DS_Store", ".gitkeep"}
ARC = "aigeothermal-pln"


def skip(rel: Path) -> bool:
    return bool(SKIP & set(rel.parts)) or rel.suffix == ".pyc"


def write_skill(z: zipfile.ZipFile, prefix: str, config: dict) -> None:
    for f in sorted(STANDALONE.rglob("*")):
        rel = f.relative_to(STANDALONE)
        if f.is_file() and not skip(rel) and rel.as_posix() != "config.json":
            z.write(f, f"{prefix}{rel.as_posix()}")
    z.writestr(f"{prefix}config.json", json.dumps(config, indent=2) + "\n")
    for f in sorted(SKILLS.rglob("*")):
        rel = f.relative_to(SKILLS)
        if f.is_file() and not skip(rel) and rel.parts[: len(KB_FILES)] != KB_FILES:
            # Hanya boleh ada satu SKILL.md per skill di claude.ai; sync.py memetakannya kembali.
            arc_rel = rel.with_name("MODULE.md") if rel.name == "SKILL.md" else rel
            z.write(f, f"{prefix}modules/{arc_rel.as_posix()}")


def check_single_skill(zpath: Path, expected: str) -> None:
    with zipfile.ZipFile(zpath) as z:
        skill_md = [n for n in z.namelist() if n.rsplit("/", 1)[-1].lower() == "skill.md"]
    if skill_md != [expected]:
        raise SystemExit(f"{zpath.name} harus berisi tepat satu SKILL.md ({expected}), ditemukan: {skill_md}")


def report(zpath: Path, config: dict) -> None:
    print(f"{zpath}\t{zpath.stat().st_size / 1024 / 1024:.2f} MiB" + ("\t(berisi token baca)" if config.get("token") else ""))


def build(out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    config = json.loads((STANDALONE / "config.json").read_text(encoding="utf-8"))
    if os.environ.get("AIGEO_READ_TOKEN"):
        config["token"] = os.environ["AIGEO_READ_TOKEN"]

    skill_zip = out / "AIGeothermal-PLN.zip"
    with zipfile.ZipFile(skill_zip, "w", zipfile.ZIP_DEFLATED) as z:
        write_skill(z, f"{ARC}/", config)
    check_single_skill(skill_zip, f"{ARC}/SKILL.md")
    report(skill_zip, config)

    manifest = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    plugin = {
        "name": manifest["name"],
        "displayName": manifest.get("displayName", "AIGeothermal-PLN"),
        "version": manifest.get("version", "1.0.0"),
        "description": "Asisten technical review geothermal PLN IP: tanya KB, review dokumen subsurface/drilling/well, "
                       "comment sheet DOCX, dan presentasi PPTX. Modul dan KB terbaru diambil dari GitHub saat dipakai.",
        "author": manifest.get("author", {"name": "Generation Business Development"}),
        "repository": manifest.get("repository", ""),
        "keywords": manifest.get("keywords", []),
    }
    plugin_zip = out / "AIGeothermal-PLN-plugin.zip"
    with zipfile.ZipFile(plugin_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{ARC}/.claude-plugin/plugin.json", json.dumps(plugin, ensure_ascii=False, indent=2) + "\n")
        write_skill(z, f"{ARC}/skills/{ARC}/", config)
    check_single_skill(plugin_zip, f"{ARC}/skills/{ARC}/SKILL.md")
    report(plugin_zip, config)
    return [skill_zip, plugin_zip]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    build(ap.parse_args().out)
