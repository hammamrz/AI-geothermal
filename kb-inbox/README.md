# kb-inbox — pintu masuk knowledge base

Taruh file sumber KB (PDF, PPTX, DOCX, XLSX, CSV, TXT, MD, gambar), atau satu ZIP berisi banyak file, di folder ini.
Setelah file masuk ke branch `main`, workflow **KB ingest & sync manifest** otomatis:

1. menghitung SHA-256 dan menolak duplikat identik;
2. memindahkan file ke `kb/files/` dengan ID `GEO-xxxx`;
3. membangun ulang `KB_MANIFEST.json`, `KB_INDEX.md`, `CHANGELOG.md`, dan `sync-manifest.json`;
4. menaikkan versi plugin dan meng-commit hasilnya ke `main`, sehingga semua akun (plugin maupun skill ZIP) mendapat KB terbaru.

## Upload banyak file sekaligus (disarankan)

Upload per file lewat web GitHub lambat. Lebih cepat bila semua file dikemas dalam **satu ZIP**:

1. Kumpulkan file KB dalam satu folder. Boleh dikelompokkan per disiplin: `geothermal-upstream/`, `geothermal-downstream/`, `drilling/`, `general-basic-theory/`. Nama subfolder yang cocok otomatis dipakai sebagai disiplin (nama pendek `upstream/`, `downstream/`, `general/` dan nama lama seperti `geology/` atau `reservoir/` juga dikenali).
2. Opsional: tambahkan `metadata.csv` di akar folder. Contohnya ada di [`docs/kb-metadata-template.csv`](../docs/kb-metadata-template.csv), bisa diedit di Excel dan disimpan sebagai CSV. Kolom `file` berisi nama file atau path relatif di dalam ZIP.
3. Kompres folder menjadi ZIP (Windows: klik kanan → *Send to → Compressed (zipped) folder*).
4. Pilih jalur upload sesuai ukuran ZIP:

| Ukuran ZIP | Cara upload |
|---|---|
| ≤ 25 MB | Upload ZIP ke folder `kb-inbox/` ini (**Add file → Upload files → Commit directly to main**) |
| > 25 MB (hingga 2 GB) | **Releases → Draft a new release**, buat tag baru berawalan `kb-` (mis. `kb-2026-10-01`), lampirkan ZIP di kotak *Attach binaries*, lalu **Publish release** |

Workflow mengekstrak ZIP, memproses setiap file, lalu menulis hasilnya di catatan release (untuk jalur release) atau di ringkasan tab Actions.

- ZIP hanya mengurangi jumlah file yang di-upload. PDF sudah terkompresi, jadi ukurannya hampir tidak berkurang. Upload besar lebih cepat lewat jalur release.
- Setiap file di dalam ZIP tetap maksimal ±95 MB (batas GitHub per file).
- Aman diulang: file yang sudah pernah masuk terdeteksi duplikat (SHA-256) dan dilewati.

## Metadata (opsional, sangat disarankan)

Untuk setiap file `NamaFile.pdf`, boleh tambahkan sidecar `NamaFile.pdf.meta.json`:

```json
{
  "title": "Casing Design for Geothermal Wells",
  "discipline": "drilling",
  "document_type": "training-material",
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
- Disiplin (pilih satu): `geothermal-upstream` (eksplorasi, geologi/geokimia/geofisika, reservoir, cadangan, produksi, well testing), `geothermal-downstream` (PLTP, SAGS/surface facilities, heat & mass balance, utilisasi), `drilling` (pemboran, desain dan konstruksi sumur, rig, casing/cementing, wellhead, DPM), `general-basic-theory` (dasar panas bumi, termodinamika/steam table, keekonomian dan studi kelayakan, aspek sosial). Nama lama (`geology`, `reservoir`, `well-testing`, `hse`, dan seterusnya) otomatis dipetakan ke disiplin induknya dan disimpan sebagai topik.
- Tipe yang disarankan: `training-material`, `quiz`, `study-package`, `calculation-tool`, `project-document`, `technical-evaluation`, `guideline`, `standard`, `reference`, `report`, `infographic`, `other`.
- Disiplin, tipe, dan keyword entri yang sudah ada dikelola di [`docs/kb-classification.csv`](../docs/kb-classification.csv). Untuk mengoreksinya, edit CSV itu lalu jalankan `python plugins/aigeothermal-pln/skills/geothermal-knowledge/scripts/kb_manager.py apply-meta docs/kb-classification.csv`.

Batas: maksimum 25 MB per file via upload web GitHub (≈95 MB via git). Jangan pakai Git LFS.
File yang gagal diproses tetap tinggal di sini dan workflow ditandai merah.
