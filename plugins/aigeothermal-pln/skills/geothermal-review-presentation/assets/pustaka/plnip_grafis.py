"""plnip_grafis.py — model grafis konsultan untuk deck PLN IP.

Diimpor otomatis oleh plnip_deck.py (`from plnip_deck import *`). Semua grafis dibangun dari
bentuk/chart asli PowerPoint (bisa diedit), memakai palet PLN IP, tanpa sudut membulat,
bayangan, atau gradien. Grafis bentuk dikelompokkan dalam satu group bernama 'Grafik <jenis>'
supaya mudah dipindah utuh di PowerPoint.

Daftar (pola di references/pola-layout.md, galeri di assets/galeri-grafis.png):
  Chart data   : add_line_chart, add_stacked_chart, add_donut, add_waterfall, add_tornado,
                 add_funnel, add_progress
  Waktu        : add_timeline (milestone), add_gantt
  Proses       : add_flow, add_stage_gate, add_swimlane, add_cycle
  Struktur     : add_issue_tree, add_org_chart, add_pillars
  Penilaian    : add_matrix_2x2, add_harvey, add_harvey_table, add_sensitivity_table
  Angka        : add_kpi_row, add_big_number
  Geografis    : add_map (peta Indonesia + titik proyek, bisa diperbesar per wilayah)
  Pendukung    : add_legend
Semua ukuran dalam inci.
"""
import json
import math
import os

from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt, Emu

import plnip_deck as _d
from plnip_deck import (A1, A4, PRIMARY, DARK, TINT, YELLOW, TEAL, MIST, INK, GRAY, OUTLINE,
                        WHITE, NEG, FONT, L, R, CW, BODY_TOP, BODY_BOTTOM, _fill_runs, _run,
                        _bullet, add_icon_badge, icon_path)

LIGHT = RGBColor(0xE6, 0xEE, 0xF2)   # netral terang (trek bar, daratan tetangga)
SERI = [PRIMARY, DARK, A4, TINT, OUTLINE, A1, TEAL]   # urutan warna seri chart multi-seri
_HERE = os.path.dirname(os.path.abspath(__file__))


# =====================================================================================
# Primitif (bekerja pada koleksi shapes: slide.shapes atau group.shapes)
# =====================================================================================
def _group(slide, nama):
    g = slide.shapes.add_group_shape()
    g.name = 'Grafik ' + nama
    return g.shapes


def _rect(S, x, y, w, h, fill=None, line=None, line_pt=0.75, shape=MSO_SHAPE.RECTANGLE, name=None):
    sh = S.add_shape(shape, Inches(x), Inches(y), Inches(max(w, 0.001)), Inches(max(h, 0.001)))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line; sh.line.width = Pt(line_pt)
    sh.shadow.inherit = False
    if name:
        sh.name = name
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    return sh


def _shape_text(sh, teks, size=12, color=INK, bold=False, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE):
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    baris = teks if isinstance(teks, (list, tuple)) else str(teks).split('\n')
    for i, b in enumerate(baris):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        _fill_runs(p, str(b), size, color, bold and i == 0 if len(baris) > 1 else bold)
    return sh


def _tb(S, teks, x, y, w, h, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, name=None):
    box = S.add_textbox(Inches(x), Inches(y), Inches(max(w, 0.05)), Inches(max(h, 0.05)))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    baris = teks if isinstance(teks, (list, tuple)) else [teks]
    for i, b in enumerate(baris):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if isinstance(b, dict):
            _fill_runs(p, str(b['text']), b.get('size', size), b.get('color', color), b.get('bold', bold))
        else:
            _fill_runs(p, str(b), size, color, bold)
    if name:
        box.name = name
    return box


