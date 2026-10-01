#!/usr/bin/env python3
"""Unduh file sumber KB geothermal per ID (GEO-xxxx) dari repo GitHub.

File KB mentah tidak ikut dibundel di plugin/skill agar ukurannya tetap kecil. Skrip ini
membaca KB_MANIFEST.json di skill ini, mengunduh hanya file yang diminta dari
`kb/files/` di repo, memverifikasi SHA-256, lalu mencetak path lokalnya (JSON).

Pemakaian:
  python scripts/kb_fetch.py GEO-0003 GEO-0007 [--out DIR]

Env opsional: AIGEO_REPO (default hammamrz/AI-geothermal), AIGEO_BRANCH (default main),
AIGEO_TOKEN (hanya untuk repo privat), AIGEO_KB_CACHE (folder cache).
Hanya pustaka standar Python.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
MANIFEST = SKILL_DIR / "references" / "KB" / "KB_MANIFEST.json"
REPO = os.environ.get("AIGEO_REPO", "hammamrz/AI-geothermal")
BRANCH = os.environ.get("AIGEO_BRANCH", "main")
TOKEN = os.environ.get("AIGEO_TOKEN") or None
KB_REPO_DIR = "kb"
TIMEOUT = 60


def http_get(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": "aigeothermal-pln-kb-fetch"}
    if accept:
        headers["Accept"] = accept
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=TIMEOUT) as resp:
        return resp.read()


def resolve_ref() -> str:
    """SHA commit terbaru (konsisten, bebas cache CDN); jatuh ke nama branch bila API tidak tersedia."""
    try:
        sha = http_get(f"https://api.github.com/repos/{REPO}/commits/{BRANCH}", "application/vnd.github.sha").decode().strip()
        if len(sha) == 40:
            return sha
    except (urllib.error.URLError, OSError, ValueError):
        pass
    return BRANCH


def explain(exc: Exception) -> str:
    code = getattr(exc, "code", None)
    if code == 404:
        return "file tidak ditemukan di GitHub (HTTP 404); KB lokal mungkin lebih baru/lama dari repo, atau repo privat"
    if code in (401, 403):
        return f"akses ditolak GitHub (HTTP {code})"
    return str(exc)


def default_cache() -> Path:
    return Path(os.environ.get("AIGEO_KB_CACHE", Path(tempfile.gettempdir()) / "aigeothermal-kb"))


def load_entries(manifest: Path = MANIFEST) -> dict:
    return {e["id"]: e for e in json.loads(manifest.read_text(encoding="utf-8")).get("entries", [])}


def fetch(ids: list[str], out: Path, manifest: Path = MANIFEST) -> list[dict]:
    """Unduh entri KB per ID; kembalikan daftar hasil (path atau error) per ID."""
    entries = load_entries(manifest)
    ref = None
    results = []
    for kb_id in ids:
        e = entries.get(kb_id.strip().upper())
        if not e:
            results.append({"id": kb_id, "error": "ID tidak ada di KB_MANIFEST (cek KB_INDEX.md)"})
            continue
        dest = out / Path(e["file"]).name
        if not (dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() == e["sha256"]):
            ref = ref or resolve_ref()
            url = f"https://raw.githubusercontent.com/{REPO}/{ref}/{urllib.parse.quote(KB_REPO_DIR + '/' + e['file'])}"
            try:
                data = http_get(url)
            except (urllib.error.URLError, OSError) as exc:
                results.append({"id": e["id"], "error": f"gagal mengunduh: {explain(exc)}"})
                continue
            if hashlib.sha256(data).hexdigest() != e["sha256"]:
                results.append({"id": e["id"], "error": "SHA-256 file unduhan tidak cocok dengan KB_MANIFEST"})
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        results.append({"id": e["id"], "title": e.get("title"), "status": e.get("status"),
                        "revision": e.get("revision"), "sha256": e["sha256"], "path": str(dest)})
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="+", help="ID entri KB, mis. GEO-0003")
    ap.add_argument("--out", type=Path, default=default_cache())
    ap.add_argument("--manifest", type=Path, default=MANIFEST, help=argparse.SUPPRESS)
    args = ap.parse_args()
    results = fetch(args.ids, args.out, args.manifest)
    for r in results:
        r.pop("sha256", None)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 2 if any("error" in r for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
