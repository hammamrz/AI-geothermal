#!/usr/bin/env python3
"""check_deck.py — pemeriksa aturan deck TVV (skill presentasi-tvv; turunan pemeriksa PLN IP).

Beda dengan versi PLN IP: narasi 14pt di bawah judul (shape 'Narasi' dari add_slide(narasi=...)) dan
baris sumber di bawah (shape 'Sumber' dari add_sumber) DIIZINKAN sesuai Template TVV; kuota ilustrasi
tidak diperiksa (deck TVV padat data); tabel data boleh 10pt; warna matriks risiko termasuk palet.

Pakai:  python3 check_deck.py deck.pptx
Keluar: kode 1 bila ada FAIL. WARN wajib dibaca, boleh diabaikan bila memang disengaja.
Butuh: python-pptx (pip install python-pptx --break-system-packages)

Yang diperiksa (nomor merujuk ke references/aturan-slide.md):
  FAIL  teks kecil di bawah judul yang BUKAN narasi resmi (pakai add_slide(..., narasi=...)) · footer teks
        "PT PLN Indonesia Power | ..."
  WARN  narasi lebih dari 2 baris · baris "Sumber:" di luar add_sumber · deck > 10 slide tanpa outline
  WARN  istilah Indonesia tak umum (tonggak, daring, luring, larik, linimasa, ...) -> istilah Inggris
        · judul kolom "Implikasi"/"Kesimpulan"/"Insight" (implikasi tambahan yang tidak diminta)
  FAIL  kanvas bukan 16:9 · sudut membulat · gradien · bullet diketik manual · emoji
        · placeholder tertinggal · judul kosong
  FAIL  kotak judul menabrak area logo (Danantara / PLN IP) · judul di bawah / tidak sebaris dengan logo
        · judul tidak muat 2 baris di lebar yang tersisa
  WARN  judul sedikit meleset dari garis tengah logo · tinggi/posisi logo tidak seragam
        · logo hanya ada di sebagian slide isi
  WARN  warna di luar palet · bayangan · kotak berisi + garis tepi · garis dekoratif di bawah judul
        · lebih dari 6 warna PLN IP dalam satu deck
        · judul satu warna (topik harus biru, sub-topik hitam) · kicker di atas judul
        · judul terlalu panjang / diakhiri titik
        · judul duplikat · teks < 9pt · lebih dari 2 jenis font · font selain Helvetica · kosakata "rasa AI"
        · istilah ganda (mis. stakeholder vs pemangku kepentingan)
  WARN  aset visual (aturan-slide.md §5.15–5.16): ilustrasi < 1 per 6 slide isi · 7 slide berturut-turut
        tanpa ikon/ilustrasi · deck > 10 slide tanpa daftar isi / pembatas bab · ilustrasi di slide chart
        atau tabel lebar · ilustrasi menimpa teks/tabel · > 1 ilustrasi per slide · ilustrasi dipakai ulang
        · ilustrasi lebih lebar dari 4,8 in
Di akhir dicetak daftar judul dan daftar keterangan per slide untuk dibaca berurutan (uji alur cerita).
"""
import re
import sys
from collections import defaultdict

try:
    from pptx import Presentation
    from pptx.util import Emu
except ImportError:
    sys.exit("python-pptx belum terpasang: pip install python-pptx --break-system-packages")

NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
EMU_IN = 914400

# ---- Palet (tanpa '#'). Tambahkan warna resmi lain di sini bila ada. ----
# Aturan "3 warna" hanya menghitung Accent 1-5. Putih, Gray, dan Outline Color
# masuk netral di pedoman, jadi tidak ikut dihitung.
PALETTE_PLNIP = {"1B4F60", "008AAC", "05365B", "29537B", "D1EDF3"}
PALETTE_EXTRA = {"FFD966", "0DAD8E", "006699", "F6F9FB"}   # palet tambahan (maks 1 per deck)
PALETTE_TRAFFIC = {"22B44A", "EFCF06", "E00102"}           # lampu lalu lintas: dikecualikan
PALETTE_NEUTRAL = {"1A1A1A", "1F2933", "FFFFFF", "000000", "E6EEF2", "B03A2E", "0A7F69", "004466",
                   "4D4D4D", "C0C0C0", "5F6B76", "C9D1D8", "A7B1BA", "333333"}
PALETTE_RISK = {"1B7F3B", "F08C00"}                        # matriks risiko TVV (plus lampu lalu lintas)
PALETTE = PALETTE_PLNIP | PALETTE_EXTRA | PALETTE_TRAFFIC | PALETTE_NEUTRAL | PALETTE_RISK

