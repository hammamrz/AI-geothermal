# Changelog

## 1.3.0 — 2026-10-01

- Gaya bahasa: panduan baru `geothermal-knowledge/references/GAYA_BAHASA.md` (bahasa Indonesia formal yang natural, istilah Inggris dicetak miring, contoh sebelum/sesudah, dan daftar istilah) yang wajib diikuti keempat modul.
- Generator DOCX dan PPTX mendukung markup `*miring*` dan `**tebal**`. Judul bab, kepala tabel, dan teks bawaan diganti ke bahasa Indonesia formal.
- Label klasifikasi temuan di modul review memakai bahasa Indonesia, misalnya "ketidaksesuaian terkonfirmasi" dan "tingkat keyakinan".
- Perbaikan PPTX: prioritas berbahasa Indonesia ("Tinggi", "Sedang") kini dihitung dan diberi warna dengan benar di ringkasan dan slide temuan.

## 1.2.0 — 2026-10-01

- Visual KB bisa dilihat dan ditampilkan: `geothermal-knowledge/scripts/kb_render.py` merender halaman/slide (PDF, PPT/PPTX, DOC/DOCX, XLS/XLSX) menjadi PNG. Sebelumnya ekstraksi teks hanya membaca caption. Claude membuka PNG untuk analisis visual dan dapat menyalinnya ke folder output agar tampil ke pengguna. Konversi Office di-cache.
- `kb_fetch.py` kini menyediakan fungsi `fetch()` yang dipakai ulang oleh `kb_render.py`.

## 1.1.0 — 2026-10-01

- Akun Pro/Max: pasang sebagai plugin lewat **Customize → Plugins → Add marketplace** (`hammamrz/AI-geothermal`). Versi plugin naik otomatis di setiap perubahan agar update tersinkron.
- Akun Free: skill ZIP diperbaiki agar diterima claude.ai. ZIP kini hanya berisi satu `SKILL.md` (instruksi modul disimpan sebagai `MODULE.md`), dan semua deskripsi skill ≤ 200 karakter.
- File KB mentah dipindah dari plugin ke `kb/files/` di repo dan diunduh per ID oleh `scripts/kb_fetch.py`, sehingga plugin dan ZIP tetap ±3 MB (batas plugin claude.ai 200 MB).

## KB rev 4 — 2026-09-30

- Tambah GEO-0050 — MP 07-Pengoperasian PLTP IP'16 (`files/GEO-0050__MP 07-Pengoperasian PLTP IP_16.doc`, 7699968 bytes, SHA-256 `ac728104531c…`).

## KB rev 3 — 2026-09-30

- Tambah GEO-0042 — 20250828 MCG_Project Overview_R1 - shared (`files/GEO-0042__20250828 MCG_Project Overview_R1 - shared.pdf`, 4770370 bytes, SHA-256 `acce4d5a9bf7…`).
- Tambah GEO-0043 — Geothermal surface solutions March 2024 rev2 (`files/GEO-0043__Geothermal surface solutions March 2024 rev2.pdf`, 1297330 bytes, SHA-256 `8dae65e2eae3…`).
- Tambah GEO-0044 — Introduction to Geothermal Project Feasibility for Indonesia Power (`files/GEO-0044__Introduction to Geothermal Project Feasibility for Indonesia Power.pdf`, 2422514 bytes, SHA-256 `f9b23734669a…`).
- Tambah GEO-0045 — Level 1 - Geothermal - Introduction to Reservoir and Drilling_9226_20250228_114359_38582 (`files/GEO-0045__Level 1 - Geothermal - Introduction to Reservoir and Drilling_9226_20250228_114359_38582.pdf`, 3730795 bytes, SHA-256 `84693a968139…`).
- Tambah GEO-0046 — PLTP (`files/GEO-0046__PLTP.docx`, 10426580 bytes, SHA-256 `26bb1647cfeb…`).
- Tambah GEO-0047 — Proposal RKAB MCG - Blawan Ijen Tahun 2023 rev 3_1 (1) (`files/GEO-0047__Proposal RKAB MCG - Blawan Ijen Tahun 2023 rev 3_1 (1).pdf`, 5872283 bytes, SHA-256 `393d70438f05…`).
- Tambah GEO-0048 — Site Visit PLTP Ijen - Combined Cycle Power Plant Study (`files/GEO-0048__Site Visit PLTP Ijen - Combined Cycle Power Plant Study.pdf`, 4074012 bytes, SHA-256 `728b9a0844dd…`).
- Tambah GEO-0049 — ucp5-grem-progress-factsheet (`files/GEO-0049__ucp5-grem-progress-factsheet.pdf`, 321470 bytes, SHA-256 `de9b8e376bb0…`).

