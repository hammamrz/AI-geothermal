#!/usr/bin/env python3
"""Build a lightweight PLN IP-style geothermal technical review PPTX from structured JSON.

The generator mirrors the formal Technical Review / Comment Sheet Report backbone:
cover -> executive summary -> agenda -> review control (optional) -> scope/basis ->
documents reviewed -> methodology -> findings -> cross-discipline risks -> data gaps ->
action/comment resolution -> conclusion/closeout -> sources -> closing.

Usage:
    python build_review_ppt.py review.json output.pptx

Preferred JSON (v0.5.2):
{
  "report_title": "TECHNICAL REVIEW PRESENTATION",
  "project_name": "Project / Field Name",
  "report_no": "TR-001",
  "revision": "0",
  "date": "30 September 2026",
  "prepared_by": "...",
  "reviewed_by": "...",
  "approved_by": "...",
  "executive_summary": ["...", "..."],
  "objective": "...",
  "scope": ["..."],
  "review_basis": ["..."],
  "documents_reviewed": [
    {"title":"...","number":"...","revision":"...","date":"...","discipline":"Drilling","scope":"..."}
  ],
  "findings": [
    {
      "id":"F-001","discipline":"Drilling","location":"Doc A p.34",
      "finding":"...","comment":"...","impact":"...","basis":"...",
      "source":"KB file p.20-22","priority":"High","status":"Open",
      "confidence":"High","image_path":null
    }
  ],
  "key_risks": [
    {"risk":"Resource confirmation below development target","interface":"Subsurface ↔ Development","impact":"Staging basis may need revision","related_findings":"F-001"}
  ],
  "data_gaps": [
    {"id":"DG-01","gap":"...","impact":"...","required":"...","owner":"...","status":"Open"}
  ],
  "actions": [
    {"id":"A-01","finding_id":"F-001","action":"...","pic":"...","due":"...","evidence":"...","status":"Open"}
  ],
  "conclusion":"...",
  "overall_status":"Revision Required",
  "references_used":["..."]
}

Backward-compatible aliases from the previous presentation generator are also accepted.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

C = {
    "deep_teal": "1F7292", "pln_blue": "006699", "energy_teal": "0DAD8E",
    "light_aqua": "68CFD6", "dark_teal": "205A72", "yellow": "FFFF00",
    "sky_blue": "3CAFF2", "white": "FFFFFF", "near_white": "F6F8F9",
    "light_gray": "D9E2E6", "mid_gray": "7A8790", "charcoal": "263238",
    "high": "C00000", "medium": "FFC000", "low": "0DAD8E",
}
FONT = "Helvetica"
SW, SH = 13.333, 7.5
ASSET_DIR = Path(__file__).resolve().parent.parent / "references" / "master_assets"
MASTER_COVER = ASSET_DIR / "MASTER_COVER.jpg"
MASTER_CONTENT = ASSET_DIR / "MASTER_CONTENT.jpg"
MASTER_CLOSING = ASSET_DIR / "MASTER_CLOSING.jpg"


def rgb(hexstr: str) -> RGBColor:
    return RGBColor.from_string(hexstr.replace("#", ""))


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def text_of(value: Any, sep: str = " • ") -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return sep.join(str(x) for x in value if x not in (None, ""))
    return str(value)


def compact(value: Any, limit: int = 180) -> str:
    s = " ".join(text_of(value).split())
    return s if len(s) <= limit else s[: max(0, limit - 1)].rstrip() + "…"


def add_master_background(slide, master_path: Path):
    if not master_path.exists():
        raise FileNotFoundError(f"Missing bundled master asset: {master_path}")
    slide.shapes.add_picture(str(master_path), 0, 0, width=Inches(SW), height=Inches(SH))


def add_text(slide, text: str, x: float, y: float, w: float, h: float,
             size: float = 18, bold: bool = False, color: str = C["charcoal"],
             align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear(); tf.word_wrap = True; tf.vertical_anchor = valign
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = str(text or "")
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = rgb(color)
    return box


def add_rect(slide, x, y, w, h, fill, line=None, radius=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill); sh.line.color.rgb = rgb(line or fill)
    return sh


def add_header(slide, title: str, section: str | None = None):
    if section:
        add_text(slide, section.upper(), 0.55, 0.17, 2.65, 0.24, 7.0, True, C["deep_teal"])
    add_text(slide, title, 0.55, 0.42, 8.35, 0.62, 22, True, C["dark_teal"])
    add_rect(slide, 0.55, 1.07, 8.35, 0.035, C["light_aqua"])


def add_footer(slide, page_num: int, source_text: str = ""):
    if source_text:
        add_text(slide, compact(source_text, 210), 0.55, 7.03, 10.95, 0.24, 6.6, False, C["mid_gray"])
    add_text(slide, str(page_num), 12.2, 7.03, 0.55, 0.22, 7, True, C["deep_teal"], PP_ALIGN.RIGHT)


def priority_color(priority: str) -> str:
    p = (priority or "").strip().lower()
    if p.startswith("h") or p.startswith("critical") or p.startswith("major"):
        return C["high"]
    if p.startswith("m"):
        return C["medium"]
    return C["low"]


def status_color(status: str) -> str:
    s = (status or "").strip().lower()
    if "closed" in s or "no material" in s:
        return C["energy_teal"]
    if "conditional" in s:
        return C["pln_blue"]
    if "revision" in s or "open" in s:
        return C["high"]
    return C["deep_teal"]


def add_bullet_list(slide, items: Iterable[Any], x: float, y: float, w: float, h: float,
                    size: float = 11.0, color: str = C["charcoal"], max_items: int = 6):
    items = [compact(i, 220) for i in list(items)[:max_items] if text_of(i).strip()]
    if not items:
        items = ["Not provided"]
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame; tf.clear(); tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {item}"; p.font.name = FONT; p.font.size = Pt(size); p.font.color.rgb = rgb(color)
        p.space_after = Pt(5)
    return box


def add_table(slide, cols: list[tuple[str, float]], rows: list[list[str]], x: float, y: float,
              header_h: float = 0.44, row_h: float = 0.62, font_size: float = 7.8,
              priority_col: int | None = None, status_col: int | None = None):
    xx = x
    for name, width in cols:
        add_rect(slide, xx, y, width, header_h, C["dark_teal"])
        add_text(slide, name, xx + 0.06, y + 0.07, width - 0.12, header_h - 0.09, font_size + 0.5, True, C["white"])
        xx += width
    for ri, row in enumerate(rows):
        yy = y + header_h + ri * row_h
        xx = x; fill = C["white"] if ri % 2 == 0 else C["near_white"]
        for ci, ((_, width), val) in enumerate(zip(cols, row)):
            add_rect(slide, xx, yy, width, row_h, fill, C["light_gray"])
            color = C["charcoal"]
            if priority_col is not None and ci == priority_col:
                color = priority_color(val)
            if status_col is not None and ci == status_col:
                color = status_color(val)
            add_text(slide, compact(val, 145), xx + 0.05, yy + 0.07, width - 0.1, row_h - 0.1,
                     font_size, ci in tuple(i for i in (priority_col, status_col) if i is not None), color)
            xx += width


def report_title(d: dict[str, Any]) -> str:
    return d.get("report_title") or d.get("title") or "Geothermal Technical Review"


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


def add_cover(prs: Presentation, d: dict[str, Any]):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_COVER)
    add_text(slide, report_title(d), 0.67, 1.15, 7.75, 1.55, 28, True, C["dark_teal"])
    add_text(slide, project_name(d), 0.69, 3.16, 6.8, 0.58, 14.5, False, C["charcoal"])
    meta = " | ".join(x for x in [f"No. {d.get('report_no')}" if d.get('report_no') else "",
                                     f"Rev. {d.get('revision')}" if d.get('revision') not in (None, "") else "",
                                     text_of(d.get("date"))] if x)
    add_text(slide, meta, 0.69, 4.02, 6.8, 0.35, 9.5, True, C["deep_teal"])


def add_summary(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Executive review summary", "Review")
    findings = [normalize_finding(f) for f in as_list(d.get("findings")) if isinstance(f, dict)]
    counts = Counter((f.get("priority") or "Unrated").title() for f in findings)
    open_count = sum(1 for f in findings if "closed" not in str(f.get("status", "")).lower())
    cards = [
        ("Total findings", len(findings), C["pln_blue"]),
        ("High", counts.get("High", 0), C["high"]),
        ("Open", open_count, C["medium"]),
        ("Data gaps", len(as_list(d.get("data_gaps"))), C["energy_teal"]),
    ]
    for i, (label, val, col) in enumerate(cards):
        x = 0.65 + i * 3.05
        add_rect(slide, x, 1.35, 2.65, 1.05, C["near_white"], C["light_gray"], True)
        add_rect(slide, x, 1.35, 0.08, 1.05, col)
        add_text(slide, str(val), x + 0.2, 1.48, 0.8, 0.45, 24, True, col)
        add_text(slide, label, x + 1.0, 1.6, 1.4, 0.35, 9.5, True, C["charcoal"])
    msgs = executive_messages(d) or ["Review completed against the available target document and selected embedded-KB evidence."]
    y = 2.78
    for n, msg in enumerate(msgs[:4], 1):
        add_rect(slide, 0.75, y, 0.42, 0.42, C["deep_teal"], radius=True)
        add_text(slide, str(n), 0.75, y + 0.03, 0.42, 0.30, 9, True, C["white"], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        add_text(slide, compact(msg, 240), 1.35, y - 0.01, 8.85, 0.65, 12.3, False, C["charcoal"])
        y += 0.78
    overall = text_of(d.get("overall_status"))
    if overall:
        col = status_color(overall)
        add_rect(slide, 10.25, 2.8, 2.35, 1.55, C["near_white"], C["light_gray"], True)
        add_text(slide, "CLOSEOUT STATUS", 10.48, 3.02, 1.9, 0.24, 7.5, True, C["mid_gray"])
        add_text(slide, overall, 10.48, 3.35, 1.85, 0.75, 12.0, True, col, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    add_footer(slide, page, "Source: review findings, gaps, actions, and evidence actually used")


def add_agenda(prs: Presentation, page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Technical review structure", "Agenda")
    items = [
        ("01", "Objectives, Scope & Review Basis"), ("02", "Documents Reviewed"),
        ("03", "Review Methodology & Comment Classification"), ("04", "Technical Findings & Reviewer Comments"),
        ("05", "Key Risks & Cross-Discipline Interfaces"), ("06", "Data Gaps, Clarifications & Assumptions"),
        ("07", "Action Plan & Comment Resolution"), ("08", "Conclusion & Closeout Status"),
    ]
    for i, (num, label) in enumerate(items):
        col = i % 2; row = i // 2; x = 0.8 + col * 6.05; y = 1.45 + row * 1.25
        add_rect(slide, x, y, 0.62, 0.62, C["deep_teal"], radius=True)
        add_text(slide, num, x, y + 0.11, 0.62, 0.28, 8.5, True, C["white"], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        add_text(slide, label, x + 0.82, y + 0.05, 4.95, 0.55, 11.5, True, C["charcoal"], valign=MSO_ANCHOR.MIDDLE)
    add_footer(slide, page)


def has_control(d: dict[str, Any]) -> bool:
    return any(d.get(k) not in (None, "", []) for k in ("report_no", "revision", "prepared_by", "reviewed_by", "approved_by"))


def add_control(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Review control and revision", "Control")
    fields = [
        ("Report / Review No.", d.get("report_no", "Not specified")),
        ("Revision", d.get("revision", "Not specified")),
        ("Issue date", d.get("date", "Not specified")),
        ("Prepared by", d.get("prepared_by", "Not specified")),
        ("Reviewed by", d.get("reviewed_by", "Not specified")),
        ("Approved by", d.get("approved_by", "Not specified")),
    ]
    for i, (lab, val) in enumerate(fields):
        col = i % 2; row = i // 2; x = 0.8 + col * 6.05; y = 1.45 + row * 1.42
        add_rect(slide, x, y, 5.5, 1.0, C["near_white"], C["light_gray"], True)
        add_text(slide, lab.upper(), x + 0.18, y + 0.14, 1.65, 0.22, 7.2, True, C["mid_gray"])
        add_text(slide, compact(val, 120), x + 1.95, y + 0.13, 3.2, 0.55, 11.2, True, C["deep_teal"], valign=MSO_ANCHOR.MIDDLE)
    add_footer(slide, page)


def add_scope(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Objectives, scope and review basis", "Scope")
    objective = d.get("objective") or "Not specified"
    add_rect(slide, 0.72, 1.35, 12.0, 0.9, C["near_white"], C["light_gray"], True)
    add_rect(slide, 0.72, 1.35, 0.11, 0.9, C["pln_blue"])
    add_text(slide, "OBJECTIVE", 1.0, 1.55, 1.5, 0.22, 8.0, True, C["pln_blue"])
    add_text(slide, compact(objective, 260), 2.45, 1.47, 9.85, 0.52, 11.5, False, C["charcoal"])
    add_text(slide, "INCLUDED / REVIEW SCOPE", 0.82, 2.55, 4.6, 0.3, 9.0, True, C["energy_teal"])
    scope = d.get("scope") or d.get("coverage") or ["Not specified"]
    add_bullet_list(slide, as_list(scope), 0.9, 2.92, 5.55, 2.8, 10.5, max_items=7)
    add_text(slide, "REVIEW BASIS / LIMITATIONS", 6.75, 2.55, 4.6, 0.3, 9.0, True, C["deep_teal"])
    basis = d.get("review_basis") or d.get("evidence_basis") or ["Target document + selected embedded geothermal KB evidence"]
    basis_items = as_list(basis) + as_list(d.get("limitations"))
    add_bullet_list(slide, basis_items, 6.82, 2.92, 5.45, 2.8, 10.5, max_items=7)
    add_footer(slide, page)


def add_documents(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Documents reviewed", "Register")
    docs = [x for x in as_list(d.get("documents_reviewed")) if isinstance(x, dict)]
    cols = [("Title", 4.0), ("No./Code", 1.7), ("Rev.", 0.7), ("Date", 1.2), ("Discipline", 1.35), ("Review scope / status", 3.2)]
    rows = []
    for doc in docs[:7]:
        rows.append([
            text_of(doc.get("title")), text_of(doc.get("number") or doc.get("code")), text_of(doc.get("revision")),
            text_of(doc.get("date")), text_of(doc.get("discipline")), text_of(doc.get("scope") or doc.get("status")),
        ])
    if not rows:
        rows = [["Target document not separately registered in structured input", "", "", "", "", ""]]
    add_table(slide, cols, rows, 0.5, 1.35, row_h=0.67, font_size=7.3)
    if len(docs) > 7:
        add_text(slide, f"+ {len(docs)-7} additional document(s) retained in source traceability / appendix", 0.62, 6.65, 7.5, 0.25, 8.2, True, C["deep_teal"])
    add_footer(slide, page)


def add_methodology(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Review methodology and comment classification", "Method")
    methods = as_list(d.get("methodology")) or [
        "Read target document and identify technical claims / decisions requiring review",
        "Retrieve only relevant embedded-KB evidence; avoid full-KB loading",
        "Cross-check narrative, tables, figures, calculations, units and revisions",
        "Classify finding, data gap and closure action with explicit traceability",
    ]
    for i, item in enumerate(methods[:4]):
        x = 0.75 + i * 3.05
        add_rect(slide, x, 1.45, 2.65, 2.05, C["near_white"], C["light_gray"], True)
        add_rect(slide, x + 0.18, 1.65, 0.5, 0.5, C["deep_teal"], radius=True)
        add_text(slide, str(i + 1), x + 0.18, 1.71, 0.5, 0.25, 9, True, C["white"], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        add_text(slide, compact(item, 155), x + 0.22, 2.32, 2.2, 0.86, 10.2, False, C["charcoal"], PP_ALIGN.CENTER)
    add_text(slide, "COMMENT CLASSIFICATION", 0.8, 4.02, 3.2, 0.25, 8.2, True, C["dark_teal"])
    classes = d.get("comment_classification")
    if isinstance(classes, dict):
        items = [(k, text_of(v)) for k, v in classes.items()]
    else:
        items = [("High", "Material technical issue / decision-impacting"), ("Medium", "Needs correction or clarification before closure"),
                 ("Low", "Minor improvement / non-material"), ("Data Gap", "Evidence insufficient for a definitive conclusion")]
    for i, (lab, desc) in enumerate(items[:4]):
        x = 0.8 + i * 3.0; col = priority_color(lab) if lab.lower() != "data gap" else C["pln_blue"]
        add_rect(slide, x, 4.42, 2.55, 1.18, C["white"], C["light_gray"], True)
        add_rect(slide, x, 4.42, 2.55, 0.1, col)
        add_text(slide, lab, x + 0.16, 4.62, 0.75, 0.25, 9, True, col)
        add_text(slide, compact(desc, 100), x + 0.95, 4.53, 1.43, 0.72, 8.2, False, C["charcoal"])
    add_footer(slide, page)


def add_findings_overview(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Technical findings and reviewer comments", "Findings")
    findings = [normalize_finding(f) for f in as_list(d.get("findings")) if isinstance(f, dict)]
    cols = [("ID", 0.6), ("Discipline", 1.3), ("Finding", 4.35), ("Priority", 1.05), ("Status", 1.35), ("Location", 3.45)]
    rows = []
    for f in findings[:7]:
        rows.append([f.get("id", ""), f.get("discipline", ""), f.get("title") or f.get("finding", ""),
                     f.get("priority", ""), f.get("status", ""), f.get("location", "")])
    if not rows:
        rows = [["-", "-", "No finding provided in structured review input", "-", "-", "-"]]
    add_table(slide, cols, rows, 0.5, 1.35, row_h=0.68, font_size=7.3, priority_col=3, status_col=4)
    if len(findings) > 7:
        add_text(slide, f"+ {len(findings)-7} finding(s) continued in detail / appendix", 0.62, 6.65, 6.5, 0.25, 8.2, True, C["deep_teal"])
    add_footer(slide, page)


def add_finding_detail(prs: Presentation, f0: dict[str, Any], page: int):
    f = normalize_finding(f0)
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    title = f.get("title") or f.get("finding") or "Technical finding"
    add_header(slide, compact(title, 110), f.get("id", "Finding"))
    pcol = priority_color(f.get("priority", "")); scol = status_color(f.get("status", ""))
    chips = [
        ("Discipline", f.get("discipline") or "Not stated", C["pln_blue"]),
        ("Priority", f.get("priority") or "Unrated", pcol),
        ("Status", f.get("status") or "Open", scol),
        ("Target", f.get("location") or "Not stated", C["deep_teal"]),
    ]
    x = 0.65
    for label, val, col in chips:
        add_rect(slide, x, 1.28, 2.35, 0.52, C["near_white"], C["light_gray"], True)
        add_text(slide, label, x + 0.08, 1.34, 0.64, 0.18, 6.6, True, C["mid_gray"])
        add_text(slide, compact(val, 55), x + 0.72, 1.32, 1.52, 0.27, 8.4, True, col)
        x += 2.55
    sections = [
        ("Finding / observation", f.get("finding", ""), C["pln_blue"]),
        ("Reviewer comment / recommendation", f.get("comment", ""), C["energy_teal"]),
        ("Why it matters / potential impact", f.get("impact", ""), pcol),
    ]
    y = 2.03
    for lab, body, col in sections:
        add_text(slide, lab.upper(), 0.7, y, 2.7, 0.23, 7.8, True, col)
        add_text(slide, compact(body or "Not stated", 420), 0.7, y + 0.27, 5.55, 0.86, 10.4, False, C["charcoal"])
        y += 1.36
    add_rect(slide, 6.55, 2.0, 6.1, 4.55, C["near_white"], C["light_gray"], True)
    add_text(slide, "TECHNICAL BASIS / EVIDENCE", 6.85, 2.25, 3.8, 0.28, 9.2, True, C["dark_teal"])
    img = f.get("image_path")
    if img and os.path.exists(str(img)):
        try:
            slide.shapes.add_picture(str(img), Inches(6.85), Inches(2.68), width=Inches(5.5), height=Inches(2.18))
            evidence_y = 5.02
        except Exception:
            evidence_y = 2.75
    else:
        evidence_y = 2.75
    basis = f.get("basis", ""); source = f.get("source", "")
    add_text(slide, compact(basis or "Not stated", 320), 6.85, evidence_y, 5.45, 1.15, 9.8, False, C["charcoal"])
    if source:
        add_text(slide, compact(source, 185), 6.85, 6.05, 5.45, 0.32, 7.2, True, C["deep_teal"])
    add_footer(slide, page, f"Target: {f.get('location','')} | Evidence: {source}".strip())


def add_risks(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Key risks and cross-discipline interfaces", "Interfaces")
    risks = as_list(d.get("key_risks"))
    if not risks:
        risks = ["No cross-discipline interface risk was separately recorded in the structured review input."]
    for i, risk in enumerate(risks[:6]):
        col = i % 2; row = i // 2; x = 0.72 + col * 6.05; y = 1.38 + row * 1.66
        add_rect(slide, x, y, 5.55, 1.36, C["near_white"], C["light_gray"], True)
        add_rect(slide, x, y, 0.09, 1.36, C["deep_teal"])
        if isinstance(risk, dict):
            label = risk.get("interface") or risk.get("title") or f"Interface {i+1}"
            main = risk.get("risk") or risk.get("issue") or ""
            impact = risk.get("impact") or risk.get("consequence") or ""
            rel = risk.get("related_findings") or risk.get("finding_id") or ""
            add_text(slide, compact(label, 70), x + 0.2, y + 0.12, 2.15, 0.24, 8.1, True, C["deep_teal"])
            add_text(slide, compact(main, 145), x + 0.2, y + 0.4, 5.05, 0.44, 9.4, True, C["charcoal"])
            add_text(slide, compact(impact, 125), x + 0.2, y + 0.86, 4.4, 0.3, 8.2, False, C["mid_gray"])
            if rel:
                add_text(slide, compact(rel, 45), x + 4.65, y + 0.1, 0.7, 0.22, 7.0, True, C["pln_blue"], PP_ALIGN.RIGHT)
        else:
            add_text(slide, f"Interface {i+1}", x + 0.2, y + 0.14, 1.15, 0.22, 7.8, True, C["deep_teal"])
            add_text(slide, compact(risk, 220), x + 0.2, y + 0.47, 5.0, 0.55, 10.0, False, C["charcoal"])
    add_footer(slide, page)


def add_gaps(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Data gaps, clarifications and assumptions", "Gaps")
    gaps = as_list(d.get("data_gaps"))
    rows: list[list[str]] = []
    for i, g in enumerate(gaps[:7]):
        if isinstance(g, dict):
            rows.append([text_of(g.get("id") or f"DG-{i+1:02d}"), text_of(g.get("gap") or g.get("item")),
                         text_of(g.get("impact")), text_of(g.get("required") or g.get("evidence")),
                         text_of(g.get("owner") or g.get("pic")), text_of(g.get("status"))])
        else:
            rows.append([f"DG-{i+1:02d}", text_of(g), "", "", "", "Open"])
    if not rows:
        rows = [["-", "No material data gap recorded", "", "", "", "-"]]
    cols = [("Gap ID", 0.75), ("Missing / unclear data", 3.4), ("Impact", 2.25), ("Required evidence", 2.75), ("Owner", 1.2), ("Status", 1.35)]
    add_table(slide, cols, rows, 0.48, 1.35, row_h=0.68, font_size=7.1, status_col=5)
    add_footer(slide, page)


def add_actions(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Action plan and comment resolution", "Actions")
    actions = as_list(d.get("actions"))
    rows = []
    for i, a in enumerate(actions[:7]):
        if isinstance(a, dict):
            rows.append([text_of(a.get("id") or f"A-{i+1:02d}"), text_of(a.get("finding_id") or a.get("related_findings")),
                         text_of(a.get("action")), text_of(a.get("pic") or a.get("owner")), text_of(a.get("due") or a.get("timing")),
                         text_of(a.get("evidence") or a.get("closure_evidence")), text_of(a.get("status"))])
        else:
            rows.append([f"A-{i+1:02d}", "", text_of(a), "TBD", "TBD", "", "Open"])
    if not rows:
        rows = [["A-01", "", "Define closure actions for material findings and data gaps", "TBD", "TBD", "", "Open"]]
    cols = [("Action", 0.72), ("Finding", 0.78), ("Action required", 4.05), ("PIC", 1.35), ("Due", 1.25), ("Closure evidence", 2.6), ("Status", 1.3)]
    add_table(slide, cols, rows, 0.4, 1.35, row_h=0.68, font_size=6.95, status_col=6)
    add_footer(slide, page)


def add_conclusion(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Conclusion and closeout status", "Closeout")
    status = text_of(d.get("overall_status")) or "Not stated"
    col = status_color(status)
    add_rect(slide, 0.8, 1.45, 3.35, 1.55, C["near_white"], C["light_gray"], True)
    add_text(slide, "OVERALL STATUS", 1.1, 1.74, 2.7, 0.25, 8, True, C["mid_gray"], PP_ALIGN.CENTER)
    add_text(slide, status, 1.05, 2.12, 2.85, 0.65, 14.5, True, col, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    findings = [normalize_finding(f) for f in as_list(d.get("findings")) if isinstance(f, dict)]
    open_material = [f for f in findings if "closed" not in str(f.get("status", "")).lower() and str(f.get("priority", "")).lower().startswith(("h", "m"))]
    add_rect(slide, 4.45, 1.45, 2.2, 1.55, C["near_white"], C["light_gray"], True)
    add_text(slide, str(len(open_material)), 4.8, 1.76, 1.5, 0.48, 25, True, C["high"], PP_ALIGN.CENTER)
    add_text(slide, "OPEN MATERIAL\nCOMMENTS", 4.75, 2.27, 1.6, 0.5, 8.2, True, C["charcoal"], PP_ALIGN.CENTER)
    add_rect(slide, 6.95, 1.45, 2.2, 1.55, C["near_white"], C["light_gray"], True)
    add_text(slide, str(len(as_list(d.get("data_gaps")))), 7.3, 1.76, 1.5, 0.48, 25, True, C["pln_blue"], PP_ALIGN.CENTER)
    add_text(slide, "DATA GAPS", 7.3, 2.35, 1.5, 0.3, 8.2, True, C["charcoal"], PP_ALIGN.CENTER)
    add_rect(slide, 9.45, 1.45, 2.2, 1.55, C["near_white"], C["light_gray"], True)
    open_actions = sum(1 for a in as_list(d.get("actions")) if not isinstance(a, dict) or "closed" not in str(a.get("status", "")).lower())
    add_text(slide, str(open_actions), 9.8, 1.76, 1.5, 0.48, 25, True, C["medium"], PP_ALIGN.CENTER)
    add_text(slide, "OPEN ACTIONS", 9.8, 2.35, 1.5, 0.3, 8.2, True, C["charcoal"], PP_ALIGN.CENTER)
    add_text(slide, "REVIEW CONCLUSION", 0.82, 3.48, 2.5, 0.28, 8.5, True, C["dark_teal"])
    add_text(slide, compact(d.get("conclusion") or "No conclusion provided.", 560), 0.85, 3.86, 11.4, 1.1, 12.0, False, C["charcoal"])
    conditions = as_list(d.get("conditions_to_proceed") or d.get("closeout_conditions"))
    if conditions:
        add_text(slide, "CONDITIONS TO PROCEED / LIMITATIONS", 0.82, 5.15, 3.8, 0.28, 8.5, True, C["energy_teal"])
        add_bullet_list(slide, conditions, 0.9, 5.5, 11.3, 1.0, 9.4, max_items=4)
    add_footer(slide, page)


def add_references(prs: Presentation, d: dict[str, Any], page: int):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CONTENT)
    add_header(slide, "Sources used and review traceability", "Appendix")
    refs = as_list(d.get("references_used") or d.get("references"))
    if not refs:
        refs = sorted({normalize_finding(f).get("source", "") for f in as_list(d.get("findings")) if isinstance(f, dict) and normalize_finding(f).get("source")})
    y = 1.38
    for i, r in enumerate(refs[:12], 1):
        add_text(slide, f"{i:02d}", 0.7, y, 0.45, 0.3, 8.5, True, C["deep_teal"])
        add_text(slide, compact(r, 220), 1.25, y, 11.0, 0.38, 9.2, False, C["charcoal"])
        y += 0.43
    if not refs:
        add_text(slide, "No source list was supplied in the structured review input.", 0.85, 1.65, 10.5, 0.45, 11, False, C["charcoal"])
    add_text(slide, "Only sources actually opened / used as technical evidence should be listed. Preserve file + page / slide / sheet / section locators where available.", 0.7, 6.62, 11.5, 0.38, 8.0, True, C["mid_gray"])
    add_footer(slide, page)


def add_closing(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6]); add_master_background(slide, MASTER_CLOSING)


def build(data: dict[str, Any], out_path: str):
    prs = Presentation(); prs.slide_width = Inches(SW); prs.slide_height = Inches(SH)
    add_cover(prs, data)
    page = 2
    add_summary(prs, data, page); page += 1
    if data.get("include_agenda", True):
        add_agenda(prs, page); page += 1
    if has_control(data) and data.get("include_review_control", True):
        add_control(prs, data, page); page += 1
    add_scope(prs, data, page); page += 1
    add_documents(prs, data, page); page += 1
    add_methodology(prs, data, page); page += 1
    add_findings_overview(prs, data, page); page += 1
    detail_limit = int(data.get("ppt_detail_limit", 6) or 6)
    for f in [x for x in as_list(data.get("findings")) if isinstance(x, dict)][:detail_limit]:
        add_finding_detail(prs, f, page); page += 1
    add_risks(prs, data, page); page += 1
    add_gaps(prs, data, page); page += 1
    add_actions(prs, data, page); page += 1
    add_conclusion(prs, data, page); page += 1
    add_references(prs, data, page); page += 1
    add_closing(prs)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True); prs.save(out_path)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__); return 2
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    build(data, sys.argv[2]); print(sys.argv[2]); return 0


if __name__ == "__main__":
    raise SystemExit(main())
