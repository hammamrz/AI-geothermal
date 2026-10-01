#!/usr/bin/env python3
"""svg_render.py: ubah SVG (ikon/ilustrasi) menjadi PNG transparan dengan warna yang diminta.

Skill ini hanya menyimpan SVG. PNG dibuat saat deck dibangun lalu disimpan di cache
(/tmp/plnip-svg), jadi mewarnai ulang cukup dengan mengganti argumen, tanpa menyimpan file baru.

Dipakai oleh plnip_deck.py (import) dan plnip-theme.js (CLI):
  python3 svg_render.py --cari kontrak tanda tangan     -> daftar nama ilustrasi yang cocok
  python3 svg_render.py <file.svg | nama> [--width 1400] [--color 008AAC] [--map 3f3d56=05365B,...] [--undraw]
  -> mencetak path PNG hasil ke stdout

--color  : mengganti `currentColor` (warna garis ikon Tabler, warna aksen unDraw)
--map    : ganti warna hex tertentu, format lama=baru dipisah koma
--undraw : terapkan pemetaan palet PLN IP untuk ilustrasi unDraw (abu gelap -> DARK, abu muda -> LIGHT)

Mesin render dicoba berurutan: cairosvg, sharp (Node), rsvg-convert, ImageMagick.
"""
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CACHE = os.environ.get('PLNIP_SVG_CACHE', os.path.join(tempfile.gettempdir(), 'plnip-svg'))

PRIMARY, DARK, TINT, LIGHT = '008AAC', '05365B', 'D1EDF3', 'E6EEF2'

A4 = '29537B'

# Warna bawaan unDraw -> palet PLN IP. Warna kulit dibiarkan asli.
UNDRAW_MAP = {c: DARK for c in ['3f3d56', '2f2e41', '090814', '3f3d58', '2f2e43', '535461',
                                  '2e2e43', '3a3768', '444053', '231f20', '010001', '010102', '0f0f10']}
UNDRAW_MAP.update({c: LIGHT for c in ['e6e6e6', 'f2f2f2', 'f0f0f0', 'e4e4e4', 'cacaca', 'cbcbcb',
                                      'dedfe0', 'd6d6e3', 'dedede', 'e5e5e5', 'f1f1f1', 'd0cde1',
                                      'b6b3c5', 'e6e8ec', 'e2e3e4', 'e0e0e0', 'd7d7d8', 'e6e7e8', 'fafafa']})
UNDRAW_MAP.update({c: A4 for c in ['ff6584', 'ff6884', 'fd6584', 'ff6582', 'ff6363', '575a89']})   # aksen kedua (merah muda)

HERE = os.path.dirname(os.path.abspath(__file__))
ILL_DIR = os.path.join(HERE, 'illustrations', 'svg')
BUNDLE = os.path.join(HERE, 'illustrations', 'undraw-pustaka.json')
_bundle = None


def pustaka():
    """Isi undraw-pustaka.json: {slug: {judul, kata, tema, rasio, svg}}. Dimuat sekali."""
    global _bundle
    if _bundle is None:
        _bundle = {}
        if os.path.exists(BUNDLE):
            with open(BUNDLE, encoding='utf-8') as f:
                _bundle = json.load(f)['ilustrasi']
    return _bundle


def semua_nama():
    flat = sorted(f[:-4] for f in os.listdir(ILL_DIR) if f.endswith('.svg')) if os.path.isdir(ILL_DIR) else []
    return flat + sorted(pustaka())


def resolve_illustration(nama):
    """Path SVG untuk nama ilustrasi: dulu assets/illustrations/svg/<nama>.svg (11 flat),
    lalu undraw-pustaka.json (diekstrak sekali ke cache)."""
    p = os.path.join(ILL_DIR, nama + '.svg')
    if os.path.exists(p):
        return p
    b = pustaka()
    if nama in b:
        d = os.path.join(CACHE, 'src')
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, nama + '.svg')
        if not os.path.exists(out):
            with open(out, 'w', encoding='utf-8') as f:
                f.write(b[nama]['svg'])
        return out
    mirip = difflib.get_close_matches(nama, semua_nama(), n=5, cutoff=0.5)
    raise FileNotFoundError('Ilustrasi tidak ada: %s. Mungkin maksudnya: %s. Cari dengan '
                            'cari_ilustrasi(\'kata\') atau python3 svg_render.py --cari kata'
                            % (nama, ', '.join(mirip) or '-'))


# 11 ilustrasi flat buatan skill (folder svg/) dengan kata kunci agar ikut ditemukan cari()
FLAT_META = {
    'plts': 'solar panel pv surya energi renewable', 'pltb': 'wind turbine angin bayu renewable',
    'pltu': 'coal thermal power plant uap batubara cooling tower', 'plta': 'hydro dam air bendungan',
    'bess': 'battery storage baterai energy', 'pipa-gas': 'gas pipeline tank lng',
    'transmisi': 'transmission tower grid jaringan listrik', 'kota-jaringan': 'city demand kota beban',
    'alur-tahapan': 'steps process tahapan alur', 'grafik-abstrak': 'chart growth grafik kinerja',
    'pola-titik': 'dots pattern pola',
}


