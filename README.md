# Geothermal Review — plugin & skills Claude

Marketplace privat berisi plugin **`geothermal-review`** untuk Claude. Plugin ini memuat empat skill:

| Skill | Fungsi |
|---|---|
| `geothermal-knowledge` | Retrieval selektif dari knowledge base (KB) bersama + pengajuan sumber KB baru dari chat |
| `geothermal-review` | Review subsurface/drilling/well berbasis bukti KB |
| `geothermal-comment-sheet-report` | DOCX comment sheet / technical review report (shell KKP PLN IP) |
| `geothermal-review-presentation` | PPTX technical review (3-layout master PLN IP) |

Repo ini adalah **satu-satunya sumber kebenaran**. Setiap perubahan yang masuk ke `main`, baik skill maupun file KB, otomatis sampai ke semua akun yang memasang plugin.

```
 Pengguna (chat)          Admin (GitHub web)
   │ "tambahkan ke KB"        │ upload file ke kb-inbox/
   ▼                          ▼
 kb_github.py submit ──► PR ke kb-inbox/ ──► merge ──► main
                                                 │
                              workflow "KB ingest" (SHA-256, ID GEO-xxxx,
                              KB_INDEX, CHANGELOG) ──► PR kb-ingest/auto ──► auto-merge
                                                 │
            ┌────────────────────────────────────┴───────────────────────────┐
   claude.ai org sync (dipicu merge PR)                  Claude Code marketplace auto-update
   → semua anggota organisasi                              → semua pengguna yang memasang plugin
```

---

## 1. Memasang plugin untuk akun lain

### A. claude.ai / Claude Desktop / Cowork (paket Team atau Enterprise), disarankan

Owner organisasi cukup melakukannya sekali, lalu skill muncul untuk semua anggota dan ikut ter-update otomatis.

1. Pastikan repo ini **private** (syarat sinkronisasi organisasi) dan **Claude GitHub App** terpasang di repo.
2. Buka **Organization settings → Plugins & skills → Marketplaces → Add plugins → Sync from GitHub**.
3. Isi `hammamrz/AI-geothermal`, branch `main`, lalu aktifkan sinkronisasi otomatis.
4. Aktifkan plugin `geothermal-review` untuk seluruh organisasi atau grup tertentu.

Sinkronisasi berjalan **setiap ada PR yang di-merge ke `main`**. Push langsung ke `main` tidak memicu sinkronisasi di GitHub, jadi workflow KB sengaja selalu lewat PR. Sinkronisasi bisa butuh sampai ±30 menit, dan dari halaman yang sama admin juga bisa menekan **Sync** manual.

Syarat organisasi: *Code execution and file creation* serta *Skills* aktif. Ukuran repo harus di bawah 200 MB.

### B. Claude Code (CLI, desktop, IDE)

```bash
/plugin marketplace add hammamrz/AI-geothermal
/plugin install geothermal-review@geothermal-review-marketplace
```

Setelah itu buka `/plugin` → **Marketplaces** → `geothermal-review-marketplace` → **Enable auto-update**.

- Karena repo privat, setiap pengguna butuh akses baca ke repo dan kredensial git yang tersimpan (`gh auth login && gh auth setup-git`, atau SSH key di `ssh-agent`).
- Plugin sengaja tidak mencantumkan `version`, sehingga setiap commit baru di `main` dianggap versi baru.
- Admin dapat mewajibkan plugin untuk semua mesin melalui managed settings:

```json
{
  "extraKnownMarketplaces": {
    "geothermal-review-marketplace": {
      "source": { "source": "github", "repo": "hammamrz/AI-geothermal" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": { "geothermal-review@geothermal-review-marketplace": true }
}
```

### C. Upload ZIP manual (akun individual Pro/Max), cadangan

Unduh ZIP per-skill dari release **`skills-latest`** (dibangun otomatis oleh workflow *Skill ZIPs*), lalu upload di **Settings → Capabilities → Skills**. Jalur ini **tidak ter-update otomatis**: ZIP harus di-upload ulang setelah ada perubahan. Build lokal: `python scripts/build_skill_zips.py`.

