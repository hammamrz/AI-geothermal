#!/usr/bin/env python3
"""Membangun PPTX technical review geothermal bergaya PLN IP dari JSON terstruktur.

Struktur deck mengikuti tulang punggung Technical Review / Comment Sheet Report:
cover -> ringkasan eksekutif -> agenda -> pengendalian dokumen (opsional) -> tujuan/lingkup ->
dokumen yang dikaji -> metodologi -> sebaran temuan -> daftar temuan -> rincian temuan ->
risiko antardisiplin -> data gap -> tindak lanjut -> kesimpulan -> sumber -> penutup.

Tampilan mengikuti framework skill presentasi-pln-ip dan presentasi-tvv (pustaka di
assets/pustaka): judul dua warna (topik biru + sub-topik hitam) tanpa label kecil di atasnya,
tanpa garis aksen, tanpa sudut membulat/bayangan/gradien, tanpa deretan kartu; tabel bersumbu
dengan penanda status bulat; model grafis asli PowerPoint (deret angka kunci, alur proses,
chart bertumpuk, matriks risiko 5x5, progres). Teks mendukung *miring* dan **tebal**.

Pemakaian:
    python build_review_ppt.py review.json output.pptx

Format JSON (kunci lama tetap diterima):
{
  "report_title": "Kajian Teknis Drilling Program Sumur X",
  "project_name": "Lapangan / proyek",
  "report_no": "TR-001", "revision": "0", "date": "30 September 2026",
  "prepared_by": "...", "reviewed_by": "...", "approved_by": "...",
  "executive_summary": ["...", "..."],
  "objective": "...", "scope": ["..."], "review_basis": ["..."], "limitations": ["..."],
  "methodology": ["..."],                              # opsional, 3-5 langkah
  "documents_reviewed": [{"title","number","revision","date","discipline","scope"}],
  "findings": [{"id","discipline","location","title","finding","comment","impact","basis",
                "source","priority","status","confidence","image_path"}],
  "key_risks": [{"interface","risk","impact","mitigation","related_findings",
                 "likelihood": 1-5, "severity": 1-5}],   # likelihood+severity -> matriks 5x5
  "data_gaps": [{"id","gap","impact","required","owner","status"}],
  "actions": [{"id","finding_id","action","pic","due","evidence","status"}],
  "conclusion": "...", "conditions_to_proceed": ["..."],
  "overall_status": "Perlu revisi", "references_used": ["..."]
}
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

PUSTAKA = Path(__file__).resolve().parent.parent / "assets" / "pustaka"
sys.path.insert(0, str(PUSTAKA))

import plnip_deck as P  # noqa: E402  palet, teks, bullet, judul kolom
import plnip_grafis as G  # noqa: E402  model grafis
import tvv_deck as T  # noqa: E402  tabel berpenanda status, matriks risiko, gambar

from pptx import Presentation  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from pptx.util import Inches  # noqa: E402

SW, SH = 13.333, 7.5
ASSET_DIR = Path(__file__).resolve().parent.parent / "references" / "master_assets"
MASTER_COVER = ASSET_DIR / "MASTER_COVER.jpg"
MASTER_CONTENT = ASSET_DIR / "MASTER_CONTENT.jpg"
MASTER_CLOSING = ASSET_DIR / "MASTER_CLOSING.jpg"

# Grid untuk master isi geothermal (logo Danantara + PLN IP di kanan atas mulai x ±9,3)
L, R = 0.55, 12.78
CW = R - L
TITLE_X, TITLE_Y, TITLE_W = 0.55, 0.32, 8.45
BODY_TOP, BODY_BOTTOM = 1.4, 6.75
LEFT_X, LEFT_W = L, 6.55
RIGHT_X, RIGHT_W = 7.5, R - 7.5
TABLE_PT = 11
_PAGED: set[int] = set()  # slide_id slide isi yang diberi nomor halaman
STATUS_PENANDA = [("Selesai", P.TL_GREEN), ("Dalam proses", P.TL_YELLOW), ("Terbuka", P.TL_RED)]


# ----------------------------------------------------------------- data
def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def text_of(value: Any, sep: str = "; ") -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return sep.join(str(x) for x in value if x not in (None, ""))
    return str(value)


def compact(value: Any, limit: int = 180) -> str:
    s = " ".join(text_of(value).split())
    if len(s) <= limit:
        return s
    s = s[: max(0, limit - 1)].rstrip()
    if " " in s[limit // 2:]:  # potong di batas kata, bukan di tengah kata
        s = s[: s.rfind(" ")].rstrip(" ,;:")
    if s.count("*") % 2:  # jangan memotong markup miring di tengah
        s = s[: s.rfind("*")].rstrip()
    return s + "…"


def report_title(d: dict[str, Any]) -> str:
    return d.get("report_title") or d.get("title") or "Kajian Teknis Geothermal"


def project_name(d: dict[str, Any]) -> str:
    return d.get("project_name") or d.get("subtitle") or ""


def executive_messages(d: dict[str, Any]) -> list[str]:
    msgs = d.get("executive_summary") or d.get("summary_messages") or []
    if isinstance(msgs, str):
        parts = [x.strip() for x in msgs.replace("\r", "\n").split("\n") if x.strip()]
        return parts or [msgs]
    return [text_of(x) for x in as_list(msgs)]


def normalize_finding(f: dict[str, Any]) -> dict[str, Any]:
    return {
        **f,
        "discipline": f.get("discipline", ""),
        "location": f.get("location") or f.get("target_location") or "",
        "comment": f.get("comment") or f.get("recommendation") or "",
        "basis": f.get("basis", ""),
        "source": f.get("source") or f.get("technical_basis") or "",
        "status": f.get("status", "Open"),
        "impact": f.get("impact") or f.get("potential_impact") or "",
    }


def findings_of(d: dict[str, Any]) -> list[dict[str, Any]]:
    return [normalize_finding(f) for f in as_list(d.get("findings")) if isinstance(f, dict)]


def priority_level(priority: str) -> str:
    """Kenali prioritas dalam bahasa Inggris maupun Indonesia."""
    p = (priority or "").strip().lower()
    if p.startswith(("h", "critical", "major", "tinggi", "kritis")):
        return "high"
    if p.startswith(("m", "sedang")):
        return "medium"
    return "low"


def status_key(status: str) -> str:
    """Petakan status bebas ke penanda: ok (selesai), proses, belum (terbuka)."""
    s = (status or "").strip().lower()
    if any(k in s for k in ("closed", "selesai", "tutup", "no material", "accepted", "diterima")):
        return "ok"
    if any(k in s for k in ("progress", "proses", "conditional", "bersyarat", "partial", "sebagian")):
        return "proses"
    return "belum"


def is_closed(status: str) -> bool:
    return status_key(status) == "ok"


# ----------------------------------------------------------------- slide dasar
def background(slide, path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Aset master tidak ditemukan: {path}")
    slide.shapes.add_picture(str(path), 0, 0, width=Inches(SW), height=Inches(SH))


def content_slide(prs, topik: str, subtopik: str = ""):
    """Slide isi: master geothermal + judul dua warna (topik biru, sub-topik hitam)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    background(slide, MASTER_CONTENT)
    teks = f"{topik} {subtopik}".strip()
    size = 22
    if P._title_lines(teks, TITLE_W, size) > 2:
        size = 18
    box = slide.shapes.add_textbox(Inches(TITLE_X), Inches(TITLE_Y), Inches(TITLE_W), Inches(0.9))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    P._fill_runs(p, topik, size, P.PRIMARY, bold=True)
    if subtopik:
        P._fill_runs(p, " " + subtopik, size, P.INK, bold=True)
    _PAGED.add(slide.slide_id)
    return slide