def cari(kata, n=15):
    """Cari ilustrasi (11 flat + pustaka unDraw) berdasarkan slug, judul, kata kunci, dan tema.
    Kata dicocokkan di awal kata ('sign' cocok dengan 'signed', tidak dengan 'design').
    Hasil diurutkan menurut jumlah kecocokan; kecocokan di nama file bernilai dua."""
    q = [w for w in re.split(r'[\s,]+', kata.lower()) if w]
    sumber = [(slug, slug.replace('-', ' ') + ' ' + ket) for slug, ket in FLAT_META.items()]
    sumber += [(slug, ' '.join([slug.replace('-', ' '), it['judul'].lower(), ' '.join(it['kata']).lower(),
                                ' '.join(it['tema']).lower()])) for slug, it in pustaka().items()]
    hasil = []
    for slug, teks in sumber:
        skor = 0
        for w in q:
            pola = r'(?<![a-z])' + re.escape(w)
            if re.search(pola, slug.replace('-', ' ')):
                skor += 2
            elif re.search(pola, teks):
                skor += 1
        if skor:
            hasil.append((-skor, slug))
    return [s for _, s in sorted(hasil)[:n]]


VARIANTS = {'primary': PRIMARY, 'dark': DARK, 'white': 'FFFFFF', 'tint': TINT}


def _hex(c):
    """Terima '008AAC', '#008AAC', nama varian, atau RGBColor python-pptx."""
    if c is None:
        return None
    c = str(c)
    if c.lower() in VARIANTS:
        return VARIANTS[c.lower()]
    c = c.lstrip('#').upper()
    if not re.fullmatch(r'[0-9A-F]{6}', c):
        raise ValueError('Warna harus hex 6 digit atau salah satu dari %s: %r' % (list(VARIANTS), c))
    return c


def recolor(svg, color=None, mapping=None):
    if color:
        svg = svg.replace('currentColor', '#' + color)
        # SVG tanpa currentColor tapi dengan atribut color= di root
        svg = re.sub(r'(<svg\b[^>]*?)\scolor="[^"]*"', r'\1', svg, count=1)
    for old, new in (mapping or {}).items():
        svg = re.sub('#' + re.escape(old.lstrip('#')), '#' + new.lstrip('#'), svg, flags=re.I)
    return svg


def _render(svg_text, out, width):
    tmp = out + '.src.svg'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(svg_text)
    errors = []
    try:
        try:
            import cairosvg
            cairosvg.svg2png(bytestring=svg_text.encode('utf-8'), write_to=out, output_width=width)
            return
        except ImportError:
            errors.append('cairosvg tidak terpasang')
        except Exception as e:
            errors.append('cairosvg: %s' % e)
        if shutil.which('node'):
            js = ("const s=require('sharp');s(process.argv[1],{density:300}).resize({width:+process.argv[3]})"
                  ".png().toFile(process.argv[2]).catch(e=>{console.error(e.message);process.exit(1)})")
            r = subprocess.run(['node', '-e', js, tmp, out, str(width)], capture_output=True, text=True)
            if r.returncode == 0 and os.path.exists(out):
                return
            errors.append('sharp: %s' % (r.stderr.strip()[:200] or 'gagal'))
        if shutil.which('rsvg-convert'):
            r = subprocess.run(['rsvg-convert', '-w', str(width), '-o', out, tmp], capture_output=True, text=True)
            if r.returncode == 0:
                return
            errors.append('rsvg-convert: %s' % r.stderr.strip()[:200])
        conv = shutil.which('magick') or shutil.which('convert')
        if conv:
            r = subprocess.run([conv, '-background', 'none', '-density', '300', tmp, '-resize', str(width), out],
                               capture_output=True, text=True)
            if r.returncode == 0:
                return
            errors.append('imagemagick: %s' % r.stderr.strip()[:200])
        raise RuntimeError('Tidak bisa merender SVG. Pasang salah satu: '
                           '`pip install cairosvg --break-system-packages` atau `npm i sharp`. '
                           'Detail: ' + '; '.join(errors))
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def svg_to_png(svg_path, width=1400, color=None, mapping=None, undraw=False):
    """Kembalikan path PNG (di cache) untuk SVG dengan warna yang diminta.
    svg_path boleh path file atau nama ilustrasi (dicari di folder svg lalu di pustaka unDraw)."""
    if not os.path.exists(svg_path) and not svg_path.endswith('.svg'):
        svg_path = resolve_illustration(svg_path)
    if not os.path.exists(svg_path):
        raise FileNotFoundError(svg_path)
    color = _hex(color)
    m = dict(UNDRAW_MAP) if undraw else {}
    for k, v in (mapping or {}).items():
        m[_hex(k).lower()] = _hex(v)
    with open(svg_path, encoding='utf-8') as f:
        src = f.read()
    svg = recolor(src, color, m)
    key = hashlib.sha1((svg + str(width)).encode('utf-8')).hexdigest()[:12]
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, '%s-%s.png' % (os.path.splitext(os.path.basename(svg_path))[0], key))
    if not os.path.exists(out):
        _render(svg, out, width)
    return out


def _main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    if argv and argv[0] == '--cari':
        for slug in cari(' '.join(argv[1:]), n=30):
            it = pustaka().get(slug)
            print('%-32s %s' % (slug, ('%s  [%s]' % (it['judul'], ', '.join(it['tema']))) if it
                                else '(flat, buatan skill)'))
        return
    ap.add_argument('svg', help='file .svg atau nama ilustrasi')
    ap.add_argument('--width', type=int, default=1400)
    ap.add_argument('--color')
    ap.add_argument('--map', default='')
    ap.add_argument('--undraw', action='store_true')
    a = ap.parse_args(argv)
    mapping = dict(p.split('=', 1) for p in a.map.split(',') if '=' in p)
    print(svg_to_png(a.svg, a.width, a.color, mapping, a.undraw))


if __name__ == '__main__':
    _main(sys.argv[1:])
