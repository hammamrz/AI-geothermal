# AIGeothermal-PLN

**AIGeothermal-PLN** adalah asisten Claude untuk technical review geothermal PLN Indonesia Power. Ada empat modul, dan Claude memilih modul yang relevan secara otomatis:

| Modul | Fungsi |
|---|---|
| `geothermal-knowledge` | Retrieval selektif dari knowledge base (KB) bersama yang dikelola admin |
| `geothermal-review` | Review subsurface/drilling/well berbasis bukti KB |
| `geothermal-comment-sheet-report` | DOCX comment sheet / technical review report (shell KKP PLN IP) |
| `geothermal-review-presentation` | PPTX technical review (3-layout master PLN IP) |

AIGeothermal-PLN dipakai di akun Claude masing-masing, tanpa perlu organisasi Claude. Cara pasangnya bergantung pada paket akun:

| Akun | Cara pasang | Update |
|---|---|---|
| **Pro / Max** | **Plugin** dengan upload ZIP (bagian 1A) | Otomatis: setiap percakapan mengambil modul dan index KB terbaru dari GitHub |
| **Free** | **Skill ZIP** (bagian 1B), karena plugin tidak tersedia di paket Free | Otomatis: setiap percakapan mengambil modul dan index KB terbaru dari GitHub |

File KB mentah disimpan di folder `kb/` repo dan **tidak** ikut di dalam plugin maupun ZIP. Claude hanya mengunduh file KB yang dibutuhkan saat menjawab, sehingga plugin dan ZIP tetap kecil (±3 MB) walaupun KB terus bertambah.

---

## 1. Untuk anggota tim: memasang AIGeothermal-PLN (sekali saja)

Syarat untuk semua akun: di claude.ai, buka **Settings → Capabilities**, lalu aktifkan **Code execution and file creation**. Akses jaringan cukup yang default, karena sudah mencakup GitHub.

### 1A. Akun Pro / Max: pasang sebagai plugin (upload ZIP)

