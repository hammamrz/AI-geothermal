---
name: geothermal-review-presentation
description: Buat presentasi PPTX technical review geothermal dengan master PLN IP: data eksisting, komentar review, langkah penyelesaian, risiko, data gap, dan sumber.
---

# Geothermal Review Presentation

Gunakan skill ini ketika pengguna meminta hasil review geothermal dalam bentuk **PowerPoint/PPT/PPTX**, bahan paparan, technical review deck, comment review presentation, checkpoint presentation, atau management review.

## Gaya bahasa (wajib)

Sebelum menulis jawaban, tabel, laporan, atau slide, baca `../geothermal-knowledge/references/GAYA_BAHASA.md` dan ikuti aturannya. Ringkasnya:
- Gunakan bahasa Indonesia baku yang natural, seperti laporan resmi seorang *engineer* senior. Jangan menyusun kalimat dengan pola terjemahan kata demi kata dari bahasa Inggris.
- Istilah Inggris yang padanannya kurang pas tetap dipakai dan **dicetak miring** dengan `*istilah*` (mis. *shut-in*, *casing*, *siting*, *reservoir engineer*, *data gap*). Akronim, nama dokumen, dan kata serapan baku tidak dimiringkan.
- Pakai padanan Indonesia yang lazim bila tepat: sumur (bukan *well*), pemboran, temuan, ahli geokimia.
- Nada lugas dan profesional, tanpa frasa pengisi ("Tentu!", "Berikut adalah …", "Penting untuk dicatat …").
- Contoh: "Apabila hasil ini digunakan sebagai dasar penentuan lokasi (*siting*) atau perencanaan sumur, perlu dilakukan verifikasi oleh ahli geokimia dan *reservoir engineer*."

## Prinsip utama

PowerPoint harus menjadi **versi presentasi dari technical review report**, bukan storyline yang berbeda.

Gunakan struktur formal dari `../geothermal-comment-sheet-report/references/REPORT_STRUCTURE.md` (bila skill diinstal terpisah sebagai ZIP, salinannya ada di `references/REPORT_STRUCTURE.md`) sebagai backbone review, lalu baca `references/TECHNICAL_REVIEW_PPT_STRUCTURE.md` untuk pemetaan ke slide.

Tujuannya:
1. audiens langsung tahu apa yang diperiksa dan basis review-nya;
2. setiap finding tetap traceable dan actionable;
3. setiap item review tampil berurutan: **data eksisting → komentar review → langkah penyelesaian**;
4. cross-discipline risk dan data gap tetap terlihat, tanpa status atau persentase penyelesaian kajian;
5. deck tetap ringkas dan cocok dipresentasikan.

## Sumber konten

1. Untuk technical findings, jalankan/ikuti `geothermal-review`.
2. Untuk evidence dari embedded knowledge base, route melalui `geothermal-knowledge`.
3. Untuk struktur report formal, selaraskan dengan `geothermal-comment-sheet-report`.
4. Jangan melakukan full-KB read hanya karena output-nya PowerPoint.
5. Deck adalah representasi hasil review, bukan kesempatan menambahkan klaim baru.

## Master yang wajib digunakan

Baca `references/PLN_IP_LITE_STYLE.md`.

Gunakan **hanya tiga** background master yang dibundel:
- `references/master_assets/MASTER_COVER.jpg`
- `references/master_assets/MASTER_CONTENT.jpg`
- `references/master_assets/MASTER_CLOSING.jpg`

`references/PLN_IP_GEOTHERMAL_3_SLIDE_MASTER_REFERENCE.pptx` berisi preview 3 layout tersebut.

Aturan:
- slide pertama = COVER;
- semua slide isi = CONTENT yang sama;
- slide terakhir = CLOSING / Terima Kasih;
- jangan memuat atau menyalin master lain dari `skill-pptplnip`;
- semua teks, tabel, shape, diagram, dan chart review tetap editable di atas background master;
- model grafis dan tabel diambil dari pustaka `assets/pustaka/` (salinan dari skill presentasi-pln-ip dan presentasi-tvv tanpa master dan ilustrasi unDraw), diletakkan di atas master geothermal ini.

## Struktur deck default

Default: **Technical Review Presentation**, umumnya 11–16 slide termasuk penutup, tergantung jumlah finding material.