## KB rev 2 — 2026-09-30

- Tambah GEO-0006 — 01 Geologi (`files/GEO-0006__01 Geologi.pdf`, 19789944 bytes, SHA-256 `82a0734d4fe3…`).
- Tambah GEO-0007 — 02 Geokimia (`files/GEO-0007__02 Geokimia.pdf`, 11104187 bytes, SHA-256 `0391d5ba6c20…`).
- Tambah GEO-0008 — 01 Konsep, Strategi, Metode dan Target Eksplorasi Geofisika (`files/GEO-0008__01 Konsep_ Strategi_ Metode dan Target Eksplorasi Geofisika.pdf`, 1161583 bytes, SHA-256 `86c20e2b072b…`).
- Tambah GEO-0009 — 02 Geophysical Data Evaluation November 2024 (`files/GEO-0009__02 Geophysical Data Evaluation November 2024.pdf`, 6896388 bytes, SHA-256 `7c8eaca6967d…`).
- Tambah GEO-0010 — 03 APPLICATION OF GEOPHYSICAL DATA TO INFER THE COMPONENT OF HYDROTHERMAL SYSTEM (`files/GEO-0010__03 APPLICATION OF GEOPHYSICAL DATA TO INFER THE COMPONENT OF HYDROTHERMAL SYSTEM.pdf`, 4527813 bytes, SHA-256 `ac2811a1cc7a…`).
- Tambah GEO-0011 — 04 Dasar-Dasar Teknik Reservoir (`files/GEO-0011__04 Dasar-Dasar Teknik Reservoir.pdf`, 1643200 bytes, SHA-256 `9bfc312e68fc…`).
- Tambah GEO-0012 — 05 Aliran dalam wellbore (`files/GEO-0012__05 Aliran dalam wellbore.pdf`, 1071588 bytes, SHA-256 `2d6f3b6d23c3…`).
- Tambah GEO-0013 — 06 Reservoir Uap dan Air (`files/GEO-0013__06 Reservoir Uap dan Air.pdf`, 2947774 bytes, SHA-256 `cefcfe7d4506…`).
- Tambah GEO-0014 — 01 Studi terpadu dan well targeting (`files/GEO-0014__01 Studi terpadu dan well targeting.pdf`, 9001762 bytes, SHA-256 `6b1b77c13408…`).
- Tambah GEO-0015 — 02 Steam Table & Reservoir (`files/GEO-0015__02 Steam Table _ Reservoir.pdf`, 771452 bytes, SHA-256 `f3e25e47fc54…`).
- Tambah GEO-0016 — 03 IAPWS IF97-Rev (`files/GEO-0016__03 IAPWS IF97-Rev.pdf`, 370896 bytes, SHA-256 `0558a9cb5d3c…`).
- Tambah GEO-0017 — 04 International Steam Tables, Springer (2008), 3540214194 (`files/GEO-0017__04 International Steam Tables_ Springer (2008)_ 3540214194.pdf`, 7897772 bytes, SHA-256 `e7e4f0b87c70…`).
- Tambah GEO-0018 — CO2 dan NaCl Rev (`files/GEO-0018__CO2 dan NaCl Rev.xlsm`, 78872 bytes, SHA-256 `bb82b95ab50a…`).
- Tambah GEO-0019 — NaCl CO2 Rev (`files/GEO-0019__NaCl CO2 Rev.pdf`, 631045 bytes, SHA-256 `7f4308f246ba…`).
- Tambah GEO-0020 — Steamprog (`files/GEO-0020__Steamprog.xlsm`, 61751 bytes, SHA-256 `41393b3b5c86…`).
- Tambah GEO-0021 — XSteam_Excel_v2.6 (`files/GEO-0021__XSteam_Excel_v2.6.xls`, 480256 bytes, SHA-256 `b0870d31d5c9…`).
- Tambah GEO-0022 — psychrometry (`files/GEO-0022__psychrometry.xls`, 36864 bytes, SHA-256 `cd9aeee510cd…`).
- Tambah GEO-0023 — 01 Cadangan Panas Bumi (`files/GEO-0023__01 Cadangan Panas Bumi.pdf`, 2738722 bytes, SHA-256 `53464968c33c…`).
- Tambah GEO-0024 — 02 Pengantar Pemboran Geothermal (`files/GEO-0024__02 Pengantar Pemboran Geothermal.pdf`, 10115734 bytes, SHA-256 `8c6ac0cd0811…`).
- Tambah GEO-0025 — Belajar Sendiri (`files/GEO-0025__Belajar Sendiri.pptx`, 441792 bytes, SHA-256 `86259940b7d7…`).
- Tambah GEO-0026 — 03 Pengantar Teknik Produksi NMS Bagian-2 Des 2024 (`files/GEO-0026__03 Pengantar Teknik Produksi NMS Bagian-2 Des 2024.pdf`, 4705921 bytes, SHA-256 `7acb739e54f9…`).
- Tambah GEO-0027 — 04 Pengantar Teknik Produksi Bag-2 NMS Jan 2024 (`files/GEO-0027__04 Pengantar Teknik Produksi Bag-2 NMS Jan 2024.pdf`, 2293030 bytes, SHA-256 `069bea503925…`).
- Tambah GEO-0028 — 05 Utilisasi Energi Geotermal NMS Des 2024 (`files/GEO-0028__05 Utilisasi Energi Geotermal NMS Des 2024.pdf`, 4631843 bytes, SHA-256 `e695699d738d…`).
- Tambah GEO-0029 — 06 Mempersiapkan Dokumen Pre-FS and FS (`files/GEO-0029__06 Mempersiapkan Dokumen Pre-FS and FS.pdf`, 3902442 bytes, SHA-256 `9c57a8d5d432…`).
- Tambah GEO-0030 — 01 Review Dokumen Pre-FS (`files/GEO-0030__01 Review Dokumen Pre-FS.pdf`, 246892 bytes, SHA-256 `379816498abd…`).
- Tambah GEO-0031 — Plan of Development (`files/GEO-0031__Plan of Development.pdf`, 316894 bytes, SHA-256 `936489320fc1…`).
- Tambah GEO-0032 — DriftFlux Model (`files/GEO-0032__DriftFlux Model.xlsm`, 1480996 bytes, SHA-256 `83f22e0dd758…`).
- Tambah GEO-0033 — GEOECON FS IP UPDATE (`files/GEO-0033__GEOECON FS IP UPDATE.xlsx`, 60839 bytes, SHA-256 `bec0a0df1357…`).
- Tambah GEO-0034 — GEOECON FS IP (`files/GEO-0034__GEOECON FS IP.xlsx`, 61018 bytes, SHA-256 `998a4640ae3b…`).
- Tambah GEO-0035 — Latihan Monte Carlo update (`files/GEO-0035__Latihan Monte Carlo update.xlsm`, 84408 bytes, SHA-256 `bc9c86e958fe…`).
- Tambah GEO-0036 — Latihan Monte Carlo (`files/GEO-0036__Latihan Monte Carlo.xlsm`, 82948 bytes, SHA-256 `703a9f46e85d…`).
- Tambah GEO-0037 — Perhitungan Cadangan Heat Stored (`files/GEO-0037__Perhitungan Cadangan Heat Stored.xlsm`, 58420 bytes, SHA-256 `65b1462f560a…`).
- Tambah GEO-0038 — SIL HEAT & MASS EDWARD UPDATE (`files/GEO-0038__SIL HEAT _ MASS EDWARD UPDATE.xls`, 638976 bytes, SHA-256 `de09432551c9…`).
- Tambah GEO-0039 — SIL HEAT & MASS EDWARD (`files/GEO-0039__SIL HEAT _ MASS EDWARD.xls`, 591872 bytes, SHA-256 `8d4ff0cf5f15…`).
- Tambah GEO-0040 — Steamprog (`files/GEO-0040__Steamprog.xlsm`, 68964 bytes, SHA-256 `6e51d8f3a052…`).
- Tambah GEO-0041 — XSteam_Excel_v2.6 (`files/GEO-0041__XSteam_Excel_v2.6.xls`, 479744 bytes, SHA-256 `097cba16370d…`).