ROUNDED = {"roundRect", "round1Rect", "round2SameRect", "round2DiagRect", "snipRoundRect",
           "flowChartAlternateProcess", "wedgeRoundRectCallout"}

TOPIC_COLORS = {"008AAC", "1B4F60", "05365B", "29537B", "006699"}  # biru yang sah untuk bagian topik judul

MANUAL_BULLET = re.compile(r"^\s*([•●▪■◆►✓✔➤→\-\*]|\d+[\.\)])\s+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F02F\u2B50\u2B06\u2194-\u21FF\u2705\u274C]")
PLACEHOLDER = re.compile(r"lorem|ipsum|\[insert|\[isi|\bTBD\b|\bTODO\b|\bxxx+\b|Text \d|Judul \d|Label \d|\bYYYY\b|◯◯", re.I)
COUNT_IN_TITLE = re.compile(r"\b(\d+|dua|tiga|empat|lima|enam|tujuh)\s+(langkah|tahap|tahapan|fase|pilar|alasan|poin|hal|faktor|strategi|kunci|aspek|inisiatif)\b", re.I)
# Istilah Indonesia yang jarang dipakai di lingkungan PLN IP -> pakai istilah Inggris yang lebih umum
UNCOMMON_ID = {
    "tonggak": "milestone", "linimasa": "timeline", "daring": "online", "luring": "offline",
    "larik": "array", "surel": "email", "pranala": "link", "peladen": "server", "gawai": "gadget/device",
    "tetikus": "mouse", "tagar": "hashtag", "warganet": "netizen", "swafoto": "selfie", "sangkil": "efisien",
    "mangkus": "efektif", "portal web": "website", "laman": "website/halaman", "unggahan": "upload",
    "papan pemuka": "dashboard", "dasbor": "dashboard", "rintisan": "startup", "pelantar": "platform",
    "perisian": "software", "kecerdasan artifisial": "AI", "mahadata": "big data", "komputasi awan": "cloud",
    "rantai blok": "blockchain", "tayangan salindia": "slide", "salindia": "slide", "narahubung": "contact person",
}
IMPLIKASI_HEAD = re.compile(r"^(implikasi|arti bagi.*|so what|jadi apa|insight|kesimpulan|key takeaway|takeaway|makna)$", re.I)
SOURCE_LINE = re.compile(r"^(sumber|source|sumber data)\s*:", re.I)
FOOTER_TEXT = re.compile(r"PT\s+PLN\s+Indonesia\s+Power\s*\||\|\s*PT\s+PLN", re.I)
pesan_pages, no_pesan, _FULLTEXT, _GRAF = [], [], [], []
LABEL_PREFIX = re.compile(r"^[^:\n]{2,35}:\s")

# Kosakata "rasa AI" berkeyakinan tinggi (lihat references/kosakata-anti-ai.md)
AI_SMELL = [
    "komprehensif", "holistik", "sinergi", "sinergis", "optimalisasi", "mengoptimalkan", "memaksimalkan potensi",
    "memberdayakan", "revolusioner", "inovatif", "transformatif", "lanskap", "game changer", "game-changer",
    "tidak hanya", "di era", "dalam rangka", "guna mewujudkan", "mewujudkan", "krusial", "esensial",
    "berkelanjutan dan", "secara signifikan", "sangat penting", "memainkan peran", "peran penting",
    "menjadi kunci", "kunci sukses", "langkah strategis", "solusi terintegrasi", "end-to-end", "seamless",
    "robust", "leverage", "unlock", "empower", "synergy", "holistic", "comprehensive", "cutting-edge",
    "next-level", "key takeaway", "pentingnya", "peran strategis", "sebagai garda terdepan", "kesimpulan utama", "mari kita", "perlu dicatat", "penting untuk dicatat",
]
TERM_PAIRS = [
    ("stakeholder", "pemangku kepentingan"), ("roadmap", "peta jalan"),
    ("power plant", "pembangkit"), ("capex", "belanja modal"), ("opex", "biaya operasi"),
    ("user", "pengguna"), ("feasibility study", "studi kelayakan"), ("baseline", "garis dasar"),
]

fails, warns = [], []


def fail(i, msg):
    fails.append(f"S{i}: {msg}")


def warn(i, msg):
    warns.append(f"S{i}: {msg}" if i else msg)


def shape_text(sh):
    return sh.text_frame.text if getattr(sh, "has_text_frame", False) and sh.has_text_frame else ""


