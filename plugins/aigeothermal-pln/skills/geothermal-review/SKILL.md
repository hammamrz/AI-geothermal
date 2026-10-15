---
name: geothermal-review
description: Review dokumen/desain geothermal subsurface, drilling, dan well berbasis bukti KB: conceptual model, target, casing/cementing, drilling program, risiko, data gap, dan temuan.
---

# Geothermal Review

Hasilkan review berbahasa Indonesia yang dapat ditelusuri ke bukti. Selalu gunakan pola **route -> retrieve -> inspect -> reason**, bukan memuat seluruh knowledge base.

## Gaya bahasa (wajib)

Sebelum menulis jawaban, tabel, laporan, atau slide, baca `../geothermal-knowledge/references/GAYA_BAHASA.md` dan ikuti aturannya. Ringkasnya:
- Gunakan bahasa Indonesia baku yang natural, seperti laporan resmi seorang *engineer* senior. Jangan menyusun kalimat dengan pola terjemahan kata demi kata dari bahasa Inggris.
- Istilah Inggris yang padanannya kurang pas tetap dipakai dan **dicetak miring** dengan `*istilah*` (mis. *shut-in*, *casing*, *siting*, *reservoir engineer*, *data gap*). Akronim, nama dokumen, dan kata serapan baku tidak dimiringkan.
- Pakai padanan Indonesia yang lazim bila tepat: sumur (bukan *well*), pemboran, temuan, ahli geokimia.
- Nada lugas dan profesional, tanpa frasa pengisi ("Tentu!", "Berikut adalah …", "Penting untuk dicatat …").
- Contoh: "Apabila hasil ini digunakan sebagai dasar penentuan lokasi (*siting*) atau perencanaan sumur, perlu dilakukan verifikasi oleh ahli geokimia dan *reservoir engineer*."

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
5. Periksa maksimum 4 visual relevan per pass secara default. Untuk melihat isi gambar (bukan hanya caption), render halamannya dengan `geothermal-knowledge/scripts/kb_render.py` lalu buka PNG-nya. Cara yang sama berlaku untuk gambar di dokumen target.
6. Jika bukti belum cukup, lakukan pass kedua yang lebih sempit.
7. Jangan membaca semua file KB untuk memastikan coverage.

## Baca dokumen target

Dokumen target boleh dibaca lebih luas karena memang objek review. Untuk dokumen panjang, review per section/topik dan nyatakan coverage. Jangan mengklaim seluruh dokumen selesai bila baru sebagian.

## Analisis berbasis bukti

1. Bedakan regulatory/standard requirement, project design criteria, training material, vendor guidance, case example, dan interpretasi AI.
2. Periksa formula, input, unit, datum, asumsi, dan basis desain. Pisahkan misalnya MD/TVD/TVDSS, gauge/absolute pressure, temperature/gradient, static/dynamic condition, dan unit conversion.
3. Klasifikasikan setiap hasil ke salah satu jenis berikut (tulis label Indonesianya di jawaban): **ketidaksesuaian terkonfirmasi**, **potensi risiko/inkonsistensi**, ***data gap***, **perlu klarifikasi**, atau **peluang perbaikan**.
4. Ketidaksesuaian terkonfirmasi wajib didukung bukti dari dokumen yang dikaji dan acuan pembanding yang berlaku. Tanpa acuan pembanding yang berlaku, jangan menyebutnya sebagai pelanggaran.
5. Prioritas High/Medium/Low harus dijelaskan berdasarkan potensi dampak. Jangan mengarang probabilitas atau skor.
6. Pisahkan tingkat keparahan (prioritas) dari tingkat keyakinan terhadap bukti.
7. Untuk well integrity, well control, H2S, pressure control, barrier, atau safety-critical issue, tandai kebutuhan verifikasi engineer dan jangan mengeluarkan approval operasi final.

## Struktur setiap item review (wajib)

Setiap item review disajikan dalam urutan tetap. Pembaca harus melihat lebih dulu apa yang sudah ada, baru kemudian penilaian reviewer:

