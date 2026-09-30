---
name: geothermal-knowledge
description: Telusuri knowledge base (KB) geothermal bersama yang dikelola admin di repo GitHub plugin. Gunakan untuk mencari referensi subsurface, reservoir, drilling, completion, well testing, standards, case studies, tabel, formula, dan visual dari file KB tanpa memuat seluruh KB ke context. Gunakan juga ketika pengguna menanyakan isi/daftar/revisi KB atau ingin menambahkan dokumen ke KB.
---

# Geothermal Knowledge

Gunakan bahasa Indonesia, pertahankan istilah teknis sumber bila lebih tepat. Knowledge base bersifat **embedded, bersama, dan dikelola admin melalui GitHub**: seluruh file sumber berada di `references/KB/files/` dan router tunggal berada di `references/KB/KB_INDEX.md`.

## Arsitektur wajib

- Hanya ada **satu knowledge base**: `references/KB/`.
- `KB_INDEX.md` adalah katalog/routing layer, bukan salinan isi sumber.
- `files/` berisi file mentah asli: PDF, PPT/PPTX, DOC/DOCX, XLS/XLSX, CSV, TXT, MD, atau gambar.
- File mentah adalah source of truth. Jangan membuat salinan Markdown penuh dari setiap dokumen.
- Jangan membaca seluruh KB saat skill aktif.

## Aturan retrieval hemat context

1. Baca `references/KB/KB_INDEX.md` terlebih dahulu (atau `python scripts/kb_manager.py search <istilah>` untuk menyaring metadata tanpa membaca seluruh index bila KB sudah besar). Gunakan hanya entri `ACTIVE` sebagai evidence final.
2. Cocokkan pertanyaan dengan `topic`, `keywords`, `document_type`, `discipline`, dan locator yang tersedia.
3. Pilih maksimal 5 sumber kandidat pada pass pertama.
4. Buka hanya file kandidat yang relevan. Jangan membuka semua file dalam `files/`. Bila file kandidat belum ada secara lokal (skill claude.ai `aigeothermal-pln` hanya membawa index), unduh per ID dengan `sync.py kb-get <ID>` milik skill induk.
5. Ambil maksimal 8 bagian/range relevan total pada pass pertama.
6. Buka konteks sekitar hanya bila diperlukan. Default sekitar 12 halaman/slide total per pass.
7. Periksa visual hanya jika diperlukan untuk menjawab atau menjadi dasar technical finding. Default maksimum 4 visual per pass.
8. Jika evidence belum cukup, lakukan pass kedua yang lebih terarah. Jangan mengganti retrieval dengan full-KB read.
9. Untuk angka, formula, batas desain, tabel, atau klaim safety-critical, verifikasi kembali ke sumber asli dan locator-nya.

## Visual

Visual penting dapat berupa well schematic, casing design, BHA, geological cross-section, conceptual model, log, pressure-temperature plot, drilling curve, map, seismic/MT section, trajectory, cementing diagram, atau tabel yang tidak terekstrak baik sebagai teks.

Saat visual diperlukan:
- buka hanya halaman/slide terkait;
- identifikasi caption, legenda, unit, sumbu, label, anotasi dan keterbacaan;
- pisahkan observasi langsung dari interpretasi;
- jangan mengklaim detail yang tidak terbaca.

## Bila index belum lengkap

`KB_INDEX.md` dapat hanya memiliki metadata ringan. Jika query cocok dengan file tetapi locator rinci belum ada, buka file kandidat secara terarah menggunakan judul, TOC, heading, keyword, atau pencarian internal. Jangan deep-ingest seluruh dokumen hanya untuk memperkaya index.

## Update KB (hanya admin, lewat GitHub)

KB bukan milik satu akun. Sumber kebenaran KB adalah repo GitHub `hammamrz/AI-geothermal` (branch `main`), folder `plugins/aigeothermal-pln/skills/geothermal-knowledge/references/KB/`. Setiap perubahan yang di-merge ke `main` disebarkan otomatis ke semua akun yang memasang plugin ini. `KB revision` di `KB_INDEX.md` menunjukkan versi KB yang sedang terpasang.

Aturan:
- Penambahan/revisi KB **hanya dilakukan admin KB** dengan meng-upload file ke folder `kb-inbox/` di repo GitHub. Workflow **KB ingest** memberi ID `GEO-xxxx`, menolak duplikat (SHA-256), membangun ulang index/manifest/CHANGELOG, lalu menyinkronkannya ke semua pengguna.
- Salinan skill yang sedang berjalan bersifat **read-only / cache**. Jangan menulis file ke `references/KB/` pada skill terinstal dan jangan menjanjikan bahwa file akan tersimpan permanen.
- File yang di-upload pengguna ke percakapan **tidak menjadi bagian KB**. Boleh dipakai sebagai dokumen pendukung di percakapan itu saja, dengan label "bukan sumber KB" pada setiap sitasi.
- Bila pengguna ingin dokumennya masuk KB, sampaikan bahwa penambahan KB dilakukan oleh admin KB, dan bantu menyiapkan usulan metadata (judul, disiplin, tipe dokumen, revisi, topik, keyword; revisi dari `GEO-xxxx` bila ada) agar mudah diteruskan ke admin. Isi sidecar mengikuti format `kb-inbox/README.md` di repo. Jangan deep-read seluruh dokumen untuk itu dan jangan mengarang revisi/locator.

### KB Management Mode (clone repo, admin/CI)

`scripts/kb_manager.py` dijalankan pada clone repo (bukan pada skill terinstal):

```bash
python scripts/kb_manager.py ingest            # proses kb-inbox/ (dipakai workflow)
python scripts/kb_manager.py add /path/source.pdf --title "..." --discipline subsurface --document-type training
python scripts/kb_manager.py update /path/revisi.pdf --id GEO-0001 --revision "Rev 2"
python scripts/kb_manager.py search casing cement   # juga berguna saat retrieval
python scripts/kb_manager.py list
python scripts/kb_manager.py check
```

- Hash yang sudah terdaftar dianggap duplikat identik dan tidak membuat entri baru.
- `update`/`supersedes` tidak pernah menimpa file lama. Revisi baru mendapat ID baru, mewarisi metadata routing yang tidak diisi ulang; entri lama menjadi `SUPERSEDED` dan menunjuk ke penggantinya.
- Setiap perubahan menaikkan `kb_revision` dan menambah catatan di `CHANGELOG.md` plugin.
- Metadata hanya dari admin. Index tetap ringan; retrieval isi sumber dilakukan saat review berlangsung.

Saat diminta menilai apakah suatu sumber ada di KB, hanya nyatakan ada jika file tercantum di index atau benar-benar terlihat di embedded KB.

## Citation/traceability dalam jawaban

Untuk setiap evidence yang dipakai, sebutkan minimal:
- nama file;
- halaman/slide/sheet/section bila tersedia;
- jenis sumber bila relevan, misalnya training material, guideline, standard, project document, atau case study.

Jangan menyebut sumber yang hanya ditemukan di index tetapi tidak benar-benar dibuka sebagai evidence final untuk klaim kritis.