def add_source(slide, teks: str):
    """Satu baris sumber (pola TVV) untuk slide yang memuat bukti teknis."""
    if teks:
        T.add_sumber(slide, compact(teks, 200))


def caption(slide, teks: str, x: float = L, w: float = CW):
    """Keterangan singkat cara membaca grafis, di bawah konten (pola PLN IP)."""
    P.add_keterangan_bawah(slide, teks, x=x, w=w, size=12)


def clean(teks: Any) -> str:
    """Simbol panah/dekoratif dari input diganti tanda baca biasa (aturan anti-dekorasi)."""
    out = text_of(teks)
    for sym, rep_ in (("↔", " / "), ("→", " ke "), ("⇒", " ke "), ("✅", ""), ("⏳", ""), ("❌", "")):
        out = out.replace(sym, rep_)
    return " ".join(out.split())


def status_legend(slide, x: float, y: float):
    G.add_legend(slide, [(lab, col, "bulat") for lab, col in STATUS_PENANDA], x, y, size=10)


def status_cell(status: str) -> dict[str, Any]:
    return {"text": "", "status": status_key(status)}


def table_pages(rows: list, per_page: int) -> list[list]:
    return [rows[i:i + per_page] for i in range(0, len(rows), per_page)] or [[]]


def text_height(teks: str, w_in: float, pt: float) -> float:
    """Perkiraan tinggi teks (inci) agar bagian berikutnya tidak berjarak terlalu jauh."""
    chars = max(20, int(w_in * 72 / (pt * 0.5)))
    lines = max(1, -(-len(teks) // chars))
    return lines * pt * 1.25 / 72 + 0.05


def number_pages(prs):
    n = 0
    for slide in prs.slides:
        n += 1
        if slide.slide_id in _PAGED:
            P.add_text(slide, str(n), 12.0, 7.08, 0.78, 0.22, size=9, color=P.GRAY, align=PP_ALIGN.RIGHT)


# ----------------------------------------------------------------- slide
def add_cover(prs, d: dict[str, Any]):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    background(slide, MASTER_COVER)
    P.add_text(slide, report_title(d), 0.67, 1.15, 7.75, 1.55, size=28, color=P.DARK, bold=True)
    if project_name(d):
        P.add_text(slide, project_name(d), 0.69, 3.16, 6.8, 0.58, size=15, color=P.INK)
    meta = " | ".join(x for x in [f"No. {d.get('report_no')}" if d.get("report_no") else "",
                                    f"Rev. {d.get('revision')}" if d.get("revision") not in (None, "") else "",
                                    text_of(d.get("date"))] if x)
    if meta:
        P.add_text(slide, meta, 0.69, 4.02, 6.8, 0.35, size=11, color=P.PRIMARY, bold=True)


def add_summary(prs, d: dict[str, Any]):
    slide = content_slide(prs, "Ringkasan Eksekutif", "Hasil Kajian Teknis")
    findings = findings_of(d)
    high = sum(1 for f in findings if priority_level(f.get("priority", "")) == "high")
    open_n = sum(1 for f in findings if not is_closed(f.get("status", "")))
    gaps = as_list(d.get("data_gaps"))
    G.add_kpi_row(slide, [
        {"nilai": str(len(findings)), "label": "Total temuan", "ket": "seluruh disiplin"},
        {"nilai": str(high), "label": "Prioritas tinggi", "ket": "perlu diselesaikan lebih dulu"},
        {"nilai": str(open_n), "label": "Masih terbuka", "ket": "belum ada bukti penyelesaian"},
        {"nilai": str(len(gaps)), "label": "Data gap", "ket": "data atau klarifikasi yang diperlukan"},
    ], L, BODY_TOP, CW, h=1.45, size=32)
    msgs = executive_messages(d) or ["Kajian dilakukan terhadap dokumen yang tersedia dengan bukti terpilih dari *knowledge base*."]
    y = P.add_column_head(slide, "Pesan utama", L, 3.15, CW)
    items: list[Any] = [compact(m, 230) for m in msgs[:4]]
    overall = text_of(d.get("overall_status"))
    if overall:
        items.append({"text": f"Status kajian: {overall}", "bold": True})
    P.add_bullets(slide, items, L, y, CW, 0.42 * len(items) + 0.2, size=13)
    caption(slide, "Angka kunci dihitung dari daftar temuan dan *data gap* pada kajian ini.")


def add_agenda(prs):
    slide = content_slide(prs, "Agenda", "Struktur Kajian Teknis")
    items = ["Tujuan, Lingkup, dan Dasar Kajian", "Dokumen yang Dikaji", "Metodologi dan Klasifikasi Komentar",
             "Temuan Teknis dan Komentar Reviewer", "Risiko Utama dan Keterkaitan Antardisiplin",
             "*Data Gap*, Klarifikasi, dan Asumsi", "Rencana Tindak Lanjut", "Kesimpulan dan Status Penyelesaian"]
    for i, label in enumerate(items):
        col, row = i % 2, i // 2
        x = L + col * 6.2
        y = BODY_TOP + 0.15 + row * 1.15
        P.add_text(slide, f"{i + 1:02d}", x, y, 0.8, 0.5, size=24, color=P.PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        P.add_text(slide, label, x + 0.9, y, 5.0, 0.5, size=15, color=P.INK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        G._line(slide.shapes, x, y + 0.72, x + 5.8, y + 0.72, P.OUTLINE, 0.75)


def has_control(d: dict[str, Any]) -> bool:
    return any(d.get(k) not in (None, "", []) for k in ("report_no", "revision", "prepared_by", "reviewed_by", "approved_by"))


def add_control(prs, d: dict[str, Any]):
    slide = content_slide(prs, "Pengendalian Dokumen", "Identitas dan Revisi Kajian")
    rows = [[lab, text_of(d.get(k)) or {"text": "", "na": True}] for lab, k in [
        ("No. laporan / kajian", "report_no"), ("Revisi", "revision"), ("Tanggal terbit", "date"),
        ("Disusun oleh", "prepared_by"), ("Diperiksa oleh", "reviewed_by"), ("Disetujui oleh", "approved_by")]]
    T.add_tabel(slide, ["Parameter", "Keterangan"], rows, L, BODY_TOP, 8.0, col_w=[2.6, 5.4], size=13)


def add_scope(prs, d: dict[str, Any]):
    slide = content_slide(prs, "Tujuan dan Lingkup", "Dasar Pelaksanaan Kajian")
    y = P.add_column_head(slide, "Tujuan kajian", L, BODY_TOP, CW)
    P.add_text(slide, compact(d.get("objective") or "Tujuan kajian belum disebutkan.", 300), L, y, CW, 0.8, size=13)
    y2 = BODY_TOP + 1.65
    ya = P.add_column_head(slide, "Lingkup kajian", LEFT_X, y2, LEFT_W - 0.3)
    scope = as_list(d.get("scope") or d.get("coverage")) or ["Lingkup belum disebutkan"]
    P.add_bullets(slide, [compact(x, 160) for x in scope[:7]], LEFT_X, ya, LEFT_W - 0.3, 3.0, size=13)
    yb = P.add_column_head(slide, "Dasar kajian dan keterbatasan", RIGHT_X - 0.4, y2, RIGHT_W + 0.4)
    basis = as_list(d.get("review_basis") or d.get("evidence_basis")) or [
        "Dokumen yang dikaji dan bukti terpilih dari *knowledge base* geothermal"]
    items = [compact(x, 160) for x in basis[:5]] + [{"text": "Keterbatasan: " + compact(x, 150)} for x in as_list(d.get("limitations"))[:2]]
    P.add_bullets(slide, items, RIGHT_X - 0.4, yb, RIGHT_W + 0.4, 3.0, size=13)


def add_documents(prs, d: dict[str, Any]):
    docs = [x for x in as_list(d.get("documents_reviewed")) if isinstance(x, dict)]
    rows = [[text_of(x.get("title")), text_of(x.get("number") or x.get("code")) or {"text": "", "na": True},
             text_of(x.get("revision")) or {"text": "", "na": True}, text_of(x.get("date")) or {"text": "", "na": True},
             text_of(x.get("discipline")), text_of(x.get("scope") or x.get("status"))] for x in docs]
    if not rows:
        rows = [["Dokumen yang dikaji belum dicatat pada data input", "", "", "", "", ""]]
    pages = table_pages(rows, 8)
    for i, chunk in enumerate(pages):
        sub = "Daftar Dokumen" + (f" ({i + 1}/{len(pages)})" if len(pages) > 1 else "")
        slide = content_slide(prs, "Dokumen yang Dikaji", sub)
        T.add_tabel(slide, ["Judul dokumen", "No./kode", "Rev.", "Tanggal", "Disiplin", "Lingkup / status kajian"],
                    chunk, L, BODY_TOP, CW, col_w=[4.2, 1.8, 0.7, 1.4, 1.5, 2.6], size=TABLE_PT, gaya="data")


def add_methodology(prs, d: dict[str, Any]):
    slide = content_slide(prs, "Metodologi Kajian", "Alur Pemeriksaan dan Klasifikasi")
    custom = [text_of(x) for x in as_list(d.get("methodology")) if text_of(x)]
    if custom:
        langkah = [{"judul": f"Langkah {i + 1}", "sub": compact(t, 110)} for i, t in enumerate(custom[:5])]
    else:
        langkah = [
            {"judul": "Pahami dokumen", "sub": "Identifikasi klaim dan keputusan teknis yang perlu diperiksa"},
            {"judul": "Telusuri KB", "sub": "Ambil bukti yang relevan saja dari *knowledge base*"},
            {"judul": "Uji konsistensi", "sub": "Narasi, tabel, gambar, perhitungan, satuan, dan revisi"},
            {"judul": "Klasifikasi", "sub": "Temuan, *data gap*, dan tindak lanjut yang dapat ditelusuri"},
        ]
    G.add_flow(slide, langkah, L, BODY_TOP + 0.1, CW, h=1.45)
    classes = d.get("comment_classification")
    if isinstance(classes, dict):
        rows = [[k, text_of(v)] for k, v in classes.items()]
        header = ["Klasifikasi", "Arti"]
        col_w = [2.6, 9.6]
    else:
        header = ["Klasifikasi", "Arti", "Perlakuan"]
        col_w = [2.4, 5.4, 4.4]
        rows = [
            ["Prioritas tinggi", "Isu teknis material yang memengaruhi keselamatan, integritas sumur, atau keputusan utama", "Diselesaikan sebelum tahap berikutnya"],
            ["Prioritas sedang", "Perlu perbaikan atau klarifikasi yang memengaruhi desain, biaya, atau jadwal", "Diselesaikan sebelum dinyatakan selesai"],
            ["Prioritas rendah", "Perbaikan minor yang tidak mengubah dasar keputusan", "Dicatat untuk revisi berikutnya"],
            ["*Data gap*", "Bukti belum cukup untuk kesimpulan yang pasti", "Dilengkapi oleh pemilik data"],
        ]
    T.add_tabel(slide, header, rows, L, BODY_TOP + 2.0, CW, col_w=col_w, size=12)
    caption(slide, "Alur di atas menunjukkan urutan pemeriksaan; tabel menjelaskan arti setiap klasifikasi komentar.")


def add_distribution(prs, d: dict[str, Any]):
    findings = findings_of(d)
    if len(findings) < 2:
        return
    disciplines: list[str] = []
    for f in findings:
        key = f.get("discipline") or "Lainnya"
        if key not in disciplines:
            disciplines.append(key)
    levels = [("Tinggi", "high"), ("Sedang", "medium"), ("Rendah", "low")]
    series = [(lab, [sum(1 for f in findings if (f.get("discipline") or "Lainnya") == disc
                         and priority_level(f.get("priority", "")) == lv) for disc in disciplines])
              for lab, lv in levels]
    series = [s for s in series if sum(s[1])] or series[:1]
    slide = content_slide(prs, "Sebaran Temuan", "per Disiplin dan Prioritas")
    y = P.add_column_head(slide, "Jumlah temuan per disiplin", LEFT_X, BODY_TOP, LEFT_W + 0.4)
    h = min(4.9, 0.75 + 0.55 * len(disciplines))
    colors = {"Tinggi": P.DARK, "Sedang": P.PRIMARY, "Rendah": P.TINT}
    G.add_stacked_chart(slide, disciplines, series, LEFT_X, y, LEFT_W + 0.4, h, horizontal=True,
                        colors=[colors[s[0]] for s in series])
    top = sorted(((sum(1 for f in findings if (f.get("discipline") or "Lainnya") == disc), disc) for disc in disciplines), reverse=True)
    ket = [f"Batang menunjukkan jumlah temuan per disiplin, dipisah menurut prioritas.",
           f"Disiplin dengan temuan terbanyak: {top[0][1]} ({top[0][0]} temuan)."]
    P.add_keterangan(slide, ket, RIGHT_X + 0.1, BODY_TOP + 0.6, RIGHT_W - 0.1)


def add_findings_overview(prs, d: dict[str, Any]):
    findings = findings_of(d)
    order = {"high": 0, "medium": 1, "low": 2}
    findings = sorted(findings, key=lambda f: order[priority_level(f.get("priority", ""))])
    rows = [[f.get("id", ""), f.get("discipline", ""), compact(f.get("title") or f.get("finding", ""), 150),
             f.get("priority", "") or {"text": "", "na": True}, status_cell(f.get("status", "")),
             compact(f.get("location", ""), 70)] for f in findings]
    if not rows:
        rows = [["—", "—", "Belum ada temuan pada data hasil kajian", "—", {"text": "", "na": True}, "—"]]
    pages = table_pages(rows, 6)
    for i, chunk in enumerate(pages):
        sub = "Daftar Temuan dan Status" + (f" ({i + 1}/{len(pages)})" if len(pages) > 1 else "")
        slide = content_slide(prs, "Temuan Teknis", sub)
        t = T.add_tabel(slide, ["ID", "Disiplin", "Temuan", "Prioritas", "Status", "Lokasi di dokumen"], chunk,
                        L, BODY_TOP, CW, col_w=[0.8, 1.5, 5.0, 1.2, 0.9, 2.8], size=TABLE_PT,
                        rata=["l", "l", "l", "l", "c", "l"])
        status_legend(slide, L, min(t["bawah"] + 0.15, 6.55))


def add_finding_detail(prs, f0: dict[str, Any]):
    f = normalize_finding(f0)
    title = compact(f.get("title") or f.get("finding") or "Temuan teknis", 95)
    slide = content_slide(prs, f.get("id") or "Temuan", title)
    T.add_tabel(slide, ["Disiplin", "Prioritas", "Status", "Tingkat keyakinan", "Lokasi di dokumen"],
                [[f.get("discipline") or {"text": "", "na": True}, f.get("priority") or {"text": "", "na": True},
                  f.get("status") or "Open", f.get("confidence") or {"text": "", "na": True},
                  compact(f.get("location"), 80) or {"text": "", "na": True}]],
                L, BODY_TOP, CW, col_w=[1.8, 1.4, 1.4, 1.8, 5.8], size=TABLE_PT)
    y = BODY_TOP + 1.05
    for head, body in [("Temuan / observasi", f.get("finding")), ("Komentar dan rekomendasi reviewer", f.get("comment")),
                       ("Alasan dan potensi dampak", f.get("impact"))]:
        y2 = P.add_column_head(slide, head, LEFT_X, y, LEFT_W, size=13)
        teks = compact(body or "Belum dinyatakan.", 330)
        h = text_height(teks, LEFT_W, 12)
        P.add_text(slide, teks, LEFT_X, y2, LEFT_W, h, size=12)
        y = y2 + h + 0.3
    yr = P.add_column_head(slide, "Dasar teknis dan bukti", RIGHT_X, BODY_TOP + 1.05, RIGHT_W, size=13)
    img = f.get("image_path")
    if img and os.path.exists(str(img)):
        T.fit_picture(slide, str(img), RIGHT_X, yr, RIGHT_W, 2.3)
        yr += 2.45
    P.add_text(slide, compact(f.get("basis") or "Belum dinyatakan.", 300), RIGHT_X, yr, RIGHT_W, 1.6, size=12)
    add_source(slide, ("Sumber: " + f["source"]) if f.get("source") else "")


def add_risks(prs, d: dict[str, Any]):
    risks = as_list(d.get("key_risks"))
    slide = content_slide(prs, "Risiko Utama", "Keterkaitan Antardisiplin")
    if not risks:
        P.add_text(slide, "Belum ada risiko keterkaitan antardisiplin yang dicatat pada data hasil kajian.",
                   L, BODY_TOP, CW, 0.5, size=13)
        return
    dict_risks = [r for r in risks if isinstance(r, dict)]
    scored = [r for r in dict_risks if str(r.get("likelihood") or r.get("kemungkinan") or "").isdigit()
              and str(r.get("severity") or r.get("dampak_level") or "").isdigit()]
    rows = []
    for i, r in enumerate(risks[:6], 1):
        if isinstance(r, dict):
            rows.append([str(i), compact(clean(r.get("interface") or r.get("title") or "—"), 60),
                         compact(clean(r.get("risk") or r.get("issue") or ""), 140),
                         compact(r.get("impact") or r.get("consequence") or "", 110) or {"text": "", "na": True},
                         compact(r.get("mitigation") or r.get("mitigasi") or "", 120) or {"text": "", "na": True},
                         text_of(r.get("related_findings") or r.get("finding_id")) or {"text": "", "na": True}])
        else:
            rows.append([str(i), "—", compact(r, 160), {"text": "", "na": True}, {"text": "", "na": True}, {"text": "", "na": True}])
    if scored:
        sebaran: dict[tuple[int, int], list[int]] = {}
        for i, r in enumerate(risks[:6], 1):
            if r in scored:
                k = int(r.get("likelihood") or r.get("kemungkinan"))
                s = int(r.get("severity") or r.get("dampak_level"))
                sebaran.setdefault((max(1, min(5, k)), max(1, min(5, s))), []).append(i)
        T.add_matriks_risiko(slide, sebaran, L, BODY_TOP, 5.2, 5.2, judul="Peta risiko (nomor = baris tabel)")
        T.add_tabel(slide, ["No.", "Keterkaitan", "Risiko", "Mitigasi"], [[r[0], r[1], r[2], r[4]] for r in rows],
                    6.0, BODY_TOP, R - 6.0, col_w=[0.5, 1.5, 2.6, 2.2], size=10)
        caption(slide, "Nomor pada peta merujuk baris tabel; warna sel menunjukkan tingkat risiko dari rendah (hijau) "
                       "hingga tinggi (merah).", x=6.0, w=R - 6.0)
    else:
        T.add_tabel(slide, ["No.", "Keterkaitan", "Risiko", "Dampak", "Mitigasi", "Temuan terkait"], rows,
                    L, BODY_TOP, CW, col_w=[0.5, 1.9, 3.4, 2.5, 2.8, 1.1], size=TABLE_PT)


def add_gaps(prs, d: dict[str, Any]):
    rows = []
    for i, g in enumerate(as_list(d.get("data_gaps"))):
        if isinstance(g, dict):
            rows.append([text_of(g.get("id") or f"DG-{i + 1:02d}"), compact(g.get("gap") or g.get("item"), 140),
                         compact(g.get("impact"), 110) or {"text": "", "na": True},
                         compact(g.get("required") or g.get("evidence"), 110) or {"text": "", "na": True},
                         text_of(g.get("owner") or g.get("pic")) or {"text": "", "na": True}, status_cell(text_of(g.get("status"))) ])
        else:
            rows.append([f"DG-{i + 1:02d}", compact(g, 140), {"text": "", "na": True}, {"text": "", "na": True},
                         {"text": "", "na": True}, status_cell("open")])
    if not rows:
        rows = [["—", "Tidak ada *data gap* material yang tercatat", "—", "—", "—", {"text": "", "na": True}]]
    pages = table_pages(rows, 6)
    for i, chunk in enumerate(pages):
        sub = "Klarifikasi dan Asumsi" + (f" ({i + 1}/{len(pages)})" if len(pages) > 1 else "")
        slide = content_slide(prs, "*Data Gap*", sub)
        t = T.add_tabel(slide, ["ID", "Data yang belum tersedia / belum jelas", "Dampak bila tidak dipenuhi",
                                "Bukti yang diperlukan", "PIC", "Status"], chunk, L, BODY_TOP, CW,
                        col_w=[0.8, 3.7, 2.8, 2.8, 1.3, 0.8], size=TABLE_PT, rata=["l", "l", "l", "l", "l", "c"])
        status_legend(slide, L, min(t["bawah"] + 0.15, 6.55))


def add_actions(prs, d: dict[str, Any]):
    rows = []
    for i, a in enumerate(as_list(d.get("actions"))):
        if isinstance(a, dict):
            rows.append([text_of(a.get("id") or f"A-{i + 1:02d}"), text_of(a.get("finding_id") or a.get("related_findings")) or {"text": "", "na": True},
                         compact(a.get("action"), 150), text_of(a.get("pic") or a.get("owner")) or {"text": "", "na": True},
                         text_of(a.get("due") or a.get("timing")) or {"text": "", "na": True},
                         compact(a.get("evidence") or a.get("closure_evidence"), 100) or {"text": "", "na": True},
                         status_cell(text_of(a.get("status")))])
        else:
            rows.append([f"A-{i + 1:02d}", {"text": "", "na": True}, compact(a, 150), {"text": "", "na": True},
                         {"text": "", "na": True}, {"text": "", "na": True}, status_cell("open")])
    if not rows:
        rows = [["A-01", "—", "Tetapkan tindak lanjut untuk temuan material dan *data gap*", "—", "—", "—", status_cell("open")]]
    pages = table_pages(rows, 6)
    for i, chunk in enumerate(pages):
        sub = "Penyelesaian Komentar" + (f" ({i + 1}/{len(pages)})" if len(pages) > 1 else "")
        slide = content_slide(prs, "Rencana Tindak Lanjut", sub)
        t = T.add_tabel(slide, ["ID", "Temuan", "Tindakan yang diperlukan", "PIC", "Target", "Bukti penyelesaian", "Status"],
                        chunk, L, BODY_TOP, CW, col_w=[0.8, 0.9, 4.2, 1.5, 1.3, 2.6, 0.9], size=TABLE_PT,
                        rata=["l", "l", "l", "l", "l", "l", "c"])
        status_legend(slide, L, min(t["bawah"] + 0.15, 6.55))


def add_conclusion(prs, d: dict[str, Any]):
    slide = content_slide(prs, "Kesimpulan", "Status Penyelesaian Kajian")
    findings = findings_of(d)
    actions = [a for a in as_list(d.get("actions"))]
    gaps = [g for g in as_list(d.get("data_gaps"))]

    def done(items, key="status"):
        return sum(1 for x in items if isinstance(x, dict) and is_closed(text_of(x.get(key))))

    y = P.add_column_head(slide, "Kemajuan penyelesaian", LEFT_X, BODY_TOP, LEFT_W)
    baris = []
    for label, items in (("Temuan", findings), ("Tindak lanjut", actions), ("*Data gap*", gaps)):
        if items:
            n_done = done(items)
            baris.append({"label": label, "nilai": round(100 * n_done / len(items)),
                          "ket": f"{n_done} dari {len(items)} selesai"})
    if baris:
        G.add_progress(slide, baris, LEFT_X, y + 0.1, LEFT_W, row_h=0.62, label_w=1.8, nilai_w=0.8)
        y += 0.25 + 0.62 * len(baris)
        P.add_keterangan(slide, "Persentase item berstatus selesai terhadap seluruh item pada tiap kelompok.",
                         LEFT_X, y + 0.05, LEFT_W, size=11)
        y += 0.3
    status = text_of(d.get("overall_status")) or "Belum dinyatakan"
    P.add_text(slide, f"Status kajian: **{status}**", LEFT_X, y + 0.35, LEFT_W, 0.35, size=14, color=P.INK)
    yr = P.add_column_head(slide, "Kesimpulan kajian", RIGHT_X - 0.2, BODY_TOP, RIGHT_W + 0.2)
    P.add_text(slide, compact(d.get("conclusion") or "Kesimpulan belum disertakan.", 420), RIGHT_X - 0.2, yr,
               RIGHT_W + 0.2, 2.0, size=13)
    conditions = as_list(d.get("conditions_to_proceed") or d.get("closeout_conditions"))
    if conditions:
        yc = P.add_column_head(slide, "Syarat untuk melanjutkan", RIGHT_X - 0.2, BODY_TOP + 2.75, RIGHT_W + 0.2)
        P.add_bullets(slide, [compact(c, 140) for c in conditions[:4]], RIGHT_X - 0.2, yc, RIGHT_W + 0.2, 2.2, size=12)


def add_references(prs, d: dict[str, Any]):
    refs = [text_of(r) for r in as_list(d.get("references_used") or d.get("references")) if text_of(r)]
    if not refs:
        refs = sorted({f.get("source", "") for f in findings_of(d) if f.get("source")})
    slide = content_slide(prs, "Lampiran", "Sumber yang Digunakan")
    if refs:
        rows = [[f"{i:02d}", compact(r, 200)] for i, r in enumerate(refs[:12], 1)]
        T.add_tabel(slide, ["No.", "Sumber (file dan halaman/slide)"], rows, L, BODY_TOP, CW, col_w=[0.7, 11.5],
                    size=TABLE_PT, sumbu=False)
    else:
        P.add_text(slide, "Daftar sumber belum disertakan pada data hasil kajian.", L, BODY_TOP, CW, 0.4, size=13)
    add_source(slide, "Hanya sumber yang benar-benar dibuka dan dipakai sebagai bukti teknis yang dicantumkan.")


def add_closing(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    background(slide, MASTER_CLOSING)


def build(data: dict[str, Any], out_path: str, extra=None):
    """extra: fungsi opsional extra(prs, data) untuk menyisipkan slide tambahan
    (gantt, stage-gate, peta, dll.) sebelum slide kesimpulan."""
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    add_cover(prs, data)
    add_summary(prs, data)
    if data.get("include_agenda", True):
        add_agenda(prs)
    if has_control(data) and data.get("include_review_control", True):
        add_control(prs, data)
    add_scope(prs, data)
    add_documents(prs, data)
    add_methodology(prs, data)
    add_distribution(prs, data)
    add_findings_overview(prs, data)
    detail_limit = int(data.get("ppt_detail_limit", 6) or 6)
    for f in [x for x in as_list(data.get("findings")) if isinstance(x, dict)][:detail_limit]:
        add_finding_detail(prs, f)
    add_risks(prs, data)
    add_gaps(prs, data)
    add_actions(prs, data)
    if extra:
        extra(prs, data)
    add_conclusion(prs, data)
    add_references(prs, data)
    add_closing(prs)
    number_pages(prs)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    prs.save(out_path)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    build(data, sys.argv[2])
    print(sys.argv[2])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
