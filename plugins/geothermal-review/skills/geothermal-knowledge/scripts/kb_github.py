#!/usr/bin/env python3
"""Hubungkan KB lokal (skill terinstal) dengan repo GitHub sumber KB.

Subcommand:
  submit   usulkan file sumber baru/revisi dari chat → branch + Pull Request ke kb-inbox/
  status   bandingkan KB lokal dengan KB terbaru di GitHub (apakah skill tertinggal?)
  fetch    unduh satu file KB (berdasarkan ID) langsung dari GitHub bila belum ada di lokal

Mode submit (--mode auto memilih otomatis, urutan: api → git → package):
  api      GitHub REST API dengan token (GH_TOKEN / GITHUB_TOKEN / `gh auth token`)
  git      git clone + push branch memakai kredensial git yang sudah ada, lalu `gh pr create`
  package  buat ZIP berisi kb-inbox/<file> + <file>.meta.json untuk di-upload manual oleh admin

Hanya pustaka standar Python. Tidak membaca isi dokumen.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
LOCAL_MANIFEST = SKILL_DIR / "references" / "KB" / "KB_MANIFEST.json"
DEFAULT_REPO = os.environ.get("KB_REPO", "hammamrz/AI-geothermal")
DEFAULT_BRANCH = os.environ.get("KB_BRANCH", "main")
KB_REPO_PATH = "plugins/geothermal-review/skills/geothermal-knowledge/references/KB"
INBOX_REPO_PATH = "kb-inbox"
MAX_FILE_BYTES = 95 * 1024 * 1024
META_FIELDS = ("title", "discipline", "document_type", "revision", "topics", "keywords",
               "useful_locators", "visual_content", "notes", "contributor", "supersedes")


# ---------------------------------------------------------------- helpers
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_name(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._()\- ]+", "_", Path(name).name).strip(" .")
    return name or "source"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "kb"


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def find_token() -> str | None:
    for var in ("KB_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(var):
            return os.environ[var]
    if shutil.which("gh"):
        r = run(["gh", "auth", "token"], check=False)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    return None


class GitHub:
    def __init__(self, repo: str, token: str | None):
        self.repo, self.token = repo, token

    def request(self, method: str, path: str, body: dict | None = None, raw: bool = False):
        url = path if path.startswith("https://") else f"https://api.github.com/repos/{self.repo}{path}"
        headers = {"Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
                   "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "geothermal-kb-submit"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        data = json.dumps(body).encode() if body is not None else None
        if data:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                payload = resp.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:500]
            raise RuntimeError(f"GitHub API {method} {path} → HTTP {exc.code}: {detail}") from None
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Tidak dapat menghubungi GitHub API: {exc.reason}") from None
        return payload if raw else (json.loads(payload) if payload else {})

    def remote_manifest(self, ref: str) -> dict:
        raw = self.request("GET", f"/contents/{KB_REPO_PATH}/KB_MANIFEST.json?ref={ref}", raw=True)
        return json.loads(raw)


def load_local_manifest() -> dict:
    if LOCAL_MANIFEST.exists():
        return json.loads(LOCAL_MANIFEST.read_text(encoding="utf-8"))
    return {"entries": []}


def build_meta(args: argparse.Namespace, src: Path, digest: str) -> dict:
    meta = {}
    for k in META_FIELDS:
        v = getattr(args, k, None)
        if v not in (None, "", []):
            meta[k] = v
    meta.setdefault("title", src.stem)
    meta["source_channel"] = "chat"
    meta["submitted_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    meta["original_filename"] = src.name
    meta["sha256"] = digest
    return meta


# ---------------------------------------------------------------- submit
def prepare(args: argparse.Namespace) -> list[tuple[Path, str, dict]]:
    """Validasi file, cek duplikat lokal, dan susun sidecar metadata."""
    if args.supersedes and len(args.files) != 1:
        raise ValueError("--supersedes hanya boleh untuk satu file per pengajuan")
    known = {e["sha256"]: e["id"] for e in load_local_manifest().get("entries", [])}
    items, seen_names = [], set()
    for f in args.files:
        src = Path(f).expanduser().resolve()
        if not src.is_file():
            raise ValueError(f"File tidak ditemukan: {src}")
        size = src.stat().st_size
        if size == 0 or size > MAX_FILE_BYTES:
            raise ValueError(f"{src.name}: ukuran {size} bytes di luar batas (1 B – {MAX_FILE_BYTES // 1024 // 1024} MiB)")
        digest = sha256(src)
        if digest in known and not args.force:
            raise ValueError(f"{src.name} identik dengan entri KB {known[digest]}; tidak perlu diajukan (pakai --force untuk tetap mengajukan)")
        name = safe_name(src.name)
        if name in seen_names:
            raise ValueError(f"Nama file ganda dalam satu pengajuan: {name}")
        seen_names.add(name)
        items.append((src, name, build_meta(args, src, digest)))
    return items


def pr_text(items, args) -> tuple[str, str]:
    titles = ", ".join(m["title"] for _, _, m in items)
    title = f"KB: {'revisi' if args.supersedes else 'tambah'} {titles}"[:120]
    lines = ["Pengajuan sumber knowledge base geothermal dari chat skill `geothermal-knowledge`.", "",
             "| File | Judul | Disiplin | Tipe | Revisi | SHA-256 |", "|---|---|---|---|---|---|"]
    for _, name, m in items:
        lines.append(f"| `{name}` | {m.get('title', '')} | {m.get('discipline', '-')} | {m.get('document_type', '-')} | {m.get('revision', '-')} | `{m['sha256'][:12]}…` |")
    if args.supersedes:
        lines += ["", f"Menggantikan entri **{args.supersedes}** (entri lama tetap disimpan sebagai SUPERSEDED)."]
    lines += ["", "Workflow **KB validate** menampilkan pratinjau ingest pada PR ini. Setelah PR di-merge, workflow **KB ingest** memindahkan file dari `kb-inbox/` ke KB, memberi ID `GEO-xxxx`, membangun ulang `KB_INDEX.md`/CHANGELOG, lalu me-merge PR `kb-ingest/auto`.",
              "Setelah itu semua akun yang memakai plugin/skill menerima KB terbaru pada sinkronisasi berikutnya."]
    return title, "\n".join(lines)


def branch_name(items) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"kb-submit/{stamp}-{slug(items[0][2]['title'])}"


def submit_api(items, args, token: str) -> str:
    gh = GitHub(args.repo, token)
    remote = {e["sha256"]: e["id"] for e in gh.remote_manifest(args.base).get("entries", [])}
    for _, name, m in items:
        if m["sha256"] in remote and not args.force:
            raise ValueError(f"{name} identik dengan entri KB {remote[m['sha256']]} di GitHub; tidak diajukan")
    base_sha = gh.request("GET", f"/git/ref/heads/{args.base}")["object"]["sha"]
    base_tree = gh.request("GET", f"/git/commits/{base_sha}")["tree"]["sha"]
    tree = []
    for src, name, meta in items:
        blob = gh.request("POST", "/git/blobs", {"content": base64.b64encode(src.read_bytes()).decode(), "encoding": "base64"})
        tree.append({"path": f"{INBOX_REPO_PATH}/{name}", "mode": "100644", "type": "blob", "sha": blob["sha"]})
        meta_blob = gh.request("POST", "/git/blobs", {"content": json.dumps(meta, ensure_ascii=False, indent=2) + "\n", "encoding": "utf-8"})
        tree.append({"path": f"{INBOX_REPO_PATH}/{name}.meta.json", "mode": "100644", "type": "blob", "sha": meta_blob["sha"]})
    new_tree = gh.request("POST", "/git/trees", {"base_tree": base_tree, "tree": tree})["sha"]
    title, body = pr_text(items, args)
    commit = gh.request("POST", "/git/commits", {"message": title, "tree": new_tree, "parents": [base_sha]})["sha"]
    branch = branch_name(items)
    gh.request("POST", "/git/refs", {"ref": f"refs/heads/{branch}", "sha": commit})
    pr = gh.request("POST", "/pulls", {"title": title, "head": branch, "base": args.base, "body": body})
    return pr["html_url"]


def submit_git(items, args) -> str:
    if not shutil.which("git"):
        raise RuntimeError("git tidak tersedia")
    url = os.environ.get("KB_GIT_URL") or f"https://github.com/{args.repo}.git"
    with tempfile.TemporaryDirectory(prefix="kb-submit-") as tmp:
        clone = Path(tmp) / "repo"
        env_ok = run(["git", "clone", "--depth", "1", "--branch", args.base, "--filter=blob:none", "--no-checkout", url, str(clone)], check=False)
        if env_ok.returncode != 0:
            raise RuntimeError(f"git clone gagal (akses repo?): {env_ok.stderr.strip()[:300]}")
        run(["git", "sparse-checkout", "set", "--no-cone", f"/{INBOX_REPO_PATH}/", f"/{KB_REPO_PATH}/KB_MANIFEST.json"], cwd=clone)
        run(["git", "checkout", args.base], cwd=clone)
        remote_manifest = clone / KB_REPO_PATH / "KB_MANIFEST.json"
        if remote_manifest.exists():
            remote = {e["sha256"]: e["id"] for e in json.loads(remote_manifest.read_text(encoding="utf-8")).get("entries", [])}
            for _, name, m in items:
                if m["sha256"] in remote and not args.force:
                    raise ValueError(f"{name} identik dengan entri KB {remote[m['sha256']]} di GitHub; tidak diajukan")
        branch = branch_name(items)
        run(["git", "checkout", "-b", branch], cwd=clone)
        inbox = clone / INBOX_REPO_PATH
        inbox.mkdir(exist_ok=True)
        for src, name, meta in items:
            shutil.copy2(src, inbox / name)
            (inbox / f"{name}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        title, body = pr_text(items, args)
        run(["git", "add", "--sparse", INBOX_REPO_PATH], cwd=clone)
        if run(["git", "config", "user.email"], cwd=clone, check=False).returncode != 0:
            run(["git", "config", "user.email", "kb-bot@users.noreply.github.com"], cwd=clone)
            run(["git", "config", "user.name", args.contributor or "KB contributor"], cwd=clone)
        run(["git", "commit", "-m", title], cwd=clone)
        push = run(["git", "push", "-u", "origin", branch], cwd=clone, check=False)
        if push.returncode != 0:
            raise RuntimeError(f"git push gagal (butuh akses tulis ke repo): {push.stderr.strip()[:300]}")
        if shutil.which("gh"):
            pr = run(["gh", "pr", "create", "--repo", args.repo, "--base", args.base, "--head", branch,
                      "--title", title, "--body", body], cwd=clone, check=False)
            if pr.returncode == 0 and pr.stdout.strip():
                return pr.stdout.strip().splitlines()[-1]
        return f"https://github.com/{args.repo}/compare/{args.base}...{branch}?expand=1 (branch sudah di-push; buka link ini untuk membuat PR)"


def submit_package(items, args) -> str:
    out_dir = Path(args.out or ".").expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    zpath = out_dir / f"kb-submission-{slug(items[0][2]['title'])}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for src, name, meta in items:
            z.write(src, f"{INBOX_REPO_PATH}/{name}")
            z.writestr(f"{INBOX_REPO_PATH}/{name}.meta.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    return str(zpath)


def cmd_submit(args: argparse.Namespace) -> int:
    try:
        items = prepare(args)
    except ValueError as exc:
        print(json.dumps({"status": "rejected", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 3
    modes = [args.mode] if args.mode != "auto" else ["api", "git", "package"]
    errors = []
    for mode in modes:
        try:
            if mode == "api":
                token = find_token()
                if not token:
                    raise RuntimeError("token GitHub tidak ditemukan (GH_TOKEN/GITHUB_TOKEN/gh auth)")
                url = submit_api(items, args, token)
            elif mode == "git":
                url = submit_git(items, args)
            else:
                path = submit_package(items, args)
                print(json.dumps({"status": "packaged", "mode": "package", "zip": path, "fallback_reasons": errors,
                                  "next_step": f"Ekstrak ZIP lalu upload isi folder kb-inbox/ (file + .meta.json) ke folder kb-inbox/ di https://github.com/{args.repo} (Add file → Upload files → 'Create a new branch … and start a pull request'), atau kirim ZIP ke admin KB."},
                                 ensure_ascii=False, indent=2))
                return 0
            print(json.dumps({"status": "submitted", "mode": mode, "pull_request": url, "fallback_reasons": errors,
                              "files": [n for _, n, _ in items]}, ensure_ascii=False, indent=2))
            return 0
        except (RuntimeError, ValueError, OSError) as exc:
            if isinstance(exc, ValueError):
                print(json.dumps({"status": "rejected", "reason": str(exc)}, ensure_ascii=False, indent=2))
                return 3
            errors.append(f"{mode}: {exc}")
    print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=False, indent=2))
    return 2


# ---------------------------------------------------------------- status / fetch
def cmd_status(args: argparse.Namespace) -> int:
    local = load_local_manifest()
    try:
        remote = GitHub(args.repo, find_token()).remote_manifest(args.base)
    except RuntimeError as exc:
        print(json.dumps({"status": "unknown", "local_kb_revision": local.get("kb_revision", 0), "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    lids = {e["id"] for e in local.get("entries", [])}
    missing = [{"id": e["id"], "title": e.get("title"), "status": e.get("status")} for e in remote.get("entries", []) if e["id"] not in lids]
    changed = [e["id"] for e in remote.get("entries", []) for le in local.get("entries", [])
               if le["id"] == e["id"] and le.get("status") != e.get("status")]
    up_to_date = not missing and not changed and local.get("kb_revision", 0) >= remote.get("kb_revision", 0)
    print(json.dumps({"status": "up_to_date" if up_to_date else "behind",
                      "local_kb_revision": local.get("kb_revision", 0), "remote_kb_revision": remote.get("kb_revision", 0),
                      "missing_locally": missing, "status_changed": changed}, ensure_ascii=False, indent=2))
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    gh = GitHub(args.repo, find_token())
    remote = gh.remote_manifest(args.base)
    entry = next((e for e in remote.get("entries", []) if e["id"] == args.id), None)
    if not entry:
        print(f"ERROR: {args.id} tidak ada di KB GitHub ({args.repo}@{args.base})", file=sys.stderr)
        return 2
    data = gh.request("GET", f"/contents/{KB_REPO_PATH}/{entry['file']}?ref={args.base}", raw=True)
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        print("ERROR: hash file unduhan tidak cocok dengan manifest", file=sys.stderr)
        return 2
    out_dir = Path(args.out or tempfile.gettempdir()).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / Path(entry["file"]).name
    out.write_bytes(data)
    print(json.dumps({"id": entry["id"], "title": entry.get("title"), "status": entry.get("status"), "path": str(out)}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=DEFAULT_REPO, help=f"owner/repo (default {DEFAULT_REPO}, env KB_REPO)")
    ap.add_argument("--base", default=DEFAULT_BRANCH, help=f"branch KB (default {DEFAULT_BRANCH}, env KB_BRANCH)")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("submit")
    p.add_argument("files", nargs="+")
    p.add_argument("--mode", choices=("auto", "api", "git", "package"), default="auto")
    p.add_argument("--out", help="folder output ZIP untuk mode package")
    p.add_argument("--force", action="store_true", help="ajukan walau hash sama dengan entri yang ada")
    p.add_argument("--title"); p.add_argument("--discipline"); p.add_argument("--document-type")
    p.add_argument("--revision"); p.add_argument("--topics", nargs="*"); p.add_argument("--keywords", nargs="*")
    p.add_argument("--useful-locators", nargs="*"); p.add_argument("--visual-content", nargs="*")
    p.add_argument("--notes"); p.add_argument("--contributor"); p.add_argument("--supersedes", help="ID entri ACTIVE yang direvisi, mis. GEO-0003")
    sub.add_parser("status")
    p = sub.add_parser("fetch")
    p.add_argument("--id", required=True)
    p.add_argument("--out")
    args = ap.parse_args()
    try:
        return {"submit": cmd_submit, "status": cmd_status, "fetch": cmd_fetch}[args.command](args)
    except (RuntimeError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
