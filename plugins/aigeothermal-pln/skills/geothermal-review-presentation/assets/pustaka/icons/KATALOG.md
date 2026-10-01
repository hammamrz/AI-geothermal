# Katalog ikon

63 ikon garis (stroke) seragam, hasil kurasi dari **Tabler Icons** (lisensi MIT) lalu diwarnai ulang ke palet PLN IP.

**Bentuk file**
- `svg/<nama>.svg` — satu-satunya bentuk yang disimpan. Garis memakai `currentColor`, jadi warnanya
  ditentukan saat dipakai; helper merendernya ke PNG transparan 256 px lewat `assets/svg_render.py`.
- Varian: `primary` (`#008AAC`, di atas latar putih), `dark` (`#05365B`, di atas TINT atau saat ikon
  harus lebih tenang), `white` (HANYA di dalam lingkaran/kotak berisi warna), `tint`, atau hex apa pun.

**Cara pakai (helper di `plnip-theme.js`)**
```js
T.addIcon(slide, 'plts', { x: 0.5, y: 2.0, size: 0.34 });            // ikon polos (primary)
T.addIcon(slide, 'plts', { x: 0.5, y: 2.0, variant: 'dark' });       // varian lain / hex
T.addIconBadge(slide, pres, 'bess', { x: 0.5, y: 2.0, d: 0.6 });      // lingkaran PRIMARY + ikon putih
T.addIconList(slide, pres, [                                          // daftar butir berikon
  { icon: 'plts', text: 'Kapasitas PLTS bertambah 120 MW pada 2027' },
  { icon: 'bess', text: 'BESS 40 MWh menyerap kelebihan produksi siang' },
], { x: 0.5, y: 2.0, w: 6.6 });
```

**Aturan pakai** (rinci di `references/aturan-slide.md` §5.15)
- Dua pemakaian: daftar 3–5 butir setara (`add_icon_list`), dan kolom sumbu tabel kualitatif 3–7 baris
  (`add_axis_table(..., row_icons=['regulasi', 'lokasi', 'biaya'])`).
- Satu slide, satu ukuran ikon dan satu gaya (semua polos, atau semua dalam lingkaran).
- Ikon tidak menggantikan data: slide analisis tetap memakai tabel atau chart. Tidak di sel isi tabel atau judul kolom.
- Satu ikon untuk satu makna dalam satu slide. Jangan mencampur ikon dari sumber lain; garisnya akan beda tebal.

## Daftar nama


### Energi & pembangkitan

| nama | ikon sumber (Tabler) |
|---|---|
| `air` | droplet |
| `beban-listrik` | plug |
| `bess` | battery-charging |
| `daur-ulang` | recycle |
| `ebt` | leaf |
| `gas` | flame |
| `keberlanjutan` | plant-2 |
| `kinerja` | gauge |
| `listrik` | bolt |
| `mesin` | engine |
| `pembangkit` | building-factory-2 |
| `pltb` | windmill |
| `plts` | solar-panel-2 |
| `transmisi` | building-broadcast-tower |

### Organisasi & orang

| nama | ikon sumber (Tabler) |
|---|---|
| `bisnis` | briefcase |
| `global` | world |
| `kemitraan` | heart-handshake |
| `masyarakat` | building-community |
| `penanggung-jawab` | user-check |
| `sistem` | network |
| `struktur-organisasi` | sitemap |
| `tim` | users-group |

### Data & analisis

| nama | ikon sumber (Tabler) |
|---|---|
| `grafik-batang` | chart-bar |
| `grafik-garis` | chart-line |
| `grafik-pai` | chart-pie |
| `grafik-sebar` | chart-dots |
| `kajian` | search |
| `laporan` | report-analytics |
| `pemantauan` | eye |
| `tabel` | table |
| `tren-naik` | trending-up |
| `tren-turun` | trending-down |

### Keuangan

| nama | ikon sumber (Tabler) |
|---|---|
| `anggaran` | wallet |
| `biaya` | coins |
| `investasi` | businessplan |
| `kas` | cash |
| `pendanaan` | building-bank |
| `perhitungan` | calculator |
| `persentase` | percentage |
| `regulasi` | scale |
| `tagihan` | receipt |

### Proyek & waktu

| nama | ikon sumber (Tabler) |
|---|---|
| `daftar-periksa` | checklist |
| `dokumen` | file-text |
| `durasi` | hourglass-high |
| `jadwal` | calendar-stats |
| `lokasi` | map-pin |
| `milestone` | flag |
| `paparan` | presentation |
| `percepatan` | rocket |
| `persetujuan` | clipboard-check |
| `pertukaran` | arrows-exchange |
| `peta-jalan` | route |
| `portofolio` | stack-2 |
| `siklus` | refresh |
| `surat` | mail |
| `target` | target-arrow |
| `waktu` | clock-hour-4 |

### Risiko & operasi

| nama | ikon sumber (Tabler) |
|---|---|
| `ide` | bulb |
| `keamanan` | lock |
| `mitigasi` | shield-check |
| `operasi` | settings |
| `pemeliharaan` | tools |
| `risiko` | alert-triangle |