---

## 2. Menambah knowledge base

### Dari chat (semua pengguna)

Upload dokumen di chat lalu minta, misalnya: *"Tambahkan file ini ke KB geothermal, disiplin drilling, materi training Rev 1."*
Skill `geothermal-knowledge` akan:

1. mengecek duplikat (SHA-256) dan menawarkan `--supersedes` bila file itu revisi entri lama;
2. mengusulkan metadata (judul, disiplin, tipe, revisi, topik, keyword) lalu meminta konfirmasi;
3. menjalankan `kb_github.py submit`, yang otomatis memilih jalur yang tersedia:

| Jalur | Kapan dipakai | Hasil |
|---|---|---|
| GitHub API | ada token `GH_TOKEN`/`GITHUB_TOKEN`/`gh auth` dengan akses tulis | branch `kb-submit/...` + PR |
| git push | kredensial git dengan akses tulis (umumnya Claude Code) | branch + PR (atau link compare) |
| Paket ZIP | tidak ada akses tulis (umumnya chat claude.ai) | ZIP berisi `kb-inbox/<file>` + `.meta.json` untuk di-upload ke GitHub atau dikirim ke admin |

Sumber baru resmi menjadi bagian KB setelah PR di-merge dan workflow ingest selesai. Admin tetap memegang kendali review.

### Upload langsung oleh admin di GitHub

1. Buka folder [`kb-inbox/`](kb-inbox/) → **Add file → Upload files**.
2. Upload file sumber, dan bila ada, sidecar `<nama-file>.meta.json` (format di [`kb-inbox/README.md`](kb-inbox/README.md)).
3. Commit ke `main`, atau pilih *create a new branch and start a pull request* lalu merge.

Workflow **KB ingest** kemudian memindahkan file ke `plugins/geothermal-review/skills/geothermal-knowledge/references/KB/files/`, memberi ID `GEO-xxxx`, membangun ulang `KB_MANIFEST.json`, `KB_INDEX.md`, dan `CHANGELOG.md`, lalu membuka dan me-merge PR `kb-ingest/auto`, yang memicu sinkronisasi ke semua akun.

Batas ukuran: 25 MB per file lewat upload web GitHub, ±95 MB per file lewat git. **Jangan pakai Git LFS**, karena file LFS tidak ikut tersinkron.

### Lewat terminal (clone repo)

```bash
python plugins/geothermal-review/skills/geothermal-knowledge/scripts/kb_manager.py --help
```

---

## 3. Pengaturan repo yang diperlukan (sekali saja)

- **Settings → Actions → General → Workflow permissions**: pilih *Read and write permissions* dan centang *Allow GitHub Actions to create and approve pull requests*.
- Opsional: variable repo `KB_AUTO_MERGE=false` bila PR `kb-ingest/auto` harus di-merge manual oleh admin (misalnya karena branch protection mewajibkan review).
- Kontributor yang mengajukan KB dari Claude Code/API butuh akses tulis (collaborator). Pengguna tanpa akses memakai jalur paket ZIP.

## 4. Struktur repo

```
.claude-plugin/marketplace.json          katalog marketplace Claude
plugins/geothermal-review/
  .claude-plugin/plugin.json             manifest plugin (tanpa version → ikut commit)
  CHANGELOG.md                           riwayat plugin + setiap revisi KB
  skills/geothermal-knowledge/
    references/KB/                       KB_INDEX.md, KB_MANIFEST.json, files/
    scripts/kb_manager.py                ingest/add/update/search/check (admin & CI)
    scripts/kb_github.py                 submit/status/fetch (dari chat)
  skills/geothermal-review/ …            skill review
  skills/geothermal-comment-sheet-report/ …
  skills/geothermal-review-presentation/ …
kb-inbox/                                pintu masuk file KB baru
scripts/build_skill_zips.py              ZIP per-skill (fallback upload manual)
.github/workflows/                       kb-ingest, kb-validate, skill-zips
```