Urutan yang digunakan:
1. Cover
2. Executive Review Summary
3. Review Structure / Agenda
4. Review Control & Revision, bila metadata tersedia dan berguna
5. Objectives, Scope & Review Basis
6. Documents Reviewed
7. Review Methodology & Comment Classification
8. Sebaran Temuan per Disiplin dan Prioritas
9. Item Review: Data Eksisting dan Komentar Review
10. Rincian per item review (data eksisting, komentar review, langkah penyelesaian), satu slide per item
11. Key Risks & Cross-Discipline Interfaces
12. Data Gap dan langkah untuk melengkapinya
13. Langkah Penyelesaian per Item Review
14. Kesimpulan dan Langkah Selanjutnya
15. Sources Used & Review Traceability
16. Terima Kasih

Jangan memaksa slide kosong. Bagian tanpa data boleh digabung, ditandai `Not provided`, atau dihilangkan jika tidak material.

### Pemetaan elemen Word yang tidak perlu disalin literal

- `Table of Contents` → `Review Structure / Agenda`.
- `List of Figures` dan `List of Tables` → tidak perlu slide khusus; caption dan source langsung pada visual/tabel yang digunakan.
- `Document Control / Revision History` → satu slide `Review Control & Revision` bila metadata tersedia.
- Lampiran rinci → hanya source traceability atau finding tambahan yang memang diperlukan untuk keputusan.

## Executive Review Summary

Ringkas minimal:
- jumlah item review;
- jumlah prioritas tinggi;
- jumlah *data gap*;
- jumlah langkah penyelesaian yang diusulkan;
- 3–5 pesan utama;
- rekomendasi kajian (`overall_status`) jika sudah dapat dinyatakan dari bukti.

Jangan menampilkan status atau persentase penyelesaian (mis. "0 dari 12 selesai").

Jangan menampilkan status approval yang tidak didukung evidence/governance.

## Objectives, Scope & Review Basis

Tampilkan:
- tujuan review;
- review stage/gate bila ada;
- included dan excluded scope;
- assumptions / limitations;
- review basis dan reference yang benar-benar digunakan.

## Documents Reviewed

Buat register ringkas dengan field:
- title;
- document number/code;
- revision;
- date;
- discipline;
- review scope.

Bila banyak dokumen, tampilkan dokumen utama pada slide dan sisanya di appendix/source traceability.

## Review Methodology & Comment Classification

Jelaskan secara ringkas:
- evidence-based review;
- retrieval/selective embedded-KB usage;
- cross-check text, table, figure, and calculation consistency;
- priority/severity definitions;
- struktur item review: data eksisting → komentar review → langkah penyelesaian.

Jangan mengklaim standard/comparator digunakan jika sumber tersebut tidak benar-benar dibuka.

## Item Review: Data Eksisting dan Komentar Review

Tabel ringkas dengan kolom berurutan:
- ID;
- disiplin;
- data eksisting (dan lokasinya di dokumen);
- komentar review;
- prioritas.

## Rincian per item review

Setiap item material mendapat satu slide dengan urutan baca yang tetap:
- baris identitas: disiplin, prioritas, tingkat keyakinan (opsional), lokasi di dokumen;
- **Data eksisting** (`existing`): apa yang tertulis atau tersedia di dokumen, apa adanya (angka, satuan, asumsi, metode). Bila tidak ada, tulis "Tidak tersedia di dokumen". Jangan memasukkan penilaian di sini;
- **Komentar review** (`finding`, ditambah `comment`): penilaian reviewer atas data eksisting itu;
- dampak bila tidak diselesaikan;
- **Langkah penyelesaian** (`resolution_steps`): langkah konkret bernomor (penomoran otomatis PowerPoint), masing-masing diawali kata kerja tindakan, menyebut objek spesifik, dan menghasilkan keluaran yang bisa diperiksa. PIC, target, dan bukti ditulis hanya bila diketahui;
- dasar teknis dan satu baris sumber (KB ID + halaman).

Item yang menurut reviewer sudah memadai cukup diberi komentar "tidak ada tindakan"; generator akan menulis "Tidak ada langkah yang diperlukan".

Jika ada visual penting, prioritaskan satu gambar/diagram besar yang terbaca daripada banyak thumbnail.

## Key Risks & Cross-Discipline Interfaces

Jangan sekadar mengulang findings. Gunakan bagian ini untuk menghubungkan isu lintas disiplin, misalnya:
- resource confirmation vs development capacity;
- well deliverability vs plant staging;
- chemistry vs scaling/corrosion dan material selection;
- reservoir model vs well targeting;
- drilling design vs subsurface uncertainty;
- well integrity vs operating envelope;
- reinjection strategy vs reservoir sustainability.

Tampilkan hubungan `driver → interface → consequence / decision` bila memungkinkan.

## Data Gaps, Clarifications & Assumptions