def iter_shapes(shapes):
    for sh in shapes:
        if sh.shape_type == 6 and hasattr(sh, "shapes"):  # group
            yield from iter_shapes(sh.shapes)
        else:
            yield sh


def max_font_pt(sh):
    best = 0
    if not (getattr(sh, "has_text_frame", False) and sh.has_text_frame):
        return 0
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            if r.font.size:
                best = max(best, r.font.size.pt)
    for rpr in sh._element.iter(NS_A + "rPr"):
        if rpr.get("sz"):
            best = max(best, int(rpr.get("sz")) / 100)
    return best


def find_title(slide):
    cands = []
    for sh in iter_shapes(slide.shapes):
        t = shape_text(sh).strip()
        if not t:
            continue
        if sh.name in ("Title", "Judul pembatas", "Judul penutup", "Judul panel") or (sh.is_placeholder and "title" in str(sh.placeholder_format.type).lower()):
            return sh
        top = (sh.top or 0) / EMU_IN
        if top < 1.6:
            cands.append((max_font_pt(sh), sh))
    cands.sort(key=lambda x: -x[0])
    return cands[0][1] if cands and cands[0][0] >= 18 else None


def est_lines(text, w_in, pt, font=None):
    """Perkiraan jumlah baris judul. Lebar rata-rata karakter: Arial ~0,53 em,
    Helvetica (font korporat PLN IP) ~0,53 em; Calibri lebih ramping ~0,42 em."""
    if not pt or not w_in:
        return 1, 999
    f = (font or "").lower()
    em = 0.42 if f.startswith("calibri") else 0.53   # Helvetica/Arial/Liberation Sans ~0,53 em
    cpl = max(int(w_in * 72 / (pt * em)), 1)
    lines = 0
    for part in re.split(r"[\n\v]", text):
        n = len(part.strip())
        lines += max(1, -(-n // cpl))
    return lines, cpl


def find_logos(slide, sw_in):
    """Gambar di kanan atas (slide, layout, master) = logo header."""
    out, seen = [], set()
    sources = [slide.shapes]
    try:
        sources += [slide.slide_layout.shapes, slide.slide_layout.slide_master.shapes]
    except Exception:
        pass
    for shapes in sources:
        for sh in iter_shapes(shapes):
            if sh.shape_type != 13 or sh.top is None or sh.height is None:
                continue
            t, h, l, w = sh.top / EMU_IN, sh.height / EMU_IN, sh.left / EMU_IN, sh.width / EMU_IN
            key = (round(l, 2), round(t, 2), round(w, 2))
            if key in seen:
                continue
            if t + h / 2 < 1.4 and l > sw_in * 0.45 and h < 1.2:
                seen.add(key)
                out.append({"l": l, "t": t, "w": w, "h": h, "name": sh.name})
    return out


def bg_has_image(slide):
    """True bila latar master/layout berupa gambar (logo master native PLN IP ada di gambar latar)."""
    NS_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
    try:
        parts = [slide.slide_layout, slide.slide_layout.slide_master]
    except Exception:
        return False
    for part in parts:
        bg = part._element.find(".//" + NS_P + "bg")
        if bg is not None and bg.find(".//" + NS_A + "blip") is not None:
            return True
        for sh in part.shapes:
            if sh.shape_type == 13:
                return True
    return False


def title_text_center(sh, lines, pt):
    top, h = sh.top / EMU_IN, sh.height / EMU_IN
    text_h = lines * (pt or 22) * 1.2 / 72
    bp = sh._element.find(".//" + NS_A + "bodyPr")
    anchor = bp.get("anchor") if bp is not None else None
    if anchor == "t":
        return top + 0.05 + text_h / 2
    if anchor == "b":
        return top + h - 0.05 - text_h / 2
    return top + h / 2


TEMPLATE_LOGO_LEFT = 9.2   # tepi kiri blok logo pada Template_PLNIP.pptx dan master desain 1 (9,36)


def title_font(sh):
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            if r.font.name:
                return r.font.name
    for f in sh._element.iter(NS_A + "latin"):
        if f.get("typeface") and not f.get("typeface").startswith("+"):
            return f.get("typeface")
    return None


def title_run_colors(sh):
    """Warna tiap run judul, urut. Run kosong dilewati."""
    out = []
    if not (getattr(sh, "has_text_frame", False) and sh.has_text_frame):
        return out
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            if not r.text.strip():
                continue
            c = r.font.color
            try:
                out.append(str(c.rgb).upper()) if c and c.type is not None else out.append("AUTO")
            except AttributeError:
                out.append("AUTO")
    return out


def check_header(i, title_sh, logos, is_cover):
    """Judul harus sebaris dengan logo: tengah vertikal sama, dan kotak judul berhenti sebelum logo."""
    if not logos:
        # Template resmi menaruh logo di GAMBAR LATAR master, jadi tidak ada shape logo.
        # Yang bisa dicek: kotak judul tidak boleh masuk ke area logo kanan atas.
        if title_sh is not None and not is_cover and title_sh.left is not None:
            right = (title_sh.left + title_sh.width) / EMU_IN
            if right > TEMPLATE_LOGO_LEFT:
                fail(i, f"kotak judul melebar sampai {right:.2f} in; area logo template mulai "
                        f"{TEMPLATE_LOGO_LEFT:.2f} in. Persempit judul")
        return
    lg_left = min(g["l"] for g in logos)
    lg_top = min(g["t"] for g in logos)
    lg_bot = max(g["t"] + g["h"] for g in logos)
    lg_mid = (lg_top + lg_bot) / 2
    mids = [g["t"] + g["h"] / 2 for g in logos]
    if max(mids) - min(mids) > 0.05:
        warn(i, "logo tidak segaris (tengah vertikal berbeda); samakan posisi y")
    hs = [g["h"] for g in logos]
    # Toleransi 0,10in: cukup untuk lockup 2 logo resmi (Danantara 0,35in / PLN IP 0,44in)
    # yang MEMANG sengaja tidak sama tinggi (mengikuti proporsi lockup masing-masing).
    if max(hs) - min(hs) > 0.10:
        warn(i, f"tinggi logo berbeda cukup jauh ({', '.join(f'{x:.2f}' for x in hs)} in); pastikan disengaja")
    if title_sh is None or is_cover or title_sh.top is None:
        return
    t_top, t_h = title_sh.top / EMU_IN, title_sh.height / EMU_IN
    t_left, t_w = title_sh.left / EMU_IN, title_sh.width / EMU_IN
    t_right, t_bot = t_left + t_w, t_top + t_h
    v_overlap = t_top < lg_bot and t_bot > lg_top
    if v_overlap and t_right > lg_left - 0.1:
        fail(i, f"kotak judul menabrak area logo (tepi kanan judul {t_right:.2f} in, logo mulai {lg_left:.2f} in); "
                f"persempit lebar judul sampai ≤ {lg_left - 0.35:.2f} in")
    pt = max_font_pt(title_sh) or 22
    lines, cpl = est_lines(title_sh.text_frame.text, t_w, pt, title_font(title_sh))
    if lines > 2:
        fail(i, f"judul diperkirakan {lines} baris pada lebar {t_w:.2f} in (±{cpl} karakter/baris); ringkas judul")
    c = title_text_center(title_sh, min(lines, 2), pt)
    if t_top >= lg_bot - 0.05 or abs(c - lg_mid) > 0.2:
        fail(i, f"judul tidak sebaris dengan logo (tengah judul {c:.2f} in, tengah logo {lg_mid:.2f} in); "
                f"letakkan judul di baris logo dengan lebar berhenti sebelum logo")
    elif abs(c - lg_mid) > 0.08:
        warn(i, f"judul belum tepat sejajar dengan logo (tengah judul {c:.2f} in, tengah logo {lg_mid:.2f} in)")


def _box(sh):
    return ((sh.left or 0) / EMU_IN, (sh.top or 0) / EMU_IN,
            (sh.width or 0) / EMU_IN, (sh.height or 0) / EMU_IN)


def _overlap(a, b):
    w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return max(w, 0) * max(h, 0)


def check_visual(i, slide, title_sh, is_cover, visual):
    """Kumpulkan ikon/ilustrasi per slide (nama gambar diberi helper: 'Ikon …', 'Ilustrasi …')."""
    ills, n_icon, wide, others, grafis = [], 0, False, [], []
    for sh in slide.shapes:          # grafis plnip_grafis = group bernama 'Grafik <jenis>'
        if sh.shape_type == 6 and (sh.name or '').startswith('Grafik ') and sh.name != 'Grafik legenda':
            grafis.append(sh.name[len('Grafik '):])
    for sh in iter_shapes(slide.shapes):
        name = sh.name or ''
        if sh.shape_type == 13 and name.startswith('Ilustrasi '):
            ills.append((name[len('Ilustrasi '):], _box(sh)))
        elif sh.shape_type == 13 and name.startswith('Ikon '):
            n_icon += 1
        else:
            if getattr(sh, 'has_chart', False) and sh.has_chart:
                grafis.append('chart')
                if _box(sh)[2] > 8.5:
                    wide = 'chart'
                wide = wide or 'chart-kecil'
            if getattr(sh, 'has_table', False) and sh.has_table and _box(sh)[2] > 8.5:
                wide = 'tabel lebar'
            has_txt = getattr(sh, 'has_text_frame', False) and sh.has_text_frame and sh.text_frame.text.strip()
            if (has_txt or getattr(sh, 'has_table', False) and sh.has_table) and sh is not title_sh:
                others.append((sh.name, _box(sh)))
    visual.append((i, is_cover, ills, n_icon + len(grafis), wide, grafis))
    if is_cover:
        return
    if len(ills) > 1:
        warn(i, f"{len(ills)} ilustrasi dalam satu slide; maksimal satu (§5.16)")
    for nama, b in ills:
        if b[2] > 4.8:
            warn(i, f"ilustrasi \"{nama}\" lebar {b[2]:.1f} in > 4,8 in; muatkan ke kolom kanan dengan fit_illustration")
        if wide in ('chart', 'chart-kecil', 'tabel lebar'):
            warn(i, f"ilustrasi \"{nama}\" di slide yang memuat {wide.replace('-kecil', '')}; ilustrasi tidak dipakai di slide analisis (§5.16)")
        for on, ob in others:
            if _overlap(b, ob) > 0.15:
                warn(i, f"ilustrasi \"{nama}\" menimpa \"{on}\"")


def check_visual_deck(visual, titles):
    isi = [v for v in visual if not v[1]]
    n = len(isi)
    ill_pages = [v[0] for v in isi if v[2]]
    icon_pages = [v[0] for v in isi if v[3] and not v[2]]
    graf = [(v[0], v[5]) for v in isi if v[5]]
    print("== REKAP ASET VISUAL ==")
    print(f"slide isi: {n} · berilustrasi: {len(ill_pages)} (S{','.join(map(str, ill_pages)) or '-'}) · "
          f"beraset visual lain (ikon/grafis/chart): {len(icon_pages)} (S{','.join(map(str, icon_pages)) or '-'})")
    names = defaultdict(list)
    for v in isi:
        for nama, _ in v[2]:
            names[nama].append(v[0])
    if graf:
        print("grafis/chart: " + " · ".join(f"S{i} {'+'.join(sorted(set(g)))}" for i, g in graf))
    if names:
        print("ilustrasi: " + ", ".join(f"{k} (S{','.join(map(str, p))})" for k, p in names.items()))
    print()
    if len(titles) > 10:
        low = [" ".join(t.split()).lower() for t in titles]
        if not any(t.startswith("outline") for t in low):
            warn(0, "deck > 10 slide tanpa slide outline (add_outline)")
    for k, p in names.items():
        if len(p) > 1:
            warn(0, f"ilustrasi \"{k}\" dipakai lebih dari sekali (S{','.join(map(str, p))})")


def check(path):
    prs = Presentation(path)
    ratio = prs.slide_width / prs.slide_height
    if abs(ratio - 16 / 9) > 0.01:
        fail(0, f"kanvas {prs.slide_width/EMU_IN:.2f}x{prs.slide_height/EMU_IN:.2f} in bukan 16:9")
    sw_in = prs.slide_width / EMU_IN

    titles, fonts, off_palette = [], set(), defaultdict(set)
    visual = []   # per slide: (ilustrasi[(nama, box)], jumlah ikon, ada chart/tabel lebar)
    all_colors = set()
    logo_slides = []
    fulltext = []

    for i, slide in enumerate(prs.slides, 1):
        xml = slide._element
        title_sh = find_title(slide)
        title = shape_text(title_sh).strip() if title_sh is not None else ""
        titles.append(title)
        is_cover = i == 1 or (title_sh is not None and title_sh.name in ("Judul pembatas", "Judul penutup", "Judul panel")) \
            or (title_sh is None and i == len(prs.slides))

        if not title:
            (warn if is_cover else fail)(i, "judul tidak ditemukan / kosong")
        else:
            one = " ".join(title.split())
            if title_sh.width:
                ln, cpl = est_lines(title, title_sh.width / EMU_IN, max_font_pt(title_sh) or 22,
                                    title_font(title_sh))
                if len(one) > cpl and "\n" not in title and "\v" not in title and not is_cover:
                    warn(i, f"judul {len(one)} karakter > ±{cpl} per baris tanpa pemisah manual; pecah di jeda makna, cek kata yatim")
            if one.endswith("."):
                warn(i, "judul diakhiri titik")
            if not is_cover:
                cols = title_run_colors(title_sh)
                if len(set(cols)) < 2 and len(one.split()) > 1:
                    warn(i, "judul satu warna; pakai topik warna biru + sub-topik warna hitam "
                            "(mis. \"Latar Belakang\" biru, \"Proyek PLTMG Minahasa\" hitam)")
                elif cols and cols[0] not in TOPIC_COLORS:
                    warn(i, f"warna bagian topik #{cols[0]} bukan biru palet PLN IP "
                            f"({', '.join('#' + c for c in sorted(TOPIC_COLORS))})")

        if title_sh is not None and title_sh.top is not None and not is_cover:
            t_top = title_sh.top / EMU_IN
            for sh in iter_shapes(slide.shapes):
                if sh is title_sh or not (getattr(sh, "has_text_frame", False) and sh.has_text_frame):
                    continue
                txt_s = sh.text_frame.text.strip()
                if not txt_s or sh.top is None or sh.left is None:
                    continue
                if (sh.top / EMU_IN) < t_top - 0.02 and (sh.left / EMU_IN) < sw_in * 0.5 \
                        and len(txt_s) < 30 and max_font_pt(sh) <= 12:
                    warn(i, f"teks kecil di atas judul (\"{txt_s[:25]}\") — kicker tidak dipakai lagi; "
                            f"topik masuk ke judul sebagai bagian biru")
            # Teks kecil tepat di bawah judul (narasi/subjudul) = ciri deck buatan AI. Kesimpulan
            # harus berada di badan slide (add_keterangan / add_keterangan_bawah).
            t_bot = (title_sh.top + title_sh.height) / EMU_IN
            for sh in slide.shapes:
                if sh is title_sh or not (getattr(sh, "has_text_frame", False) and sh.has_text_frame):
                    continue
                txt_s = sh.text_frame.text.strip()
                if not txt_s or sh.top is None or sh.width is None:
                    continue
                if sh.name == "Narasi":         # narasi resmi Template TVV
                    ln_n, _ = est_lines(txt_s, sh.width / EMU_IN, max_font_pt(sh) or 14, "helvetica")
                    if ln_n > 2:
                        warn(i, f"narasi ±{ln_n} baris; ringkas jadi 1–2 baris berangka")
                    continue
                top_in, w_in = sh.top / EMU_IN, sh.width / EMU_IN
                runs = [r for p in sh.text_frame.paragraphs for r in p.runs if r.text.strip()]
                all_bold = runs and all(r.font.bold for r in runs)
                if t_bot - 0.1 <= top_in < t_bot + 0.35 and w_in > sw_in * 0.4 \
                        and max_font_pt(sh) <= 13 and not all_bold:
                    fail(i, f"teks kecil di bawah judul (\"{txt_s[:40]}\") di luar narasi resmi. "
                            f"Pakai add_slide(..., narasi=...) atau pindahkan ke badan slide (add_keterangan)")

        # Baris sumber dan footer teks tidak dipakai (materi internal PLN IP)
        if not is_cover:
            for sh in iter_shapes(slide.shapes):
                if not (getattr(sh, "has_text_frame", False) and sh.has_text_frame):
                    continue
                for p in sh.text_frame.paragraphs:
                    ptxt = "".join(r.text for r in p.runs).strip()
                    if SOURCE_LINE.match(ptxt) and sh.name != "Sumber":
                        warn(i, f"baris sumber \"{ptxt[:40]}\" di luar add_sumber; pakai add_sumber(s, teks)")
                        break
                txt_s = sh.text_frame.text.strip()
                if sh.top is not None and sh.top / EMU_IN > 6.7 and FOOTER_TEXT.search(txt_s):
                    fail(i, f"footer teks \"{txt_s[:40]}\" — tidak dipakai; hapus (nomor halaman saja)")
            if any((sh.name or '') in ('Pesan', 'Narasi') for sh in iter_shapes(slide.shapes)):
                psh = next(sh for sh in iter_shapes(slide.shapes) if (sh.name or '') in ('Pesan', 'Narasi'))
                pesan_pages.append((i, " · ".join("".join(r.text for r in p.runs).strip()
                                                  for p in psh.text_frame.paragraphs if p.runs)))
            else:
                no_pesan.append((i, title))

        logos = find_logos(slide, sw_in)
        if not is_cover:
            logo_slides.append((i, bool(logos) or bg_has_image(slide)))
        check_header(i, title_sh, logos, is_cover)

        check_visual(i, slide, title_sh, is_cover, visual)

        title_bottom = ((title_sh.top + title_sh.height) / EMU_IN) if title_sh is not None and title_sh.top is not None else 1.4

        for sh in iter_shapes(slide.shapes):
            el = sh._element
            geom = el.find(".//" + NS_A + "prstGeom")
            h_in = (sh.height or 0) / EMU_IN
            w_in = (sh.width or 0) / EMU_IN
            top_in = (sh.top or 0) / EMU_IN
            if geom is not None and geom.get("prst") in ROUNDED and h_in >= 0.4:
                fail(i, f"bentuk bersudut bulat ({geom.get('prst')}) \"{sh.name}\"")
            if el.find(".//" + NS_A + "gradFill") is not None:
                fail(i, f"isian gradien pada \"{sh.name}\"")
            if el.find(".//" + NS_A + "outerShdw") is not None:
                warn(i, f"bayangan pada \"{sh.name}\"")
            sppr = el.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}spPr")
            if sppr is not None:
                sf = sppr.find(NS_A + "solidFill")
                fill_val = (sf.find(NS_A + "srgbClr").get("val") if sf is not None and sf.find(NS_A + "srgbClr") is not None else "")
                has_fill = sf is not None and fill_val.upper() != "FFFFFF"      # isian putih = kotak bergaris
                ln = sppr.find(NS_A + "ln")
                ln_clr = ln.find(".//" + NS_A + "srgbClr") if ln is not None else None
                has_line = ln is not None and ln.find(NS_A + "noFill") is None and len(ln) > 0 \
                    and not (ln_clr is not None and ln_clr.get("val", "").upper() == "FFFFFF")   # garis putih = pemisah
                is_line_shape = geom is not None and geom.get("prst") in ("line", "straightConnector1")
                if has_fill and has_line and not is_line_shape:
                    warn(i, f"kotak berisi warna sekaligus bergaris tepi \"{sh.name}\"")
                if is_line_shape or (h_in < 0.06 and w_in > 0.5 and has_fill):
                    if title_bottom - 0.05 <= top_in <= title_bottom + 0.35 and w_in > sw_in * 0.6:
                        warn(i, "garis/pita lebar tepat di bawah judul (dekorasi khas AI); hapus kecuali garis sumbu")
            if geom is not None and geom.get("prst") in ("rect",) and w_in < 0.12 and h_in > 0.8:
                warn(i, f"pita vertikal tipis \"{sh.name}\" (aksen tepi khas AI)")

            for tag in ("srgbClr",):
                for c in el.iter(NS_A + tag):
                    v = (c.get("val") or "").upper()
                    if not v:
                        continue
                    all_colors.add(v)
                    if v not in PALETTE:
                        off_palette[v].add(i)

            if getattr(sh, "has_text_frame", False) and sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    ptxt = "".join(r.text for r in p.runs)
                    if MANUAL_BULLET.match(ptxt) and len(ptxt) > 3:
                        fail(i, f"bullet diketik manual: \"{ptxt[:40]}\" — pakai bullet PowerPoint")
                    for r in p.runs:
                        if r.font.name:
                            fonts.add(r.font.name)
                        if r.font.size and r.font.size.pt < 9 and r.text.strip():
                            warn(i, f"teks {r.font.size.pt:g}pt terlalu kecil: \"{r.text[:30]}\"")
                t = sh.text_frame.text
                fulltext.append((i, t))
            if getattr(sh, "has_table", False) and sh.has_table:
                for row in sh.table.rows:
                    for cell in row.cells:
                        fulltext.append((i, cell.text))
                        for p in cell.text_frame.paragraphs:
                            ptxt = "".join(r.text for r in p.runs)
                            if MANUAL_BULLET.match(ptxt) and len(ptxt) > 3:
                                fail(i, f"bullet diketik manual di tabel: \"{ptxt[:40]}\"")
                        for rpr in cell._tc.iter(NS_A + "rPr"):
                            if rpr.get("sz") and int(rpr.get("sz")) < 1000:
                                warn(i, f"teks tabel {int(rpr.get('sz'))/100:g}pt (<10pt)")
                                break
            for f in el.iter(NS_A + "latin"):
                if f.get("typeface") and not f.get("typeface").startswith("+"):
                    fonts.add(f.get("typeface"))

    # ---- lintas deck ----
    check_visual_deck(visual, titles)
    with_logo = [i for i, has in logo_slides if has]
    without = [i for i, has in logo_slides if not has]
    if with_logo and without:
        warn(0, f"logo ada di S{','.join(map(str, with_logo))} tetapi tidak ada di S{','.join(map(str, without))}")
    for i, t in fulltext:
        if EMOJI.search(t):
            fail(i, f"emoji/simbol dekoratif: \"{t.strip()[:40]}\"")
        if PLACEHOLDER.search(t):
            fail(i, f"placeholder tertinggal: \"{t.strip()[:40]}\"")
        if " — " in t or "—" in t.strip()[1:]:
            warn(i, f"em dash dalam kalimat: \"{t.strip()[:50]}\" — ganti titik/koma/titik dua")
    smell = defaultdict(set)
    low = [(i, t.lower()) for i, t in fulltext]
    for w in AI_SMELL:
        for i, t in low:
            if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", t):
                smell[w].add(i)
    for w, pages in smell.items():
        warn(0, f"kosakata rasa-AI \"{w}\" di S{','.join(map(str, sorted(pages)))}")
    alltext = " ".join(t for _, t in low)
    for a, b in TERM_PAIRS:
        if re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", alltext) and re.search(r"(?<!\w)" + re.escape(b) + r"(?!\w)", alltext):
            warn(0, f"istilah ganda: \"{a}\" dan \"{b}\" sama-sama dipakai; pilih satu")
    if len(fonts) > 2:
        warn(0, f"lebih dari 2 jenis font: {', '.join(sorted(fonts))}")
    lain = sorted(f for f in fonts if f and not f.lower().startswith(("helvetica", "arial")))
    if lain:
        warn(0, f"font selain Helvetica dipakai: {', '.join(lain)} (font korporat PLN IP = Helvetica)")
    for col, pages in sorted(off_palette.items()):
        warn(0, f"warna di luar palet #{col} di S{','.join(map(str, sorted(pages)))}")
    used_brand = {c for c in all_colors if c in PALETTE_PLNIP} | {c for c in all_colors if c in PALETTE_EXTRA}
    if len(used_brand) > 6:
        warn(0, f"{len(used_brand)} warna PLN IP dipakai ({', '.join('#' + c for c in sorted(used_brand))}); "
                f"pedoman menganjurkan 3 warna untuk slide teks/tabel. Lebih dari itu wajar pada chart, "
                f"flowchart, atau diagram yang memang butuh pembeda; pastikan setiap warna punya arti dan legenda")
    seen = defaultdict(list)
    for i, t in enumerate(titles, 1):
        if t:
            seen[" ".join(t.split()).lower()].append(i)
    for t, pages in seen.items():
        if len(pages) > 1:
            warn(0, f"judul sama di S{','.join(map(str, pages))}: \"{t[:50]}\"")
    _FULLTEXT[:] = fulltext
    _GRAF[:] = [v[0] for v in visual if v[5] and not v[1]]
    return titles


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    titles = check(sys.argv[1])
    print("== DAFTAR JUDUL (baca berurutan: apakah membentuk satu cerita?) ==")
    for i, t in enumerate(titles, 1):
        print(f"{i:>2}. {' / '.join(x.strip() for x in t.splitlines()) if t else '(tanpa judul)'}")
    print()
    if pesan_pages:
        print("== KETERANGAN PER SLIDE (add_keterangan / add_keterangan_bawah) ==")
        for i, t in pesan_pages:
            print(f"S{i:>2}. {t[:140]}")
        print()
    for w, eng in UNCOMMON_ID.items():
        pages = sorted({i for i, t in _FULLTEXT if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", t.lower())})
        if pages:
            warn(0, f"istilah Indonesia tak umum \"{w}\" di S{','.join(map(str, pages))}; pakai \"{eng}\"")
    heads = sorted({i for i, t in _FULLTEXT if IMPLIKASI_HEAD.match(t.strip())})
    if heads:
        warn(0, f"judul kolom implikasi/kesimpulan di S{','.join(map(str, heads))}; teks pendamping cukup "
                f"menjelaskan singkat apa yang ditampilkan grafis, kecuali user memang memberi/meminta kesimpulan")
    lacking = [i for i, t in no_pesan if i in _GRAF]      # hanya slide bergrafis/chart
    if lacking:
        warn(0, f"slide bergrafis/chart tanpa keterangan di badan slide: S{','.join(map(str, lacking))}. Tambahkan penjelasan "
                f"singkat apa yang ditampilkan grafis/chart/gambar (add_keterangan / add_keterangan_bawah), "
                f"kecuali isinya sudah teks yang menjelaskan diri sendiri (mis. ringkasan eksekutif)")
    for w in warns:
        print("WARN ", w)
    for f in fails:
        print("FAIL ", f)
    print(f"\n{len(fails)} FAIL / {len(warns)} WARN")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