def _line(S, x1, y1, x2, y2, color=OUTLINE, pt=0.75, dash=False, panah=False,
          kind=MSO_CONNECTOR.STRAIGHT):
    ln = S.add_connector(kind, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb = color
    ln.line.width = Pt(pt)
    if dash:
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        ln.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    if panah:
        _arrowhead(ln)
    return ln


def _arrowhead(conn):
    ln = conn.line._get_or_add_ln()
    for el in ln.findall(qn('a:tailEnd')):
        ln.remove(el)
    ln.append(ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'}))


def _connect(S, a, b, sa, sb, color=OUTLINE, pt=1.0, elbow=True, panah=True):
    """Konektor yang menempel ke dua bentuk. Titik sambung persegi: 0 atas, 1 kiri, 2 bawah, 3 kanan."""
    c = S.add_connector(MSO_CONNECTOR.ELBOW if elbow else MSO_CONNECTOR.STRAIGHT, 0, 0, 0, 0)
    c.begin_connect(a, sa)
    c.end_connect(b, sb)
    c.line.color.rgb = color
    c.line.width = Pt(pt)
    if panah:
        _arrowhead(c)
    return c


def _vtb(S, teks, cx, cy, panjang, size, bold=False, align=PP_ALIGN.CENTER, color=INK):
    """Teks tegak (diputar -90 derajat) berpusat di (cx, cy); dibaca dari bawah ke atas."""
    tb = S.add_textbox(Inches(cx - panjang / 2), Inches(cy - 0.14), Inches(panjang), Inches(0.28))
    tb.rotation = -90
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    _run(p, teks, size, color, bold=bold)
    return tb


def _fmt(v, fmt='{:,.0f}'):
    """Format angka Indonesia: ribuan titik, desimal koma."""
    if isinstance(v, str):
        return v
    s = fmt.format(v)
    return s.replace(',', '#').replace('.', ',').replace('#', '.')


def _text_color_on(fill):
    return WHITE if fill in (PRIMARY, DARK, A1, A4, NEG, TEAL) else INK


def add_legend(slide, items, x, y, w=None, size=10, gap=0.25):
    """items: [(label, warna, 'kotak'|'garis'|'bulat'|'belah')] berjajar horizontal.
    Mengembalikan lebar yang terpakai."""
    S = _group(slide, 'legenda')
    xx = x
    for lab, col, bentuk in items:
        if bentuk == 'garis':
            _line(S, xx, y + 0.09, xx + 0.28, y + 0.09, col, 2.25)
            sw = 0.28
        elif bentuk == 'bulat':
            _rect(S, xx, y + 0.02, 0.15, 0.15, col, shape=MSO_SHAPE.OVAL); sw = 0.15
        elif bentuk == 'belah':
            _rect(S, xx, y, 0.18, 0.18, col, shape=MSO_SHAPE.DIAMOND); sw = 0.18
        elif bentuk == 'kotak-garis':
            _rect(S, xx, y + 0.02, 0.15, 0.15, None, line=col, line_pt=1.25); sw = 0.15
        else:
            _rect(S, xx, y + 0.02, 0.15, 0.15, col); sw = 0.15
        tw = max(0.4, len(lab) * size * 0.55 / 72 + 0.1)
        _tb(S, lab, xx + sw + 0.08, y - 0.01, tw, 0.22, size=size, color=GRAY)
        xx += sw + 0.08 + tw + gap
    return xx - x


# =====================================================================================
# Chart data
# =====================================================================================
def _style_chart(ch, size=11):
    ch.font.name = FONT
    ch.font.size = Pt(size)
    ch.font.color.rgb = INK


def _no_gridlines(ax):
    ax.has_major_gridlines = False
    ax.has_minor_gridlines = False


def add_line_chart(slide, categories, series, x, y, w, h, highlight=0, number_format='#,##0',
                   proyeksi_mulai=None, label_semua=None, sumbu_nilai=False, fmt=None):
    """Tren waktu. series: [(nama, [nilai...]), ...]. Seri `highlight` PRIMARY tebal, seri lain abu.
    Nilai dilabel langsung pada seri sorotan; seri lain abu tanpa label, legenda kecil di atas.
    proyeksi_mulai : indeks kategori pertama yang merupakan proyeksi -> garis putus-putus.
    label_semua    : label nilai di semua titik seri sorotan (default: bila <= 8 kategori)."""
    from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_MARKER_STYLE
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    data = CategoryChartData()
    data.categories = list(categories)
    for nama, vals in series:
        data.add_series(nama, tuple(vals), number_format)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(x), Inches(y), Inches(w), Inches(h), data)
    ch = gf.chart
    _style_chart(ch)
    ch.has_legend = False
    ch.has_title = False
    n = len(categories)
    if label_semua is None:
        label_semua = n <= 8
    if fmt is None:
        desimal = any(isinstance(v, float) and v != int(v) for _, vs in series for v in vs if v is not None)
        fmt = '{:,.1f}' if desimal else '{:,.0f}'
    for k, ser in enumerate(ch.plots[0].series):
        top = k == highlight
        col = PRIMARY if top else (OUTLINE if len(series) > 2 else A4)
        ser.format.line.color.rgb = col
        ser.format.line.width = Pt(2.5 if top else 1.5)
        ser.smooth = False
        ser.marker.style = XL_MARKER_STYLE.CIRCLE if top else XL_MARKER_STYLE.NONE
        ser.marker.size = 6
        ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = col
        ser.marker.format.line.color.rgb = col
        if proyeksi_mulai is not None:
            for i in range(proyeksi_mulai, n):
                pt = ser.points[i]
                pt.format.line.color.rgb = col
                pt.format.line.width = Pt(2.5 if top else 1.5)
                pt.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        if not top:
            continue
        idxs = range(n) if label_semua else [0, n - 1]
        vals = series[k][1]
        for i in idxs:
            if vals[i] is None:
                continue
            dl = ser.points[i].data_label
            dl.has_text_frame = True
            dl.text_frame.text = _fmt(vals[i], fmt) if isinstance(vals[i], (int, float)) else str(vals[i])
            r = dl.text_frame.paragraphs[0].runs[0]
            r.font.size = Pt(11); r.font.name = FONT; r.font.bold = True
            r.font.color.rgb = PRIMARY
            dl.position = XL_LABEL_POSITION.ABOVE
    if len(series) > 1:                      # legenda di atas; nilai hanya pada seri sorotan
        from pptx.enum.chart import XL_LEGEND_POSITION
        ch.has_legend = True
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(10)
    va = ch.value_axis
    _no_gridlines(va)
    va.visible = sumbu_nilai
    va.tick_labels.font.size = Pt(10)
    ca = ch.category_axis
    _no_gridlines(ca)
    ca.format.line.color.rgb = OUTLINE
    ca.tick_labels.font.size = Pt(11)
    return ch


def add_stacked_chart(slide, categories, series, x, y, w, h, horizontal=False, persen=False,
                      colors=None, number_format='#,##0', legend=True, gap=55, label_min=None):
    """Komposisi per periode/item. series: [(nama, [nilai...]), ...], maks 5 seri.
    Urutan seri = urutan tumpukan (bawah ke atas) = urutan legenda.
    label_min : nilai minimum yang diberi label (segmen kecil tanpa label agar tidak sesak)."""
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
    data = CategoryChartData()
    data.categories = list(categories)
    for nama, vals in series:
        data.add_series(nama, tuple(vals), number_format)
    if horizontal:
        ct = XL_CHART_TYPE.BAR_STACKED_100 if persen else XL_CHART_TYPE.BAR_STACKED
    else:
        ct = XL_CHART_TYPE.COLUMN_STACKED_100 if persen else XL_CHART_TYPE.COLUMN_STACKED
    gf = slide.shapes.add_chart(ct, Inches(x), Inches(y), Inches(w), Inches(h), data)
    ch = gf.chart
    _style_chart(ch)
    ch.has_title = False
    ch.has_legend = legend and len(series) > 1
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(10)
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.overlap = 100
    cols = colors or SERI
    for k, ser in enumerate(plot.series):
        c = cols[k % len(cols)]
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb = c
        ser.format.line.color.rgb = WHITE; ser.format.line.width = Pt(0.75)
        vals = series[k][1]
        for i, v in enumerate(vals):
            if v is None or (label_min is not None and v < label_min) or v == 0:
                continue
            dl = ser.points[i].data_label
            dl.has_text_frame = True
            dl.text_frame.text = _fmt(v)
            r = dl.text_frame.paragraphs[0].runs[0]
            r.font.size = Pt(10); r.font.name = FONT
            r.font.color.rgb = _text_color_on(c)
            dl.position = XL_LABEL_POSITION.CENTER
    va = ch.value_axis
    _no_gridlines(va)
    va.visible = False
    ca = ch.category_axis
    _no_gridlines(ca)
    ca.format.line.color.rgb = OUTLINE
    ca.tick_labels.font.size = Pt(11)
    if horizontal:
        scaling = ca._element.find(qn('c:scaling'))
        for el in scaling.findall(qn('c:orientation')):
            scaling.remove(el)
        scaling.insert(0, scaling.makeelement(qn('c:orientation'), {'val': 'maxMin'}))
    return ch


def add_donut(slide, labels, values, x, y, d, highlight=0, tengah=None, tengah_sub=None,
              legenda=True, colors=None, legend_w=3.2, fmt='{:,.0f}', satuan=''):
    """Komposisi satu waktu (2–6 bagian). Bagian `highlight` PRIMARY, sisanya DARK/A4/TINT/abu.
    tengah : teks besar di lubang donat (mis. total '1.250 MW'). Legenda tabel kecil di kanan
    berisi label, nilai, dan persen."""
    from pptx.enum.chart import XL_CHART_TYPE
    data = CategoryChartData()
    data.categories = list(labels)
    data.add_series('seri', tuple(values))
    gf = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(x), Inches(y), Inches(d), Inches(d), data)
    ch = gf.chart
    _style_chart(ch)
    ch.has_legend = False
    ch.has_title = False
    dn = ch._chartSpace.find('.//' + qn('c:doughnutChart'))
    hs = dn.find(qn('c:holeSize'))
    if hs is None:
        hs = dn.makeelement(qn('c:holeSize'), {}); dn.append(hs)
    hs.set('val', '62')
    base = colors or [c for c in (DARK, A4, TINT, OUTLINE, A1)]
    warna = []
    j = 0
    for i in range(len(values)):
        if i == highlight:
            warna.append(PRIMARY)
        else:
            warna.append(base[j % len(base)]); j += 1
    ser = ch.plots[0].series[0]
    for i, pt in enumerate(ser.points):
        pt.format.fill.solid(); pt.format.fill.fore_color.rgb = warna[i]
        pt.format.line.color.rgb = WHITE; pt.format.line.width = Pt(1.5)
    if tengah:
        box = _tb(slide.shapes, [tengah] + ([tengah_sub] if tengah_sub else []), x + d * 0.2, y + d * 0.36,
                  d * 0.6, d * 0.3, size=20, color=DARK, bold=True, align=PP_ALIGN.CENTER,
                  anchor=MSO_ANCHOR.MIDDLE, name='Label tengah donat')
        if tengah_sub:
            r = box.text_frame.paragraphs[1].runs[0]
            r.font.size = Pt(11); r.font.bold = False; r.font.color.rgb = GRAY
    if legenda:
        S = _group(slide, 'legenda donat')
        tot = float(sum(values)) or 1.0
        rh = min(0.42, d / max(len(values), 1))
        y0 = y + (d - rh * len(values)) / 2
        for i, (lab, v) in enumerate(zip(labels, values)):
            yy = y0 + i * rh
            _rect(S, x + d + 0.3, yy + rh / 2 - 0.08, 0.16, 0.16, warna[i])
            _tb(S, lab, x + d + 0.6, yy, legend_w - 1.5, rh, size=12, bold=(i == highlight),
                anchor=MSO_ANCHOR.MIDDLE)
            _tb(S, '%s%s  (%s%%)' % (_fmt(v, fmt), satuan, _fmt(100 * v / tot, '{:.0f}')),
                x + d + legend_w - 0.9, yy, 1.4, rh, size=12, color=GRAY, align=PP_ALIGN.RIGHT,
                anchor=MSO_ANCHOR.MIDDLE)
    return ch