Field minimum:
- Gap ID;
- missing/unclear data;
- impact if unresolved;
- langkah untuk melengkapi (`resolution_steps`, atau `required` yang ditampilkan sebagai "Sediakan …");
- PIC bila diketahui.

Data yang belum tersedia tidak boleh dikonversi menjadi finding definitif.

## Langkah Penyelesaian per Item Review

Tabel per item, diurutkan dari prioritas tertinggi: ID, item review, langkah penyelesaian bernomor, PIC, target, dan bukti penyelesaian. Kolom yang tidak diketahui diisi "—", bukan tebakan. `actions` (format lama) tetap diterima dan dipakai untuk item yang tidak punya `resolution_steps`.

Pastikan setiap item material punya langkah penyelesaian yang konkret. Hindari langkah kabur seperti "perlu dikaji lebih lanjut".

## Kesimpulan dan Langkah Selanjutnya

Tampilkan:
- kesimpulan atas dokumen yang dikaji;
- rekomendasi kajian (`overall_status`), misalnya "Perlu revisi" atau "Dapat dilanjutkan setelah langkah prioritas tinggi diselesaikan", tanpa mengarang persetujuan teknis;
- 3–5 langkah selanjutnya yang berurutan (`next_steps`, alias `conditions_to_proceed`). Bila kosong, generator mengambil langkah pertama dari item prioritas tertinggi;
- keterbatasan kesimpulan kajian.

Jangan menampilkan bar progres, status, atau persentase penyelesaian kajian.

## Framework visual (dari skill presentasi-pln-ip dan presentasi-tvv)

Deck mengikuti framework konsultan PLN IP. Aturan lengkap ada di `references/aturan-slide.md`, `references/aturan-tvv.md`, dan `references/pedoman-plnip.md`. Katalog pola slide dan model grafis ("kapan dipakai / kapan jangan") ada di `references/pola-layout.md`, dengan bentuk visualnya di `references/galeri/galeri-grafis-plnip.jpg` dan `references/galeri/galeri-tvv.jpg`.

Aturan inti:
- **Judul dua warna**: topik biru `#008AAC` + sub-topik hitam, satu baris (maksimal dua), tanpa titik. Tidak ada label kecil (*kicker*) di atas judul dan tidak ada garis aksen di bawahnya.
- **Satu slide, satu pesan.** Isi disusun kiri → kanan: grafis/data di kiri, keterangan atau isi pendamping di kanan.
- **Keterangan grafis** berisi penjelasan singkat apa yang ditampilkan dan cara membacanya (arti warna, satuan, periode). Jangan menambah implikasi atau "*so what*" yang tidak didukung hasil review.
- **Tabel bersumbu**: baris = item, kolom = aspek. Kolom pertama tebal, header bergaris bawah biru, tanpa zebra. Sel kosong diisi "—" berlatar biru muda. Daftar langkah di dalam sel memakai penomoran otomatis PowerPoint.
- **Dilarang**: sudut membulat, bayangan, gradien, deretan kartu berwarna, emoji/simbol dekoratif (✅ ⏳ ↔), dan pita warna di tepi kotak.
- **Palet PLN IP**: PRIMARY `#008AAC`, DARK `#05365B`, TINT `#D1EDF3`, abu `#4D4D4D`/`#C0C0C0`. Warna tingkat risiko hanya untuk matriks risiko.
- **Satu baris sumber** (gaya TVV) boleh dipakai di slide yang memuat bukti teknis, misalnya rincian temuan.

### Model grafis untuk kebutuhan review

| Kebutuhan pada deck review | Model | Helper |
|---|---|---|
| Angka kunci di ringkasan (item review, prioritas tinggi, *data gap*, langkah penyelesaian) | Deret angka kunci tanpa kartu | `G.add_kpi_row` |
| Tahapan metodologi review | Alur proses | `G.add_flow` |
| Sebaran temuan per disiplin dan prioritas | Chart batang bertumpuk | `G.add_stacked_chart` |
| Daftar item review, *data gap*, langkah penyelesaian | Tabel bersumbu | `T.add_tabel` |
| Risiko dengan kemungkinan × dampak (skala 1–5) | Matriks risiko 5×5 | `T.add_matriks_risiko` |
| Langkah penyelesaian yang sudah bertanggal | *Gantt* / *timeline* | `G.add_gantt`, `G.add_timeline` |
| Tahapan proyek berpintu (FEED, pemboran, uji produksi) | *Stage-gate* | `G.add_stage_gate` |
| Proses lintas pihak (operator, kontraktor, regulator) | *Swimlane* | `G.add_swimlane` |
| Akar masalah suatu temuan | *Issue tree* | `G.add_issue_tree` |
| Prioritas temuan dua sumbu (dampak × kemudahan) | Matriks 2×2 | `G.add_matrix_2x2` |
| Penilaian kualitatif per aspek | *Harvey table* | `G.add_harvey_table` |
| Lokasi sumur/wilayah kerja | Peta Indonesia | `G.add_map` |
| Gambar bukti (render halaman KB, skema sumur) | Gambar dimuat proporsional | `T.fit_picture` |

