---
name: geothermal-review-presentation
description: Buat presentasi PPTX technical review geothermal dengan 3-layout master PLN IP: ringkasan, temuan, risiko lintas disiplin, data gap, action plan, closeout, dan sumber.
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
3. cross-discipline risk, data gap, action, dan closeout status tetap terlihat;
4. deck tetap ringkas dan cocok dipresentasikan.

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
8. Findings Overview
9. Material Findings & Reviewer Comments, satu atau beberapa slide
10. Key Risks & Cross-Discipline Interfaces
11. Data Gaps, Clarifications & Assumptions
12. Action Plan & Comment Resolution
13. Conclusion & Closeout Status
14. Sources Used & Review Traceability
15. Terima Kasih

Jangan memaksa slide kosong. Bagian tanpa data boleh digabung, ditandai `Not provided`, atau dihilangkan jika tidak material.

### Pemetaan elemen Word yang tidak perlu disalin literal

- `Table of Contents` → `Review Structure / Agenda`.
- `List of Figures` dan `List of Tables` → tidak perlu slide khusus; caption dan source langsung pada visual/tabel yang digunakan.
- `Document Control / Revision History` → satu slide `Review Control & Revision` bila metadata tersedia.
- Lampiran rinci → hanya source traceability atau finding tambahan yang memang diperlukan untuk keputusan.

## Executive Review Summary

Ringkas minimal:
- total findings;
- jumlah High / Medium atau priority lain yang digunakan;
- jumlah open findings;
- jumlah data gaps;
- 3–5 pesan utama;
- overall closeout status jika sudah dapat dinyatakan dari evidence.

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
- review scope/status.

Bila banyak dokumen, tampilkan dokumen utama pada slide dan sisanya di appendix/source traceability.

## Review Methodology & Comment Classification

Jelaskan secara ringkas:
- evidence-based review;
- retrieval/selective embedded-KB usage;
- cross-check text, table, figure, and calculation consistency;
- priority/severity definitions;
- comment closure rule.

Jangan mengklaim standard/comparator digunakan jika sumber tersebut tidak benar-benar dibuka.

## Findings Overview

Pertahankan field technical review report:
- Finding ID;
- Discipline;
- Finding / observation;
- Priority;
- Status;
- Target document / exact location.

Boleh tambahkan confidence sebagai field sekunder jika review engine memang menghasilkan confidence.

## Detailed finding / reviewer comment

Untuk finding material tampilkan:
- Finding ID + discipline;
- priority + status + optional confidence;
- target document / exact location;
- finding / observation;
- reviewer comment / recommendation;
- why it matters / potential impact bila relevan;
- target-document evidence;
- KB/comparator evidence dengan file + page/slide/section;
- required clarification / closure evidence jika masih open.

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
- required evidence/deliverable;
- owner/status bila diketahui.

Data yang belum tersedia tidak boleh dikonversi menjadi finding definitif.

## Action Plan & Comment Resolution

Field minimum:
- Action ID;
- related finding(s);
- action required;
- PIC/owner;
- target date;
- closure evidence;
- status.

Pastikan setiap material open finding memiliki jalur closure yang jelas atau secara eksplisit dinyatakan belum memiliki action owner.

## Conclusion & Closeout Status

Tampilkan:
- overall status dokumen yang direview;
- material comments yang masih open;
- conditions to proceed ke tahap berikutnya;
- limitations pada review conclusion.

Preferred wording:
- Open for Comment
- Revision Required
- Conditionally Acceptable subject to listed closure actions
- Closed / No Material Open Comments

Gunakan approval wording lebih kuat hanya jika governance pengguna memang mendukungnya.

## Framework visual (dari skill presentasi-pln-ip dan presentasi-tvv)