## KB rev 1 — 2026-09-30

- Tambah GEO-0001 — 01 Berbagai Jenis Sistem Panas Bumi dan Karakterisasinya (`files/GEO-0001__01 Berbagai Jenis Sistem Panas Bumi dan Karakterisasinya.pdf`, 9197417 bytes, SHA-256 `0e0f707c9870…`).
- Tambah GEO-0002 — 02 Sistem Geoterma karakteristik dan komposisi fluidal (`files/GEO-0002__02 Sistem Geoterma karakteristik dan komposisi fluidal.pdf`, 2149640 bytes, SHA-256 `66589983f19c…`).
- Tambah GEO-0003 — 03 Pengantar Teknik Geotermal Nov 2024 (`files/GEO-0003__03 Pengantar Teknik Geotermal Nov 2024.pdf`, 3870021 bytes, SHA-256 `fe9017056054…`).
- Tambah GEO-0004 — 04  Intro Kegiatan Eksp dan Utilisasi 2024 (`files/GEO-0004__04  Intro Kegiatan Eksp dan Utilisasi 2024.pdf`, 2805555 bytes, SHA-256 `3b81187852a3…`).
- Tambah GEO-0005 — Ringkasan (`files/GEO-0005__Ringkasan.docx`, 1018502 bytes, SHA-256 `e7bdbfdf6c0a…`).