Semua model dibangun dari bentuk dan chart asli PowerPoint, sehingga tetap bisa diedit.

## Judul slide

Judul memakai format **topik + sub-topik**, misalnya `Item Review` `Data Eksisting dan Komentar Review`, atau `F-001` `Beban termal *production casing* belum dihitung untuk kondisi *shut-in*`. Untuk slide rincian temuan, sub-topik berisi inti temuan. Jangan membuat judul lebih tegas daripada bukti yang tersedia.

## Data integrity

- Pertahankan MD/TVD/TVDSS, satuan, datum, basis temperatur/tekanan, kondisi statis/dinamis, dan revisi.
- Jangan mengubah angka untuk membuat chart terlihat rapi.
- Jika acuan pembanding tidak berlaku atau bukti lemah, tampilkan sebagai klarifikasi/*data gap*, bukan ketidaksesuaian.
- PIC, tanggal target, dan bukti penyelesaian jangan diisi dengan tebakan.

## Pembuatan PPTX

Utamakan output **editable PPTX**.

1. Susun JSON hasil review (format di docstring `scripts/build_review_ppt.py`), lalu jalankan:
   ```bash
   python scripts/build_review_ppt.py review.json output.pptx
   ```
   Generator sudah memakai master geothermal dan pustaka grafis di atas. Teks mendukung `*miring*` dan `**tebal**`. Untuk matriks risiko 5×5, isi `likelihood` dan `severity` (1–5) pada `key_risks`.
2. Untuk slide tambahan yang tidak dibuat generator (mis. *gantt* langkah penyelesaian, *stage-gate*, peta lokasi), tulis fungsi kecil dan berikan ke `build(..., extra=...)`; slide akan disisipkan sebelum kesimpulan:
   ```python
   import json, sys; sys.path.insert(0, 'scripts')
   import build_review_ppt as B          # sekaligus memuat pustaka: B.P, B.G, B.T

   def tambahan(prs, data):
       s = B.content_slide(prs, 'Langkah Penyelesaian', 'Jadwal Pelaksanaan')
       B.G.add_gantt(s, periode, baris, B.L, B.BODY_TOP, B.CW)
       B.caption(s, 'Batang menunjukkan rentang waktu tiap langkah; garis tegak = hari ini.')

   B.build(json.load(open('review.json')), 'output.pptx', extra=tambahan)
   ```
   Lihat docstring tiap fungsi di `assets/pustaka/plnip_grafis.py` dan `tvv_deck.py` untuk parameternya. Ikon dari `assets/pustaka/icons/` memerlukan `cairosvg` (`pip install cairosvg`). Bila tidak tersedia, jangan memakai ikon.
3. Jangan memasukkan seluruh dokumen sumber ke JSON. Masukkan hanya hasil review dan bukti yang benar-benar dipakai.

## Quality check

1. Jalankan `python scripts/check_deck.py output.pptx` sampai **0 FAIL** (pemeriksa dari skill presentasi-tvv). Baca setiap WARN dan perbaiki kecuali disengaja. Peringatan "tanpa slide outline" dan "judul tidak ditemukan" pada slide penutup boleh diabaikan.
2. Render setiap slide menjadi gambar dan periksa:
   - logo Danantara + PLN IP tidak tertutup;
   - teks tidak terpotong atau bertumpuk;
   - langkah bernomor di dalam sel rata dan terbaca;
   - label chart terbaca;
   - tidak ada setengah slide yang kosong tanpa alasan.
3. Periksa isi:
   - urutan slide konsisten dengan laporan review;
   - setiap item tampil berurutan: data eksisting, komentar review, langkah penyelesaian;
   - prioritas dan tingkat keyakinan tidak tertukar;
   - setiap klaim teknis material punya lokasi sumber;
   - risiko lintas disiplin bukan sekadar mengulang temuan;
   - setiap item material punya langkah penyelesaian yang konkret atau *data gap* yang jelas;
   - angka, satuan, dan tanggal sesuai sumber;
   - daftar sumber hanya berisi sumber yang benar-benar dipakai;
   - tidak ada status atau persentase penyelesaian kajian, dan rekomendasi kajian tidak melampaui kewenangan atau bukti;
   - slide penutup Terima Kasih berada paling akhir.
