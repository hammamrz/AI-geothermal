"""tvv_deck.py — pembuat deck TVV (paparan usulan investasi RKAP) dari master native Template TVV.

Dasar deck: assets/masters/TVV_Master.pptx (Template TVV tanpa slide: cover berilustrasi
PROPER + master isi berlogo Danantara dan PLN IP). Semua fungsi umum dari skill PLN IP
(teks, bullet, ikon, chart, model grafis) ikut ter-impor dari plnip_deck.py / plnip_grafis.py;
fungsi yang namanya sama di bawah ini (new_deck, save, set_cover, add_slide, add_divider)
menggantikannya untuk gaya TVV.

Pakai:
    import sys; sys.path.insert(0, 'assets')
    from tvv_deck import *

    prs = new_deck()
    set_cover(prs, 'Usulan Program Investasi Murni', sorot='RKAP 2027',
              kicker='RAPAT PEMBAHASAN', subjudul='PLN Indonesia Power  |  32 proyek setara 4,8 GW',
              unit='Divisi Generation Business Development', tanggal='28 September 2026')
    s = add_slide(prs, 'Latar Belakang', 'Dasar Penyusunan Usulan RKAP 2027',
                  narasi='Usulan RKAP 2027 disusun berdasarkan ...')
    add_tabel(s, header, rows, L, body_top(s), CW, gabung=[0], ikon={0: 'regulasi'})
    save(prs, 'keluaran.pptx')

Semua ukuran dalam inci. Kanvas 13,333 x 7,5 (16:9).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import plnip_deck as _pd  # noqa: E402
from plnip_deck import *  # noqa: E402,F401,F403
from plnip_deck import (_run, _fill_runs, _set_border, _cell_fill, _bullet, _no_bullet,  # noqa: E402
                        _move_slide, _drop_slide, _strip_part, _title_lines)
import plnip_grafis as _g  # noqa: E402
from plnip_grafis import _group, _rect, _tb, _line, _vtb, LIGHT  # noqa: E402

from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from pptx.oxml.ns import qn  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402

TVV_MASTER = os.path.join(HERE, 'masters', 'TVV_Master.pptx')

# ---------- Warna khusus TVV (di luar palet PLN IP, hanya untuk tujuan ini) ----------
# Matriks risiko 5x5 (tingkat risiko PLN). Dipakai hanya di add_kajian_risiko, selalu dengan legenda.
RISK_LOW = RGBColor(0x1B, 0x7F, 0x3B)       # Low
RISK_LM = RGBColor(0x22, 0xB4, 0x4A)        # Low to Moderate (= hijau lampu lalu lintas)
RISK_MOD = RGBColor(0xEF, 0xCF, 0x06)       # Moderate (= kuning lampu lalu lintas)
RISK_MH = RGBColor(0xF0, 0x8C, 0x00)        # Moderate to High
RISK_HIGH = RGBColor(0xE0, 0x01, 0x02)      # High (= merah lampu lalu lintas)
TEKS_2 = RGBColor(0x33, 0x33, 0x33)         # teks keterangan di outline (template TVV)

# ---------- Grid TVV (diukur dari Template TVV) ----------
L, R = 0.4, 12.93
CW = R - L
TITLE_X, TITLE_Y, TITLE_H, TITLE_PT = 0.4, 0.26, 0.57, 20
LOGO_KIRI = 9.36                      # tepi kiri blok logo Danantara + PLN IP di semua master isi
TITLE_W = LOGO_KIRI - 0.25 - TITLE_X  # 8,71 in
NARASI_Y, NARASI_H, NARASI_PT = 0.88, 0.56, 14
BODY_TOP = 1.05                       # tanpa narasi
BODY_TOP_NARASI = 1.6                 # dengan narasi di bawah judul
BODY_BOTTOM = 6.85
SUMBER_Y, SUMBER_PT = 6.9, 11
HEAD_H = 0.42
LEFT_X, LEFT_W = L, 6.1
RIGHT_X, RIGHT_W = 6.9, R - 6.9
HALF_W = (CW - 0.4) / 2
HALF2_X = L + HALF_W + 0.4

# Fungsi umum plnip_deck (add_keterangan_bawah, _content_bottom, dll.) membaca grid modulnya
# sendiri; samakan dengan grid TVV.
for _k in ('L', 'R', 'CW', 'BODY_TOP', 'BODY_BOTTOM', 'LEFT_X', 'LEFT_W', 'RIGHT_X', 'RIGHT_W',
           'HALF_W', 'HALF2_X'):
    setattr(_pd, _k, globals()[_k])

# Desain master TVV: (indeks master di TVV_Master.pptx, nama layout)
DESAIN = {
    'cover':          (0, 'Custom Layout'),   # ilustrasi PLTA/PLTS + PROPER, judul di kanan
    'isi':            (4, 'Blank'),           # latar biru muda + siluet pembangkit (paling banyak dipakai)
    'isi-putih':      (3, 'Blank'),           # putih + siluet pembangkit abu
    'isi-gelombang':  (1, 'Blank'),           # putih + gelombang biru di bawah
    'isi-polos':      (2, 'Blank'),           # putih polos + siluet tipis
}
_STATE = {'layouts': {}, 'isi': 'isi'}


# =====================================================================================
# Deck
# =====================================================================================
def new_deck(desain_isi='isi'):
    """Deck baru dari TVV_Master.pptx (semua master Template TVV, tanpa slide).
    desain_isi: 'isi' (default, latar biru muda seperti mayoritas slide template), 'isi-putih',
    'isi-gelombang', atau 'isi-polos'. Satu deck sebaiknya memakai satu desain isi."""
    if not os.path.exists(TVV_MASTER):
        raise FileNotFoundError('Master TVV tidak ketemu: ' + TVV_MASTER +
                                '. Salin seluruh folder assets/ ke direktori kerja.')
    if desain_isi not in DESAIN or desain_isi == 'cover':
        raise ValueError('desain_isi harus salah satu dari %s' % [k for k in DESAIN if k != 'cover'])
    prs = Presentation(TVV_MASTER)
    for _ in range(len(prs.slides)):
        _drop_slide(prs, 0)
    masters = list(prs.slide_masters)
    lay = {}
    for key, (mi, nama) in DESAIN.items():
        cand = [x for x in masters[mi].slide_layouts if x.name == nama]
        if not cand:
            raise ValueError('Layout %s tidak ada di master %d' % (nama, mi))
        lay[key] = cand[0]
    _STATE['layouts'] = lay
    _STATE['isi'] = desain_isi
    _pd._STATE.update(dasar='tvv')
    return prs


def _new_slide(prs, desain):
    lay = _STATE['layouts'].get(desain)
    if lay is None:
        raise ValueError('Desain %r tidak dikenal. Pilihan: %s' % (desain, list(DESAIN)))
    s = prs.slides.add_slide(lay)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    return s


def _prune(prs):
    """Buang master yang tidak dipakai, lalu layout yang tidak dipakai di master yang tersisa
    (ilustrasi cover lain di master 0 ikut terbuang sehingga berkas lebih kecil)."""
    used_layouts = {s.slide_layout.part for s in prs.slides}
    used_masters = {s.slide_layout.slide_master.part for s in prs.slides}
    lst = prs.slide_masters._sldMasterIdLst
    for el in list(lst):
        if prs.part.related_part(el.rId) not in used_masters:
            rId = el.rId
            lst.remove(el)
            prs.part.drop_rel(rId)
    for m in prs.slide_masters:
        for lay in list(m.slide_layouts):
            if lay.part not in used_layouts:
                m.slide_layouts.remove(lay)


def save(prs, path):
    """Simpan deck: master/layout tak terpakai dibuang, revisionInfo dibuang (lolos validator)."""
    _prune(prs)
    prs.save(path)
    _strip_part(path, 'ppt/revisionInfo.xml')
    return path


def body_top(slide):
    """y awal bidang isi slide ini (1,05 tanpa narasi; 1,6 dengan narasi)."""
    return getattr(slide, '_tvv_body_top', BODY_TOP)


# =====================================================================================
# Cover, judul, narasi, sumber
# =====================================================================================
def set_cover(prs, judul, sorot='', kicker='RAPAT PEMBAHASAN', subjudul='', unit='', tanggal=''):
    """Cover TVV (layout cover Template TVV: ilustrasi di kiri, PROPER di kiri atas).

    kicker   : baris kecil biru di atas judul ('RAPAT PEMBAHASAN', 'PAPARAN DIREKSI', ...)
    judul    : judul utama 36pt navy ('Usulan Program Investasi Murni')
    sorot    : ujung judul yang dibesarkan 44pt ('RKAP 2027'); kosongkan bila tidak perlu
    subjudul : satu baris 18pt ('PLN Indonesia Power  |  32 proyek setara 4,8 GW')
    unit, tanggal : dua baris kecil di kanan bawah. Tanggal ditulis Indonesia ('28 September 2026').
    """
    s = _new_slide(prs, 'cover')
    box = s.shapes.add_textbox(Inches(4.59), Inches(1.94), Inches(8.48), Inches(2.92))
    box.name = 'Title'
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    paras = []
    if kicker:
        paras.append([(kicker, 18, PRIMARY, True)])
    utama = [(judul, 36, DARK, True)]
    if sorot:
        utama += [(' ', 36, DARK, True), (sorot, 44, DARK, True)]
    paras.append(utama)
    if subjudul:
        paras.append([(subjudul, 18, A4, False)])
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.RIGHT
        p.line_spacing = 0.95
        p.space_after = Pt(6 if i == 0 else 2)
        for t, sz, col, b in runs:
            _fill_runs(p, t, sz, col, bold=b)
    meta = [t for t in (unit, tanggal) if t]
    if meta:
        add_text(s, meta, 9.36, 5.62, 3.7, 0.7, size=11, color=PRIMARY, bold=True, space_after=2)
    _move_slide(prs, s, 0)
    return s


def add_slide(prs, topik, subtopik='', narasi=None, desain=None, nomor=True):
    """Slide isi TVV: judul 20pt dua warna (topik biru + sub-topik hitam) sebaris dengan logo,
    opsional satu kalimat narasi 14pt abu di bawah judul (gaya Template TVV), nomor halaman.

    narasi : 1–2 kalimat yang merangkum isi slide dengan angka kunci (mis. "Dari 255 proyek alokasi
             RUPTL, 54 proyek sudah masuk RKAP 2026 ..."). Bukan kalimat pengantar umum.
    desain : 'isi' (default dari new_deck), 'isi-putih', 'isi-gelombang', 'isi-polos'.
    Bidang isi mulai di body_top(s): 1,05 in tanpa narasi, 1,6 in dengan narasi.
    """
    s = _new_slide(prs, desain or _STATE['isi'])
    full = (topik + ' ' + subtopik).replace('*', '').strip()
    pt, n = TITLE_PT, _title_lines(full, TITLE_W, TITLE_PT)
    for cand in (TITLE_PT - 2, TITLE_PT - 4):
        if n == 1:
            break
        pt, n = cand, _title_lines(full, TITLE_W, cand)
    if n > 1:
        print('PERINGATAN S%d: judul "%s" butuh %d baris di lebar %.2f in; persingkat sub-topik.'
              % (len(prs.slides._sldIdLst), full, n, TITLE_W))
    title_h = max(TITLE_H, n * pt * 1.2 / 72)
    box = s.shapes.add_textbox(Inches(TITLE_X), Inches(TITLE_Y), Inches(TITLE_W), Inches(title_h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    _fill_runs(p, topik, pt, PRIMARY, bold=True)
    if subtopik:
        _run(p, ' ', pt, INK, bold=True)
        _fill_runs(p, subtopik, pt, INK, bold=True)
    box.name = 'Title'
    s._tvv_body_top = BODY_TOP
    if narasi:
        nb = add_text(s, narasi, TITLE_X, NARASI_Y + max(0, title_h - TITLE_H), CW, NARASI_H,
                      size=NARASI_PT, color=GRAY, line=1.0, space_after=0)
        nb.name = 'Narasi'
        if _title_lines(narasi.replace('*', ''), CW, NARASI_PT, em=0.5) > 2:
            print('PERINGATAN S%d: narasi lebih dari 2 baris; ringkas jadi satu kalimat berangka.'
                  % len(prs.slides._sldIdLst))
        s._tvv_body_top = BODY_TOP_NARASI + max(0, title_h - TITLE_H)
    if nomor:
        add_text(s, str(len(prs.slides._sldIdLst)), R - 0.6, 7.08, 0.6, 0.25, size=9,
                 color=GRAY, align=PP_ALIGN.RIGHT)
    return s


def add_sumber(slide, teks):
    """Baris sumber/catatan dasar angka di bawah bidang isi (gaya Template TVV), 11pt abu.
    Isi: dokumen asal angka ('Sumber: Nodin FIN PLN IP, KEU PLN, RKAP 2026'). Satu baris."""
    box = add_text(slide, teks, L, SUMBER_Y, R - L - 0.9, 0.3, size=SUMBER_PT, color=GRAY,
                   anchor=MSO_ANCHOR.MIDDLE)
    box.name = 'Sumber'
    return box


add_source = add_sumber


# =====================================================================================
# Pembatas
# =====================================================================================
def add_divider(prs, judul, keterangan='', desain=None):
    """Pembatas bagian (slide 10 template): judul 36pt navy + keterangan 16pt abu, di latar isi."""
    s = _new_slide(prs, desain or _STATE['isi'])
    box = add_text(s, judul, 0.83, 2.6, 11.67, 1.2, size=36, color=DARK, bold=True,
                   anchor=MSO_ANCHOR.BOTTOM, line=0.95)
    box.name = 'Judul pembatas'
    if keterangan:
        add_text(s, keterangan, 0.83, 3.95, 11.67, 0.8, size=16, color=GRAY)
    add_text(s, str(len(prs.slides._sldIdLst)), R - 0.6, 7.08, 0.6, 0.25, size=9,
             color=GRAY, align=PP_ALIGN.RIGHT)
    return s


def add_divider_proyek(prs, nomor, nama, keterangan='', desain=None):
    """Pembatas per proyek (slide 12 template): nomor besar '01' + nama proyek + kapasitas.
    nama: 'PLTA Sulbagsel (Kuota) Tersebar Tambahan II'; keterangan: 'Kapasitas 400 MW'."""
    s = _new_slide(prs, desain or _STATE['isi'])
    add_text(s, '%02d' % nomor if isinstance(nomor, int) else str(nomor), 0.88, 2.35, 2.6, 2.1,
             size=115, color=A1, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    box = s.shapes.add_textbox(Inches(3.55), Inches(2.85), Inches(8.9), Inches(1.1))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    _fill_runs(p, nama, 24, INK, bold=True)
    if keterangan:
        p2 = tf.add_paragraph()
        _fill_runs(p2, keterangan, 18, GRAY)
    box.name = 'Judul pembatas'
    return s


# =====================================================================================
# Outline dan rekap
# =====================================================================================
def add_outline(prs, topik, subtopik, bab, panel=None, sorot=None):
    """Outline pembahasan (slide 2 template): panel angka navy di kiri, daftar bab bernomor di kanan.

    bab   : [{'judul': 'Latar Belakang', 'ket': 'Kebijakan dan dokumen URKAP 2027'}, ...] 3–6 butir.
            Judul bab sama dengan topik (bagian biru) judul slide di bab itu.
    panel : {'label': 'Usulan RKAP 2027', 'angka': '32', 'satuan': 'proyek',
             'baris': ['(25 gabungan)', 'setara 4,8 GW'], 'catatan': 'Paparan ini disampaikan ...'}
    sorot : nomor bab (1..n) yang diberi latar TINT, mis. bab yang berisi permintaan keputusan.
    """
    s = add_slide(prs, topik, subtopik)
    y0, h = 1.17, 5.56
    x_panel, w_panel = L, 3.75
    if panel:
        pn = _rect(s.shapes, x_panel, y0, w_panel, h, DARK, name='Panel ringkas')
        tb = s.shapes.add_textbox(Inches(x_panel + 0.3), Inches(y0 + 0.35), Inches(w_panel - 0.6),
                                  Inches(h - 0.7))
        tb.name = 'Panel ringkas teks'
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        _fill_runs(p, panel.get('label', ''), 14, TINT, bold=True)
        p.space_after = Pt(18)
        if panel.get('angka'):
            p = tf.add_paragraph()
            _run(p, str(panel['angka']), 72, WHITE, bold=True)
            if panel.get('satuan'):
                _run(p, ' ' + panel['satuan'], 24, WHITE, bold=True)
            p.line_spacing = 0.9
        for i, b in enumerate(panel.get('baris', [])):
            p = tf.add_paragraph()
            _fill_runs(p, b, 22, WHITE if i == 0 else TINT, bold=True)
        if panel.get('catatan'):
            p = tf.add_paragraph()
            p.space_before = Pt(28)
            _fill_runs(p, panel['catatan'], 13, WHITE)
        x_list = x_panel + w_panel + 0.28
    else:
        x_list = L
    w_list = R - x_list
    n = len(bab)
    rh = h / n
    for i, b in enumerate(bab, 1):
        y = y0 + (i - 1) * rh
        if sorot == i:
            _rect(s.shapes, x_list, y, w_list, rh, TINT, name='Sorotan bab')
        d = 0.53
        c = _rect(s.shapes, x_list + 0.16, y + 0.29, d, d, DARK if sorot == i else PRIMARY,
                  shape=MSO_SHAPE.OVAL, name='Nomor %02d' % i)
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        _run(p0, '%02d' % i, 16, WHITE, bold=True)
        tb = s.shapes.add_textbox(Inches(x_list + 0.89), Inches(y + 0.12), Inches(w_list - 1.0),
                                  Inches(rh - 0.2))
        tb.name = 'Bab %02d' % i
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        _fill_runs(p, b['judul'], 16, DARK, bold=True)
        if b.get('ket'):
            p2 = tf.add_paragraph()
            p2.space_before = Pt(2)
            _fill_runs(p2, b['ket'], 13, TEKS_2)
        if i < n and sorot not in (i, i + 1):
            _line(s.shapes, x_list, y + rh, x_list + w_list, y + rh, OUTLINE, 0.75)
    return s


def add_rekap(prs, panel, header, rows, narasi='', catatan='', col_w=None, size=14, **kw):
    """Rekapitulasi dengan panel kiri setinggi slide (slide 7 template).

    panel : {'label': 'REKAPITULASI', 'judul': 'Program Murni URKAP 2027', 'unit': 'Bidang GRB',
             'angka': '32', 'satuan': 'proyek', 'baris': ['(25 gabungan)', 'Rp 17.206,0 miliar AI 2027']}
    narasi: satu kalimat berangka di atas tabel (16pt abu).
    header/rows: tabel rekap (gaya sumbu); baris terakhir 'Total' otomatis bold.
    catatan: definisi singkatan / cara hitung di bawah tabel (12pt abu)."""
    s = _new_slide(prs, _STATE['isi'])
    pw = 4.43
    _rect(s.shapes, 0, 0, pw, 7.5, DARK, name='Panel rekap')
    tb = s.shapes.add_textbox(Inches(0.42), Inches(1.5), Inches(pw - 0.8), Inches(2.8))
    tb.name = 'Judul panel'
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.BOTTOM
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    _run(p, panel.get('label', 'REKAPITULASI'), 14, TINT, bold=True)
    p.space_after = Pt(6)
    p = tf.add_paragraph()
    _fill_runs(p, panel.get('judul', ''), 30, WHITE, bold=True)
    p.line_spacing = 0.95
    if panel.get('unit'):
        p = tf.add_paragraph()
        _fill_runs(p, panel['unit'], 18, TINT)
    if panel.get('angka'):
        tb2 = s.shapes.add_textbox(Inches(0.42), Inches(4.55), Inches(pw - 0.8), Inches(1.9))
        tb2.name = 'Angka panel'
        tf = tb2.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        _run(p, str(panel['angka']), 66, WHITE, bold=True)
        if panel.get('satuan'):
            _run(p, ' ' + panel['satuan'], 20, WHITE, bold=True)
        p.line_spacing = 0.9
        for i, b in enumerate(panel.get('baris', [])):
            p = tf.add_paragraph()
            _fill_runs(p, b, 18 if i == 0 else 15, WHITE if i == 0 else TINT, bold=(i == 0))
    x, w = 4.86, R - 4.86
    y = 1.3
    if narasi:
        nb = add_text(s, narasi, x, y, w, 0.7, size=16, color=GRAY, line=1.05)
        nb.name = 'Narasi'
        y += 0.95
    rows = [list(r) for r in rows]
    if rows and str(rows[-1][0]).strip().lower().startswith('total'):
        rows[-1] = [c if isinstance(c, dict) else {'text': c, 'bold': True} for c in rows[-1]]
    t = add_tabel(s, header, rows, x + 0.1, y, w - 0.1, col_w=col_w, size=size, row_h=0.8, **kw)
    if catatan:
        add_text(s, catatan, x, max(t['bawah'] + 0.3, 6.2), w, 0.5, size=12, color=GRAY)
    add_text(s, str(len(prs.slides._sldIdLst)), R - 0.6, 7.08, 0.6, 0.25, size=9,
             color=GRAY, align=PP_ALIGN.RIGHT)
    return s


# =====================================================================================
# Tabel
# =====================================================================================
def _est_h(teks, w_in, pt, bold=False):
    """Perkiraan tinggi teks (inci) di lebar w_in."""
    if teks is None:
        return 0
    is_list = isinstance(teks, (list, tuple)) and len(teks) > 1
    parts = teks if isinstance(teks, (list, tuple)) else str(teks).split('\n')
    if is_list:
        w_in -= 0.3
    lines = 0
    for part in parts:
        part = str(part).replace('*', '')
        lines += _title_lines(part, max(w_in, 0.2), pt, em=0.56 if bold else 0.5) if part.strip() else 1
    return lines * pt * 1.22 / 72 + 0.1 + (0.03 * len(parts) if is_list else 0)


STATUS_WARNA = {'ok': TL_GREEN, 'proses': TL_YELLOW, 'belum': TL_RED}
STATUS_LABEL = {'ok': 'Lengkap', 'proses': 'Dalam proses', 'belum': 'Belum ada'}


def add_tabel(slide, header, rows, x, y, w, col_w=None, row_h=0.36, size=12, gaya='sumbu',
              rata=None, gabung=(), sorot_kolom=None, sumbu=True, head_h=None, ikon=None,
              ikon_d=0.38, status_d=0.2, head_size=None):
    """Tabel TVV. Tinggi baris dihitung dari panjang teks supaya ikon dan penanda status tepat posisi.

    gaya        : 'sumbu' (default; header tanpa isian, garis bawah PRIMARY; untuk tabel kualitatif
                  3–10 baris) atau 'data' (header isian PRIMARY teks putih; untuk tabel angka padat
                  banyak kolom seperti status dokumen dan rekap proyek).
    rows        : sel = teks, None (lanjutan sel gabungan di atasnya, untuk kolom di `gabung`), atau
                  dict {'text', 'bold', 'na' (tampil '—' latar TINT), 'sorot' (kuning),
                  'warna', 'status': 'ok'|'proses'|'belum' (penanda bulat lampu lalu lintas)}.
                  'text' boleh list -> beberapa butir (bullet asli).
    rata        : daftar 'l'|'c'|'r' per kolom (default: kiri; gaya data: kolom angka kanan).
    gabung      : indeks kolom yang sel None-nya digabung (merge) dengan sel di atasnya.
    sorot_kolom : indeks (atau daftar) kolom berlatar TINT, mis. kolom usulan tahun ini.
    ikon        : {indeks_baris: 'nama-ikon'} lingkaran ikon di kolom pertama baris itu (pola
                  kolom sumbu berikon, template slide Latar Belakang).
    Mengembalikan dict: tbl, y_baris (daftar y atas tiap baris isi), tinggi_baris, bawah.
    """
    n_cols = len(header) if header else len(rows[0])
    col_w = list(col_w) if col_w else [w / n_cols] * n_cols
    k = w / sum(col_w)
    col_w = [c * k for c in col_w]
    head_size = head_size or (size + 2 if gaya == 'sumbu' else size)
    sorot_kolom = set(sorot_kolom if isinstance(sorot_kolom, (list, tuple, set)) else
                      ([] if sorot_kolom is None else [sorot_kolom]))
    ikon = ikon or {}
    if rata is None:
        rata = ['l'] * n_cols

    def norm(c):
        if c is None:
            return None
        return c if isinstance(c, dict) else {'text': c}
    rows = [[norm(c) for c in r] for r in rows]
    # tinggi header
    if header:
        hh = max(_est_h(hd, cw - 0.12, head_size, True) for hd, cw in zip(header, col_w))
        head_h = max(head_h or (HEAD_H if gaya == 'sumbu' else 0.36), hh)
    # tinggi baris
    heights = []
    for i, r in enumerate(rows):
        hmax = row_h
        for j, c in enumerate(r):
            if c is None or c.get('status'):
                continue
            first = sumbu and j == 0 and gaya == 'sumbu'
            sz = size + 2 if first else size
            cw = col_w[j] - 0.12 - ((ikon_d + 0.14) if (j == 0 and i in ikon) else 0)
            if j in gabung:
                continue   # sel gabungan dihitung di bawah
            hmax = max(hmax, _est_h(c.get('text', ''), cw, sz, c.get('bold', False) or first))
        heights.append(hmax)
    # sel gabungan: pastikan total tinggi grup cukup untuk teksnya (+ ikon)
    for j in gabung:
        i = 0
        while i < len(rows):
            if rows[i][j] is None:
                i += 1
                continue
            e = i + 1
            while e < len(rows) and rows[e][j] is None:
                e += 1
            c = rows[i][j]
            first = sumbu and j == 0 and gaya == 'sumbu'
            sz = size + 2 if first else size
            cw = col_w[j] - 0.12 - ((ikon_d + 0.14) if (j == 0 and i in ikon) else 0)
            need = max(_est_h(c.get('text', ''), cw, sz, c.get('bold', False) or first),
                       (ikon_d + 0.16) if (j == 0 and i in ikon) else 0)
            have = sum(heights[i:e])
            if need > have:
                heights[e - 1] += need - have
            i = e
    n_rows = len(rows) + (1 if header else 0)
    total_h = (head_h if header else 0) + sum(heights)
    shape = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(total_h))
    shape.name = 'Tabel'
    tbl = shape.table
    tbl.first_row = bool(header)
    tbl.horz_banding = False
    tblPr = tbl._tbl.tblPr
    for el in tblPr.findall(qn('a:tableStyleId')):
        tblPr.remove(el)
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    al = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}
    r0 = 0
    if header:
        tbl.rows[0].height = Inches(head_h)
        for j, hd in enumerate(header):
            c = tbl.cell(0, j)
            if gaya == 'data':
                _isi_sel(c, hd, head_size, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
                _cell_fill(c, PRIMARY)
                for e in ('top', 'bottom', 'left', 'right'):
                    _set_border(c, e, WHITE if e in ('left', 'right') else None, 0.75)
            else:
                _isi_sel(c, hd, head_size, INK, True, al[rata[j]], MSO_ANCHOR.BOTTOM)
                _cell_fill(c, TINT if j in sorot_kolom else None)
                _set_border(c, 'bottom', PRIMARY, 1.5)
                for e in ('top', 'left', 'right'):
                    _set_border(c, e, None, 0)
        r0 = 1
    ys, yy = [], y + (head_h if header else 0)
    for i, r in enumerate(rows):
        ys.append(yy)
        yy += heights[i]
        tbl.rows[i + r0].height = Inches(heights[i])
    status_cells = []
    for i, r in enumerate(rows):
        last = i == len(rows) - 1
        for j, c in enumerate(r):
            cell = tbl.cell(i + r0, j)
            # garis bawah: tidak di dalam grup gabungan
            nxt_cont = (j in gabung and i + 1 < len(rows) and rows[i + 1][j] is None)
            for e in ('top', 'left', 'right'):
                _set_border(cell, e, None, 0)
            _set_border(cell, 'bottom', None if (last or nxt_cont) else OUTLINE, 0.75)
            if c is None:
                _cell_fill(cell, TINT if j in sorot_kolom else None)
                continue
            first = sumbu and j == 0 and gaya == 'sumbu'
            sz = size + 2 if first else size
            col = c.get('warna') or (GRAY if c.get('na') else (DARK if first else INK))
            teks = '—' if c.get('na') else c.get('text', '')
            if c.get('status'):
                teks = ''
                status_cells.append((i, j, c['status']))
            align = PP_ALIGN.CENTER if c.get('na') or c.get('status') else al[rata[j]]
            anchor = MSO_ANCHOR.TOP if (first and j in gabung) else MSO_ANCHOR.MIDDLE
            _isi_sel(cell, teks, sz, col, c.get('bold', False) or first, align, anchor)
            fill = YELLOW if c.get('sorot') else (TINT if (c.get('na') or j in sorot_kolom) else None)
            _cell_fill(cell, fill)
            if j == 0 and i in ikon:
                cell.margin_left = Inches(ikon_d + 0.2)
    # gabung sel
    for j in gabung:
        i = 0
        while i < len(rows):
            e = i + 1
            while e < len(rows) and rows[e][j] is None:
                e += 1
            if e - i > 1:
                a = tbl.cell(i + r0, j)
                a.merge(tbl.cell(e - 1 + r0, j))
                _set_border(a, 'bottom', None if e >= len(rows) else OUTLINE, 0.75)
            i = e
    # ikon di kolom pertama
    for i, nama in ikon.items():
        if nama and i < len(rows):
            add_icon_badge(slide, nama, x + 0.06, ys[i] + 0.07, d=ikon_d)
    # penanda status
    xs = [x + sum(col_w[:j]) for j in range(n_cols)]
    for i, j, st in status_cells:
        colr = STATUS_WARNA.get(st)
        if colr is None:
            continue
        cx, cy = xs[j] + col_w[j] / 2, ys[i] + heights[i] / 2
        o = _rect(slide.shapes, cx - status_d / 2, cy - status_d / 2, status_d, status_d, colr,
                  shape=MSO_SHAPE.OVAL, name='Status ' + st)
    return {'tbl': tbl, 'y_baris': ys, 'tinggi_baris': heights, 'bawah': y + total_h,
            'kolom_x': xs, 'kolom_w': col_w}


def _isi_sel(cell, teks, size, color, bold, align, anchor):
    cell.vertical_anchor = anchor
    cell.margin_left = Inches(0.06)
    cell.margin_right = Inches(0.06)
    cell.margin_top = Inches(0.03)
    cell.margin_bottom = Inches(0.03)
    tf = cell.text_frame
    tf.word_wrap = True
    items = teks if isinstance(teks, (list, tuple)) else [teks]
    for k, t in enumerate(items):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = align
        if len(items) > 1:
            _bullet(p, '•', 0)
            p.space_after = Pt(2)
        _fill_runs(p, str(t), size, color, bold)


def legenda_status(slide, x, y, pakai=('ok', 'proses', 'belum'), na=True, size=11):
    """Legenda penanda status dokumen (bulat hijau/kuning/merah + '—' tidak berlaku)."""
    items = [(STATUS_LABEL[k], STATUS_WARNA[k], 'bulat') for k in pakai]
    w = _g.add_legend(slide, items, x, y, size=size)
    if na:
        _tb(slide.shapes, '—  tidak berlaku', x + w + 0.1, y - 0.01, 1.8, 0.22, size=size, color=GRAY)
    return w


def bagi_baris(rows, per_slide, kolom_gabung=0):
    """Pecah baris tabel menjadi beberapa halaman tanpa memutus grup gabungan
    (baris lanjutan = sel None di kolom_gabung)."""
    pages, cur = [], []
    grup = []
    for r in rows:
        if r[kolom_gabung] is not None and grup:
            if len(cur) + len(grup) > per_slide and cur:
                pages.append(cur)
                cur = []
            cur += grup
            grup = []
        grup.append(r)
    if grup:
        if len(cur) + len(grup) > per_slide and cur:
            pages.append(cur)
            cur = []
        cur += grup
    if cur:
        pages.append(cur)
    return pages


def add_tabel_bersambung(prs, topik, subtopik, header, rows, per_slide=13, narasi=None,
                         legenda=None, **kw):
    """Tabel panjang dipecah ke beberapa slide berjudul '(1/2)', '(2/2)' dengan tata letak identik
    (status dokumen, rekap proyek). kw diteruskan ke add_tabel (gaya='data', col_w, size, dll.).
    legenda: 'status' untuk legenda penanda status di bawah tabel."""
    pages = bagi_baris(rows, per_slide, kw.get('gabung', [0])[0] if kw.get('gabung') else 0)
    slides = []
    for k, pg in enumerate(pages, 1):
        sub = subtopik + (' (%d/%d)' % (k, len(pages)) if len(pages) > 1 else '')
        s = add_slide(prs, topik, sub, narasi=narasi if k == 1 else None)
        t = add_tabel(s, header, pg, L, body_top(s), CW, **kw)
        if t['bawah'] > BODY_BOTTOM - (0.35 if legenda else 0) + 0.05:
            print('PERINGATAN: tabel "%s" halaman %d turun sampai y %.2f in; kurangi per_slide '
                  'atau size.' % (subtopik, k, t['bawah']))
        if legenda == 'status':
            legenda_status(s, L, min(t['bawah'] + 0.12, 6.95))
        slides.append(s)
    return slides


# =====================================================================================
# Blok proyek
# =====================================================================================
def _wilayah_untuk(lon, lat):
    best = None
    for k, (a, b, c, d) in _g.WILAYAH.items():
        if k == 'indonesia':
            continue
        if a <= lon <= c and b <= lat <= d:
            area = (c - a) * (d - b)
            if best is None or area < best[0]:
                best = (area, k)
    return best[1] if best else 'indonesia'


def add_profil_proyek(prs, nama, info, latar, lokasi=None, gambar=None, ket_gambar='',
                      topik='Profil Proyek', narasi=None):
    """Profil proyek (slide 13 template).

    Kiri : tabel data proyek (item | isi).  Kanan atas: 'Informasi proyek' 3–5 butir latar/tujuan.
    Kanan bawah: peta wilayah dengan titik lokasi + koordinat dan kebutuhan lahan; bila `gambar`
    diberikan (peta sistem/SLD/foto lokasi dari dokumen user) gambar itu menggantikan peta.

    info   : [('Nama', '...'), ('Kapasitas', '400 MW'), ('Lokasi', ...), ('Interkoneksi', ...),
              ('Target COD', '2033'), ('Skema/sumber dana', ...), ('Nilai proyek', [...]), ('Pengembang', 'IPP')]
             isi boleh list -> beberapa butir dalam satu sel.
    latar  : 3–5 butir alasan/latar proyek.
    lokasi : {'lat': -5.1477, 'lon': 119.4327, 'label': 'Rencana lokasi',
              'wilayah': 'sulawesi' (opsional; otomatis dari koordinat), 'lahan': '±100–2.000 ha ...',
              'keterangan': 'Rencana lokasi berada di sistem ...' (opsional)}
    ket_gambar : satu kalimat apa yang ditampilkan gambar.
    """
    s = add_slide(prs, topik, nama, narasi=narasi)
    y0 = body_top(s)
    lw = 5.9
    yt = add_column_head(s, 'Data proyek', L, y0, lw)
    add_tabel(s, None, [[a_, b_] for a_, b_ in info], L, yt - 0.06, lw, col_w=[1.6, 4.3], size=12,
              row_h=0.4)
    rx, rw = L + lw + 0.45, R - (L + lw + 0.45)
    yr = add_column_head(s, 'Informasi proyek', rx, y0, rw)
    n_l = sum(_title_lines(str(t).replace('*', ''), rw - 0.3, 12) for t in latar)
    hl = n_l * 12 * 1.25 / 72 + 0.1 * len(latar)
    add_bullets(s, latar, rx, yr, rw, hl, size=12)
    yb = yr + hl + 0.25
    hb = BODY_BOTTOM - yb
    teks = []
    if lokasi:
        lat, lon = lokasi['lat'], lokasi['lon']
        teks = [('Koordinat lokasi', True),
                ('Lintang %s° %s' % (('%.4f' % abs(lat)).replace('.', ','), 'LS' if lat < 0 else 'LU'), False),
                ('Bujur %s° BT' % ('%.4f' % lon).replace('.', ','), False)]
        if lokasi.get('lahan'):
            teks += [('Kebutuhan lahan', True), (lokasi['lahan'], False)]
    ket = ket_gambar if gambar else (lokasi or {}).get('keterangan')
    if ket:
        teks += [(ket, False)]
    if gambar:
        vw = rw * 0.58
        fit_picture(s, gambar, rx, yb, vw, hb)
    elif lokasi:
        wil = lokasi.get('wilayah') or _wilayah_untuk(lokasi['lon'], lokasi['lat'])
        bb = _g.WILAYAH[wil] if isinstance(wil, str) else wil
        vw = min(rw * 0.55, hb * (bb[2] - bb[0]) / (bb[3] - bb[1]))
        _g.add_map(s, [{'nama': lokasi.get('label', 'Lokasi'), 'lon': lokasi['lon'], 'lat': lokasi['lat'],
                        'sorot': True}], rx, yb, vw, wilayah=wil, legenda=False, size=10,
                   daratan=OUTLINE, tetangga=False)
    else:
        vw = -0.3
    if teks:
        box = add_text(s, [t for t, _ in teks], rx + vw + 0.3, yb, rw - vw - 0.3, hb, size=12,
                       space_after=3)
        for p, (_, bold) in zip(box.text_frame.paragraphs, teks):
            for r in p.runs:
                r.font.bold = bold
        box.name = 'Pesan'
    return s


def fit_picture(slide, path, x, y, w, h, align='center', nama='Gambar'):
    """Gambar dari user (hasil simulasi, peta, SLD, matriks) dimuatkan ke kotak tanpa mengubah rasio."""
    from PIL import Image
    pw, ph = Image.open(path).size
    sc = min(w / pw, h / ph)
    ww, hh = pw * sc, ph * sc
    xx = x + (w - ww) / 2
    yy = y + (h - hh) / 2 if align == 'center' else y
    pic = slide.shapes.add_picture(path, Inches(xx), Inches(yy), Inches(ww), Inches(hh))
    pic.name = nama
    return pic


def _kotak_gambar(slide, x, y, w, h, gambar, pengganti):
    if gambar:
        return fit_picture(slide, gambar, x, y, w, h)
    b = _rect(slide.shapes, x, y, w, h, MIST, name='Tempat gambar')
    _g._shape_text(b, pengganti, size=11, color=GRAY)
    return b


def add_kko_parameter(prs, nama, parameter, potensi='', produksi='', gambar=None,
                      judul_gambar='Potensi energi di lokasi pembangkit', bagian='(1/3)', narasi=None):
    """Ringkasan KKO bagian parameter (slide 14 template).

    parameter : [('Kapasitas pembangkit net', 'MWac', '400'), ('Capacity factor', '%', '50%'), ...]
    potensi   : 1–2 kalimat sumber daya di lokasi (di bawah gambar kiri).
    produksi  : 1 kalimat hitungan produksi energi (di bawah tabel kanan).
    gambar    : peta potensi/hidrologi dari dokumen KKO (path). Tanpa gambar: kotak pengganti abu.
    """
    s = add_slide(prs, 'Ringkasan KKO', '%s %s' % (nama, bagian), narasi=narasi)
    y0 = body_top(s)
    lw = 5.9
    yl = add_column_head(s, judul_gambar, L, y0, lw)
    gh = 3.55 if potensi else 5.2
    _kotak_gambar(s, L, yl, lw, gh, gambar, 'Gambar potensi energi dari dokumen KKO')
    if potensi:
        add_keterangan(s, potensi, L, yl + gh + 0.2, lw, BODY_BOTTOM - (yl + gh + 0.2))
    rx, rw = L + lw + 0.5, R - (L + lw + 0.5)
    yr = add_column_head(s, 'Parameter pembangkit', rx, y0, rw)
    t = add_tabel(s, ['Parameter', 'Satuan', 'Nilai'], [list(p) for p in parameter], rx, yr - 0.06,
                  rw, col_w=[2.9, 1.1, 1.5], size=12, rata=['l', 'c', 'r'], row_h=0.36)
    if produksi:
        add_text(s, produksi, rx, t['bawah'] + 0.25, rw, 1.2, size=13)
    return s


def add_kko_analisis(prs, nama, butir, bagian='', narasi=None):
    """Ringkasan KKO bagian analisis sistem (slide 15–16 template), 2 butir per slide.

    butir : [{'judul': 'Aliran daya', 'ikon': 'listrik', 'gambar': 'aliran.png' | None,
              'keterangan': '...', 'status': 'Normal'}]
            Urutan baku KKO: aliran daya, hubung singkat, stabilitas transien, stabilitas frekuensi.
    bagian: '(2/3)'. Kolom: Analisis | Hasil (gambar simulasi) | Keterangan.
    """
    s = add_slide(prs, 'Ringkasan KKO', ('%s %s' % (nama, bagian)).strip(), narasi=narasi)
    y0 = body_top(s)
    cw = [2.3, 5.4, CW - 2.3 - 5.4]
    xs = [L, L + cw[0], L + cw[0] + cw[1]]
    for j, hd in enumerate(['Analisis', 'Hasil simulasi', 'Keterangan']):
        add_column_head(s, hd, xs[j] + (0.1 if j else 0), y0, cw[j] - (0.2 if j < 2 else 0.1))
    top = y0 + HEAD_H + 0.2
    n = len(butir)
    rh = (BODY_BOTTOM - top) / max(n, 1)
    for i, b in enumerate(butir):
        y = top + i * rh
        if b.get('ikon'):
            add_icon_badge(s, b['ikon'], xs[0], y + 0.05, d=0.5)
        add_text(s, b['judul'], xs[0] + (0.62 if b.get('ikon') else 0), y + 0.05,
                 cw[0] - 0.7, 0.9, size=14, color=DARK, bold=True, anchor=MSO_ANCHOR.TOP)
        _kotak_gambar(s, xs[1] + 0.1, y + 0.05, cw[1] - 0.2, rh - 0.25, b.get('gambar'),
                      'Grafik hasil simulasi %s' % b['judul'].lower())
        teks = [b.get('keterangan', '')]
        if b.get('status'):
            teks.append({'text': 'Status: %s' % b['status'], 'bold': True})
        box = add_text(s, [t['text'] if isinstance(t, dict) else t for t in teks], xs[2] + 0.1,
                       y + 0.05, cw[2] - 0.1, rh - 0.2, size=12, line=1.05)
        if b.get('status'):
            for r in box.text_frame.paragraphs[-1].runs:
                r.font.bold = True
        box.name = 'Pesan'
        if i < n - 1:
            _line(s.shapes, L, y + rh - 0.1, R, y + rh - 0.1, OUTLINE, 0.75)
    return s


def add_kkf(prs, nama, asumsi, hasil, sensitivitas=None, kesimpulan='', judul_asumsi=None):
    """Ringkasan KKF (slide 17 template).

    asumsi       : [('Total biaya proyek', 'Rp 15.563,9 miliar', 'Kajian Kelayakan Proyek ...'), ...]
                   nilai boleh list (mis. tarif per stage).
    hasil        : [('Equity IRR', '10,50%'), ('Project IRR', '6,95%'), ...]
    sensitivitas : {'header': ['Skenario', 'NPV (Rp juta)', 'E-IRR', 'BCR', 'PBP'],
                    'rows': [['Base case', ...], ...], 'col_w': [...] (opsional)}
    kesimpulan   : kesimpulan dari dokumen KKF (bukan karangan), ditulis sebagai narasi di bawah judul
                   dengan angka kuncinya: 'Proyek layak secara finansial: Equity IRR 10,50% dan
                   NPV ekuitas Rp 205,4 miliar.'
    """
    s = add_slide(prs, 'Ringkasan KKF', nama, narasi=kesimpulan or None)
    y0 = body_top(s)
    lw = 7.3
    yl = add_column_head(s, judul_asumsi or 'Asumsi kajian finansial', L, y0, lw)
    t1 = add_tabel(s, ['Asumsi', 'Nilai', 'Dasar'], [list(a_) for a_ in asumsi], L, yl - 0.06, lw,
                   col_w=[1.8, 2.3, 3.2], size=10, row_h=0.26, head_size=11)
    rx, rw = L + lw + 0.4, R - (L + lw + 0.4)
    yr = add_column_head(s, 'Hasil perhitungan', rx, y0, rw)
    t = add_tabel(s, None, [list(h) for h in hasil], rx, yr - 0.06, rw, col_w=[2.6, 2.1], size=11,
                  row_h=0.27, rata=['l', 'r'], sumbu=False)
    for i in range(len(hasil)):     # label hasil tetap bold
        for p in t['tbl'].cell(i, 0).text_frame.paragraphs:
            for r in p.runs:
                r.font.bold = True
    bawah = max(t1['bawah'], t['bawah'])
    if sensitivitas:
        ys = add_column_head(s, 'Sensitivitas kasus terburuk', rx, t['bawah'] + 0.2, rw)
        hd = sensitivitas['header']
        t2 = add_tabel(s, hd, sensitivitas['rows'], rx, ys - 0.06, rw, size=10, row_h=0.25,
                       head_size=10, rata=['l'] + ['r'] * (len(hd) - 1), sumbu=False,
                       col_w=sensitivitas.get('col_w'))
        bawah = max(bawah, t2['bawah'])
    if bawah > BODY_BOTTOM + 0.05:
        print('PERINGATAN: Ringkasan KKF "%s" turun sampai y %.2f in; ringkas asumsi atau sensitivitas.'
              % (nama, bawah))
    return s


# Tingkat risiko per sel matriks 5x5: baris = kemungkinan V (atas) .. I (bawah), kolom = dampak 1..5
RISK_GRID = [
    ['LM', 'M', 'MH', 'H', 'H'],     # V  Hampir pasti terjadi
    ['L', 'LM', 'M', 'MH', 'H'],     # IV Sangat mungkin terjadi
    ['L', 'LM', 'M', 'MH', 'H'],     # III Bisa terjadi
    ['L', 'LM', 'LM', 'MH', 'H'],    # II Jarang terjadi
    ['L', 'L', 'LM', 'M', 'H'],      # I  Sangat jarang terjadi
]
RISK_NAMA = {'L': 'Low', 'LM': 'Low to Moderate', 'M': 'Moderate', 'MH': 'Moderate to High', 'H': 'High'}
RISK_WARNA = {'L': RISK_LOW, 'LM': RISK_LM, 'M': RISK_MOD, 'MH': RISK_MH, 'H': RISK_HIGH}
KEMUNGKINAN = ['Hampir pasti terjadi', 'Sangat mungkin terjadi', 'Bisa terjadi', 'Jarang terjadi',
               'Sangat jarang terjadi']
DAMPAK = ['Sangat rendah', 'Rendah', 'Moderat', 'Tinggi', 'Sangat tinggi']


def add_matriks_risiko(slide, sebaran, x, y, w, h, judul=None, grid=None, size=9):
    """Peta risiko 5x5 (kemungkinan x dampak) dari bentuk asli.
    sebaran : {(kemungkinan 1..5, dampak 1..5): [nomor risiko]} — nomor merujuk daftar risiko.
    grid    : tingkat per sel (default RISK_GRID; ganti bila unit memakai matriks lain)."""
    grid = grid or RISK_GRID
    S = _group(slide, 'matriks risiko')
    yt = y
    if judul:
        _tb(S, judul, x, y, w, 0.28, size=12, bold=True, color=INK)
        yt = y + 0.32
    lab_w, rom_w, foot_h = 1.25, 0.3, 0.55
    gx, gw = x + lab_w + rom_w, w - lab_w - rom_w
    gh = h - (yt - y) - foot_h
    cw, ch = gw / 5, gh / 5
    romawi = ['V', 'IV', 'III', 'II', 'I']
    _vtb(S, 'Kemungkinan', x + 0.12, yt + gh / 2, gh, 10, bold=True)
    for r in range(5):
        yy = yt + r * ch
        _tb(S, KEMUNGKINAN[r], x + 0.28, yy, lab_w - 0.3, ch, size=size, bold=True,
            anchor=MSO_ANCHOR.MIDDLE)
        _tb(S, romawi[r], x + lab_w, yy, rom_w, ch, size=size, bold=True, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)
        for c in range(5):
            lv = grid[r][c]
            col = RISK_WARNA[lv]
            box = _rect(S, gx + c * cw, yy, cw, ch, col, line=WHITE, line_pt=1.0,
                        name='Sel %s%d' % (romawi[r], c + 1))
            ids = sebaran.get((5 - r, c + 1), [])
            if ids:
                txt = ', '.join(str(i) for i in ids)
                _g._shape_text(box, txt, size=size, color=WHITE if lv in ('L', 'H') else INK, bold=True)
    for c in range(5):
        _tb(S, [str(c + 1), DAMPAK[c]], gx + c * cw, yt + gh + 0.03, cw, foot_h - 0.25,
            size=size, bold=False, align=PP_ALIGN.CENTER)
    _tb(S, 'Dampak', gx, yt + gh + foot_h - 0.22, gw, 0.22, size=10, bold=True, align=PP_ALIGN.CENTER)
    return S


def add_kajian_risiko(prs, nama, daftar, sebelum, sesudah, size=9, per_kolom=None, narasi=None):
    """Kajian risiko (slide 18 template): peta risiko sebelum -> sesudah mitigasi + daftar risiko.

    daftar  : ['3.6.13.3.0129 - Penundaan proyek', ...] (urutan = nomor risiko 1..n)
    sebelum : {(kemungkinan, dampak): [nomor, ...]} posisi risiko inheren
    sesudah : {(kemungkinan, dampak): [nomor, ...]} posisi risiko setelah mitigasi
    Daftar yang tidak muat dilanjutkan ke slide '(lanjutan)' dengan tata letak sama.
    """
    s = add_slide(prs, 'Kajian Risiko', nama, narasi=narasi)
    y0 = body_top(s)
    mh = 3.25
    mw = 5.55
    add_matriks_risiko(s, sebelum, L, y0, mw, mh, judul='Risiko inheren')
    ax = L + mw + 0.12
    aw = CW - 2 * mw - 0.24
    arr = _rect(s.shapes, ax + 0.1, y0 + 1.25, aw - 0.2, 0.5, PRIMARY, shape=MSO_SHAPE.RIGHT_ARROW,
                name='Panah mitigasi')
    add_text(s, 'Dimitigasi', ax, y0 + 1.8, aw, 0.3, size=11, color=DARK, bold=True, align=PP_ALIGN.CENTER)
    add_matriks_risiko(s, sesudah, R - mw, y0, mw, mh, judul='Risiko setelah mitigasi')
    items = list(RISK_NAMA.items())
    _g.add_legend(s, [(v, RISK_WARNA[k], 'kotak') for k, v in items], L, y0 + mh + 0.08, size=10)
    yl = y0 + mh + 0.45
    hl = BODY_BOTTOM - yl
    line_h = size * 1.25 / 72
    cap = per_kolom or max(int(hl / line_h), 1)
    colw = (CW - 0.4) / 2
    chars = int(colw * 72 / (size * 0.5)) - 5

    def lines(t):
        return max(1, -(-len(t) // chars))
    kolom, cur, used = [], [], 0
    for k, t in enumerate(daftar, 1):
        n = lines(t)
        if used + n > cap and cur:
            kolom.append(cur)
            cur, used = [], 0
        cur.append((k, t))
        used += n
    if cur:
        kolom.append(cur)
    halaman = [kolom[i:i + 2] for i in range(0, len(kolom), 2)]
    slides = [s]
    for hi, kol in enumerate(halaman):
        if hi > 0:
            s2 = add_slide(prs, 'Kajian Risiko', nama + ' (lanjutan)')
            slides.append(s2)
            target, yy, hh = s2, body_top(s2), BODY_BOTTOM - body_top(s2)
        else:
            target, yy, hh = s, yl, hl
        for ci, isi in enumerate(kol):
            box = target.shapes.add_textbox(Inches(L + ci * (colw + 0.4)), Inches(yy), Inches(colw),
                                            Inches(hh))
            box.name = 'Daftar risiko'
            tf = box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            for m, (k, t) in enumerate(isi):
                p = tf.paragraphs[0] if m == 0 else tf.add_paragraph()
                pPr = p._p.get_or_add_pPr()
                pPr.set('marL', str(int(0.3 * 914400)))
                pPr.set('indent', str(int(-0.3 * 914400)))
                pPr.append(pPr.makeelement(qn('a:buFont'), {'typeface': 'Arial'}))
                pPr.append(pPr.makeelement(qn('a:buAutoNum'), {'type': 'arabicPeriod', 'startAt': str(k)}))
                _fill_runs(p, t, size, INK)
    return slides


# Tahapan baku proyek pembangkit (urutan dan label dari Template TVV). Tanggal diisi dari user.
TAHAP_BAKU = [
    ('Inisiasi', ['Feasibility Study', 'RUPS persetujuan RKAP, penugasan, TMD']),
    ('Perencanaan', ['Penugasan proyek', 'Pengadaan di PLN', 'Due diligence',
                     'PPA negotiation, SHA, pembentukan SPC']),
    ('Prakonstruksi', ['PPA signing*', 'Financing date', 'Perizinan', 'Pengadaan EPC', 'EPC contract sign*']),
    ('Konstruksi', ['Engineering, procurement, civil preparation', 'Construction',
                    'Test and commissioning', 'COD*']),
]   # * = milestone


def add_timeline_proyek(prs, nama, tahap, mulai, selesai, semester=True, size=10, hari_ini=None,
                        topik='Indicative Timeline', narasi=None):
    """Indicative timeline proyek bergaya Gantt dengan pita tahapan (slide 19 template).

    tahap : [{'nama': 'Inisiasi', 'kegiatan': [
                {'label': 'Feasibility Study', 'mulai': 2026.25, 'selesai': 2026.75},
                {'label': 'PPA signing', 'milestone': 2028.9}, ...]}, ...]
            Waktu dalam tahun desimal: 2027.0 = awal 2027, 2027.5 = awal semester 2 (SM2).
    mulai, selesai : tahun pertama dan terakhir yang ditampilkan (inklusif).
    hari_ini: tahun desimal untuk garis 'Saat ini' (opsional).
    Lihat TAHAP_BAKU untuk urutan kegiatan baku; tanggal hanya dari dokumen user.
    """
    s = add_slide(prs, topik, nama, narasi=narasi)
    y0 = body_top(s)
    S = _group(s, 'timeline proyek')
    stage_w = 1.55
    gx, gw = L + stage_w, CW - stage_w
    tahun = list(range(int(mulai), int(selesai) + 1))
    ny = len(tahun)
    t0, t1 = float(tahun[0]), float(tahun[-1] + 1)
    X = lambda t: gx + (t - t0) / (t1 - t0) * gw
    hy = 0.26
    head_h = hy * (2 if semester else 1)
    kp = _rect(S, L, y0, stage_w, head_h, DARK, line=WHITE, line_pt=0.75, name='Kepala tahap')
    _g._shape_text(kp, 'Tahapan proyek', size=10, color=WHITE, bold=True)
    for k, th in enumerate(tahun):
        b = _rect(S, X(th), y0, gw / ny, hy, DARK, line=WHITE, line_pt=0.75)
        _g._shape_text(b, str(th), size=size, color=WHITE, bold=True)
        if semester:
            for sm in (0, 1):
                b2 = _rect(S, X(th + sm * 0.5), y0 + hy, gw / ny / 2, hy, A1, line=WHITE, line_pt=0.75)
                _g._shape_text(b2, 'SM%d' % (sm + 1), size=9, color=WHITE)
    n_rows = sum(len(t['kegiatan']) for t in tahap)
    top = y0 + head_h + 0.04
    rh = min(0.42, (BODY_BOTTOM - top - 0.35) / max(n_rows, 1))
    yy = top
    band = [MIST, LIGHT]
    yy = top
    for ti, t in enumerate(tahap):          # pita tahap dan label tahap
        hh = rh * len(t['kegiatan'])
        _rect(S, gx, yy, gw, hh, band[ti % 2], name='Pita ' + t['nama'])
        lab = _rect(S, L, yy, stage_w, hh, TINT, line=WHITE, line_pt=1.0, name='Tahap ' + t['nama'])
        _g._shape_text(lab, t['nama'].upper(), size=11, color=DARK, bold=True)
        yy += hh
    n_col = ny * (2 if semester else 1)
    for k in range(1, n_col):                # garis kolom semester/tahun di bawah batang
        xx = gx + k * gw / n_col
        _line(S, xx, top, xx, yy, WHITE if (semester and k % 2) else OUTLINE, 0.5)
    ms = []
    yy = top
    for t in tahap:
        for kg in t['kegiatan']:
            if 'milestone' in kg:
                m = kg['milestone']
                d = rh * 0.62
                _rect(S, X(m) - d / 2, yy + (rh - d) / 2, d, d, PRIMARY, shape=MSO_SHAPE.DIAMOND,
                      name='Milestone ' + kg['label'])
                x_end, x_start = X(m) + d / 2, X(m) - d / 2
                ms.append(kg)
            else:
                bh = rh * 0.52
                x_start, x_end = X(kg['mulai']), X(kg['selesai'])
                _rect(S, x_start, yy + (rh - bh) / 2, max(x_end - x_start, 0.04), bh, DARK,
                      name='Batang ' + kg['label'])
            tw = len(kg['label']) * size * 0.5 / 72 + 0.15
            if x_end + 0.06 + tw <= R:
                _tb(S, kg['label'], x_end + 0.06, yy, tw, rh, size=size, anchor=MSO_ANCHOR.MIDDLE)
            else:
                _tb(S, kg['label'], x_start - 0.06 - tw, yy, tw, rh, size=size, align=PP_ALIGN.RIGHT,
                    anchor=MSO_ANCHOR.MIDDLE)
            yy += rh
    if hari_ini is not None:
        _line(S, X(hari_ini), top, X(hari_ini), yy + 0.05, NEG, 1.25, dash=True)
        _tb(S, 'Saat ini', X(hari_ini) - 0.6, yy + 0.06, 1.2, 0.2, size=9, color=NEG, bold=True,
            align=PP_ALIGN.CENTER)
    leg = [('Kegiatan', DARK, 'kotak')]
    if ms:
        leg.append(('Milestone', PRIMARY, 'belah'))
    _g.add_legend(s, leg, L, min(yy + 0.12, 6.95))
    return s


__all__ = [n for n in dir() if not n.startswith('_')]