def add_waterfall(slide, labels, values, x, y, w, h, total=(0, -1), fmt='{:,.0f}', satuan='',
                  label_size=11, naik=PRIMARY, turun=NEG, warna_total=DARK):
    """Jembatan dari angka awal ke angka akhir (EBITDA, biaya, kapasitas).
    labels/values : nilai total untuk indeks di `total`, selisih (+/-) untuk sisanya.
    Contoh: add_waterfall(s, ['RKAP 2026','Harga gas','Kurs','Efisiensi','Prognosa'],
                             [1250, -180, -60, 95, 1105], L, BODY_TOP, CW, 4.5)
    Dibangun dari bentuk (bukan chart) supaya label, garis penghubung, dan warna presisi."""
    S = _group(slide, 'waterfall')
    n = len(values)
    tot_idx = {i % n for i in total}
    tops, bases, run = [], [], 0.0
    for i, v in enumerate(values):
        if i in tot_idx:
            bases.append(0.0); tops.append(float(v)); run = float(v)
        else:
            a, b = run, run + v
            bases.append(min(a, b)); tops.append(max(a, b)); run = b
    lo = min(0.0, min(bases))
    hi = max(tops) * 1.0
    lab_h, cat_h = 0.3, 0.5
    py, ph = y + lab_h, h - lab_h - cat_h
    scale = ph / ((hi - lo) or 1)
    slot = w / n
    bw = slot * 0.62
    Y = lambda v: py + (hi - v) * scale
    _line(S, x, Y(0), x + w, Y(0), OUTLINE, 1.0)
    prev_end = None
    for i, v in enumerate(values):
        cx = x + slot * i + (slot - bw) / 2
        if i in tot_idx:
            col = warna_total
        else:
            col = naik if v >= 0 else turun
        _rect(S, cx, Y(tops[i]), bw, max(Y(bases[i]) - Y(tops[i]), 0.01), col, name='Batang ' + str(labels[i]))
        txt = _fmt(v, fmt) + satuan
        if i not in tot_idx and v > 0:
            txt = '+' + txt
        _tb(S, txt, cx - 0.2, Y(tops[i]) - 0.28, bw + 0.4, 0.26, size=label_size,
            color=INK if i in tot_idx else (PRIMARY if v >= 0 else turun), bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
        _tb(S, labels[i], x + slot * i + 0.03, Y(lo) + 0.08, slot - 0.06, cat_h - 0.08, size=11,
            color=INK, bold=i in tot_idx, align=PP_ALIGN.CENTER)
        level = tops[i] if (i in tot_idx or v >= 0) else bases[i]
        if prev_end is not None:
            _line(S, prev_end[0], Y(prev_end[1]), cx, Y(prev_end[1]), GRAY, 0.5, dash=True)
        prev_end = (cx + bw, level)
    return S


def add_tornado(slide, faktor, rendah, tinggi, dasar, x, y, w, h, fmt='{:.1f}', satuan='%',
                label_w=2.4, judul_rendah='Skenario rendah', judul_tinggi='Skenario tinggi'):
    """Sensitivitas (IRR/NPV/LCOE) terhadap beberapa faktor. rendah/tinggi = nilai hasil (bukan
    selisih) saat faktor di ujung bawah/atas. Diurutkan otomatis dari rentang terbesar.
    Batang dasar -> kiri abu, kanan PRIMARY; garis tegak = kasus dasar."""
    S = _group(slide, 'tornado')
    rows = sorted(zip(faktor, rendah, tinggi), key=lambda r: -abs(r[2] - r[1]))
    lo = min(min(r[1], r[2]) for r in rows + [('', dasar, dasar)])
    hi = max(max(r[1], r[2]) for r in rows + [('', dasar, dasar)])
    pad = (hi - lo) * 0.18 or 1
    lo, hi = lo - pad, hi + pad
    head = 0.45
    gx, gw = x + label_w, w - label_w
    X = lambda v: gx + (v - lo) / (hi - lo) * gw
    rh = (h - head) / len(rows)
    bh = min(rh * 0.6, 0.42)
    _tb(S, judul_rendah, gx, y, X(dasar) - gx - 0.1, 0.3, size=10, color=GRAY, align=PP_ALIGN.RIGHT)
    _tb(S, judul_tinggi, X(dasar) + 0.1, y, gx + gw - X(dasar) - 0.1, 0.3, size=10, color=GRAY)
    for k, (f, a, b) in enumerate(rows):
        yy = y + head + k * rh + (rh - bh) / 2
        _tb(S, f, x, yy - 0.05, label_w - 0.15, bh + 0.1, size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        for v in (a, b):
            left, right = min(v, dasar), max(v, dasar)
            col = PRIMARY if v > dasar else OUTLINE
            _rect(S, X(left), yy, max(X(right) - X(left), 0.02), bh, col)
            txt = _fmt(v, fmt) + satuan
            if v >= dasar:
                _tb(S, txt, X(right) + 0.06, yy, 0.9, bh, size=11, color=INK, anchor=MSO_ANCHOR.MIDDLE)
            else:
                _tb(S, txt, X(left) - 0.96, yy, 0.9, bh, size=11, color=INK, align=PP_ALIGN.RIGHT,
                    anchor=MSO_ANCHOR.MIDDLE)
        if k < len(rows) - 1:
            _line(S, x, y + head + (k + 1) * rh, x + w, y + head + (k + 1) * rh, LIGHT, 0.5)
    _line(S, X(dasar), y + head - 0.1, X(dasar), y + h, DARK, 1.25)
    _tb(S, 'Dasar ' + _fmt(dasar, fmt) + satuan, X(dasar) - 0.8, y + h + 0.02, 1.6, 0.25, size=10,
        color=DARK, bold=True, align=PP_ALIGN.CENTER)
    return S


def add_funnel(slide, tahap, x, y, w, h, satuan='', fmt='{:,.0f}', label_w=2.6, sorot=None,
               konversi=True):
    """Corong pipeline (kapasitas potensi -> tersaring -> siap lelang -> COD).
    tahap: [{'label','nilai','ket'(opsional)}]. Batang terpusat, lebar sebanding nilai.
    Kolom kanan: persentase terhadap tahap sebelumnya bila konversi=True."""
    S = _group(slide, 'corong')
    n = len(tahap)
    mx = max(t['nilai'] for t in tahap) or 1
    right_w = 1.5 if konversi else 0.0
    gx, gw = x + label_w, w - label_w - right_w
    rh = h / n
    bh = rh * 0.72
    for i, t in enumerate(tahap):
        yy = y + i * rh
        bw = max(gw * t['nilai'] / mx, 0.5)
        on = (sorot is None and i == n - 1) or sorot == i
        col = PRIMARY if on else (DARK if i == 0 else A4)
        b = _rect(S, gx + (gw - bw) / 2, yy + (rh - bh) / 2, bw, bh, col)
        lab = _fmt(t['nilai'], fmt) + (' ' + satuan if satuan else '')
        if bw >= len(lab) * 13 * 0.6 / 72 + 0.2:
            _shape_text(b, lab, 13, WHITE, True)
        else:                                   # batang sempit: label di kanan batang
            _tb(S, lab, gx + (gw + bw) / 2 + 0.08, yy, 1.4, rh, size=13, color=col, bold=True,
                anchor=MSO_ANCHOR.MIDDLE)
        _tb(S, [{'text': t['label'], 'bold': True}] + ([{'text': t['ket'], 'size': 10, 'color': GRAY}]
            if t.get('ket') else []), x, yy, label_w - 0.2, rh, size=12, anchor=MSO_ANCHOR.MIDDLE)
        if konversi and i > 0:
            p = 100.0 * t['nilai'] / (tahap[i - 1]['nilai'] or 1)
            _tb(S, _fmt(p, '{:.0f}') + '%', gx + gw + 0.2, yy - rh * 0.15, right_w - 0.2, rh * 0.3,
                size=11, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
    if konversi:
        _tb(S, 'Lolos dari tahap sebelumnya', gx + gw + 0.2, y - 0.35, right_w, 0.3, size=9, color=GRAY)
    return S


def add_progress(slide, baris, x, y, w, row_h=0.5, label_w=3.0, nilai_w=0.8, header=None,
                 target_label='Target', status=False):
    """Kemajuan per proyek/paket (progress fisik, serapan anggaran, capaian KPI).
    baris : [{'label','nilai'(0-100),'target'(opsional),'ket'(opsional),'status':'hijau'|'kuning'|'merah'}]
    Trek abu terang, isian PRIMARY (DARK bila >= target), garis tegak = target.
    status=True menambah kolom lampu lalu lintas (satu kolom, dengan legenda di pemanggil)."""
    from plnip_deck import TL_GREEN, TL_YELLOW, TL_RED
    S = _group(slide, 'progres')
    st_w = 0.75 if status else 0.0
    gx = x + label_w
    gw = w - label_w - nilai_w - st_w
    yy0 = y
    if header:
        for j, (tx, xx, ww, al) in enumerate([(header[0], x, label_w, PP_ALIGN.LEFT),
                                               (header[1], gx, gw + nilai_w, PP_ALIGN.LEFT)] +
                                              ([(header[2], gx + gw + nilai_w, st_w, PP_ALIGN.CENTER)]
                                               if status and len(header) > 2 else [])):
            _tb(S, tx, xx, y, ww, 0.36, size=12, bold=True, align=al, anchor=MSO_ANCHOR.BOTTOM)
        _line(S, x, y + 0.42, x + w, y + 0.42, PRIMARY, 1.5)
        yy0 = y + 0.5
    bh = min(row_h * 0.42, 0.24)
    for i, b in enumerate(baris):
        yy = yy0 + i * row_h
        lab = [{'text': b['label'], 'bold': True}]
        if b.get('ket'):
            lab.append({'text': b['ket'], 'size': 10, 'color': GRAY})
        _tb(S, lab, x, yy, label_w - 0.15, row_h, size=12, anchor=MSO_ANCHOR.MIDDLE)
        by = yy + (row_h - bh) / 2
        _rect(S, gx, by, gw, bh, LIGHT)
        v = max(0, min(100, b['nilai']))
        tgt = b.get('target')
        col = DARK if (tgt is not None and v >= tgt) else PRIMARY
        if v > 0:
            _rect(S, gx, by, gw * v / 100.0, bh, col)
        if tgt is not None:
            tx = gx + gw * tgt / 100.0
            _line(S, tx, by - 0.08, tx, by + bh + 0.08, INK, 1.5)
        _tb(S, _fmt(b['nilai'], '{:.0f}') + '%', gx + gw + 0.1, yy, nilai_w - 0.1, row_h, size=12,
            bold=True, color=col, anchor=MSO_ANCHOR.MIDDLE)
        if status and b.get('status'):
            c = {'hijau': TL_GREEN, 'kuning': TL_YELLOW, 'merah': TL_RED}[b['status']]
            _rect(S, gx + gw + nilai_w + st_w / 2 - 0.1, yy + row_h / 2 - 0.1, 0.2, 0.2, c, shape=MSO_SHAPE.OVAL)
        if i < len(baris) - 1:
            _line(S, x, yy + row_h, x + w, yy + row_h, LIGHT, 0.5)
    if any(b.get('target') is not None for b in baris):
        yl = yy0 + len(baris) * row_h + 0.1
        _line(S, gx, yl + 0.02, gx, yl + 0.2, INK, 1.5)
        _tb(S, target_label, gx + 0.08, yl, 1.5, 0.22, size=10, color=GRAY)
    return S


# =====================================================================================
# Waktu
# =====================================================================================
def _tpos(t, t0, t1, x, w):
    return x + (float(t) - t0) / float(t1 - t0) * w


def add_timeline(slide, milestones, x, y, w, mulai, selesai, fase=None, hari_ini=None,
                 label_hari_ini='Saat ini', tick=1.0, tick_fmt=lambda t: str(int(t)), label_w=1.7):
    """Timeline milestone terstruktur (bukan lingkaran mengambang): pita tahun sebagai sumbu, pita fase,
    dan baris milestone dengan label pada baris tetap di bawah garis.

    Waktu dalam angka desimal tahun (2026.0 = Jan 2026, 2026.5 = Jul 2026) atau indeks bebas.
    milestones : [{'t': 2027.25, 'label': 'FC', 'ket': 'Apr 2027', 'status': 'selesai'|'rencana'|'kunci'}]
    fase       : [{'mulai','selesai','label','redup':bool}]  (baris pita di atas garis milestone)
    hari_ini   : waktu penanda 'saat ini' (garis tegak putus-putus PRIMARY)."""
    S = _group(slide, 'timeline')
    X = lambda t: _tpos(t, mulai, selesai, x, w)
    # sumbu periode (seperti header tabel)
    t = mulai
    while t < selesai - 1e-9:
        t2 = min(t + tick, selesai)
        _tb(S, tick_fmt(t), X(t), y, X(t2) - X(t), 0.32, size=12, bold=True, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.BOTTOM)
        if t > mulai:
            _line(S, X(t), y + 0.4, X(t), y + 0.4 + (0.55 if fase else 0) + 0.75, LIGHT, 0.75)
        t = t2
    _line(S, x, y + 0.38, x + w, y + 0.38, PRIMARY, 1.5)
    yy = y + 0.52
    if fase:
        for f in fase:
            b = _rect(S, X(f['mulai']) + 0.02, yy, X(f['selesai']) - X(f['mulai']) - 0.04, 0.38,
                      OUTLINE if f.get('redup') else TINT)
            _shape_text(b, f['label'], 11, INK, True)
        yy += 0.55
    ly = yy + 0.3
    _line(S, x, ly, x + w, ly, OUTLINE, 1.5)
    # milestone + label anti-tabrakan (baris kedua bila terlalu rapat)
    ms = sorted(milestones, key=lambda m: m['t'])
    last_end = [-99.0, -99.0]
    for m in ms:
        cx = X(m['t'])
        st = m.get('status', 'rencana')
        d = 0.26 if st == 'kunci' else 0.2
        fill = {'selesai': PRIMARY, 'kunci': DARK}.get(st)
        _rect(S, cx - d / 2, ly - d / 2, d, d, fill if fill else WHITE, line=None if fill else PRIMARY,
              line_pt=1.5, shape=MSO_SHAPE.DIAMOND, name='Milestone ' + m['label'])
        row = 0 if cx - label_w / 2 > last_end[0] + 0.05 else (1 if cx - label_w / 2 > last_end[1] + 0.05 else 0)
        last_end[row] = cx + label_w / 2
        ty = ly + 0.25 + row * 0.72
        if row:
            _line(S, cx, ly + 0.15, cx, ty, LIGHT, 0.75)
        teks = [{'text': m['label'], 'bold': True}]
        if m.get('ket'):
            teks.append({'text': m['ket'], 'size': 10, 'color': GRAY})
        _tb(S, teks, cx - label_w / 2, ty, label_w, 0.62, size=11, align=PP_ALIGN.CENTER)
    if hari_ini is not None:
        hx = X(hari_ini)
        _line(S, hx, y + 0.4, hx, ly + 1.55, PRIMARY, 1.25, dash=True)
        _tb(S, label_hari_ini, hx + 0.05, ly + 1.35, 1.6, 0.22, size=10, color=PRIMARY, bold=True)
    return S


def add_gantt(slide, periode, baris, x, y, w, label_w=2.8, row_h=0.4, hari_ini=None,
              label_hari_ini='Saat ini', legenda=True, ket_w=0.0):
    """Jadwal/peta jalan bergaya Gantt.

    periode : label kolom waktu ['Q1 26', 'Q2 26', ...] atau ['2026', '2027', ...]
    baris   : [{'label', 'mulai', 'selesai', 'status': 'selesai'|'berjalan'|'rencana'|'kritis',
                'milestone': t (opsional; alias lama 'tonggak'), 'grup': True (baris judul kelompok), 'ket': teks kanan}]
              mulai/selesai dalam satuan kolom (0 = awal kolom pertama, 2.5 = pertengahan kolom ke-3).
    hari_ini: posisi dalam satuan kolom (garis tegak putus-putus)."""
    S = _group(slide, 'gantt')
    n = len(periode)
    gx = x + label_w
    gw = w - label_w - ket_w
    cw = gw / n
    X = lambda t: gx + t * cw
    for j, p in enumerate(periode):
        _tb(S, p, X(j), y, cw, 0.34, size=11, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
    _line(S, x, y + 0.4, x + w, y + 0.4, PRIMARY, 1.5)
    top = y + 0.46
    for j in range(1, n):
        _line(S, X(j), top, X(j), top + row_h * len(baris), LIGHT, 0.75)
    warna = {'selesai': DARK, 'berjalan': PRIMARY, 'rencana': TINT, 'kritis': NEG}
    for i, b in enumerate(baris):
        yy = top + i * row_h
        grup = b.get('grup')
        _tb(S, b['label'], x + (0 if grup else 0.15), yy, label_w - 0.2, row_h, size=12 if grup else 11,
            bold=grup, color=INK if grup else INK, anchor=MSO_ANCHOR.MIDDLE)
        if 'mulai' in b and 'selesai' in b:
            bh = row_h * (0.22 if grup else 0.5)
            col = DARK if grup else warna.get(b.get('status', 'rencana'), TINT)
            _rect(S, X(b['mulai']), yy + (row_h - bh) / 2, X(b['selesai']) - X(b['mulai']), bh, col)
        ms = b.get('milestone', b.get('tonggak'))
        if ms is not None:
            d = row_h * 0.55
            _rect(S, X(ms) - d / 2, yy + (row_h - d) / 2, d, d, DARK, shape=MSO_SHAPE.DIAMOND)
        if ket_w and b.get('ket'):
            _tb(S, b['ket'], gx + gw + 0.1, yy, ket_w - 0.1, row_h, size=10, color=GRAY,
                anchor=MSO_ANCHOR.MIDDLE)
        if grup and i > 0:
            _line(S, x, yy, x + w, yy, OUTLINE, 0.75)
    bottom = top + row_h * len(baris)
    _line(S, x, bottom, x + w, bottom, OUTLINE, 0.75)
    if hari_ini is not None:
        _line(S, X(hari_ini), y + 0.4, X(hari_ini), bottom + 0.05, PRIMARY, 1.25, dash=True)
        _tb(S, label_hari_ini, X(hari_ini) - 0.8, bottom + 0.06, 1.6, 0.22, size=10, color=PRIMARY,
            bold=True, align=PP_ALIGN.CENTER)
    if legenda:
        pakai = []
        st = {b.get('status') for b in baris if not b.get('grup') and 'mulai' in b}
        for k, lab in (('selesai', 'Selesai'), ('berjalan', 'Berjalan'), ('rencana', 'Rencana'), ('kritis', 'Kritis')):
            if k in st:
                pakai.append((lab, warna[k], 'kotak'))
        if any(b.get('milestone', b.get('tonggak')) is not None for b in baris):
            pakai.append(('Milestone', DARK, 'belah'))
        if pakai:
            add_legend(slide, pakai, x, bottom + 0.35)
    return S


# =====================================================================================
# Proses
# =====================================================================================
def add_flow(slide, langkah, x, y, w, h=1.3, arah='h', sorot=None, gap=0.45, ikon_d=0.5):
    """Alur proses/energi (PLTS -> BESS -> Gardu -> Beban; pengadaan -> kontrak -> konstruksi).
    langkah : [{'judul','sub'(opsional),'ikon'(opsional)}]; 2–6 langkah.
    arah    : 'h' (kiri->kanan) atau 'v' (atas->bawah; h = tinggi total).
    Kotak TINT tanpa garis tepi; langkah `sorot` (indeks atau daftar) PRIMARY dengan teks putih."""
    S = _group(slide, 'alur')
    n = len(langkah)
    sor = set(sorot) if isinstance(sorot, (list, tuple, set)) else ({sorot} if sorot is not None else set())
    if arah == 'h':
        bw = (w - gap * (n - 1)) / n
        boxes = [(x + i * (bw + gap), y, bw, h) for i in range(n)]
    else:
        bh = (h - gap * (n - 1)) / n
        boxes = [(x, y + i * (bh + gap), w, bh) for i in range(n)]
    for i, (lk, (bx, by, bw_, bh_)) in enumerate(zip(langkah, boxes)):
        on = i in sor
        fill = PRIMARY if on else TINT
        tc = WHITE if on else INK
        _rect(S, bx, by, bw_, bh_, fill, name='Langkah ' + str(i + 1))
        ty = by + 0.12
        if lk.get('ikon') and arah == 'h':
            pic = S.add_picture(icon_path(lk['ikon'], 'white' if on else 'primary'),
                                Inches(bx + (bw_ - ikon_d) / 2), Inches(by + 0.15), Inches(ikon_d), Inches(ikon_d))
            pic.name = 'Ikon ' + lk['ikon']
            ty = by + 0.2 + ikon_d
        elif lk.get('ikon'):
            pic = S.add_picture(icon_path(lk['ikon'], 'white' if on else 'primary'),
                                Inches(bx + 0.15), Inches(by + (bh_ - ikon_d) / 2), Inches(ikon_d), Inches(ikon_d))
            pic.name = 'Ikon ' + lk['ikon']
        tx = bx + (0.3 + ikon_d if (lk.get('ikon') and arah != 'h') else 0.1)
        tw = bw_ - (tx - bx) - 0.1
        teks = [{'text': lk['judul'], 'bold': True, 'size': 13}]
        if lk.get('sub'):
            teks.append({'text': lk['sub'], 'size': 11, 'color': tc})
        _tb(S, teks, tx, ty, tw, by + bh_ - ty - 0.08, size=12, color=tc,
            align=PP_ALIGN.CENTER if arah == 'h' else PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP if (arah == 'h' and lk.get('ikon')) else MSO_ANCHOR.MIDDLE)
        if i < n - 1:
            if arah == 'h':
                ax, ay = bx + bw_ + 0.08, by + bh_ / 2
                a = S.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(ax + (gap - 0.16) / 2 - 0.04),
                                Inches(ay - 0.12), Inches(0.24), Inches(0.24))
                a.rotation = 90
            else:
                ax, ay = bx + bw_ / 2, by + bh_ + 0.08
                a = S.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(ax - 0.12),
                                Inches(ay + (gap - 0.16) / 2 - 0.1), Inches(0.24), Inches(0.2))
                a.rotation = 180
            a.fill.solid(); a.fill.fore_color.rgb = PRIMARY; a.line.fill.background(); a.shadow.inherit = False
    return S


def add_stage_gate(slide, tahap, x, y, w, h, gerbang=None, aktif=None, head_h=0.6, size=11):
    """Tahapan berpintu (stage-gate) atau rantai nilai.
    tahap   : [{'judul', 'butir': [...]}] 3–6 tahap. Chevron di atas, kolom butir sejajar di bawahnya.
    gerbang : label gerbang antar-tahap (len = jumlah tahap - 1), mis. ['G1', 'G2', 'G3']; None = rantai nilai.
    aktif   : indeks tahap saat ini; tahap sesudahnya dibuat abu."""
    S = _group(slide, 'tahapan')
    n = len(tahap)
    overlap = 0.12
    sw = (w + overlap * (n - 1)) / n
    for i, t in enumerate(tahap):
        sx = x + i * (sw - overlap)
        redup = aktif is not None and i > aktif
        shp = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        c = S.add_shape(shp, Inches(sx), Inches(y), Inches(sw), Inches(head_h))
        c.fill.solid(); c.fill.fore_color.rgb = OUTLINE if redup else (DARK if aktif == i else PRIMARY)
        c.line.fill.background(); c.shadow.inherit = False
        _shape_text(c, t['judul'], 12, WHITE, True)
        col_x = sx + 0.12 + (0.1 if i else 0)
        col_w = sw - overlap - 0.24
        box = S.add_textbox(Inches(col_x), Inches(y + head_h + 0.2), Inches(col_w), Inches(h - head_h - 0.2))
        tf = box.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for k, b in enumerate(t.get('butir', [])):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.space_after = Pt(5)
            _bullet(p, '•', 0)
            _fill_runs(p, b, size, GRAY if redup else INK)
        if i > 0:
            lx = sx + overlap / 2 + 0.02
            _line(S, lx, y + head_h + 0.15, lx, y + h, LIGHT, 0.75)
    if gerbang:
        for i, g in enumerate(gerbang[:n - 1]):
            gx = x + (i + 1) * (sw - overlap) + overlap / 2
            d = 0.42
            dm = _rect(S, gx - d / 2, y + head_h / 2 - d / 2, d, d, DARK, shape=MSO_SHAPE.DIAMOND, name='Gerbang ' + g)
            _shape_text(dm, g, 9, WHITE, True)
            dm.text_frame.margin_left = dm.text_frame.margin_right = 0
    return S


def add_swimlane(slide, lajur, langkah, n_kolom, x, y, w, h, alur=None, kolom=None,
                 label_w=1.6, box_h=0.62, sorot=None, size=10):
    """Proses lintas pihak (PLN - PLN IP - EPC - Lender; tata kelola persetujuan).
    lajur   : nama pihak per lajur (atas ke bawah).
    langkah : [{'lajur': i, 'kolom': j, 'teks': '...'}]  (j = urutan waktu/fase, mulai 0)
    alur    : [(a, b), ...] indeks langkah yang disambung panah; None = urut sesuai daftar.
    kolom   : label fase di atas kolom (opsional). sorot: indeks langkah keputusan (PRIMARY)."""
    S = _group(slide, 'swimlane')
    head = 0.4 if kolom else 0.0
    lh = (h - head) / len(lajur)
    gx = x + label_w
    cw = (w - label_w) / n_kolom
    if kolom:
        for j, k in enumerate(kolom):
            _tb(S, k, gx + j * cw, y, cw, 0.32, size=11, bold=True, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.BOTTOM)
        _line(S, gx, y + 0.36, x + w, y + 0.36, PRIMARY, 1.5)
    for i, nama in enumerate(lajur):
        ly = y + head + i * lh
        lb = _rect(S, x, ly + 0.03, label_w - 0.1, lh - 0.06, TINT)
        _shape_text(lb, nama, 12, DARK, True)
        if i < len(lajur) - 1:
            _line(S, x, ly + lh, x + w, ly + lh, OUTLINE, 0.75, dash=True)
    sor = set(sorot) if isinstance(sorot, (list, tuple, set)) else ({sorot} if sorot is not None else set())
    shapes = []
    bw = cw * 0.84
    for k, st in enumerate(langkah):
        bx = gx + st['kolom'] * cw + (cw - bw) / 2
        by = y + head + st['lajur'] * lh + (lh - box_h) / 2
        on = k in sor
        b = _rect(S, bx, by, bw, box_h, PRIMARY if on else WHITE, line=None if on else PRIMARY,
                  line_pt=1.0, name='Langkah %d' % (k + 1))
        _shape_text(b, st['teks'], size, WHITE if on else INK, on)
        shapes.append((b, st))
    pairs = alur if alur is not None else [(k, k + 1) for k in range(len(langkah) - 1)]
    for a, bb in pairs:
        sa, sta = shapes[a]
        sb, stb = shapes[bb]
        if sta['lajur'] == stb['lajur']:
            _connect(S, sa, sb, 3, 1, GRAY, 1.0, elbow=False)
        elif sta['kolom'] == stb['kolom']:
            down = stb['lajur'] > sta['lajur']
            _connect(S, sa, sb, 2 if down else 0, 0 if down else 2, GRAY, 1.0, elbow=False)
        else:
            _connect(S, sa, sb, 3, 1, GRAY, 1.0, elbow=True)
    try:
        S._recalculate_extents()        # konektor dibuat di (0,0) lalu ditempel: rapikan batas group
    except Exception:
        pass
    return S


def add_cycle(slide, langkah, cx, cy, r, sorot=None, d=0.62, label_w=2.6, size=11):
    """Siklus berulang (cadence rapat, PDCA, siklus pemeliharaan). 3–6 langkah.
    langkah: [{'judul','sub'}]; nomor dalam lingkaran di atas cincin, teks di luar cincin."""
    S = _group(slide, 'siklus')
    ring = _rect(S, cx - r, cy - r, 2 * r, 2 * r, None, line=OUTLINE, line_pt=1.5, shape=MSO_SHAPE.OVAL)
    n = len(langkah)
    for i, lk in enumerate(langkah):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
        # panah arah di tengah busur
        am = ang + math.pi / n
        ax, ay = cx + r * math.cos(am), cy + r * math.sin(am)
        t = S.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(ax - 0.09), Inches(ay - 0.09), Inches(0.18), Inches(0.18))
        t.rotation = math.degrees(am) + 180
        t.fill.solid(); t.fill.fore_color.rgb = OUTLINE; t.line.fill.background(); t.shadow.inherit = False
        on = sorot == i
        c = _rect(S, px - d / 2, py - d / 2, d, d, DARK if on else PRIMARY, shape=MSO_SHAPE.OVAL)
        _shape_text(c, str(i + 1), 14, WHITE, True)
        c.text_frame.margin_left = c.text_frame.margin_right = 0
        # teks di luar cincin
        ox = math.cos(ang); oy = math.sin(ang)
        tx = px + ox * (d / 2 + 0.15)
        ty = py + oy * (d / 2 + 0.1)
        al = PP_ALIGN.LEFT if ox > 0.3 else (PP_ALIGN.RIGHT if ox < -0.3 else PP_ALIGN.CENTER)
        bx = tx if al == PP_ALIGN.LEFT else (tx - label_w if al == PP_ALIGN.RIGHT else tx - label_w / 2)
        by = ty - 0.3 if abs(oy) < 0.5 else (ty if oy > 0 else ty - 0.62)
        teks = [{'text': lk['judul'], 'bold': True}]
        if lk.get('sub'):
            teks.append({'text': lk['sub'], 'size': size - 1, 'color': GRAY})
        _tb(S, teks, bx, by, label_w, 0.62, size=size + 1, align=al)
    return S


# =====================================================================================
# Struktur
# =====================================================================================
def add_issue_tree(slide, akar, cabang, x, y, w, h, root_w=2.2, l1_w=3.0, size=11):
    """Pohon isu kiri->kanan (masalah -> penyebab -> bukti/sub-penyebab).
    cabang: [{'teks', 'anak': [...], 'utama': bool}]  'utama' = penyebab terbukti (bold + garis PRIMARY)."""
    S = _group(slide, 'pohon isu')
    n = len(cabang)
    rh = h / n
    rb = _rect(S, x, y + h / 2 - 0.55, root_w, 1.1, DARK)
    _shape_text(rb, akar, 13, WHITE, True)
    l1x = x + root_w + 0.55
    l2x = l1x + l1_w + 0.5
    jx = x + root_w + 0.25
    _line(S, x + root_w, y + h / 2, jx, y + h / 2, OUTLINE, 1.0)
    ys = [y + i * rh + rh / 2 for i in range(n)]
    _line(S, jx, ys[0], jx, ys[-1], OUTLINE, 1.0)
    for i, c in enumerate(cabang):
        cy = ys[i]
        key = c.get('utama')
        col = PRIMARY if key else OUTLINE
        _line(S, jx, cy, l1x, cy, col, 1.5 if key else 1.0)
        bh = min(rh - 0.12, 0.8)
        b = _rect(S, l1x, cy - bh / 2, l1_w, bh, PRIMARY if key else TINT)
        _shape_text(b, c['teks'], size + 1, WHITE if key else INK, key, align=PP_ALIGN.LEFT)
        anak = c.get('anak', [])
        if anak:
            _line(S, l1x + l1_w, cy, l2x - 0.15, cy, col, 1.0)
            box = S.add_textbox(Inches(l2x), Inches(cy - rh / 2 + 0.05), Inches(x + w - l2x), Inches(rh - 0.1))
            tf = box.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            for k, a in enumerate(anak):
                p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
                p.space_after = Pt(2)
                _bullet(p, '•', 0)
                _fill_runs(p, a, size, INK, bold=False)
        if i < n - 1:
            _line(S, l1x, cy + rh / 2, x + w, cy + rh / 2, LIGHT, 0.5)
    return S


def add_org_chart(slide, pohon, x, y, w, h, box_w=None, box_h=0.7, size=11):
    """Struktur organisasi / kepemilikan / tata kelola, atas->bawah, maksimal 3 tingkat.
    pohon: {'teks','sub', 'anak': [{'teks','sub','label' (mis. '51%' di garis), 'anak': [...]}]}
    Tingkat 0 DARK, tingkat 1 PRIMARY/TINT (sorot=True -> PRIMARY), tingkat 2 teks TINT."""
    S = _group(slide, 'struktur')

    def leaves(nd):
        a = nd.get('anak', [])
        return max(1, sum(leaves(c) for c in a)) if a else 1

    levels = 1 + (1 if pohon.get('anak') else 0) + (1 if any(c.get('anak') for c in pohon.get('anak', [])) else 0)
    vgap = (h - box_h * levels) / max(levels - 1, 1)
    total = leaves(pohon)
    unit = w / total
    bw_default = box_w or min(unit * 0.86, 2.6)

    def draw(nd, lvl, x0, x1):
        cx = (x0 + x1) / 2
        by = y + lvl * (box_h + vgap)
        bw = min(bw_default, x1 - x0 - 0.1) if lvl else min(max(bw_default, 2.4), w)
        fill = DARK if lvl == 0 else (PRIMARY if (lvl == 1 and nd.get('sorot')) else TINT)
        b = _rect(S, cx - bw / 2, by, bw, box_h, fill)
        teks = [nd['teks']] + ([nd['sub']] if nd.get('sub') else [])
        _shape_text(b, teks, size + 1, _text_color_on(fill), True)
        if nd.get('sub'):
            r = b.text_frame.paragraphs[1].runs[0]
            r.font.size = Pt(size - 1); r.font.bold = False
        kids = nd.get('anak', [])
        if kids:
            my = by + box_h + vgap / 2
            _line(S, cx, by + box_h, cx, my, GRAY, 1.0)
            xs = []
            cur = x0
            for c in kids:
                span = (x1 - x0) * leaves(c) / leaves(nd)
                xs.append((cur, cur + span)); cur += span
            ccx = [(a + b_) / 2 for a, b_ in xs]
            _line(S, min(ccx), my, max(ccx), my, GRAY, 1.0)
            for c, (a, b_) in zip(kids, xs):
                kx = (a + b_) / 2
                _line(S, kx, my, kx, my + vgap / 2, GRAY, 1.0, panah=True)
                if c.get('label'):
                    _tb(S, c['label'], kx + 0.06, my + 0.02, 1.0, vgap / 2 - 0.04, size=10, color=PRIMARY,
                        bold=True, anchor=MSO_ANCHOR.MIDDLE)
                draw(c, lvl + 1, a, b_)
    draw(pohon, 0, x, x + w)
    return S


def add_pillars(slide, atap, pilar, x, y, w, h, fondasi=None, gap=0.25, size=12):
    """Rumah strategi: atap (aspirasi) - pilar (inisiatif) - fondasi (enabler).
    pilar: [{'judul', 'butir': [...]}] 3–5 pilar. Pilar tanpa isian warna; judul bergaris bawah PRIMARY."""
    S = _group(slide, 'pilar')
    rh = 0.7
    roof = _rect(S, x, y, w, rh, DARK)
    _shape_text(roof, atap, 14, WHITE, True)
    fh = 0.55 if fondasi else 0
    n = len(pilar)
    pw = (w - gap * (n - 1)) / n
    py = y + rh + 0.2
    ph = h - rh - 0.2 - (fh + 0.2 if fondasi else 0)
    for i, p in enumerate(pilar):
        px = x + i * (pw + gap)
        _tb(S, p['judul'], px, py, pw, 0.45, size=size + 1, bold=True, anchor=MSO_ANCHOR.BOTTOM)
        _line(S, px, py + 0.5, px + pw, py + 0.5, PRIMARY, 1.5)
        box = S.add_textbox(Inches(px), Inches(py + 0.62), Inches(pw), Inches(ph - 0.62))
        tf = box.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for k, b in enumerate(p.get('butir', [])):
            para = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            para.space_after = Pt(5)
            _bullet(para, '•', 0)
            _fill_runs(para, b, size - 1, INK)
        if i:
            _line(S, px - gap / 2, py + 0.1, px - gap / 2, py + ph, LIGHT, 0.75)
    if fondasi:
        fb = _rect(S, x, y + h - fh, w, fh, TINT)
        _shape_text(fb, fondasi, 12, DARK, True)
    return S


# =====================================================================================
# Penilaian
# =====================================================================================
def add_matrix_2x2(slide, items, x, y, w, h, sumbu_x=('Rendah', 'Tinggi', 'Kemudahan'),
                   sumbu_y=('Rendah', 'Tinggi', 'Dampak'), kuadran=None, rekomendasi=1,
                   d=0.22, size=11):
    """Matriks dua sumbu (dampak x kemudahan, daya tarik x kemampuan menang).
    items    : [{'label', 'x': 0..1, 'y': 0..1, 'sorot': bool, 'nilai': ukuran relatif (opsional)}]
    kuadran  : nama 4 kuadran urut [kiri-atas, kanan-atas, kiri-bawah, kanan-bawah]
    rekomendasi : indeks kuadran berlatar MIST (0..3) atau None."""
    S = _group(slide, 'matriks')
    ax_w = 0.45
    gx, gy, gw, gh = x + ax_w, y, w - ax_w, h - 0.45
    qx = [gx, gx + gw / 2]
    qy = [gy, gy + gh / 2]
    if rekomendasi is not None:
        i, j = rekomendasi // 2, rekomendasi % 2
        _rect(S, qx[j], qy[i], gw / 2, gh / 2, TINT, name='Kuadran rekomendasi')
    _line(S, gx, gy + gh, gx + gw, gy + gh, GRAY, 1.25, panah=True)
    _line(S, gx, gy + gh, gx, gy, GRAY, 1.25, panah=True)
    _line(S, gx + gw / 2, gy, gx + gw / 2, gy + gh, OUTLINE, 0.75, dash=True)
    _line(S, gx, gy + gh / 2, gx + gw, gy + gh / 2, OUTLINE, 0.75, dash=True)
    _tb(S, sumbu_x[0], gx, gy + gh + 0.05, 1.5, 0.22, size=10, color=GRAY)
    _tb(S, sumbu_x[1], gx + gw - 1.5, gy + gh + 0.05, 1.5, 0.22, size=10, color=GRAY, align=PP_ALIGN.RIGHT)
    _tb(S, sumbu_x[2], gx, gy + gh + 0.05, gw, 0.3, size=12, bold=True, align=PP_ALIGN.CENTER)
    _vtb(S, sumbu_y[2], x + 0.15, gy + gh / 2, gh * 0.6, 12, True, PP_ALIGN.CENTER)
    _vtb(S, sumbu_y[1], x + 0.15, gy + 0.6, 1.2, 9, False, PP_ALIGN.RIGHT, GRAY)
    _vtb(S, sumbu_y[0], x + 0.15, gy + gh - 0.6, 1.2, 9, False, PP_ALIGN.LEFT, GRAY)
    if kuadran:
        pos = [(qx[0], qy[0], PP_ALIGN.LEFT), (qx[1], qy[0], PP_ALIGN.RIGHT),
               (qx[0], qy[1], PP_ALIGN.LEFT), (qx[1], qy[1], PP_ALIGN.RIGHT)]
        for k, nama in enumerate(kuadran[:4]):
            qx_, qy_, al = pos[k]
            _tb(S, nama, qx_ + 0.12, qy_ + 0.08, gw / 2 - 0.24, 0.3, size=11,
                color=DARK if k == rekomendasi else GRAY, bold=k == rekomendasi, align=al)
    vmax = max([it.get('nilai', 1) for it in items] + [1])
    for it in items:
        dd = d * (0.7 + 0.9 * math.sqrt(it.get('nilai', vmax) / vmax)) if any('nilai' in i for i in items) else d
        px = gx + it['x'] * gw
        py = gy + (1 - it['y']) * gh
        _rect(S, px - dd / 2, py - dd / 2, dd, dd, PRIMARY if it.get('sorot') else A4, shape=MSO_SHAPE.OVAL,
              name='Titik ' + it['label'])
        kiri = it['x'] > 0.8
        _tb(S, it['label'], (px - dd / 2 - 2.05) if kiri else (px + dd / 2 + 0.07), py - 0.13, 2.0, 0.26,
            size=size, bold=it.get('sorot', False), align=PP_ALIGN.RIGHT if kiri else PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.MIDDLE)
    return S


def add_harvey(slide, x, y, nilai, d=0.28, color=PRIMARY):
    """Harvey ball 0..4 (0 kosong, 4 penuh)."""
    S = slide.shapes if not hasattr(slide, 'add_shape') else slide
    o = _rect(S, x, y, d, d, WHITE, line=color, line_pt=1.25, shape=MSO_SHAPE.OVAL, name='Harvey %s' % nilai)
    o.fill.background()
    if nilai >= 4:
        _rect(S, x, y, d, d, color, shape=MSO_SHAPE.OVAL)
    elif nilai > 0:
        pie = S.add_shape(MSO_SHAPE.PIE, Inches(x), Inches(y), Inches(d), Inches(d))
        pie.fill.solid(); pie.fill.fore_color.rgb = color; pie.line.fill.background(); pie.shadow.inherit = False
        ang = 360 * nilai / 4.0          # sudut OOXML: 60000/derajat; python-pptx membagi 100000
        pie.adjustments[0] = 270 * 0.6
        pie.adjustments[1] = ((270 + ang) % 360) * 0.6
    return o


def add_harvey_table(slide, header, rows, x, y, w, col_w=None, row_h=0.55, legenda=True,
                     label_legenda=('Tidak memenuhi', 'Memenuhi penuh')):
    """Tabel penilaian kualitatif. Sel berisi int 0..4 menjadi Harvey ball; sel teks tetap teks."""
    tbl_rows = [[('' if isinstance(c, int) and not isinstance(c, bool) else c) for c in r] for r in rows]
    tbl = _d.add_axis_table(slide, header, tbl_rows, x, y, w, col_w=col_w, row_h=row_h)
    for j in range(len(header)):
        if any(isinstance(r[j], int) and not isinstance(r[j], bool) for r in rows):
            for p in tbl.cell(0, j).text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
    cws = col_w or [w / len(header)] * len(header)
    top = y + _d.HEAD_H
    d = min(0.3, row_h * 0.55)
    S = _group(slide, 'harvey')
    for i, r in enumerate(rows):
        cx0 = x
        for j, c in enumerate(r):
            if isinstance(c, int) and not isinstance(c, bool):
                add_harvey(S, cx0 + (cws[j] - d) / 2, top + i * row_h + (row_h - d) / 2, c, d)
            cx0 += cws[j]
    if legenda:
        ly = top + len(rows) * row_h + 0.15
        xx = x
        _tb(S, label_legenda[0], xx, ly, 1.4, 0.24, size=10, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
        xx += 1.35
        for k in range(5):
            add_harvey(S, xx, ly + 0.02, k, 0.2)
            xx += 0.3
        _tb(S, label_legenda[1], xx + 0.05, ly, 1.6, 0.24, size=10, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
    return S


def add_sensitivity_table(slide, label_baris, label_kolom, matriks, x, y, w, h=None,
                          judul_baris='', judul_kolom='', dasar=None, ambang=None, fmt='{:.1f}',
                          satuan='%', row_h=0.42, label_w=1.8):
    """Matriks sensitivitas dua variabel (IRR vs tarif x capex, NPV vs WACC x CF).
    dasar  : (i, j) sel kasus dasar -> PRIMARY, teks putih tebal.
    ambang : sel >= ambang berlatar TINT (lolos hurdle rate), sel < ambang teks abu. Tambahkan
             legenda/penjelasan ambang di pemanggil (mis. 'Arsir = IRR >= WACC 8,5%')."""
    S = _group(slide, 'sensitivitas')
    nr, nc = len(label_baris), len(label_kolom)
    cw = (w - label_w) / nc
    top = y + 0.75
    _tb(S, judul_kolom, x + label_w, y, w - label_w, 0.3, size=12, bold=True, align=PP_ALIGN.CENTER)
    for j, k in enumerate(label_kolom):
        _tb(S, k, x + label_w + j * cw, y + 0.32, cw, 0.34, size=12, bold=True, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.BOTTOM)
    _line(S, x + label_w, y + 0.7, x + w, y + 0.7, PRIMARY, 1.5)
    _tb(S, judul_baris, x, y + 0.32, label_w - 0.1, 0.34, size=12, bold=True, anchor=MSO_ANCHOR.BOTTOM)
    for i, rl in enumerate(label_baris):
        yy = top + i * row_h
        _tb(S, rl, x, yy, label_w - 0.1, row_h, size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        for j in range(nc):
            v = matriks[i][j]
            base = dasar == (i, j)
            ok = ambang is not None and v >= ambang
            fill = PRIMARY if base else (TINT if ok else None)
            c = _rect(S, x + label_w + j * cw + 0.02, yy + 0.02, cw - 0.04, row_h - 0.04, fill)
            col = WHITE if base else (INK if (ambang is None or ok) else GRAY)
            _shape_text(c, _fmt(v, fmt) + satuan, 12, col, base)
    return S


# =====================================================================================
# Angka
# =====================================================================================
def add_kpi_row(slide, kpi, x, y, w, h=1.5, gap=0.35, size=36):
    """Deret 2–4 angka kunci untuk slide proposisi investasi / ringkasan kinerja.
    kpi: [{'nilai': '1,1', 'satuan': 'GW', 'label': 'Kapasitas BESS', 'ket': 'target COD 2029'}]
    Tanpa kartu berisi warna: garis atas PRIMARY, angka DARK besar, label tebal, keterangan abu.
    Batas pakai: satu slide seperti ini per deck, dan angkanya harus menjadi inti pesan slide."""
    S = _group(slide, 'angka kunci')
    n = len(kpi)
    cw = (w - gap * (n - 1)) / n
    for i, k in enumerate(kpi):
        cx = x + i * (cw + gap)
        _line(S, cx, y, cx + cw, y, PRIMARY, 2.0)
        box = S.add_textbox(Inches(cx), Inches(y + 0.1), Inches(cw), Inches(size / 72 * 1.3))
        tf = box.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        _run(p, str(k['nilai']), size, DARK, bold=True)
        if k.get('satuan'):
            _run(p, ' ' + k['satuan'], int(size * 0.45), DARK, bold=True)
        yy = y + 0.12 + size / 72 * 1.3
        _tb(S, k['label'], cx, yy, cw, 0.3, size=13, bold=True)
        if k.get('ket'):
            _tb(S, k['ket'], cx, yy + 0.32, cw, h - (yy - y) - 0.32, size=11, color=GRAY)
    return S


def add_big_number(slide, angka, keterangan, x, y, w, satuan='', size=60):
    """Pola N: satu angka yang menjadi seluruh pesan slide (maksimal sekali per deck)."""
    S = _group(slide, 'angka besar')
    box = S.add_textbox(Inches(x), Inches(y), Inches(w), Inches(size / 72 * 1.25))
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    _run(p, str(angka), size, PRIMARY, bold=True)
    if satuan:
        _run(p, ' ' + satuan, int(size * 0.4), PRIMARY, bold=True)
    _tb(S, keterangan, x, y + size / 72 * 1.3, w, 0.9, size=14, color=INK)
    return S


# =====================================================================================
# Geografis
# =====================================================================================
WILAYAH = {
    'indonesia':      (94.6, -11.2, 141.2, 6.3),
    'sumatera':       (94.6, -6.3, 106.8, 6.2),
    'jawa-bali':      (105.0, -9.0, 116.3, -5.6),
    'jawa':           (105.0, -8.9, 114.7, -5.7),
    'kalimantan':     (108.4, -4.4, 119.4, 4.6),
    'sulawesi':       (118.6, -6.2, 125.6, 2.2),
    'nusa-tenggara':  (114.3, -11.0, 125.3, -7.9),
    'maluku-papua':   (124.2, -9.3, 141.2, 2.8),
    'papua':          (130.8, -9.2, 141.2, 0.3),
}
_MAP = None


def _map_data():
    global _MAP
    if _MAP is None:
        with open(os.path.join(_HERE, 'maps', 'indonesia.json'), encoding='utf-8') as f:
            _MAP = json.load(f)
    return _MAP


def map_height(w, wilayah='indonesia'):
    """Tinggi peta (inci) untuk lebar w, menjaga proporsi (proyeksi ekuirektangular)."""
    b = WILAYAH[wilayah] if isinstance(wilayah, str) else wilayah
    return w * (b[3] - b[1]) / (b[2] - b[0])


def add_map(slide, titik, x, y, w, wilayah='indonesia', label=True, jenis_warna=None,
            legenda=True, ukuran_nilai=False, satuan='', d=0.16, tetangga=True, size=10,
            daratan=TINT):
    """Peta Indonesia (atau satu wilayah) dengan titik proyek/aset, dibangun dari bentuk
    freeform asli (bisa diedit/diwarnai ulang di PowerPoint).

    titik   : [{'nama', 'lon', 'lat', 'jenis' (opsional), 'nilai' (opsional), 'sorot': bool,
                'posisi': 'kanan'|'kiri'|'atas'|'bawah' (opsional, arah label)}]
    wilayah : kunci WILAYAH ('indonesia', 'sumatera', 'jawa-bali', 'kalimantan', 'sulawesi',
              'nusa-tenggara', 'maluku-papua', 'papua') atau (lon0, lat0, lon1, lat1).
    jenis_warna : {'PLTS': PRIMARY, 'BESS': DARK, ...}; default otomatis dari SERI.
    ukuran_nilai: lingkaran sebanding akar nilai (mis. MW).
    Tinggi peta = map_height(w, wilayah). Koordinat: derajat desimal (lintang selatan negatif).
    Sumber batas: Natural Earth 1:10m (domain publik), disederhanakan; bukan peta resmi batas negara."""
    data = _map_data()
    b = WILAYAH[wilayah] if isinstance(wilayah, str) else wilayah
    lon0, lat0, lon1, lat1 = b
    h = map_height(w, b)
    sx = w / (lon1 - lon0)
    X = lambda lon: x + (lon - lon0) * sx
    Y = lambda lat: y + (lat1 - lat) * sx
    view_area = (lon1 - lon0) * (lat1 - lat0)
    min_area = view_area * 2e-5
    EMU = 914400

    def draw(G, polys, fill, nama):
        for poly in polys:
            if poly['a'] < min_area:
                continue
            pts = poly['p']
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            if max(xs) < lon0 or min(xs) > lon1 or max(ys) < lat0 or min(ys) > lat1:
                continue
            ep = [(int(X(max(lon0, min(lon1, p[0]))) * EMU),
                   int(Y(max(lat0, min(lat1, p[1]))) * EMU)) for p in pts]
            fb = G.build_freeform(ep[0][0], ep[0][1], scale=1.0)
            fb.add_line_segments(ep[1:], close=True)
            shp = fb.convert_to_shape()
            shp.fill.solid(); shp.fill.fore_color.rgb = fill
            shp.line.color.rgb = WHITE; shp.line.width = Pt(0.25)
            shp.shadow.inherit = False
            shp.name = nama

    Gm = _group(slide, 'peta')
    if tetangga:
        draw(Gm, data['tetangga'], LIGHT, 'Negara tetangga')
    draw(Gm, data['indonesia'], daratan, 'Daratan Indonesia')
    # titik
    jenis = []
    for t in titik:
        if t.get('jenis') and t['jenis'] not in jenis:
            jenis.append(t['jenis'])
    palet = [PRIMARY, DARK, TEAL, A4, YELLOW, A1]
    jw = dict(jenis_warna or {})
    for k, j in enumerate(jenis):
        jw.setdefault(j, palet[k % len(palet)])
    vmax = max([t.get('nilai', 0) for t in titik] + [1])
    Gt = _group(slide, 'titik peta')
    placed = []
    for t in titik:                       # titik jadi penghalang label
        px, py = X(t['lon']), Y(t['lat'])
        rr = d * (0.6 + 1.8 * math.sqrt(t.get('nilai', 0) / vmax)) / 2 if ukuran_nilai and t.get('nilai') else d / 2
        placed.append((px - rr, py - rr, px + rr, py + rr))
    for t in titik:
        px, py = X(t['lon']), Y(t['lat'])
        dd = d * (0.6 + 1.8 * math.sqrt(t.get('nilai', 0) / vmax)) if ukuran_nilai and t.get('nilai') else d
        col = jw.get(t.get('jenis'), PRIMARY)
        if t.get('sorot'):
            _rect(Gt, px - dd / 2 - 0.05, py - dd / 2 - 0.05, dd + 0.1, dd + 0.1, None, line=DARK,
                  line_pt=1.5, shape=MSO_SHAPE.OVAL)
        _rect(Gt, px - dd / 2, py - dd / 2, dd, dd, col, line=WHITE, line_pt=0.75, shape=MSO_SHAPE.OVAL,
              name='Titik ' + t['nama'])
        if label:
            teks = t['nama'] + ((' (%s%s)' % (_fmt(t['nilai']), (' ' + satuan) if satuan else '')) if
                                (t.get('nilai') and satuan) else '')
            tw = len(teks) * size * 0.52 / 72 + 0.1
            th = size * 1.3 / 72
            cands = {'kanan': (px + dd / 2 + 0.05, py - th / 2), 'kiri': (px - dd / 2 - 0.05 - tw, py - th / 2),
                     'atas': (px - tw / 2, py - dd / 2 - th - 0.02), 'bawah': (px - tw / 2, py + dd / 2 + 0.02)}
            order = [t['posisi']] if t.get('posisi') else ['kanan', 'kiri', 'atas', 'bawah']
            pick = None
            for o in order:
                bx, by = cands[o]
                r = (bx, by, bx + tw, by + th)
                if bx < x or bx + tw > x + w or by < y or by + th > y + h:
                    continue
                if all(r[2] < q[0] or r[0] > q[2] or r[3] < q[1] or r[1] > q[3] for q in placed):
                    pick = (bx, by, o); break
            if pick is None:
                bx, by = cands[order[0]]; pick = (bx, by, order[0])
            bx, by, o = pick
            placed.append((bx, by, bx + tw, by + th))
            _tb(Gt, teks, bx, by, tw, th, size=size, bold=t.get('sorot', False),
                align=PP_ALIGN.RIGHT if o == 'kiri' else (PP_ALIGN.CENTER if o in ('atas', 'bawah') else PP_ALIGN.LEFT),
                anchor=MSO_ANCHOR.MIDDLE)
    if legenda and jenis:
        add_legend(slide, [(j, jw[j], 'bulat') for j in jenis], x, y + h + 0.1)
    return h
