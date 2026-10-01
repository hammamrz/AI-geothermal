#!/usr/bin/env python3
"""Render halaman/slide sumber KB menjadi PNG agar visual (foto, peta, penampang,
well schematic, grafik, tabel bergambar) bisa dilihat dan ditampilkan.

Ekstraksi teks hanya membaca caption; gambar baru terbaca setelah halamannya dirender.

Pemakaian:
  python scripts/kb_render.py GEO-0007 --pages 20-22
  python scripts/kb_render.py GEO-0001 --pages 17,19 --dpi 150
  python scripts/kb_render.py /path/dokumen.pptx --pages 3      # file lokal (mis. dokumen yang direview)
  python scripts/kb_render.py GEO-0007 --info                   # jumlah halaman saja

Format: PDF langsung; PPT/PPTX/DOC/DOCX/XLS/XLSX/XLSM dikonversi ke PDF dulu lewat
LibreOffice (hasil konversi di-cache). Gambar (PNG/JPG) dikembalikan apa adanya.
Renderer dicoba berurutan: PyMuPDF → pypdfium2 → pdftoppm (poppler).
Output JSON: daftar {page, path, width, height}. Hanya pustaka standar + tool di atas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_fetch  # noqa: E402

OFFICE_EXT = {".ppt", ".pptx", ".pps", ".ppsx", ".doc", ".docx", ".xls", ".xlsx", ".xlsm", ".odt", ".odp", ".ods", ".rtf"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp"}
MAX_PAGES_DEFAULT = 6


def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    pages = []
    for part in spec.replace(" ", "").split(","):
        if not part:
            continue
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", part)
        if not m:
            raise ValueError(f"format --pages tidak valid: {part!r} (contoh: 3 atau 20-22 atau 1,4-6)")
        a, b = int(m[1]), int(m[2] or m[1])
        pages.extend(range(min(a, b), max(a, b) + 1))
    out = sorted({p for p in pages if 1 <= p <= total})
    if not out:
        raise ValueError(f"halaman di luar rentang dokumen (1-{total})")
    return out


def to_pdf(src: Path, cache: Path) -> Path:
    if src.suffix.lower() == ".pdf":
        return src
    if src.suffix.lower() not in OFFICE_EXT:
        raise ValueError(f"format {src.suffix} belum didukung untuk render")
    digest = hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    out_dir = cache / "pdf" / digest
    pdf = out_dir / (src.stem + ".pdf")
    if pdf.exists():
        return pdf
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("LibreOffice (soffice) tidak tersedia untuk mengonversi dokumen Office ke PDF")
    out_dir.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(src)],
                       capture_output=True, text=True, timeout=300)
    if not pdf.exists():
        found = list(out_dir.glob("*.pdf"))
        if not found:
            raise RuntimeError(f"konversi ke PDF gagal: {(r.stderr or r.stdout).strip()[:300]}")
        pdf = found[0]
    return pdf


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        head = f.read(24)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", head[16:24])
    return (0, 0)


def page_count(pdf: Path) -> int:
    try:
        import fitz  # type: ignore
        with fitz.open(pdf) as doc:
            return doc.page_count
    except ImportError:
        pass
    try:
        import pypdfium2 as pdfium  # type: ignore
        return len(pdfium.PdfDocument(str(pdf)))
    except ImportError:
        pass
    if shutil.which("pdfinfo"):
        r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
        m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
        if m:
            return int(m[1])
    raise RuntimeError("tidak ada renderer PDF (PyMuPDF/pypdfium2/poppler) yang tersedia")


def render(pdf: Path, pages: list[int], dpi: int, out_dir: Path, stem: str) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        import fitz  # type: ignore
        with fitz.open(pdf) as doc:
            for p in pages:
                path = out_dir / f"{stem}_p{p:03d}.png"
                doc[p - 1].get_pixmap(dpi=dpi).save(path)
                results.append(path)
        return [{"page": p, "path": str(x)} for p, x in zip(pages, results)]
    except ImportError:
        pass
    try:
        import pypdfium2 as pdfium  # type: ignore
        doc = pdfium.PdfDocument(str(pdf))
        for p in pages:
            path = out_dir / f"{stem}_p{p:03d}.png"
            doc[p - 1].render(scale=dpi / 72).to_pil().save(path)
            results.append(path)
        return [{"page": p, "path": str(x)} for p, x in zip(pages, results)]
    except ImportError:
        pass
    if not shutil.which("pdftoppm"):
        raise RuntimeError("tidak ada renderer PDF (PyMuPDF/pypdfium2/pdftoppm) yang tersedia")
    for p in pages:
        prefix = out_dir / f"{stem}_p{p:03d}"
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-f", str(p), "-l", str(p), "-singlefile",
                        str(pdf), str(prefix)], check=True, capture_output=True)
        results.append(prefix.with_suffix(".png"))
    return [{"page": p, "path": str(x)} for p, x in zip(pages, results)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="ID KB (GEO-xxxx) atau path file lokal")
    ap.add_argument("--pages", help="halaman/slide, mis. 5 atau 20-22 atau 1,4-6 (wajib kecuali dokumen ≤ batas)")
    ap.add_argument("--dpi", type=int, default=110, help="110 cukup untuk dibaca; naikkan (150-200) untuk detail kecil")
    ap.add_argument("--max-pages", type=int, default=MAX_PAGES_DEFAULT, help="batas halaman per panggilan (hemat context)")
    ap.add_argument("--out", type=Path, help="folder output PNG")
    ap.add_argument("--info", action="store_true", help="hanya cetak jumlah halaman")
    args = ap.parse_args()
    cache = kb_fetch.default_cache()
    try:
        meta = {}
        if re.fullmatch(r"(?i)GEO-\d+", args.source.strip()):
            res = kb_fetch.fetch([args.source], cache)[0]
            if "error" in res:
                raise RuntimeError(f"{res['id']}: {res['error']}")
            src = Path(res["path"])
            meta = {"id": res["id"], "title": res.get("title")}
        else:
            src = Path(args.source).expanduser().resolve()
            if not src.is_file():
                raise ValueError(f"file tidak ditemukan: {src}")
        stem = meta.get("id") or re.sub(r"[^A-Za-z0-9_-]+", "_", src.stem)[:40]
        if src.suffix.lower() in IMAGE_EXT:
            print(json.dumps({**meta, "source": str(src), "images": [{"page": 1, "path": str(src)}]}, ensure_ascii=False, indent=2))
            return 0
        pdf = to_pdf(src, cache)
        total = page_count(pdf)
        if args.info:
            print(json.dumps({**meta, "source": str(src), "pages": total}, ensure_ascii=False, indent=2))
            return 0
        pages = parse_pages(args.pages, total)
        if len(pages) > args.max_pages:
            raise ValueError(f"{len(pages)} halaman diminta; batas {args.max_pages} per panggilan. Persempit --pages "
                             f"(dokumen ini {total} halaman) atau naikkan --max-pages bila memang perlu.")
        out_dir = args.out or (cache / "render" / stem)
        images = render(pdf, pages, args.dpi, out_dir, stem)
        for img in images:
            img["width"], img["height"] = png_size(Path(img["path"]))
        print(json.dumps({**meta, "source": str(src), "pages_total": total, "dpi": args.dpi, "images": images},
                         ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"source": args.source, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