Deck mengikuti framework konsultan PLN IP. Aturan lengkap ada di `references/aturan-slide.md`, `references/aturan-tvv.md`, dan `references/pedoman-plnip.md`. Katalog pola slide dan model grafis ("kapan dipakai / kapan jangan") ada di `references/pola-layout.md`, dengan bentuk visualnya di `references/galeri/galeri-grafis-plnip.jpg` dan `references/galeri/galeri-tvv.jpg`.

Aturan inti:
- **Judul dua warna**: topik biru `#008AAC` + sub-topik hitam, satu baris (maksimal dua), tanpa titik. Tidak ada label kecil (*kicker*) di atas judul dan tidak ada garis aksen di bawahnya.
- **Satu slide, satu pesan.** Isi disusun kiri → kanan: grafis/data di kiri, keterangan atau isi pendamping di kanan.
- **Keterangan grafis** berisi penjelasan singkat apa yang ditampilkan dan cara membacanya (arti warna, satuan, periode). Jangan menambah implikasi atau "*so what*" yang tidak didukung hasil review.
- **Tabel bersumbu**: baris = item, kolom = aspek. Kolom pertama tebal, header bergaris bawah biru, tanpa zebra. Sel kosong diisi "—" berlatar biru muda. Status memakai **penanda bulat lampu lalu lintas** (hijau selesai, kuning dalam proses, merah terbuka) di satu kolom, dengan legenda.
- **Dilarang**: sudut membulat, bayangan, gradien, deretan kartu berwarna, emoji/simbol dekoratif (✅ ⏳ ↔), dan pita warna di tepi kotak.
- **Palet PLN IP**: PRIMARY `#008AAC`, DARK `#05365B`, TINT `#D1EDF3`, abu `#4D4D4D`/`#C0C0C0`. Lampu lalu lintas hanya untuk status, dan warna tingkat risiko hanya untuk matriks risiko.
- **Satu baris sumber** (gaya TVV) boleh dipakai di slide yang memuat bukti teknis, misalnya rincian temuan.

### Model grafis untuk kebutuhan review

| Kebutuhan pada deck review | Model | Helper |
|---|---|---|
| Angka kunci di ringkasan (total temuan, prioritas tinggi, terbuka, *data gap*) | Deret angka kunci tanpa kartu | `G.add_kpi_row` |
| Tahapan metodologi review | Alur proses | `G.add_flow` |
| Sebaran temuan per disiplin dan prioritas | Chart batang bertumpuk | `G.add_stacked_chart` |
| Daftar temuan, *data gap*, tindak lanjut | Tabel bersumbu + penanda status | `T.add_tabel` (+ `G.add_legend`) |
| Risiko dengan kemungkinan × dampak (skala 1–5) | Matriks risiko 5×5 | `T.add_matriks_risiko` |
| Kemajuan penyelesaian temuan/tindak lanjut | Progres | `G.add_progress` |
| Rencana tindak lanjut bertanggal | *Gantt* / *timeline* | `G.add_gantt`, `G.add_timeline` |
| Tahapan proyek berpintu (FEED, pemboran, uji produksi) | *Stage-gate* | `G.add_stage_gate` |
| Proses lintas pihak (operator, kontraktor, regulator) | *Swimlane* | `G.add_swimlane` |
| Akar masalah suatu temuan | *Issue tree* | `G.add_issue_tree` |
| Prioritas temuan dua sumbu (dampak × kemudahan) | Matriks 2×2 | `G.add_matrix_2x2` |
| Penilaian kualitatif per aspek | *Harvey table* | `G.add_harvey_table` |
| Lokasi sumur/wilayah kerja | Peta Indonesia | `G.add_map` |
| Gambar bukti (render halaman KB, skema sumur) | Gambar dimuat proporsional | `T.fit_picture` |

Semua model dibangun dari bentuk dan chart asli PowerPoint, sehingga tetap bisa diedit.

## Judul slide

