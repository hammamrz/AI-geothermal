# kb-inbox — pintu masuk knowledge base

Taruh file sumber KB (PDF, PPTX, DOCX, XLSX, CSV, TXT, MD, gambar) di folder ini.
Setelah file masuk ke branch `main`, workflow **KB ingest** otomatis:

1. menghitung SHA-256 dan menolak duplikat identik;
2. memindahkan file ke `plugins/geothermal-review/skills/geothermal-knowledge/references/KB/files/` dengan ID `GEO-xxxx`;
3. membangun ulang `KB_MANIFEST.json`, `KB_INDEX.md`, dan `CHANGELOG.md`;
4. membuka PR `kb-ingest/auto` dan me-merge-nya, sehingga semua akun yang memakai plugin menerima KB terbaru.

## Metadata (opsional, sangat disarankan)

Untuk setiap file `NamaFile.pdf`, boleh tambahkan sidecar `NamaFile.pdf.meta.json`:

```json
{
  "title": "Casing Design for Geothermal Wells",
  "discipline": "drilling",
  "document_type": "training",
  "revision": "Rev 1",
  "topics": ["casing", "cementing"],
  "keywords": ["thermal load", "collapse", "burst"],
  "useful_locators": ["hal. 12-20 casing load cases"],
  "notes": "Materi training internal 2025",
  "contributor": "Nama Anda",
  "supersedes": "GEO-0003"
}
```

- Tanpa sidecar, judul diambil dari nama file dan disiplin/tipe diisi `other`.
- `supersedes` hanya diisi bila file adalah revisi dari entri ACTIVE yang sudah ada; entri lama tidak dihapus, hanya ditandai `SUPERSEDED`.
- Disiplin yang disarankan: `subsurface`, `geology`, `geochemistry`, `geophysics`, `reservoir`, `drilling`, `well-design`, `completion`, `well-testing`, `hse`, `standard`, `other`.
- Tipe yang disarankan: `training`, `guideline`, `standard`, `regulation`, `project-document`, `case-study`, `vendor`, `paper`, `other`.

Batas: maksimum 25 MB per file via upload web GitHub (≈95 MB via git). Jangan pakai Git LFS.
File yang gagal diproses tetap tinggal di sini dan workflow ditandai merah.
