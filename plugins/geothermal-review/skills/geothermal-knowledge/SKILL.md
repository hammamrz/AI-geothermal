---
name: geothermal-knowledge
description: Telusuri knowledge base (KB) geothermal bersama yang tersinkron dari repo GitHub plugin, dan kelola penambahan sumber KB dari chat. Gunakan untuk mencari referensi subsurface, reservoir, drilling, completion, well testing, standards, case studies, tabel, formula, dan visual dari file KB tanpa memuat seluruh KB ke context. Gunakan juga ketika pengguna ingin menambahkan/meng-upload/merevisi dokumen ke KB ("tambahkan ke KB", "masukkan ke knowledge base", "ini revisi dari GEO-xxxx"), menanyakan isi/daftar KB, atau apakah KB sudah versi terbaru.
---

# Geothermal Knowledge

Gunakan bahasa Indonesia, pertahankan istilah teknis sumber bila lebih tepat. Knowledge base bersifat **embedded, bersama, dan tersinkron dari GitHub**: seluruh file sumber berada di `references/KB/files/` dan router tunggal berada di `references/KB/KB_INDEX.md`.

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
4. Buka hanya file kandidat yang relevan. Jangan membuka semua file dalam `files/`.
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

## Update KB (KB bersama, tersinkron dari GitHub)

KB bukan milik satu akun. Sumber kebenaran KB adalah repo GitHub `hammamrz/AI-geothermal` (branch `main`), folder `plugins/geothermal-review/skills/geothermal-knowledge/references/KB/`. Setiap perubahan yang di-merge ke `main` disebarkan otomatis ke semua akun yang memasang plugin ini (sinkronisasi organisasi claude.ai atau auto-update marketplace Claude Code).

Konsekuensinya:
- Salinan skill yang sedang berjalan bersifat **read-only / cache**. Jangan menulis file langsung ke `references/KB/` pada skill terinstal; perubahan itu hilang dan tidak sampai ke pengguna lain.
- File yang di-upload ke percakapan **tidak otomatis menjadi KB permanen**. File baru masuk KB hanya lewat pengajuan ke `kb-inbox/` di GitHub (alur di bawah).

### Cek apakah KB lokal sudah terbaru

```bash
python scripts/kb_github.py status      # bandingkan KB lokal vs GitHub main
python scripts/kb_github.py fetch --id GEO-0007 --out /tmp/kb   # ambil satu file terbaru bila belum ada di lokal
```

Butuh akses jaringan ke `api.github.com` dan token (`GH_TOKEN`/`GITHUB_TOKEN`/`gh auth`) bila repo privat. Jika tidak bisa diakses, lanjutkan dengan KB lokal dan sebutkan `KB revision` dari `KB_INDEX.md` sebagai batas cakupan.

### Menambah sumber KB dari chat (semua pengguna)

Jalankan alur ini ketika pengguna meminta file yang di-upload dimasukkan ke KB:

1. **Pastikan file-nya jelas**: file yang dimaksud, dan apakah file baru atau revisi dari entri ACTIVE (cari dengan `python scripts/kb_manager.py search <kata kunci>`; jika revisi, catat ID-nya untuk `--supersedes`).
2. **Susun metadata ringan**: `title`, `discipline`, `document_type`, `revision`, `topics`, `keywords`, opsional `useful_locators`, `visual_content`, `notes`, `contributor` (nama pengguna). Boleh melihat sekilas judul/cover/daftar isi untuk mengusulkan metadata, tetapi **jangan deep-read seluruh dokumen** dan jangan mengarang revisi/locator. Tampilkan usulan metadata dan minta konfirmasi pengguna sebelum mengajukan.
3. **Ajukan**:
   ```bash
   python scripts/kb_github.py submit "/path/ke/file.pdf" \
     --title "Judul dokumen" --discipline drilling --document-type training \
     --revision "Rev 1" --topics casing cementing --keywords "thermal load" collapse \
     --contributor "Nama Pengguna"            # tambah --supersedes GEO-0003 bila revisi
   ```
   `--mode auto` mencoba berurutan: GitHub API (butuh token) → `git push` + PR (butuh kredensial git dengan akses tulis) → paket ZIP.
4. **Laporkan hasil** apa adanya dari output JSON:
   - `submitted`: berikan link PR. Jelaskan bahwa sumber menjadi KB resmi setelah PR di-merge admin dan workflow ingest selesai; sebelum itu jangan menyebutnya sebagai bagian KB.
   - `packaged`: berikan file ZIP kepada pengguna (salin ke folder output yang bisa diunduh) dan jelaskan langkah `next_step`: upload isi `kb-inbox/` ke GitHub atau kirim ke admin KB.
   - `rejected`: biasanya duplikat identik (sebutkan ID yang sudah ada) atau ukuran file melebihi batas.
5. Boleh memakai file yang baru di-upload sebagai **dokumen pendukung sementara** di percakapan ini, tetapi beri label "belum masuk KB" pada setiap sitasi.

Beberapa file sekaligus boleh diajukan dalam satu perintah bila metadata-nya sama; bila berbeda, ajukan terpisah. `--supersedes` hanya untuk satu file.

### Upload langsung oleh admin (tanpa chat)

Admin cukup meng-upload file (dan opsional sidecar `<nama-file>.meta.json`) ke folder `kb-inbox/` di GitHub. Workflow **KB ingest** menghitung SHA-256, menolak duplikat, memberi ID `GEO-xxxx`, memindahkan file ke `references/KB/files/`, membangun ulang `KB_MANIFEST.json` + `KB_INDEX.md` + `CHANGELOG.md`, lalu me-merge PR `kb-ingest/auto` sehingga sinkronisasi berjalan. Format sidecar: lihat `kb-inbox/README.md` di repo.

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
- Metadata hanya dari operator/kontributor. Index tetap ringan; retrieval isi sumber dilakukan saat review berlangsung.

Saat diminta menilai apakah suatu sumber ada di KB, hanya nyatakan ada jika file tercantum di index atau benar-benar terlihat di embedded KB. Pengajuan yang PR-nya belum di-merge **belum** termasuk KB.

## Citation/traceability dalam jawaban

Untuk setiap evidence yang dipakai, sebutkan minimal:
- nama file;
- halaman/slide/sheet/section bila tersedia;
- jenis sumber bila relevan, misalnya training material, guideline, standard, project document, atau case study.

Jangan menyebut sumber yang hanya ditemukan di index tetapi tidak benar-benar dibuka sebagai evidence final untuk klaim kritis.
