#!/usr/bin/env python3
"""Kelola embedded geothermal KB tanpa deep-read isi sumber.

Subcommand:
  add      tambah satu file sumber ke KB (dipakai admin/CI di clone repo)
  update   simpan revisi baru; entri lama menjadi SUPERSEDED (tidak ditimpa)
  ingest   proses folder inbox (default: <repo>/kb-inbox): file lepas, ZIP batch,
           metadata.csv, dan sidecar .meta.json
  search   cari entri berdasarkan kata kunci pada metadata (routing ringan)
  list     tampilkan katalog + validasi
  check    validasi file, ukuran, hash, dan duplikasi

Hanya byte, ukuran, dan SHA-256 yang dihitung. Tidak ada OCR/ekstraksi teks.
Metadata berasal dari operator/kontributor, bukan dikarang.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
KB_DIR = SKILL_DIR / "references" / "KB"
MANIFEST = KB_DIR / "KB_MANIFEST.json"
INDEX = KB_DIR / "KB_INDEX.md"
PLUGIN_ROOT = SKILL_DIR.parents[1]
CHANGELOG = PLUGIN_ROOT / "CHANGELOG.md"
REPO_ROOT = PLUGIN_ROOT.parents[1]
DEFAULT_INBOX = REPO_ROOT / "kb-inbox"
# File KB mentah disimpan di luar plugin (<repo>/kb/files/) agar plugin tetap kecil;
# entri manifest menyimpan path relatif terhadap <repo>/kb/ (mis. "files/GEO-0001__x.pdf").
KB_STORE = REPO_ROOT / "kb"
FILES_DIR = KB_STORE / "files"

# GitHub menolak file >100 MB; beri margin.
MAX_FILE_BYTES = 95 * 1024 * 1024
META_SUFFIX = ".meta.json"
INBOX_IGNORE = {"README.md", ".gitkeep", ".DS_Store", "Thumbs.db", "desktop.ini"}
CSV_META = "metadata.csv"
KNOWN_DISCIPLINES = {"subsurface", "geology", "geochemistry", "geophysics", "reservoir", "drilling", "well-design",
                     "completion", "well-testing", "hse", "standard", "other"}
META_FIELDS = ("title", "discipline", "document_type", "revision", "topics", "keywords",
               "useful_locators", "visual_content", "notes", "contributor", "source_channel",
               "submitted_at", "original_filename")
INHERITED_FIELDS = ("title", "discipline", "document_type", "topics", "keywords", "visual_content")
LIST_FIELDS = {"topics", "keywords", "useful_locators", "visual_content"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_name(name: str) -> str:
    name = Path(name).name
    name = re.sub(r"[^A-Za-z0-9._()\- ]+", "_", name).strip(" .")
    return name or "source"


def load_manifest() -> dict:
    if MANIFEST.exists():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    else:
        data = {}
    data.setdefault("schema_version", 2)
    data.setdefault("kb_revision", 0)
    data.setdefault("entries", [])
    return data


def cell(value) -> str:
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def save_manifest(data: dict) -> None:
    data["schema_version"] = 2
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    entries = data["entries"]
    active = [e for e in entries if e.get("status", "ACTIVE") == "ACTIVE"]
    lines = [
        "# Geothermal Embedded Knowledge Base Index", "",
        "Status: ACTIVE", "Index mode: LIGHT / ROUTING ONLY", "Knowledge base root: `kb/files/` di repo GitHub (diunduh per ID dengan `scripts/kb_fetch.py`)",
        f"KB revision: {data.get('kb_revision', 0)} (updated {data.get('updated_at', 'n/a')})", "",
        "Metadata router only; original source files are the source of truth. Files are added and indexed without deep-reading their contents.",
        "Index ini dibangun ulang otomatis oleh `scripts/kb_manager.py`; jangan edit manual.", "",
        "## Source register", "",
    ]
    if not entries:
        lines.append("Belum ada raw KB yang dibundel.")
    else:
        lines += [f"Aktif: {len(active)} · Superseded: {len(entries) - len(active)}", "",
                  "| ID | Status | Judul | File | Disiplin | Tipe | Revisi | Topik / keyword | Locator | SHA-256 (prefix) |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for e in entries:
            status = e.get("status", "ACTIVE")
            if status == "SUPERSEDED" and e.get("superseded_by"):
                status += f" → {e['superseded_by']}"
            tags = (e.get("topics") or []) + (e.get("keywords") or [])
            vals = [e["id"], status, e.get("title", ""), e["file"], e.get("discipline", "other"),
                    e.get("document_type", "other"), e.get("revision", "unknown"), tags,
                    e.get("useful_locators") or "", e["sha256"][:12]]
            lines.append("| " + " | ".join(cell(v) for v in vals) + " |")
    lines += ["", "## Retrieval defaults", "", "- Candidate sources/pass: 5", "- Evidence ranges/pass: 8",
              "- Expanded pages/slides/pass: sekitar 12", "- Visuals/pass: 4",
              "- Expand only when evidence remains insufficient",
              "- Gunakan hanya entri ACTIVE sebagai evidence final; entri SUPERSEDED hanya untuk histori revisi", ""]
    INDEX.write_text("\n".join(lines), encoding="utf-8")


def changelog(lines: list[str], kb_revision: int) -> None:
    if not lines:
        return
    today = datetime.now(timezone.utc).date().isoformat()
    block = f"## KB rev {kb_revision} — {today}\n\n" + "\n".join(lines) + "\n"
    old = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else "# Changelog\n"
    head, sep, rest = old.partition("\n## ")
    new = head.rstrip() + "\n\n" + block + (("\n## " + rest) if sep else "")
    CHANGELOG.write_text(new.rstrip() + "\n", encoding="utf-8")


def next_id(entries: list[dict]) -> str:
    nums = [int(m.group(1)) for e in entries if (m := re.fullmatch(r"GEO-(\d+)", e.get("id", "")))]
    return f"GEO-{(max(nums, default=0) + 1):04d}"


def clean_meta(meta: dict) -> dict:
    out = {}
    for k in META_FIELDS:
        v = meta.get(k)
        if v in (None, "", []):
            continue
        if k in LIST_FIELDS:
            if isinstance(v, str):
                v = [s.strip() for s in re.split(r"[,;]", v) if s.strip()]
            v = [str(s).strip() for s in v if str(s).strip()]
            if not v:
                continue
        elif isinstance(v, str):
            v = v.strip()
        out[k] = v
    for k in ("discipline", "document_type"):
        if k in out:
            out[k] = str(out[k]).lower().replace(" ", "-")
    return out


def add_source(src: Path, data: dict, meta: dict, supersedes: str | None = None) -> tuple[dict, str]:
    """Tambahkan satu file. Tidak menyimpan manifest; pemanggil yang menyimpan."""
    src = src.expanduser().resolve()
    if not src.is_file():
        raise ValueError(f"File sumber tidak ditemukan: {src}")
    size = src.stat().st_size
    if size > MAX_FILE_BYTES:
        raise ValueError(f"{src.name}: {size / 1024 / 1024:.1f} MiB melebihi batas {MAX_FILE_BYTES // 1024 // 1024} MiB per file (batas GitHub). Pecah/kompres file terlebih dahulu.")
    if size == 0:
        raise ValueError(f"{src.name}: file kosong")
    digest = sha256(src)
    for e in data["entries"]:
        if e["sha256"] == digest:
            return e, "duplicate"
    meta = clean_meta(meta)
    if supersedes:
        previous = next((e for e in data["entries"] if e["id"] == supersedes), None)
        if not previous:
            raise ValueError(f"ID tidak dikenal: {supersedes}")
        if previous.get("status") != "ACTIVE":
            raise ValueError(f"ID {supersedes} bukan entri ACTIVE")
        # Revisi mewarisi metadata routing entri lama bila tidak diisi ulang.
        for k in INHERITED_FIELDS:
            if k not in meta and previous.get(k) not in (None, "", [], "other"):
                meta[k] = previous[k]
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    new_id = next_id(data["entries"])
    # Prefix ID mencegah tabrakan nama sambil mempertahankan basename asli.
    relative = Path("files") / f"{new_id}__{safe_name(src.name)}"
    dest = KB_STORE / relative
    shutil.copy2(src, dest)
    entry = {
        "id": new_id, "file": relative.as_posix(), "title": meta.pop("title", None) or src.stem,
        "discipline": meta.pop("discipline", None) or "other",
        "document_type": meta.pop("document_type", None) or "other",
        "revision": meta.pop("revision", None) or "unknown", "status": "ACTIVE",
        "size_bytes": dest.stat().st_size, "sha256": digest, "added_at": now_iso(),
        **meta,
    }
    if supersedes:
        entry["supersedes"] = supersedes
        for old in data["entries"]:
            if old["id"] == supersedes:
                old["status"] = "SUPERSEDED"
                old["superseded_by"] = new_id
                break
    data["entries"].append(entry)
    return entry, "added"


def commit_changes(data: dict, log_lines: list[str]) -> None:
    data["kb_revision"] = int(data.get("kb_revision", 0)) + 1
    data["updated_at"] = now_iso()
    save_manifest(data)
    changelog(log_lines, data["kb_revision"])


def log_line(entry: dict) -> str:
    verb = f"Revisi {entry['supersedes']} →" if entry.get("supersedes") else "Tambah"
    who = f" oleh {entry['contributor']}" if entry.get("contributor") else ""
    return f"- {verb} {entry['id']} — {entry.get('title', '')} (`{entry['file']}`, {entry['size_bytes']} bytes, SHA-256 `{entry['sha256'][:12]}…`){who}."


def load_csv_meta(path: Path) -> dict[str, dict]:
    """metadata.csv: satu baris per file; kolom `file` = nama file atau path relatif."""
    text = path.read_text(encoding="utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(text.splitlines()[0] if text else ",", delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rows = {}
    for row in csv.DictReader(text.splitlines(), dialect=dialect):
        row = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
        key = row.pop("file", "")
        if key:
            rows[key.replace("\\", "/").strip("/")] = {k: v for k, v in row.items() if v}
    return rows


def is_source(p: Path, root: Path) -> bool:
    rel = p.relative_to(root)
    return (p.is_file() and p.name not in INBOX_IGNORE and not p.name.endswith(META_SUFFIX)
            and p.name.lower() != CSV_META and p.suffix.lower() != ".zip"
            and not any(part.startswith(".") or part == "__MACOSX" for part in rel.parts))


def ingest_dir(root: Path, data: dict, dry_run: bool, label: str, consume: bool) -> tuple[dict, list[str]]:
    result = {"added": [], "duplicates": [], "errors": [], "warnings": []}
    log_lines: list[str] = []
    csv_path = root / CSV_META
    try:
        csv_meta = load_csv_meta(csv_path) if csv_path.exists() else {}
    except (OSError, csv.Error, UnicodeDecodeError) as exc:
        result["errors"].append({"file": f"{label}{CSV_META}", "error": f"metadata.csv tidak terbaca: {exc}"})
        return result, log_lines
    used_rows = set()
    for src in sorted(p for p in root.rglob("*") if is_source(p, root)):
        rel = src.relative_to(root).as_posix()
        shown = f"{label}{rel}"
        meta_path = src.with_name(src.name + META_SUFFIX)
        try:
            row_key = rel if rel in csv_meta else (src.name if src.name in csv_meta else None)
            meta = dict(csv_meta.get(row_key, {}))
            if row_key:
                used_rows.add(row_key)
            if meta_path.exists():
                side = json.loads(meta_path.read_text(encoding="utf-8"))
                if not isinstance(side, dict):
                    raise ValueError("sidecar .meta.json harus berupa objek JSON")
                meta.update(side)
            top = src.relative_to(root).parts[0].lower().replace(" ", "-") if len(src.relative_to(root).parts) > 1 else ""
            if "discipline" not in meta and top in KNOWN_DISCIPLINES:
                meta["discipline"] = top
            meta.setdefault("source_channel", "github-inbox" if not label else f"zip:{label.rstrip(':/ ')}")
            if meta.get("sha256") and meta["sha256"] != sha256(src):
                raise ValueError("SHA-256 di metadata tidak cocok dengan file (file berubah/korup saat upload)")
            if dry_run:
                result["added"].append({"file": shown, "dry_run": True})
                continue
            entry, status = add_source(src, data, meta, meta.get("supersedes") or None)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            result["errors"].append({"file": shown, "error": str(exc)})
            continue
        if status == "duplicate":
            result["duplicates"].append({"file": shown, "existing_id": entry["id"]})
        else:
            result["added"].append({"file": shown, "id": entry["id"], "title": entry["title"],
                                    "supersedes": entry.get("supersedes")})
            log_lines.append(log_line(entry))
        if consume:
            src.unlink()
            if meta_path.exists():
                meta_path.unlink()
    for key in sorted(set(csv_meta) - used_rows):
        result["warnings"].append({"file": f"{label}{CSV_META}", "warning": f"baris untuk '{key}' tidak menemukan file (diabaikan)"})
    # Sidecar yatim (tanpa file sumber) dilaporkan agar tidak diam-diam tertinggal.
    for orphan in sorted(root.rglob("*" + META_SUFFIX)):
        if not orphan.with_name(orphan.name[: -len(META_SUFFIX)]).exists():
            result["errors"].append({"file": f"{label}{orphan.relative_to(root).as_posix()}", "error": "sidecar tanpa file sumber"})
    if consume and csv_path.exists() and not result["errors"] and not dry_run:
        csv_path.unlink()
    return result, log_lines


def extract_zip(zpath: Path, dest: Path) -> None:
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            name = info.filename.replace("\\", "/")
            if info.is_dir():
                continue
            target = (dest / name).resolve()
            if name.startswith("/") or ".." in Path(name).parts or dest.resolve() not in target.parents:
                raise ValueError(f"path tidak aman di dalam ZIP: {info.filename}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as fsrc, target.open("wb") as fdst:
                shutil.copyfileobj(fsrc, fdst)


def ingest(inbox: Path, data: dict, dry_run: bool = False) -> dict:
    """Proses inbox: file lepas, ZIP batch (diekstrak otomatis), metadata.csv dan sidecar.

    File/ZIP yang sukses atau duplikat dihapus dari inbox. ZIP yang sebagian isinya gagal
    tetap disimpan; menjalankan ulang aman karena file yang sudah masuk terdeteksi duplikat.
    """
    result = {"added": [], "duplicates": [], "errors": [], "warnings": []}
    if not inbox.is_dir():
        raise ValueError(f"Folder inbox tidak ditemukan: {inbox}")
    log_lines: list[str] = []

    def merge(sub: dict, lines: list[str]) -> None:
        for k in result:
            result[k] += sub[k]
        log_lines.extend(lines)

    for zpath in sorted(p for p in inbox.rglob("*.zip") if p.is_file()):
        label = f"{zpath.relative_to(inbox).as_posix()}: "
        with tempfile.TemporaryDirectory(prefix="kb-zip-") as tmp:
            try:
                extract_zip(zpath, Path(tmp))
            except (zipfile.BadZipFile, ValueError, OSError) as exc:
                result["errors"].append({"file": label.rstrip(": "), "error": f"ZIP tidak dapat dibuka: {exc}"})
                continue
            sub, lines = ingest_dir(Path(tmp), data, dry_run, label, consume=False)
        merge(sub, lines)
        if not sub["errors"] and not dry_run:
            zpath.unlink()
    merge(*ingest_dir(inbox, data, dry_run, "", consume=True))
    if log_lines and not dry_run:
        commit_changes(data, log_lines)
    return result


def validate(data: dict) -> list[str]:
    errs, seen = [], {}
    if not FILES_DIR.exists():
        # Salinan plugin terinstal tidak membawa file KB mentah; hanya repo/CI yang memvalidasi file.
        return errs
    ids = [e.get("id") for e in data.get("entries", [])]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        errs.append(f"ID duplikat: {dup}")
    for e in data.get("entries", []):
        path = KB_STORE / e.get("file", "")
        if not path.is_file():
            errs.append(f"{e.get('id')}: file hilang: {e.get('file')}")
            continue
        actual_hash = sha256(path)
        if actual_hash != e.get("sha256"):
            errs.append(f"{e.get('id')}: hash tidak cocok")
        if path.stat().st_size != e.get("size_bytes"):
            errs.append(f"{e.get('id')}: ukuran tidak cocok")
        if actual_hash in seen:
            errs.append(f"Hash duplikat: {seen[actual_hash]} dan {e.get('id')}")
        seen[actual_hash] = e.get("id")
    tracked = {str((KB_STORE / e["file"]).resolve()) for e in data.get("entries", [])}
    for p in FILES_DIR.rglob("*") if FILES_DIR.exists() else []:
        if p.is_file() and p.name != ".gitkeep" and str(p.resolve()) not in tracked:
            errs.append(f"File tidak terdaftar di manifest: {p.relative_to(KB_STORE)}")
    return errs


def search(data: dict, terms: list[str], include_superseded: bool) -> list[tuple[int, dict]]:
    terms = [t.lower() for t in terms if t.strip()]
    hits = []
    for e in data.get("entries", []):
        if e.get("status") != "ACTIVE" and not include_superseded:
            continue
        hay = " ".join(cell(e.get(k)) for k in ("id", "title", "file", "discipline", "document_type", "revision",
                                                  "topics", "keywords", "useful_locators", "visual_content", "notes")).lower()
        score = sum(hay.count(t) for t in terms)
        if score:
            hits.append((score, e))
    return sorted(hits, key=lambda x: -x[0])


def show_report(data: dict) -> None:
    entries = data.get("entries", [])
    total = sum(e.get("size_bytes", 0) for e in entries)
    errs = validate(data)
    print(f"KB revision: {data.get('kb_revision', 0)} (updated {data.get('updated_at', 'n/a')})")
    print(f"Jumlah entri: {len(entries)} (aktif {sum(e.get('status') == 'ACTIVE' for e in entries)}, superseded {sum(e.get('status') == 'SUPERSEDED' for e in entries)})")
    print(f"Ukuran total raw KB: {total} bytes ({total / 1024 / 1024:.3f} MiB)")
    print(f"Validasi: {'LULUS' if not errs else 'GAGAL'}")
    for err in errs:
        print(f"- {err}")


def add_meta_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--title"); p.add_argument("--discipline"); p.add_argument("--document-type")
    p.add_argument("--revision"); p.add_argument("--topics", nargs="*"); p.add_argument("--keywords", nargs="*")
    p.add_argument("--useful-locators", nargs="*"); p.add_argument("--visual-content", nargs="*")
    p.add_argument("--notes"); p.add_argument("--contributor")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    for cmd in ("add", "update"):
        p = sub.add_parser(cmd)
        p.add_argument("source", type=Path)
        if cmd == "update":
            p.add_argument("--id", required=True, help="ID sumber ACTIVE yang akan ditandai SUPERSEDED")
        add_meta_args(p)
    p = sub.add_parser("ingest")
    p.add_argument("inbox", type=Path, nargs="?", default=DEFAULT_INBOX)
    p.add_argument("--summary", type=Path, help="tulis ringkasan Markdown (mis. untuk body PR)")
    p.add_argument("--json", action="store_true", help="cetak hasil sebagai JSON")
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("search")
    p.add_argument("terms", nargs="+")
    p.add_argument("--all", action="store_true", help="sertakan entri SUPERSEDED")
    p.add_argument("--limit", type=int, default=10)
    sub.add_parser("list")
    sub.add_parser("check")
    args = ap.parse_args()
    data = load_manifest()
    try:
        if args.command in ("add", "update"):
            meta = {k: getattr(args, k, None) for k in META_FIELDS}
            meta["source_channel"] = "cli"
            e, status = add_source(args.source, data, meta, args.id if args.command == "update" else None)
            if status == "duplicate":
                print(f"Duplikat identik; tidak ditambahkan: {e['id']} {e['file']}")
            else:
                commit_changes(data, [log_line(e)])
                print(f"Tersimpan: {e['id']} {e['file']} ({e['size_bytes']} bytes, SHA-256 {e['sha256']})")
        elif args.command == "ingest":
            res = ingest(args.inbox, data, args.dry_run)
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                for a in res["added"]:
                    print(f"Tambah: {a.get('id', '(dry-run)')} ← {a['file']}" + (f" (revisi {a['supersedes']})" if a.get("supersedes") else ""))
                for d in res["duplicates"]:
                    print(f"Duplikat (dibuang dari inbox): {d['file']} = {d['existing_id']}")
                for er in res["errors"]:
                    print(f"GAGAL: {er['file']}: {er['error']}")
                for w in res["warnings"]:
                    print(f"PERINGATAN: {w['file']}: {w['warning']}")
            if args.summary:
                md = [f"KB revision: **{data.get('kb_revision', 0)}**", ""]
                md += [f"- ✅ `{a.get('id')}` {a.get('title', '')} ← `{a['file']}`" + (f" (menggantikan `{a['supersedes']}`)" if a.get("supersedes") else "") for a in res["added"]]
                md += [f"- ♻️ Duplikat `{d['file']}` sudah ada sebagai `{d['existing_id']}` — tidak ditambahkan" for d in res["duplicates"]]
                md += [f"- ❌ `{er['file']}`: {er['error']}" for er in res["errors"]]
                md += [f"- ⚠️ `{w['file']}`: {w['warning']}" for w in res["warnings"]]
                args.summary.write_text("\n".join(md) + "\n", encoding="utf-8")
            if res["errors"]:
                show_report(data)
                return 1
        elif args.command == "search":
            hits = search(data, args.terms, args.all)[: args.limit]
            if not hits:
                print("Tidak ada entri yang cocok di metadata KB. Pertimbangkan sinonim/istilah lain atau nyatakan sebagai data gap.")
            for score, e in hits:
                print(f"{e['id']}\t{e.get('status')}\tskor={score}\t{e['file']}\t{e.get('title', '')}\t[{cell(e.get('topics'))}; {cell(e.get('keywords'))}]")
            return 0
        elif args.command == "list":
            for e in data["entries"]:
                print(f"{e['id']}\t{e.get('status', 'ACTIVE')}\t{e['size_bytes']} B\t{e.get('revision', 'unknown')}\t{e['file']}\t{e.get('title', '')}")
        show_report(data)
        return 1 if validate(data) else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