Judul memakai format **topik + sub-topik**, misalnya `Temuan Teknis` `Daftar Temuan dan Status`, atau `F-001` `Beban termal *production casing* belum dihitung untuk kondisi *shut-in*`. Untuk slide rincian temuan, sub-topik berisi inti temuan. Jangan membuat judul lebih tegas daripada bukti yang tersedia.

## Data integrity

- Pertahankan MD/TVD/TVDSS, satuan, datum, basis temperatur/tekanan, kondisi statis/dinamis, dan revisi.
- Jangan mengubah angka untuk membuat chart terlihat rapi.
- Jika acuan pembanding tidak berlaku atau bukti lemah, tampilkan sebagai klarifikasi/*data gap*, bukan ketidaksesuaian.
- Status, PIC, tanggal target, dan bukti penyelesaian jangan diisi dengan tebakan.

## Pembuatan PPTX

Utamakan output **editable PPTX**.

1. Susun JSON hasil review (format di docstring `scripts/build_review_ppt.py`), lalu jalankan:
   ```bash
   python scripts/build_review_ppt.py review.json output.pptx
   ```
   Generator sudah memakai master geothermal dan pustaka grafis di atas. Teks mendukung `*miring*` dan `**tebal**`. Untuk matriks risiko 5×5, isi `likelihood` dan `severity` (1–5) pada `key_risks`.
2. Untuk slide tambahan yang tidak dibuat generator (mis. *gantt* tindak lanjut, *stage-gate*, peta lokasi), tulis fungsi kecil dan berikan ke `build(..., extra=...)`; slide akan disisipkan sebelum kesimpulan:
   ```python
   import json, sys; sys.path.insert(0, 'scripts')
   import build_review_ppt as B          # sekaligus memuat pustaka: B.P, B.G, B.T

   def tambahan(prs, data):
       s = B.content_slide(prs, 'Rencana Tindak Lanjut', 'Jadwal Penyelesaian')
       B.G.add_gantt(s, periode, baris, B.L, B.BODY_TOP, B.CW)
       B.caption(s, 'Batang menunjukkan rentang waktu tiap tindak lanjut; garis tegak = hari ini.')

   B.build(json.load(open('review.json')), 'output.pptx', extra=tambahan)
   ```
   Lihat docstring tiap fungsi di `assets/pustaka/plnip_grafis.py` dan `tvv_deck.py` untuk parameternya. Ikon dari `assets/pustaka/icons/` memerlukan `cairosvg` (`pip install cairosvg`). Bila tidak tersedia, jangan memakai ikon.
3. Jangan memasukkan seluruh dokumen sumber ke JSON. Masukkan hanya hasil review dan bukti yang benar-benar dipakai.

## Quality check

1. Jalankan `python scripts/check_deck.py output.pptx` sampai **0 FAIL** (pemeriksa dari skill presentasi-tvv). Baca setiap WARN dan perbaiki kecuali disengaja. Peringatan "tanpa slide outline" dan "judul tidak ditemukan" pada slide penutup boleh diabaikan.
2. Render setiap slide menjadi gambar dan periksa:
   - logo Danantara + PLN IP tidak tertutup;
   - teks tidak terpotong atau bertumpuk;
   - penanda status berada di tengah sel;
   - label chart terbaca;
   - tidak ada setengah slide yang kosong tanpa alasan.
3. Periksa isi:
   - urutan slide konsisten dengan laporan review;
   - prioritas, status, dan tingkat keyakinan tidak tertukar;
   - setiap klaim teknis material punya lokasi sumber;
   - risiko lintas disiplin bukan sekadar mengulang temuan;
   - setiap temuan material yang masih terbuka punya tindak lanjut atau *data gap* yang jelas;
   - angka, satuan, dan tanggal sesuai sumber;
   - daftar sumber hanya berisi sumber yang benar-benar dipakai;
   - status penyelesaian tidak melampaui kewenangan atau bukti;
   - slide penutup Terima Kasih berada paling akhir.
