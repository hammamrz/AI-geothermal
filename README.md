# AIGeothermal-PLN — skill Claude

**AIGeothermal-PLN** adalah satu skill Claude untuk technical review geothermal PLN Indonesia Power. Skill ini berisi empat modul, dan Claude memilih modul yang relevan secara otomatis:

| Modul | Fungsi |
|---|---|
| `geothermal-knowledge` | Retrieval selektif dari knowledge base (KB) bersama yang dikelola admin |
| `geothermal-review` | Review subsurface/drilling/well berbasis bukti KB |
| `geothermal-comment-sheet-report` | DOCX comment sheet / technical review report (shell KKP PLN IP) |
| `geothermal-review-presentation` | PPTX technical review (3-layout master PLN IP) |

Skill bisa dipakai oleh **akun individual masing-masing, termasuk Free, Pro, dan Max**, tanpa perlu organisasi Claude.

## Cara kerja update otomatis

```
 Admin ── upload file ke kb-inbox/ (GitHub web) ──► main
                                                     │
                     workflow "KB ingest & sync manifest"
                     (ID GEO-xxxx, KB_INDEX, CHANGELOG, sync-manifest.json)
                                                     │
                                                     ▼
 Akun pengguna (skill AIGeothermal-PLN, di-upload sekali)
   └─ setiap percakapan: sync.py update ──► ambil modul + index KB terbaru dari GitHub
   └─ saat butuh sumber:  sync.py kb-get GEO-xxxx ──► unduh file KB itu saja
```

- ZIP skill cukup di-upload **sekali** per akun.
- Instruksi modul dan KB diambil versi terbarunya dari repo ini di awal setiap percakapan. Perubahan dari admin sampai ke semua akun tanpa upload ulang.
- Bila GitHub tidak terjangkau, skill memakai salinan bawaan dan memberi tahu pengguna.
- Upload ulang ZIP hanya perlu bila folder `standalone/` (SKILL.md induk atau `sync.py`) berubah. Hal ini jarang terjadi dan akan dicatat di `CHANGELOG`.

---

## 1. Untuk pengguna: memasang skill (sekali saja)

1. Unduh **AIGeothermal-PLN.zip** dari release [`skills-latest`](https://github.com/hammamrz/AI-geothermal/releases/tag/skills-latest).
2. Di claude.ai (web atau desktop): **Settings → Capabilities**, lalu pastikan **Code execution and file creation** aktif. Pada pengaturan akses jaringan, cukup yang default (*package managers*, sudah mencakup GitHub), atau izinkan `github.com`, `api.github.com`, dan `raw.githubusercontent.com`.
3. Buka **Customize → Skills → + → Upload a skill**, lalu pilih `AIGeothermal-PLN.zip`.
4. Pastikan skill **aigeothermal-pln** dalam keadaan aktif.
5. Uji dengan pertanyaan: *"Apa saja isi KB geothermal AIGeothermal-PLN?"* Claude seharusnya menjalankan sinkronisasi dan menyebut `KB revision`.

Catatan untuk akun Free: skill dapat dipakai, tetapi batas penggunaan Free kecil. Membaca PDF besar atau membuat DOCX/PPTX lebih cepat menghabiskan kuota.

### Pengguna Claude Code (opsional)

```bash
/plugin install aigeothermal-pln --marketplace hammamrz/AI-geothermal
```

Setelah itu buka `/plugin` → **Marketplaces** → `aigeothermal-pln-marketplace` → **Enable auto-update**. Di Claude Code, keempat modul tampil sebagai skill terpisah di bawah plugin **AIGeothermal-PLN**, dan file KB ikut terunduh bersama plugin.

---

## 2. Untuk admin: menambah atau merevisi KB

Hanya admin yang menambah atau merevisi KB. File yang di-upload pengguna di chat **tidak** masuk KB; Claude memakainya hanya di percakapan itu dengan label "bukan sumber KB".

1. Buka folder [`kb-inbox/`](kb-inbox/) → **Add file → Upload files**.
2. Upload file sumber (PDF, PPTX, DOCX, XLSX, CSV, TXT, MD, atau gambar). Bila ada, sertakan juga sidecar `<nama-file>.meta.json` berisi judul, disiplin, tipe, revisi, topik, dan keyword; formatnya ada di [`kb-inbox/README.md`](kb-inbox/README.md). Untuk revisi dokumen lama, isi `"supersedes": "GEO-xxxx"`.
3. Pilih **Commit directly to the main branch**.
4. Buka tab **Actions** dan tunggu workflow **KB ingest & sync manifest** hijau (±1 menit). Setelah itu, percakapan baru di semua akun memakai KB terbaru.

Workflow tersebut menghitung SHA-256 (duplikat identik ditolak), memberi ID `GEO-xxxx`, memindahkan file ke `plugins/aigeothermal-pln/skills/geothermal-knowledge/references/KB/files/`, lalu membangun ulang `KB_MANIFEST.json`, `KB_INDEX.md`, `CHANGELOG.md`, dan `sync-manifest.json`. Entri lama yang direvisi tidak dihapus, hanya ditandai `SUPERSEDED`.

Batas ukuran: 25 MB per file lewat upload web GitHub (±95 MB lewat git). **Jangan pakai Git LFS.**

### Pengaturan repo (sekali saja)

- **Settings → Actions → General → Workflow permissions**: pilih *Read and write permissions*.
- Batasi akses tulis repo hanya untuk admin. Pengguna skill tidak butuh akun GitHub.

### Publik atau privat?

Skill di akun individual mengambil update dari GitHub tanpa login, jadi repo harus **publik**. Konsekuensinya, isi repo (file KB, template KKP, dan master PPT PLN IP) dapat diunduh siapa pun yang tahu alamatnya. Unggah ke KB hanya dokumen yang boleh bersifat publik.

Bila KB harus rahasia:
1. Jadikan repo privat.
2. Buat *fine-grained personal access token* dengan akses **read-only (Contents)** hanya ke repo ini.
3. Bangun ZIP secara lokal dengan `AIGEO_READ_TOKEN=<token> python scripts/build_skill_zips.py`, lalu bagikan ZIP itu hanya ke tim.

Token tersebut ikut terbawa di ZIP, sehingga siapa pun yang memegang ZIP bisa membaca repo. Jangan menaruh ZIP bertoken di release publik, dan ganti token bila ZIP bocor.

---

## 3. Struktur repo

```
standalone/aigeothermal-pln/        skill induk yang di-upload ke claude.ai
  SKILL.md                          router + langkah sinkronisasi
  scripts/sync.py                   update / kb-get / kb-search dari GitHub
  config.json                       repo & branch sumber
plugins/aigeothermal-pln/           plugin Claude Code + sumber 4 modul
  skills/geothermal-knowledge/
    references/KB/                  KB_INDEX.md, KB_MANIFEST.json, files/
    scripts/kb_manager.py           ingest/add/update/search/check
  skills/geothermal-review/ …
  skills/geothermal-comment-sheet-report/ …
  skills/geothermal-review-presentation/ …
  CHANGELOG.md                      riwayat plugin + setiap revisi KB
kb-inbox/                           pintu masuk file KB baru (admin)
sync-manifest.json                  daftar file modul + hash (dibuat otomatis)
scripts/build_skill_zips.py         bangun AIGeothermal-PLN.zip
scripts/build_sync_manifest.py      bangun sync-manifest.json
.claude-plugin/marketplace.json     marketplace untuk Claude Code
.github/workflows/                  kb-ingest, kb-validate, skill-zips
```
