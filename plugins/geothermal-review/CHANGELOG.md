# Changelog

## 1.0.0 — 2026-09-30 (konversi ke Claude)

- Konversi dari plugin Codex/ChatGPT ke **plugin Claude** dalam marketplace privat (`.claude-plugin/marketplace.json`, `plugins/geothermal-review/.claude-plugin/plugin.json`). Manifest Codex (`.agents/`, `.codex-plugin/`, `plugin.json` Agent Plugins) dihapus.
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
