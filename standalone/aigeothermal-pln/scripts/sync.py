#!/usr/bin/env python3
"""Sinkronkan skill AIGeothermal-PLN dengan versi terbaru di GitHub.

Skill yang di-upload ke akun Claude hanya berisi salinan bawaan (snapshot). Skrip ini
mengambil instruksi modul dan index KB terbaru dari repo GitHub ke folder kerja,
sehingga perubahan admin sampai ke semua akun tanpa upload ulang ZIP.

Subcommand:
  update             sinkronkan modul + index KB ke folder kerja (jalankan sekali per percakapan)
  kb-get ID [ID..]   unduh file KB (GEO-xxxx) ke folder kerja, verifikasi SHA-256
  kb-search KATA..   cari metadata KB (delegasi ke kb_manager.py search)
  where              cetak lokasi folder kerja dan status sinkronisasi terakhir

Bila GitHub tidak dapat dijangkau, skrip memakai salinan bawaan dan melaporkannya.
Hanya pustaka standar Python.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
BUNDLED = SKILL_DIR / "modules"
CONFIG = json.loads((SKILL_DIR / "config.json").read_text(encoding="utf-8"))
REPO = os.environ.get("AIGEO_REPO", CONFIG["repo"])
BRANCH = os.environ.get("AIGEO_BRANCH", CONFIG.get("branch", "main"))
TOKEN = os.environ.get("AIGEO_TOKEN") or CONFIG.get("token") or None
WORK = Path(os.environ.get("AIGEO_WORKDIR", Path(tempfile.gettempdir()) / "aigeothermal-pln"))
MODULES = WORK / "modules"
STATE = WORK / "STATE.json"
KB_REL = Path("geothermal-knowledge") / "references" / "KB"
TIMEOUT = 30


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def http_get(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": "aigeothermal-pln-sync"}
    if accept:
        headers["Accept"] = accept
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def resolve_ref() -> str:
    """Pakai SHA commit terbaru agar snapshot konsisten (tidak terkena cache CDN).
    Bila API GitHub tidak tersedia/limit, jatuh ke nama branch."""
    try:
        sha = http_get(f"https://api.github.com/repos/{REPO}/commits/{BRANCH}", "application/vnd.github.sha").decode().strip()
        if len(sha) == 40:
            return sha
    except (urllib.error.URLError, OSError, ValueError):
        pass
    return BRANCH


def raw_url(ref: str, repo_path: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{ref}/{urllib.parse.quote(repo_path)}"


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_state(state: dict) -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def kb_manifest() -> dict:
    p = MODULES / KB_REL / "KB_MANIFEST.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"entries": []}


def use_bundled(reason: str) -> dict:
    MODULES.mkdir(parents=True, exist_ok=True)
    for f in BUNDLED.rglob("*"):
        if f.is_file():
            dest = MODULES / f.relative_to(BUNDLED)
            if not dest.exists() or sha256_file(dest) != sha256_file(f):
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
    state = {"source": "bundled", "reason": reason, "synced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "repo": REPO, "ref": None, "kb_revision": kb_manifest().get("kb_revision", 0)}
    save_state(state)
    return state


def cmd_update(args: argparse.Namespace) -> int:
    if args.offline:
        state = use_bundled("mode --offline")
    else:
        try:
            ref = resolve_ref()
            manifest = json.loads(http_get(raw_url(ref, "sync-manifest.json")))
            base = manifest["base_path"]
            wanted, warnings, downloaded = set(), [], 0
            for item in manifest["files"]:
                rel = Path(item["path"])
                wanted.add(rel.as_posix())
                dest = MODULES / rel
                if dest.exists() and sha256_file(dest) == item["sha256"]:
                    continue
                bundled = BUNDLED / rel
                if bundled.exists() and sha256_file(bundled) == item["sha256"]:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(bundled, dest)
                    continue
                data = http_get(raw_url(ref, f"{base}/{rel.as_posix()}"))
                if sha256_bytes(data) != item["sha256"]:
                    warnings.append(f"{rel}: hash tidak cocok (cache GitHub?), memakai salinan lama bila ada")
                    if not dest.exists() and bundled.exists():
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(bundled, dest)
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                downloaded += 1
            # Buang modul yang sudah dihapus admin; file KB unduhan tetap disimpan sebagai cache.
            kb_files = (MODULES / KB_REL / "files").resolve()
            for f in list(MODULES.rglob("*")):
                if f.is_file() and f.relative_to(MODULES).as_posix() not in wanted and kb_files not in f.resolve().parents:
                    f.unlink()
            state = {"source": "github", "repo": REPO, "ref": ref, "files_downloaded": downloaded, "warnings": warnings,
                     "synced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "kb_revision": manifest.get("kb_revision", 0)}
            save_state(state)
        except (urllib.error.URLError, OSError, ValueError, KeyError) as exc:
            state = use_bundled(f"Gagal mengambil versi terbaru dari GitHub: {exc}")
    kb = kb_manifest()
    active = [e for e in kb.get("entries", []) if e.get("status") == "ACTIVE"]
    print(json.dumps({
        **state,
        "workdir": str(MODULES),
        "modules": {p.name: str(p / "SKILL.md") for p in sorted(MODULES.iterdir()) if (p / "SKILL.md").exists()},
        "kb_index": str(MODULES / KB_REL / "KB_INDEX.md"),
        "kb_active_entries": len(active),
        "kb_total_entries": len(kb.get("entries", [])),
    }, ensure_ascii=False, indent=2))
    return 0


def ensure_synced() -> None:
    if not (MODULES / KB_REL / "KB_MANIFEST.json").exists():
        cmd_update(argparse.Namespace(offline=False))


def cmd_kb_get(args: argparse.Namespace) -> int:
    ensure_synced()
    entries = {e["id"]: e for e in kb_manifest().get("entries", [])}
    state = load_state()
    ref = state.get("ref") or BRANCH
    base = f"plugins/aigeothermal-pln/skills/{KB_REL.as_posix()}"
    results, code = [], 0
    for kb_id in args.ids:
        e = entries.get(kb_id.upper())
        if not e:
            results.append({"id": kb_id, "error": "ID tidak ada di KB_MANIFEST (cek KB_INDEX.md)"})
            code = 2
            continue
        dest = MODULES / KB_REL / e["file"]
        if not (dest.exists() and sha256_file(dest) == e["sha256"]):
            try:
                data = http_get(raw_url(ref, f"{base}/{e['file']}"))
            except (urllib.error.URLError, OSError) as exc:
                results.append({"id": e["id"], "error": f"gagal mengunduh dari GitHub: {exc}"})
                code = 2
                continue
            if sha256_bytes(data) != e["sha256"]:
                results.append({"id": e["id"], "error": "SHA-256 file unduhan tidak cocok dengan manifest"})
                code = 2
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        results.append({"id": e["id"], "title": e.get("title"), "status": e.get("status"),
                        "revision": e.get("revision"), "path": str(dest)})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return code


def cmd_kb_search(args: argparse.Namespace) -> int:
    ensure_synced()
    script = MODULES / "geothermal-knowledge" / "scripts" / "kb_manager.py"
    extra = ["--all"] if args.all else []
    return subprocess.call([sys.executable, str(script), "search", *args.terms, *extra])


def cmd_where(_: argparse.Namespace) -> int:
    print(json.dumps({"workdir": str(MODULES), **load_state()}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("update")
    p.add_argument("--offline", action="store_true", help="pakai salinan bawaan tanpa menghubungi GitHub")
    p = sub.add_parser("kb-get")
    p.add_argument("ids", nargs="+")
    p = sub.add_parser("kb-search")
    p.add_argument("terms", nargs="+")
    p.add_argument("--all", action="store_true", help="sertakan entri SUPERSEDED")
    sub.add_parser("where")
    args = ap.parse_args()
    return {"update": cmd_update, "kb-get": cmd_kb_get, "kb-search": cmd_kb_search, "where": cmd_where}[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
