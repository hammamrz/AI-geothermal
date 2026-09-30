#!/usr/bin/env python3
"""Build a PLN IP-style geothermal technical review / comment sheet report.

Usage:
  python build_comment_sheet.py input.json output.docx

The generated DOCX contains real Word fields for TOC, List of Figures,
List of Tables, and page numbers. Word is instructed to update fields on open.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from datetime import date
from docx import Document
from docx.shared import Mm, Pt, Inches, RGBColor
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
REF = HERE.parent / "references"
MASTER = REF / "PLN_IP_COMMENT_SHEET_REPORT_TEMPLATE.docx"

PLN_BLUE = "006699"
DEEP_BLUE = "0B3558"
LIGHT_BLUE = "DCEEF5"
LIGHT_GRAY = "E7E6E6"
DARK_GRAY = "404040"
YELLOW = "FFD600"
RED = "C00000"
AMBER = "FFC000"
GREEN = "70AD47"


def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tcPr.append(shd)
    shd.set(qn('w:fill'), fill)


def set_cell_margins(cell, top=70, start=70, bottom=70, end=70):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in('w:tcMar')
    if tcMar is None:
        tcMar = OxmlElement('w:tcMar')
        tcPr.append(tcMar)
    for m, v in [('top', top), ('start', start), ('bottom', bottom), ('end', end)]:
        node = tcMar.find(qn('w:' + m))
        if node is None:
            node = OxmlElement('w:' + m)
            tcMar.append(node)
        node.set(qn('w:w'), str(v))
        node.set(qn('w:type'), 'dxa')


def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)


def set_table_borders(table, color="808080", size="4"):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = tblPr.first_child_found_in('w:tblBorders')
    if borders is None:
        borders = OxmlElement('w:tblBorders')
        tblPr.append(borders)
    for edge in ('top','left','bottom','right','insideH','insideV'):
        tag = 'w:' + edge
        el = borders.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            borders.append(el)
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), size)
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), color)


def add_field(paragraph, instruction, placeholder=''):
    run = paragraph.add_run()
    begin = OxmlElement('w:fldChar'); begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = instruction
    sep = OxmlElement('w:fldChar'); sep.set(qn('w:fldCharType'), 'separate')
    txt = OxmlElement('w:t'); txt.text = placeholder
    end = OxmlElement('w:fldChar'); end.set(qn('w:fldCharType'), 'end')
    run._r.extend([begin, instr, sep, txt, end])
    return run


def add_page_number(paragraph):
    add_field(paragraph, ' PAGE ', '1')


def add_caption(doc, label, title):
    p = doc.add_paragraph(style='Caption')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f'{label} ')
    r.bold = True
    seq = p.add_run()
    begin = OxmlElement('w:fldChar'); begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = f' SEQ {label} \\* ARABIC '
    sep = OxmlElement('w:fldChar'); sep.set(qn('w:fldCharType'), 'separate')
    txt = OxmlElement('w:t'); txt.text = '1'
    end = OxmlElement('w:fldChar'); end.set(qn('w:fldCharType'), 'end')
    seq._r.extend([begin, instr, sep, txt, end])
    p.add_run(f'. {title}')
    return p


def set_update_fields(doc):
    settings = doc.settings._element
    upd = settings.find(qn('w:updateFields'))
    if upd is None:
        upd = OxmlElement('w:updateFields')
        settings.append(upd)
    upd.set(qn('w:val'), 'true')


def style_doc(doc):
    styles = doc.styles
    normal = styles['Normal']
    normal.font.name = 'Arial'; normal.font.size = Pt(10)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.08
    for nm, size in [('Title', 20), ('Heading 1', 14), ('Heading 2', 12), ('Heading 3', 10.5)]:
        st = styles[nm]
        st.font.name = 'Arial'; st.font.size = Pt(size); st.font.bold = True; st.font.color.rgb = RGBColor(0,0,0)
        st.paragraph_format.space_before = Pt(8); st.paragraph_format.space_after = Pt(5)
        # The KKP source Heading styles carry its own A/B/C and 1/1.1 numbering.
        # This report writes chapter numbers explicitly, so suppress inherited auto-numbering.
        pPr = st.element.get_or_add_pPr()
        numPr = pPr.find(qn('w:numPr'))
        if numPr is not None:
            pPr.remove(numPr)
    cap = styles['Caption']; cap.font.name = 'Arial'; cap.font.size = Pt(9); cap.font.bold = True
    for nm in ['TOC 1','TOC 2','TOC 3']:
        if nm in styles:
            styles[nm].font.name='Arial'; styles[nm].font.size=Pt(10)


def body_section_setup(section, landscape=False):
    if landscape:
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width, section.page_height = Mm(297), Mm(210)
        section.left_margin = Mm(15); section.right_margin = Mm(15)
        section.top_margin = Mm(18); section.bottom_margin = Mm(18)
    else:
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width, section.page_height = Mm(210), Mm(297)
        section.left_margin = Mm(20); section.right_margin = Mm(18)
        section.top_margin = Mm(22); section.bottom_margin = Mm(22)
    section.header_distance = Mm(8)
    section.footer_distance = Mm(8)


def set_header_footer(section, meta):
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False
    header = section.header
    hp = header.paragraphs[0]
    hp.clear()
    tbl = header.add_table(rows=1, cols=2, width=section.page_width - section.left_margin - section.right_margin)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.columns[0].width = Mm(25); tbl.columns[1].width = Mm(140)
    c0, c1 = tbl.rows[0].cells
    if LOGO.exists():
        c0.paragraphs[0].add_run().add_picture(str(LOGO), width=Mm(13))
    p = c1.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    for i, line in enumerate(['PT PLN (PERSERO)', 'PT PLN INDONESIA POWER', 'Jl. Jend. Gatot Subroto Kav. 18 Kuningan Timur, Kecamatan Setiabudi Jakarta Selatan']):
        r = p.add_run(line + ('\n' if i<2 else ''))
        r.font.name='Arial'; r.font.size=Pt(8 if i<2 else 7.5); r.bold = i<2
    # bottom border under header table
    set_table_borders(tbl, color='000000', size='6')
    for cell in tbl.rows[0].cells:
        set_cell_margins(cell, top=0, bottom=0, start=0, end=0)
    # remove default empty header paragraph spacing
    for par in header.paragraphs:
        par.paragraph_format.space_after = Pt(0)

    footer = section.footer
    for p in footer.paragraphs:
        p.clear()
    line = footer.paragraphs[0]
    line.paragraph_format.space_after = Pt(2)
    line.add_run('________________________________________________________________________________').font.size = Pt(6)
    t = footer.add_table(rows=1, cols=3, width=section.page_width - section.left_margin - section.right_margin)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    left = t.cell(0,0).paragraphs[0]; center = t.cell(0,1).paragraphs[0]; right = t.cell(0,2).paragraphs[0]
    left.add_run('Comment Sheet Report\n' + meta.get('project_name','Geothermal Project') + '\nPT PLN Indonesia Power')
    center.alignment = WD_ALIGN_PARAGRAPH.CENTER; add_page_number(center)
    right.alignment = WD_ALIGN_PARAGRAPH.RIGHT; right.add_run('Revisi ' + str(meta.get('revision','0')))
    for p in (left,center,right):
        for r in p.runs: r.font.name='Arial'; r.font.size=Pt(7)
    conf = footer.add_paragraph()
    conf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr=conf.add_run('Dokumen ini milik PT PLN (Persero) / PT PLN Indonesia Power. Dilarang memperbanyak atau menyampaikan kepada pihak lain tanpa izin.')
    rr.italic=True; rr.font.name='Arial'; rr.font.size=Pt(6.5)


def add_title(doc, text, level=1):
    p=doc.add_paragraph(style=f'Heading {level}')
    p.add_run(text)
    return p


def add_bullet(doc, text, level=0):
    # The original KKP style set does not include Word's built-in List Bullet styles.
    # Use a manual bullet so the report can stay on the exact KKP style/template base.
    p=doc.add_paragraph(style='Normal')
    p.paragraph_format.left_indent = Mm(7 + 5*level)
    p.paragraph_format.first_line_indent = Mm(-4)
    p.add_run('• ' + str(text))
    return p


def add_kv_table(doc, rows, caption=None, widths=None):
    if caption: add_caption(doc, 'Tabel', caption)
    tbl=doc.add_table(rows=1, cols=2)
    tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit=False
    hdr=tbl.rows[0].cells
    hdr[0].text='Parameter'; hdr[1].text='Keterangan'
    for c in hdr:
        set_cell_shading(c, LIGHT_GRAY); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for r in c.paragraphs[0].runs: r.bold=True; r.font.size=Pt(9)
    set_repeat_table_header(tbl.rows[0])
    for k,v in rows:
        cells=tbl.add_row().cells; cells[0].text=str(k); cells[1].text=str(v)
    set_table_borders(tbl)
    for row in tbl.rows:
        for c in row.cells:
            set_cell_margins(c)
            for p in c.paragraphs:
                for r in p.runs: r.font.name='Arial'; r.font.size=Pt(9)
    return tbl


def add_documents_table(doc, documents):
    add_caption(doc,'Tabel','Daftar Dokumen yang Diperiksa')
    tbl=doc.add_table(rows=1, cols=6); tbl.alignment=WD_TABLE_ALIGNMENT.CENTER; tbl.autofit=False
    headers=['No.','Judul Dokumen','No./Kode Dokumen','Revisi','Tanggal','Lingkup Review']
    for i,h in enumerate(headers):
        tbl.cell(0,i).text=h; set_cell_shading(tbl.cell(0,i), LIGHT_GRAY)
        for r in tbl.cell(0,i).paragraphs[0].runs: r.bold=True; r.font.size=Pt(8.5)
    set_repeat_table_header(tbl.rows[0])
    for idx,d in enumerate(documents,1):
        vals=[idx,d.get('title',''),d.get('number',''),d.get('revision',''),d.get('date',''),d.get('scope','')]
        cells=tbl.add_row().cells
        for i,v in enumerate(vals): cells[i].text=str(v)
    set_table_borders(tbl)
    for row in tbl.rows:
        for c in row.cells:
            set_cell_margins(c,50,55,50,55); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
            for p in c.paragraphs:
                for r in p.runs: r.font.name='Arial'; r.font.size=Pt(8)
    return tbl


def priority_fill(value):
    x=str(value).strip().lower()
    if x in ('critical','high','tinggi','major'): return RED
    if x in ('medium','sedang'): return AMBER
    if x in ('low','rendah','minor'): return GREEN
    return LIGHT_GRAY


def add_findings_table(doc, findings):
    add_caption(doc,'Tabel','Detailed Findings and Reviewer Comments')
    tbl=doc.add_table(rows=1, cols=8); tbl.alignment=WD_TABLE_ALIGNMENT.CENTER; tbl.autofit=False
    headers=['ID','Discipline','Dokumen / Lokasi','Finding / Observation','Reviewer Comment / Recommendation','Technical Basis / Reference','Priority','Status']
    widths=[Mm(12),Mm(21),Mm(36),Mm(48),Mm(56),Mm(38),Mm(18),Mm(18)]
    for i,h in enumerate(headers):
        c=tbl.cell(0,i); c.text=h; set_cell_shading(c, PLN_BLUE)
        for r in c.paragraphs[0].runs: r.bold=True; r.font.color.rgb=RGBColor(255,255,255); r.font.size=Pt(7.5)
        c.width=widths[i]
    set_repeat_table_header(tbl.rows[0])
    for idx,f in enumerate(findings,1):
        vals=[f.get('id',f'F-{idx:03d}'),f.get('discipline',''),f.get('location',''),f.get('finding',''),f.get('comment',f.get('recommendation','')),f.get('basis',''),f.get('priority',''),f.get('status','Open')]
        cells=tbl.add_row().cells
        for i,v in enumerate(vals):
            cells[i].text=str(v); cells[i].width=widths[i]
        set_cell_shading(cells[6], priority_fill(vals[6]))
    set_table_borders(tbl)
    for row in tbl.rows:
        for c in row.cells:
            c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP; set_cell_margins(c,45,45,45,45)
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(1)
                for r in p.runs: r.font.name='Arial'; r.font.size=Pt(7.2)
    return tbl


def add_data_gaps_table(doc, gaps):
    add_caption(doc,'Tabel','Data Gaps / Clarifications Required')
    tbl=doc.add_table(rows=1, cols=5); tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    headers=['ID','Data / Clarification Required','Why It Matters / Impact','Required Evidence / Deliverable','Status']
    for i,h in enumerate(headers):
        c=tbl.cell(0,i); c.text=h; set_cell_shading(c,LIGHT_GRAY)
        for r in c.paragraphs[0].runs: r.bold=True; r.font.size=Pt(8)
    set_repeat_table_header(tbl.rows[0])
    for idx,g in enumerate(gaps,1):
        vals=[g.get('id',f'DG-{idx:02d}'),g.get('gap',''),g.get('impact',''),g.get('required',''),g.get('status','Open')]
        cells=tbl.add_row().cells
        for i,v in enumerate(vals): cells[i].text=str(v)
    set_table_borders(tbl)
    for row in tbl.rows:
        for c in row.cells:
            set_cell_margins(c); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
            for p in c.paragraphs:
                for r in p.runs: r.font.name='Arial'; r.font.size=Pt(8)
    return tbl


def add_actions_table(doc, actions):
    add_caption(doc,'Tabel','Action Plan / Comment Resolution Register')
    tbl=doc.add_table(rows=1, cols=7); tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    headers=['ID','Related Finding','Required Action','PIC / Owner','Target Date','Evidence for Closure','Status']
    for i,h in enumerate(headers):
        c=tbl.cell(0,i); c.text=h; set_cell_shading(c,PLN_BLUE)
        for r in c.paragraphs[0].runs: r.bold=True; r.font.color.rgb=RGBColor(255,255,255); r.font.size=Pt(8)
    set_repeat_table_header(tbl.rows[0])
    for idx,a in enumerate(actions,1):
        vals=[a.get('id',f'A-{idx:02d}'),a.get('finding_id',''),a.get('action',''),a.get('pic',''),a.get('due',''),a.get('evidence',''),a.get('status','Open')]
        cells=tbl.add_row().cells
        for i,v in enumerate(vals): cells[i].text=str(v)
    set_table_borders(tbl)
    for row in tbl.rows:
        for c in row.cells:
            set_cell_margins(c); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
            for p in c.paragraphs:
                for r in p.runs: r.font.name='Arial'; r.font.size=Pt(8)
    return tbl


def set_page_numbering(section, fmt=None, start=None):
    sectPr = section._sectPr
    pg = sectPr.find(qn('w:pgNumType'))
    if pg is None:
        pg = OxmlElement('w:pgNumType')
        sectPr.append(pg)
    if fmt:
        pg.set(qn('w:fmt'), fmt)
    if start is not None:
        pg.set(qn('w:start'), str(start))


def link_exact_header_footer(section):
    """Reuse the exact KKP header/footer XML from the preceding section."""
    section.header.is_linked_to_previous = True
    section.footer.is_linked_to_previous = True
    section.first_page_header.is_linked_to_previous = True
    section.first_page_footer.is_linked_to_previous = True


def _remove_report_marker(doc):
    """Remove the generator marker while retaining the exact cover + body section break."""
    for p in list(doc.paragraphs):
        if '[[REPORT_BODY_MARKER]]' in p.text:
            p._element.getparent().remove(p._element)
            break


def _update_exact_shell_meta(doc, data):
    """Change only variable footer text; layout, rules, logo, typography remain KKP-original."""
    sec = doc.sections[1] if len(doc.sections) > 1 else doc.sections[0]
    footer = sec.footer
    if len(footer.paragraphs) >= 6:
        p = footer.paragraphs[1]
        runs = p.runs
        if len(runs) >= 2:
            runs[0].text = 'Technical '
            runs[1].text = 'Review Report'
        for r in runs:
            if r.text and 'Revisi' in r.text:
                r.text = '\tRevisi ' + str(data.get('revision', '0'))
        footer.paragraphs[2].text = str(data.get('project_name','[PROJECT / FIELD / WELL NAME]'))
        footer.paragraphs[3].text = 'PT PLN Indonesia Power'
        footer.paragraphs[4].text = 'Dokumen ini milik PT PLN (Persero)'
        footer.paragraphs[5].text = 'Dilarang menyalin atau memperbanyak dokumen kepada pihak lain tanpa seijin dari PT PLN (Persero)'
        # preserve source-like Arial sizing after changing text through python-docx
        for idx, size, italic in [(2,7,False),(3,7,False),(4,6.5,True),(5,6.5,True)]:
            for r in footer.paragraphs[idx].runs:
                r.font.name='Arial'; r.font.size=Pt(size); r.italic=italic


def build(data, out_path):
    # Start from an exact, stripped copy of the user's KKP DOCX. This preserves the
    # original cover artwork, logo/address header, horizontal rules, footer geometry,
    # page-number field, and confidentiality treatment without recreating them.
    doc = Document(MASTER)
    _remove_report_marker(doc)
    _update_exact_shell_meta(doc, data)
    style_doc(doc)
    set_update_fields(doc)

    # Master contains two sections: exact full-bleed cover (section 0) and the
    # KKP body shell (section 1) with exact logo/address header and footer.
    sec0 = doc.sections[0]
    sec0.different_first_page_header_footer = True
    set_page_numbering(sec0, 'lowerRoman', 1)
    if len(doc.sections) > 1:
        set_page_numbering(doc.sections[1], 'lowerRoman', 2)

    # Page 2: report identification, in the same restrained report language.
    p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run('TECHNICAL REVIEW & COMMENT SHEET REPORT'); r.bold=True; r.font.name='Arial'; r.font.size=Pt(16)
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(str(data.get('project_name','GEOTHERMAL PROJECT'))); r.bold=True; r.font.name='Arial'; r.font.size=Pt(13)
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(f"No: {data.get('report_no','-')}\nRevisi {data.get('revision','0')}"); r.bold=True; r.font.name='Arial'; r.font.size=Pt(11)

    add_title(doc,'DOCUMENT CONTROL',1)
    rows=[('Judul Laporan',data.get('report_title','Technical Review & Comment Sheet Report')),('Proyek',data.get('project_name','-')),('No. Dokumen',data.get('report_no','-')),('Revisi',data.get('revision','0')),('Tanggal',data.get('date',date.today().isoformat())),('Disusun oleh',data.get('prepared_by','-')),('Diperiksa oleh',data.get('reviewed_by','-')),('Disetujui oleh',data.get('approved_by','-'))]
    add_kv_table(doc,rows,'Document Control')
    add_title(doc,'Revision History',2)
    add_kv_table(doc,[('Rev. '+str(data.get('revision','0')),data.get('revision_note','Initial issue'))],'Revision History')

    # Executive Summary
    doc.add_page_break(); add_title(doc,'RINGKASAN EKSEKUTIF',1)
    summary=data.get('executive_summary') or 'Ringkasan hasil review teknis, temuan material, risiko utama, data gap, dan tindak lanjut yang diperlukan.'
    doc.add_paragraph(summary)
    findings=data.get('findings',[])
    counts={}
    for f in findings: counts[str(f.get('priority','Unrated')).title()]=counts.get(str(f.get('priority','Unrated')).title(),0)+1
    if findings:
        doc.add_paragraph('Ringkasan findings:')
        for k,v in counts.items(): add_bullet(doc,f'{k}: {v} finding(s)')

    # Automatic front matter
    doc.add_page_break(); add_title(doc,'DAFTAR ISI',1)
    p=doc.add_paragraph(); add_field(p,' TOC \\o "1-3" \\h \\z \\u ','Daftar isi diperbarui otomatis saat field Word di-update.')
    doc.add_page_break(); add_title(doc,'DAFTAR GAMBAR',1)
    p=doc.add_paragraph(); add_field(p,' TOC \\h \\z \\c "Gambar" ','Daftar gambar diperbarui otomatis.')
    doc.add_page_break(); add_title(doc,'DAFTAR TABEL',1)
    p=doc.add_paragraph(); add_field(p,' TOC \\h \\z \\c "Tabel" ','Daftar tabel diperbarui otomatis.')

    # Main report begins with Arabic page 1, mirroring the KKP front-matter/body logic.
    sec_main=doc.add_section(WD_SECTION.NEW_PAGE)
    body_section_setup(sec_main, False); link_exact_header_footer(sec_main); set_page_numbering(sec_main,'decimal',1)

    add_title(doc,'1. TUJUAN, LINGKUP, DAN BASIS REVIEW',1)
    doc.add_paragraph(data.get('objective','Melakukan review teknis terhadap dokumen yang diperiksa untuk mengidentifikasi inkonsistensi, risiko teknis, data gap, serta tindakan yang diperlukan sebelum dokumen dapat digunakan sebagai basis keputusan atau tahap pekerjaan berikutnya.'))
    add_title(doc,'1.1 Lingkup Review',2)
    scopes=data.get('scope',[]) or ['Subsurface / resource basis','Drilling / well design','Cross-discipline interfaces','Consistency, completeness, assumptions, and technical risks']
    for x in scopes: add_bullet(doc,x)
    add_title(doc,'1.2 Basis dan Kriteria Review',2)
    basis=data.get('review_basis',[]) or ['Target document and its stated design basis','Embedded geothermal knowledge base and applicable project references','Internal consistency across text, tables, figures, calculations, and assumptions','Engineering good practice; external standards only when explicitly provided or requested']
    for x in basis: add_bullet(doc,x)

    add_title(doc,'2. DOKUMEN YANG DIPERIKSA',1)
    add_documents_table(doc,data.get('documents_reviewed',[]) or [{'title':'[Dokumen target]','number':'-','revision':'-','date':'-','scope':'Technical review'}])

    add_title(doc,'3. METODOLOGI REVIEW DAN KLASIFIKASI KOMENTAR',1)
    doc.add_paragraph('Review dilakukan dengan pendekatan evidence-based dan retrieval-first. Setiap komentar harus dapat ditelusuri ke lokasi dokumen target dan, bila digunakan, ke sumber knowledge base atau referensi teknis yang mendasarinya.')
    add_kv_table(doc,[('Critical / High','Dapat mempengaruhi keselamatan, well integrity, resource confidence, operability, atau keputusan utama; perlu ditutup sebelum approval/gate berikutnya.'),('Major / Medium','Temuan material yang dapat mempengaruhi desain, biaya, jadwal, reliability, atau kualitas keputusan; memerlukan tindakan atau klarifikasi.'),('Minor / Low','Perbaikan, konsistensi, atau klarifikasi yang tidak mengubah basis keputusan utama.'),('Observation','Catatan good practice, opportunity for improvement, atau informasi tambahan tanpa kewajiban closeout.')],'Klasifikasi Priority / Severity')

    # Landscape register pages still inherit the exact KKP header/footer.
    sec_land=doc.add_section(WD_SECTION.NEW_PAGE); body_section_setup(sec_land, True); link_exact_header_footer(sec_land)
    add_title(doc,'4. TECHNICAL FINDINGS AND REVIEWER COMMENTS',1)
    doc.add_paragraph('Findings dikelompokkan berdasarkan disiplin dan diberi ID unik agar dapat ditelusuri sampai tahap closure.')
    add_findings_table(doc, findings or [{'id':'F-001','discipline':'[Discipline]','location':'[Document / section / page]','finding':'[Finding / observation]','comment':'[Reviewer comment / recommendation]','basis':'[Technical basis / KB source]','priority':'Medium','status':'Open'}])

    sec_p=doc.add_section(WD_SECTION.NEW_PAGE); body_section_setup(sec_p, False); link_exact_header_footer(sec_p)
    add_title(doc,'5. KEY RISKS DAN CROSS-DISCIPLINE INTERFACES',1)
    risks=data.get('key_risks',[]) or ['[Summarize material technical risks and interfaces identified during review.]']
    for x in risks: add_bullet(doc,x)

    add_title(doc,'6. DATA GAPS, CLARIFICATIONS, DAN ASSUMPTIONS',1)
    add_data_gaps_table(doc,data.get('data_gaps',[]) or [{'id':'DG-01','gap':'[Missing data / clarification]','impact':'[Impact if unresolved]','required':'[Required evidence]','status':'Open'}])

    sec_a=doc.add_section(WD_SECTION.NEW_PAGE); body_section_setup(sec_a, True); link_exact_header_footer(sec_a)
    add_title(doc,'7. ACTION PLAN DAN COMMENT RESOLUTION REGISTER',1)
    add_actions_table(doc,data.get('actions',[]) or [{'id':'A-01','finding_id':'F-001','action':'[Required action]','pic':'[PIC]','due':'[Target date]','evidence':'[Closure evidence]','status':'Open'}])

    sec_c=doc.add_section(WD_SECTION.NEW_PAGE); body_section_setup(sec_c, False); link_exact_header_footer(sec_c)
    add_title(doc,'8. KESIMPULAN DAN CLOSEOUT STATUS',1)
    doc.add_paragraph(data.get('conclusion','Secara keseluruhan, status penerimaan dokumen ditentukan berdasarkan closure atas findings material, penyelesaian data gaps, serta verifikasi evidence yang disepakati pada action plan.'))
    status=data.get('overall_status','Open for Comment / Revision Required')
    p=doc.add_paragraph(); r=p.add_run('Overall Review Status: ' + status); r.bold=True; r.font.size=Pt(12); r.font.color.rgb=RGBColor(0,102,153)
    add_title(doc,'8.1 Penutup',2)
    doc.add_paragraph(data.get('closing','Dokumen comment sheet ini merupakan catatan review teknis berdasarkan informasi yang tersedia pada saat review. Perubahan data, revisi dokumen, atau bukti teknis baru dapat memerlukan pembaruan terhadap findings dan status closure.'))

    doc.add_page_break(); add_title(doc,'LAMPIRAN',1)
    add_title(doc,'Lampiran A - Discipline-Specific Review Coverage',2)
    disciplines=data.get('discipline_coverage',[]) or [
        'Subsurface: geology, geochemistry, geophysics, conceptual model, resource estimate, uncertainty, well targeting.',
        'Drilling/Well: objectives, well architecture, trajectory, casing/cement, fluids/hydraulics, well control/BOP, BHA, lost circulation, testing/completion, HSE, time/cost and contingencies.',
        'Cross-discipline: production/reinjection strategy, fluid chemistry, scaling/corrosion, surface-upstream interfaces, operability, and data consistency.'
    ]
    for x in disciplines: add_bullet(doc,x)
    add_title(doc,'Lampiran B - Reference / Knowledge Base Sources Used',2)
    for x in data.get('references_used',[]) or ['[List only references actually used in the review, including exact page/slide where available.]']:
        add_bullet(doc,x)

    out_path=Path(out_path); out_path.parent.mkdir(parents=True,exist_ok=True)
    doc.save(out_path)
    return out_path


def main():
    if len(sys.argv) != 3:
        print('Usage: build_comment_sheet.py input.json output.docx', file=sys.stderr); return 2
    data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    build(data,sys.argv[2]); print(sys.argv[2]); return 0

if __name__=='__main__':
    raise SystemExit(main())
