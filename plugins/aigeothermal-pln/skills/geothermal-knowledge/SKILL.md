---
name: geothermal-knowledge
description: Cari dan kutip referensi dari KB geothermal PLN IP (subsurface, reservoir, drilling, well, standar). Gunakan untuk pertanyaan geothermal berbasis KB atau isi/daftar/revisi KB.
---

# Geothermal Knowledge

Gunakan bahasa Indonesia, pertahankan istilah teknis sumber bila lebih tepat. Knowledge base bersifat **bersama dan dikelola admin melalui GitHub**. Router tunggal (index + manifest) ikut di skill ini di `references/KB/`. File sumber mentah disimpan di repo GitHub (`kb/files/`) dan **diunduh per ID hanya saat dibutuhkan**.

## Arsitektur wajib

- Hanya ada **satu knowledge base**: `references/KB/KB_INDEX.md` + `KB_MANIFEST.json` sebagai router, dan file mentah di repo.
- `KB_INDEX.md` adalah katalog/routing layer, bukan salinan isi sumber.
- File mentah asli (PDF, PPT/PPTX, DOC/DOCX, XLS/XLSX, CSV, TXT, MD, atau gambar) diambil dengan:
  ```bash
  python scripts/kb_fetch.py GEO-0003 GEO-0007
  ```
  Skrip mengunduh dari GitHub, memverifikasi SHA-256, dan mencetak `path` lokal tiap file (JSON). Baca file dari path itu. Bila unduhan gagal, sebutkan ID dan alasannya sebagai keterbatasan cakupan.
- File mentah adalah source of truth. Jangan membuat salinan Markdown penuh dari setiap dokumen.
- Jangan membaca seluruh KB saat skill aktif.

## Aturan retrieval hemat context

1. Baca `references/KB/KB_INDEX.md` terlebih dahulu (atau `python scripts/kb_manager.py search <istilah>` untuk menyaring metadata tanpa membaca seluruh index bila KB sudah besar). Gunakan hanya entri `ACTIVE` sebagai evidence final.
2. Cocokkan pertanyaan dengan `topic`, `keywords`, `document_type`, `discipline`, dan locator yang tersedia.
3. Pilih maksimal 5 sumber kandidat pada pass pertama.
4. Buka hanya file kandidat yang relevan. Jangan mengunduh semua file KB. Unduh hanya file kandidat itu dengan `scripts/kb_fetch.py <ID>`.
5. Ambil maksimal 8 bagian/range relevan total pada pass pertama.
6. Buka konteks sekitar hanya bila diperlukan. Default sekitar 12 halaman/slide total per pass.
7. Periksa visual hanya jika diperlukan untuk menjawab atau menjadi dasar technical finding. Default maksimum 4 visual per pass.
8. Jika evidence belum cukup, lakukan pass kedua yang lebih terarah. Jangan mengganti retrieval dengan full-KB read.
9. Untuk angka, formula, batas desain, tabel, atau klaim safety-critical, verifikasi kembali ke sumber asli dan locator-nya.

## Visual (gambar, foto, diagram)

Visual penting dapat berupa foto lapangan/manifestasi, well schematic, casing design, BHA, geological cross-section, conceptual model, log, pressure-temperature plot, drilling curve, peta, seismic/MT section, trajectory, cementing diagram, atau tabel yang tidak terekstrak baik sebagai teks.

**Ekstraksi teks hanya membaca caption, bukan isi gambar.** Bila halaman/slide berisi gambar yang relevan, atau pengguna meminta melihat/menampilkan gambar, **render halamannya menjadi PNG lalu lihat gambarnya**:

```bash
python scripts/kb_render.py GEO-0007 --pages 20-22          # PDF / PPT(X) / DOC(X) / XLS(X)
python scripts/kb_render.py GEO-0007 --info                 # jumlah halaman
python scripts/kb_render.py /path/dokumen-target.pdf --pages 5   # juga untuk dokumen yang sedang direview
```

1. Output JSON berisi `images[].path`. **Buka setiap PNG dengan tool untuk melihat gambar** (mis. tool `view`/membaca file gambar) sebelum menarik kesimpulan visual. Jangan menilai visual hanya dari teks/caption.
2. Detail kecil (label sumbu, angka di skema, legenda) tidak terbaca → render ulang halaman itu dengan `--dpi 160`–`200`.
3. **Tampilkan gambar kepada pengguna** bila diminta atau bila gambar menjadi dasar jawaban/temuan: salin PNG ke folder output yang bisa dilihat pengguna (di claude.ai: `/mnt/user-data/outputs/`, mis. `GEO-0007_hal21.png`) dan sebutkan nama filenya, atau sisipkan ke DOCX/PPTX bila sedang membuat laporan/presentasi. Beri keterangan: `Sumber: GEO-0007 "<judul>", hal. 21`.
4. Batas default: maksimum 4 visual per pass (skrip membatasi 6 halaman per panggilan). Render hanya halaman kandidat, bukan seluruh dokumen.

Saat menganalisis visual:
- identifikasi caption, legenda, unit, sumbu, label, skala, anotasi, dan keterbacaan;
- pisahkan observasi langsung ("terlihat kolom lumpur mendidih dengan gelembung") dari interpretasi;
- jangan mengklaim detail yang tidak terbaca walau sudah dirender; sebutkan bila resolusi tidak cukup;
- jangan memperkirakan angka presisi dari piksel; labeli sebagai estimasi visual.

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
