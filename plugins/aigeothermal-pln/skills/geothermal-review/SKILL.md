---
name: geothermal-review
description: Review dokumen/desain geothermal subsurface, drilling, dan well berbasis bukti KB: conceptual model, target, casing/cementing, drilling program, risiko, data gap, dan temuan.
---

# Geothermal Review

Hasilkan review berbahasa Indonesia yang dapat ditelusuri ke bukti. Selalu gunakan pola **route -> retrieve -> inspect -> reason**, bukan memuat seluruh knowledge base.

## Sumber knowledge

Gunakan skill `geothermal-knowledge` sebagai router ke **satu embedded KB** di `skills/geothermal-knowledge/references/KB/`. Jangan mencari atau meminta Google Drive/Library sebagai default bila sumber yang dibutuhkan sudah ada dalam embedded KB.

Baca `references/review-checklist.md` hanya sebagai checklist cakupan, bukan sebagai sumber batas teknis atau angka desain.

## Tetapkan cakupan

1. Identifikasi dokumen target, revisi, proyek/lapangan, fase, tipe sumur, tujuan, dan data yang tersedia.
2. Pisahkan dokumen yang sedang direview dari sumber KB.
3. Jika ada gap, lanjutkan bagian yang masih dapat diperiksa dan tandai gap tersebut.
4. Jangan menganggap dokumen target sebagai referensi pembanding kecuali pengguna secara eksplisit menetapkannya demikian.

## Retrieval KB hemat context

Untuk setiap isu/topik:
1. Route melalui `KB_INDEX.md`.
2. Pilih maksimal 5 sumber kandidat.
3. Ambil maksimal 8 snippet/range relevan total pada pass awal.
4. Buka konteks seperlunya, default sekitar maksimum 12 halaman/slide sumber per pass.
5. Periksa maksimum 4 visual relevan per pass secara default.
6. Jika bukti belum cukup, lakukan pass kedua yang lebih sempit.
7. Jangan membaca semua file KB untuk memastikan coverage.

## Baca dokumen target

Dokumen target boleh dibaca lebih luas karena memang objek review. Untuk dokumen panjang, review per section/topik dan nyatakan coverage. Jangan mengklaim seluruh dokumen selesai bila baru sebagian.

## Analisis berbasis bukti

1. Bedakan regulatory/standard requirement, project design criteria, training material, vendor guidance, case example, dan interpretasi AI.
2. Periksa formula, input, unit, datum, asumsi, dan basis desain. Pisahkan misalnya MD/TVD/TVDSS, gauge/absolute pressure, temperature/gradient, static/dynamic condition, dan unit conversion.
3. Klasifikasikan hasil sebagai: `confirmed nonconformance`, `potential risk/inconsistency`, `data gap`, `clarification`, atau `improvement opportunity`.
4. `Confirmed nonconformance` wajib memiliki bukti target + comparator applicable yang jelas. Tanpa comparator applicable, jangan menyebut pelanggaran.
5. Prioritas High/Medium/Low harus dijelaskan berdasarkan potensi dampak. Jangan mengarang probabilitas atau skor.
6. Pisahkan severity dari confidence evidence.
7. Untuk well integrity, well control, H2S, pressure control, barrier, atau safety-critical issue, tandai kebutuhan verifikasi engineer dan jangan mengeluarkan approval operasi final.

## Bila KB tidak cukup

Nyatakan bahwa evidence relevan tidak ditemukan pada cakupan embedded KB yang diperiksa. Jika pengguna mengizinkan sumber eksternal, pisahkan sumber eksternal dari KB. Jangan otomatis memasukkan jawaban AI atau sumber eksternal ke embedded KB.

Sebutkan `KB revision` dari `KB_INDEX.md` sebagai batas cakupan. Jika pengguna memiliki dokumen sumber yang seharusnya ada di KB, sampaikan bahwa penambahan KB dilakukan oleh admin KB lewat repo GitHub. Dokumen dari percakapan boleh dipakai sebagai pendukung dengan label "bukan sumber KB".

## Output PowerPoint

Jika pengguna meminta hasil review sebagai PPT/PPTX/presentation, setelah technical findings dan evidence cukup, gunakan skill `geothermal-review-presentation`. Jangan mengulang retrieval KB dari nol bila evidence review yang diperlukan sudah tersedia; teruskan hanya findings, locator sumber, data gap, dan rekomendasi yang benar-benar dipakai.

## Keluaran default

Mulai dengan ringkasan findings utama dan coverage. Gunakan tabel:

| ID | Lokasi target | Temuan & jenis | Dasar & sumber KB | Dampak & prioritas | Rekomendasi & verifikasi | Confidence |
|---|---|---|---|---|---|---|

Untuk evidence visual, sebutkan file + page/slide + objek visual yang diperiksa. Akhiri dengan:
- data tambahan yang dibutuhkan;
- konflik sumber bila ada;
- bagian review yang selesai/belum;
- daftar referensi KB yang benar-benar dibuka.