1. **Data eksisting.** Apa yang tertulis atau tersedia saat ini di dokumen/data yang dikaji, disajikan apa adanya: angka, satuan, asumsi, metode, dan lokasinya (dokumen, bab, halaman, tabel, gambar). Bila datanya memang tidak ada, tulis "Tidak tersedia di dokumen" beserta bagian yang sudah diperiksa. Jangan memasukkan penilaian di bagian ini.
2. **Komentar review.** Penilaian reviewer atas data eksisting tersebut: apa yang kurang, tidak konsisten, atau berisiko. Sertakan dasar pembandingnya (sumber KB + halaman, kriteria proyek, atau konsistensi internal), jenis temuan, dan prioritasnya.
3. **Langkah penyelesaian.** Langkah konkret dan berurutan untuk menyelesaikan item tersebut. Setiap langkah:
   - diawali kata kerja tindakan (hitung ulang, lengkapi, verifikasi, revisi, ambil data, jalankan uji);
   - menyebut objek yang spesifik (parameter, dokumen, bab, sumur, interval kedalaman);
   - menyebut keluaran yang bisa diperiksa (lampiran perhitungan, log, revisi dokumen, berita acara);
   - menyebut pihak yang paling tepat mengerjakan bila dapat diketahui dari konteks (mis. *drilling engineer*, ahli geokimia, *reservoir engineer*). Jangan mengarang nama orang atau tanggal.

   Hindari langkah yang kabur seperti "perlu dikaji lebih lanjut", "perlu perhatian", atau "dioptimalkan". Ganti dengan tindakan nyata, misalnya: "Hitung ulang beban *collapse* dan *burst* *production casing* 13⅜" untuk kondisi *shut-in* pada temperatur statis 280 °C; lampirkan perhitungan dan *grade* casing terpilih."

Jangan menampilkan persentase atau status penyelesaian kajian (mis. "0 dari 12 selesai"). Fokus keluaran adalah cara menyelesaikan setiap item.

## Bila KB tidak cukup

Nyatakan bahwa evidence relevan tidak ditemukan pada cakupan embedded KB yang diperiksa. Jika pengguna mengizinkan sumber eksternal, pisahkan sumber eksternal dari KB. Jangan otomatis memasukkan jawaban AI atau sumber eksternal ke embedded KB.

Sebutkan `KB revision` dari `KB_INDEX.md` sebagai batas cakupan. Jika pengguna memiliki dokumen sumber yang seharusnya ada di KB, sampaikan bahwa penambahan KB dilakukan oleh admin KB lewat repo GitHub. Dokumen dari percakapan boleh dipakai sebagai pendukung dengan label "bukan sumber KB".

## Output PowerPoint

Jika pengguna meminta hasil review sebagai PPT/PPTX/presentation, setelah technical findings dan evidence cukup, gunakan skill `geothermal-review-presentation`. Jangan mengulang retrieval KB dari nol bila evidence review yang diperlukan sudah tersedia; teruskan hanya findings, locator sumber, data gap, dan rekomendasi yang benar-benar dipakai.

## Keluaran default

Mulai dengan ringkasan temuan utama dan cakupan kajian, lalu sajikan tabel:

| ID | Data eksisting (dan lokasinya) | Komentar review (jenis, dasar, sumber KB) | Prioritas | Langkah penyelesaian |
|---|---|---|---|---|

- Kolom "Data eksisting" selalu diisi lebih dulu dan hanya berisi fakta dari dokumen/data.
- Kolom "Langkah penyelesaian" berisi langkah bernomor sesuai aturan di atas.
- Tingkat keyakinan terhadap bukti disebutkan di dalam komentar review bila relevan.

Untuk bukti visual, sebutkan file, halaman/slide, dan objek visual yang diperiksa. Akhiri dengan:
- langkah selanjutnya yang diprioritaskan (3–5 langkah terpenting dari seluruh item, berurutan);
- data tambahan yang dibutuhkan;
- konflik sumber bila ada;
- bagian dokumen yang sudah dan belum dikaji;
- daftar referensi KB yang benar-benar dibuka.