1. Unduh **[AIGeothermal-PLN-plugin.zip](https://github.com/hammamrz/AI-geothermal/releases/download/skills-latest/AIGeothermal-PLN-plugin.zip)**.
2. Buka **Customize → Plugins → Add → Upload plugin**, lalu pilih ZIP tadi (**jangan diekstrak**).
3. Pastikan plugin **AIGeothermal-PLN** aktif.
4. Uji dengan pertanyaan: *"Apa saja isi KB geothermal AIGeothermal-PLN?"*

Plugin ini "tipis", sama seperti skill untuk akun Free: modul dan KB terbaru diambil dari GitHub setiap kali dipakai, sehingga plugin cukup di-upload sekali. Plugin juga otomatis tersedia di Cowork dan Claude Code dengan akun yang sama.

> **Kenapa tidak lewat "Add marketplace"?** Repo ini menyimpan file KB (ratusan MB), sedangkan claude.ai menolak marketplace dari repo sebesar itu ("Failed to add marketplace"). Upload ZIP plugin tidak terpengaruh ukuran repo. Untuk Claude Code, perintah marketplace di bawah tetap berfungsi.

### 1B. Akun Free: pasang sebagai skill ZIP

1. Unduh **[AIGeothermal-PLN.zip](https://github.com/hammamrz/AI-geothermal/releases/download/skills-latest/AIGeothermal-PLN.zip)**. Link ini selalu mengarah ke versi terbaru dan bisa dibuka tanpa akun GitHub.
2. Buka **Customize → Skills → + → Upload a skill**, lalu pilih ZIP tadi. **Jangan diekstrak.**
3. Pastikan skill **aigeothermal-pln** aktif.
4. Uji dengan pertanyaan: *"Apa saja isi KB geothermal AIGeothermal-PLN?"* Claude menjalankan sinkronisasi lalu menyebut `KB revision`.

ZIP (skill maupun plugin) cukup di-upload sekali. Upload ulang hanya perlu bila admin mengumumkan perubahan pada skill pemuat (folder `standalone/`), yang jarang terjadi. Batas pemakaian paket Free kecil, sehingga membaca PDF besar atau membuat DOCX/PPTX lebih cepat menghabiskan kuota.

### Pengguna Claude Code (opsional)

```bash
/plugin install aigeothermal-pln --marketplace hammamrz/AI-geothermal
```

Setelah itu buka `/plugin` → **Marketplaces** → `aigeothermal-pln-marketplace` → **Enable auto-update**.

---

## 2. Untuk admin: menambah atau merevisi KB

Hanya admin yang menambah atau merevisi KB. File yang di-upload pengguna di chat **tidak** masuk KB; Claude memakainya hanya di percakapan itu dengan label "bukan sumber KB".

**Cara tercepat: satu ZIP berisi banyak file.**

1. Kumpulkan file dalam satu folder. Subfolder bernama disiplin (`drilling/`, `geology/`, …) otomatis menjadi disiplin. Opsional, sertakan `metadata.csv` berisi judul/tipe/revisi/keyword per file ([template](docs/kb-metadata-template.csv)).
2. Kompres folder menjadi ZIP.
3. Upload sesuai ukuran:
   - **≤ 25 MB**: upload ZIP ke [`kb-inbox/`](kb-inbox/) → **Commit directly to the main branch**.
   - **> 25 MB (hingga 2 GB)**: **Releases → Draft a new release**, tag berawalan `kb-` (mis. `kb-2026-10-01`), lampirkan ZIP, lalu **Publish release**.
4. Buka tab **Actions** dan tunggu workflow **KB ingest & sync manifest** hijau. Untuk jalur release, hasilnya juga ditulis di catatan release.

File satuan tetap bisa di-upload langsung ke `kb-inbox/`, beserta sidecar `<nama-file>.meta.json` bila perlu. Detail format ada di [`kb-inbox/README.md`](kb-inbox/README.md). Untuk revisi dokumen lama, isi `supersedes` dengan ID lama (`GEO-xxxx`).

Workflow tersebut menghitung SHA-256 (duplikat identik ditolak), memberi ID `GEO-xxxx`, memindahkan file ke `kb/files/`, lalu membangun ulang `KB_MANIFEST.json`, `KB_INDEX.md`, `CHANGELOG.md`, dan `sync-manifest.json`, serta menaikkan versi plugin. Entri lama yang direvisi tidak dihapus, hanya ditandai `SUPERSEDED`.

Batas ukuran: 25 MB per upload web ke `kb-inbox/`, 2 GB per aset release, dan ±95 MB per file KB setelah diekstrak (batas GitHub). **Jangan pakai Git LFS.**

### Pengaturan repo (sekali saja)

- **Settings → Actions → General → Workflow permissions**: pilih *Read and write permissions*.
- Batasi akses tulis repo hanya untuk admin. Pengguna skill tidak butuh akun GitHub.

### Repo publik

Repo ini publik, sehingga skill di akun mana pun bisa mengambil update tanpa login dan tanpa token. Konsekuensinya, semua isi repo (file KB, template KKP, dan master PPT PLN IP) bisa diunduh siapa saja yang tahu alamatnya. **Unggah ke KB hanya dokumen yang boleh bersifat publik.**

---

## 3. Struktur repo

```
standalone/aigeothermal-pln/        skill ZIP untuk akun Free
  SKILL.md                          router + langkah sinkronisasi
  scripts/sync.py                   update / kb-get / kb-search dari GitHub
  config.json                       repo & branch sumber
plugins/aigeothermal-pln/           plugin (Pro/Max, Claude Code) + sumber 4 modul
  skills/geothermal-knowledge/
    references/KB/                  KB_INDEX.md, KB_MANIFEST.json (router KB)
    scripts/kb_manager.py           ingest/add/update/search/check (admin & CI)
    scripts/kb_fetch.py             unduh file KB per ID dari GitHub
  skills/geothermal-review/ …
  skills/geothermal-comment-sheet-report/ …
  skills/geothermal-review-presentation/ …
  CHANGELOG.md                      riwayat plugin + setiap revisi KB
kb/files/                           file KB mentah (GEO-xxxx__nama), dikelola workflow
kb-inbox/                           pintu masuk file/ZIP KB baru (admin)
docs/kb-metadata-template.csv       template metadata.csv untuk upload ZIP
sync-manifest.json                  daftar file modul + hash (dibuat otomatis)
scripts/build_skill_zips.py         bangun AIGeothermal-PLN.zip (skill) dan AIGeothermal-PLN-plugin.zip (plugin)
scripts/build_sync_manifest.py      bangun sync-manifest.json
.claude-plugin/marketplace.json     marketplace untuk Claude Code
.github/workflows/                  kb-ingest, kb-validate, skill-zips
```