## 1.0.0 — 2026-09-30 (konversi ke Claude)

- Nama **AIGeothermal-PLN**. Untuk akun claude.ai individual (Free/Pro/Max) tersedia satu skill `aigeothermal-pln` (`standalone/`, `AIGeothermal-PLN.zip`) yang saat dipakai mengambil modul + index KB terbaru dari GitHub lewat `scripts/sync.py`; file KB diunduh per ID sesuai kebutuhan. Untuk Claude Code tersedia plugin `aigeothermal-pln` di marketplace `aigeothermal-pln-marketplace`.
- Konversi dari plugin Codex/ChatGPT ke **plugin Claude** dalam marketplace privat (`.claude-plugin/marketplace.json`, `plugins/aigeothermal-pln/.claude-plugin/plugin.json`). Manifest Codex (`.agents/`, `.codex-plugin/`, `plugin.json` Agent Plugins) dihapus.
- Plugin tidak mencantumkan `version`, sehingga setiap commit di `main` langsung menjadi versi terbaru bagi pengguna Claude Code (auto-update).
- KB bersama berbasis GitHub: folder `kb-inbox/` + workflow **KB ingest & sync manifest** (ingest dan `sync-manifest.json`, commit langsung ke `main`) dan **KB validate** (pratinjau di PR).
- `kb_manager.py`: subcommand `ingest` (sidecar `.meta.json`, verifikasi SHA-256), `search`, `kb_revision` pengganti version bump, pewarisan metadata pada revisi, batas ukuran file GitHub.
- KB hanya dikelola admin lewat `kb-inbox/` di GitHub; file yang di-upload pengguna di chat tidak masuk KB.
- Upload KB massal: satu ZIP (diekstrak otomatis, `metadata.csv`, subfolder disiplin) lewat `kb-inbox/` (≤25 MB) atau GitHub Release bertag `kb-*` (hingga 2 GB).
- Mode privat: ZIP skill dibangun GitHub Actions dengan token baca dari secret `AIGEO_READ_TOKEN`; build ditolak bila repo masih publik.
- `scripts/build_skill_zips.py` + workflow **Skill ZIP** (release `skills-latest`): `AIGeothermal-PLN.zip` untuk upload di claude.ai.
- Skill review/report/presentation tidak diubah kecuali rujukan lintas-skill dan aturan KB.

## 0.6.0 — 2026-10-01

- Add KB Management Mode for source add/list/update, SHA-256 duplicate checks, immutable revision retention, lightweight index generation, validation, version bumping, and changelog records. No existing review/report generator or template was replaced.
- Add Codex marketplace manifest for importing this repository from GitHub.
- Add root Agent Plugins manifest alongside the existing `.codex-plugin/plugin.json` compatibility manifest.
- Confirm the embedded KB is empty in the v0.5.2 input archive; no training materials were added by this release.
