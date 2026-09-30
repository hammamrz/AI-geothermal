# Changelog

## KB rev 1 — 2026-09-30

- Tambah GEO-0001 — 01 Berbagai Jenis Sistem Panas Bumi dan Karakterisasinya (`files/GEO-0001__01 Berbagai Jenis Sistem Panas Bumi dan Karakterisasinya.pdf`, 9197417 bytes, SHA-256 `0e0f707c9870…`).
- Tambah GEO-0002 — 02 Sistem Geoterma karakteristik dan komposisi fluidal (`files/GEO-0002__02 Sistem Geoterma karakteristik dan komposisi fluidal.pdf`, 2149640 bytes, SHA-256 `66589983f19c…`).
- Tambah GEO-0003 — 03 Pengantar Teknik Geotermal Nov 2024 (`files/GEO-0003__03 Pengantar Teknik Geotermal Nov 2024.pdf`, 3870021 bytes, SHA-256 `fe9017056054…`).
- Tambah GEO-0004 — 04  Intro Kegiatan Eksp dan Utilisasi 2024 (`files/GEO-0004__04  Intro Kegiatan Eksp dan Utilisasi 2024.pdf`, 2805555 bytes, SHA-256 `3b81187852a3…`).
- Tambah GEO-0005 — Ringkasan (`files/GEO-0005__Ringkasan.docx`, 1018502 bytes, SHA-256 `e7bdbfdf6c0a…`).

## 1.0.0 — 2026-09-30 (konversi ke Claude)

- Plugin bernama **AIGeothermal-PLN** (ID `aigeothermal-pln`, marketplace `aigeothermal-pln-marketplace`).
- Konversi dari plugin Codex/ChatGPT ke **plugin Claude** dalam marketplace privat (`.claude-plugin/marketplace.json`, `plugins/aigeothermal-pln/.claude-plugin/plugin.json`). Manifest Codex (`.agents/`, `.codex-plugin/`, `plugin.json` Agent Plugins) dihapus.
- Plugin tidak mencantumkan `version`, sehingga setiap commit di `main` langsung menjadi versi terbaru bagi pengguna Claude Code (auto-update) dan sinkronisasi organisasi claude.ai.
- KB bersama berbasis GitHub: folder `kb-inbox/` + workflow **KB ingest** (ingest otomatis lalu merge PR `kb-ingest/auto`) dan **KB validate** (pratinjau di PR).
- `kb_manager.py`: subcommand `ingest` (sidecar `.meta.json`, verifikasi SHA-256), `search`, `kb_revision` pengganti version bump, pewarisan metadata pada revisi, batas ukuran file GitHub.
- KB hanya dikelola admin lewat `kb-inbox/` di GitHub; file yang di-upload pengguna di chat tidak masuk KB.
- `scripts/build_skill_zips.py` + workflow **Skill ZIPs** (release `skills-latest`): ZIP plugin utuh dan ZIP per-skill untuk upload manual.
- Skill review/report/presentation tidak diubah kecuali rujukan lintas-skill dan aturan KB.

## 0.6.0 — 2026-10-01

- Add KB Management Mode for source add/list/update, SHA-256 duplicate checks, immutable revision retention, lightweight index generation, validation, version bumping, and changelog records. No existing review/report generator or template was replaced.
- Add Codex marketplace manifest for importing this repository from GitHub.
- Add root Agent Plugins manifest alongside the existing `.codex-plugin/plugin.json` compatibility manifest.
- Confirm the embedded KB is empty in the v0.5.2 input archive; no training materials were added by this release.
