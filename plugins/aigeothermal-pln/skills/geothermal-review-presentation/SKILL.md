---
name: geothermal-review-presentation
description: Buat PowerPoint editable hasil technical review subsurface, drilling, dan well geothermal dengan 3-layout master PLN Indonesia Power. Struktur deck mengikuti backbone formal Technical Review / Comment Sheet Report: scope, document register, methodology, findings/comments, cross-discipline risks, data gaps, action plan, closeout status, dan source traceability.
---

# Geothermal Review Presentation

Gunakan skill ini ketika pengguna meminta hasil review geothermal dalam bentuk **PowerPoint/PPT/PPTX**, bahan paparan, technical review deck, comment review presentation, checkpoint presentation, atau management review.

## Prinsip utama

PowerPoint harus menjadi **versi presentasi dari technical review report**, bukan storyline yang berbeda.

Gunakan struktur formal dari `../geothermal-comment-sheet-report/references/REPORT_STRUCTURE.md` (bila skill diinstal terpisah sebagai ZIP, salinannya ada di `references/REPORT_STRUCTURE.md`) sebagai backbone review, lalu baca `references/TECHNICAL_REVIEW_PPT_STRUCTURE.md` untuk pemetaan ke slide.

Tujuannya:
1. audiens langsung tahu apa yang diperiksa dan basis review-nya;
2. setiap finding tetap traceable dan actionable;
3. cross-discipline risk, data gap, action, dan closeout status tetap terlihat;
4. deck tetap ringkas dan cocok dipresentasikan.

## Sumber konten

1. Untuk technical findings, jalankan/ikuti `geothermal-review`.
2. Untuk evidence dari embedded knowledge base, route melalui `geothermal-knowledge`.
3. Untuk struktur report formal, selaraskan dengan `geothermal-comment-sheet-report`.
4. Jangan melakukan full-KB read hanya karena output-nya PowerPoint.
5. Deck adalah representasi hasil review, bukan kesempatan menambahkan klaim baru.

## Master yang wajib digunakan

Baca `references/PLN_IP_LITE_STYLE.md`.

Gunakan **hanya tiga** background master yang dibundel:
- `references/master_assets/MASTER_COVER.jpg`
- `references/master_assets/MASTER_CONTENT.jpg`
- `references/master_assets/MASTER_CLOSING.jpg`

`references/PLN_IP_GEOTHERMAL_3_SLIDE_MASTER_REFERENCE.pptx` berisi preview 3 layout tersebut.

Aturan:
- slide pertama = COVER;
- semua slide isi = CONTENT yang sama;
- slide terakhir = CLOSING / Terima Kasih;
- jangan memuat atau menyalin master lain dari `skill-pptplnip`;
- semua teks, tabel, shape, diagram, dan chart review tetap editable di atas background master.

## Struktur deck default

Default: **Technical Review Presentation**, umumnya 11–16 slide termasuk penutup, tergantung jumlah finding material.

Urutan yang digunakan:
1. Cover
2. Executive Review Summary
3. Review Structure / Agenda
4. Review Control & Revision, bila metadata tersedia dan berguna
5. Objectives, Scope & Review Basis
6. Documents Reviewed
7. Review Methodology & Comment Classification
8. Findings Overview
9. Material Findings & Reviewer Comments, satu atau beberapa slide
10. Key Risks & Cross-Discipline Interfaces
11. Data Gaps, Clarifications & Assumptions
12. Action Plan & Comment Resolution
13. Conclusion & Closeout Status
14. Sources Used & Review Traceability
15. Terima Kasih

Jangan memaksa slide kosong. Bagian tanpa data boleh digabung, ditandai `Not provided`, atau dihilangkan jika tidak material.

### Pemetaan elemen Word yang tidak perlu disalin literal

- `Table of Contents` → `Review Structure / Agenda`.
- `List of Figures` dan `List of Tables` → tidak perlu slide khusus; caption dan source langsung pada visual/tabel yang digunakan.
- `Document Control / Revision History` → satu slide `Review Control & Revision` bila metadata tersedia.
- Lampiran rinci → hanya source traceability atau finding tambahan yang memang diperlukan untuk keputusan.

## Executive Review Summary

Ringkas minimal:
- total findings;
- jumlah High / Medium atau priority lain yang digunakan;
- jumlah open findings;
- jumlah data gaps;
- 3–5 pesan utama;
- overall closeout status jika sudah dapat dinyatakan dari evidence.

Jangan menampilkan status approval yang tidak didukung evidence/governance.

## Objectives, Scope & Review Basis

Tampilkan:
- tujuan review;
- review stage/gate bila ada;
- included dan excluded scope;
- assumptions / limitations;
- review basis dan reference yang benar-benar digunakan.

## Documents Reviewed

Buat register ringkas dengan field:
- title;
- document number/code;
- revision;
- date;
- discipline;
- review scope/status.

Bila banyak dokumen, tampilkan dokumen utama pada slide dan sisanya di appendix/source traceability.

## Review Methodology & Comment Classification

Jelaskan secara ringkas:
- evidence-based review;
- retrieval/selective embedded-KB usage;
- cross-check text, table, figure, and calculation consistency;
- priority/severity definitions;
- comment closure rule.

Jangan mengklaim standard/comparator digunakan jika sumber tersebut tidak benar-benar dibuka.

## Findings Overview

Pertahankan field technical review report:
- Finding ID;
- Discipline;
- Finding / observation;
- Priority;
- Status;
- Target document / exact location.

Boleh tambahkan confidence sebagai field sekunder jika review engine memang menghasilkan confidence.

## Detailed finding / reviewer comment

Untuk finding material tampilkan:
- Finding ID + discipline;
- priority + status + optional confidence;
- target document / exact location;
- finding / observation;
- reviewer comment / recommendation;
- why it matters / potential impact bila relevan;
- target-document evidence;
- KB/comparator evidence dengan file + page/slide/section;
- required clarification / closure evidence jika masih open.

Jika ada visual penting, prioritaskan satu gambar/diagram besar yang terbaca daripada banyak thumbnail.

## Key Risks & Cross-Discipline Interfaces

Jangan sekadar mengulang findings. Gunakan bagian ini untuk menghubungkan isu lintas disiplin, misalnya:
- resource confirmation vs development capacity;
- well deliverability vs plant staging;
- chemistry vs scaling/corrosion dan material selection;
- reservoir model vs well targeting;
- drilling design vs subsurface uncertainty;
- well integrity vs operating envelope;
- reinjection strategy vs reservoir sustainability.

Tampilkan hubungan `driver → interface → consequence / decision` bila memungkinkan.

## Data Gaps, Clarifications & Assumptions

Field minimum:
- Gap ID;
- missing/unclear data;
- impact if unresolved;
- required evidence/deliverable;
- owner/status bila diketahui.

Data yang belum tersedia tidak boleh dikonversi menjadi finding definitif.

## Action Plan & Comment Resolution

Field minimum:
- Action ID;
- related finding(s);
- action required;
- PIC/owner;
- target date;
- closure evidence;
- status.

Pastikan setiap material open finding memiliki jalur closure yang jelas atau secara eksplisit dinyatakan belum memiliki action owner.

## Conclusion & Closeout Status

Tampilkan:
- overall status dokumen yang direview;
- material comments yang masih open;
- conditions to proceed ke tahap berikutnya;
- limitations pada review conclusion.

Preferred wording:
- Open for Comment
- Revision Required
- Conditionally Acceptable subject to listed closure actions
- Closed / No Material Open Comments

Gunakan approval wording lebih kuat hanya jika governance pengguna memang mendukungnya.

## Framework pemilihan visual

Gunakan hanya framework yang relevan:
- executive summary / KPI cards;
- document register;
- review workflow / methodology flow;
- findings matrix;
- risk / priority matrix;
- technical concept / annotated evidence;
- target vs KB comparison;
- cross-discipline interface map;
- timeline / stage-gate;
- action / comment-resolution register;
- closeout status panel;
- appendix traceability.

## Action title

Setiap slide konten sebaiknya punya satu pesan utama. Gunakan action title bila evidence cukup.

Contoh buruk: `Casing Design Review`

Contoh lebih baik: `Production casing basis belum menunjukkan verifikasi thermal load pada kondisi shut-in`

Jangan membuat action title lebih tegas daripada evidence.

## Data integrity

- Pertahankan MD/TVD/TVDSS, unit, datum, temperature/pressure basis, static/dynamic condition, dan revision.
- Jangan mengubah angka untuk membuat chart terlihat rapi.
- Jika comparator tidak applicable atau evidence lemah, tampilkan sebagai clarification/data gap, bukan nonconformance.
- `confirmed nonconformance` hanya boleh digunakan bila comparator authoritative dan applicable.
- Status, PIC, due date, dan closure evidence jangan diisi dengan tebakan.

## Pembuatan PPTX

Utamakan output **editable PPTX**.

Gunakan `scripts/build_review_ppt.py` sebagai baseline generator dari JSON terstruktur. Generator v0.5.2 menerima struktur JSON technical review report dan tetap backward-compatible dengan key lama dari presentation skill.

Jangan memasukkan seluruh dokumen sumber ke JSON. Masukkan hanya hasil review dan evidence yang benar-benar dipakai.

## Quality check

Periksa:
- 16:9;
- Helvetica pada editable text;
- cover/content/closing memakai master yang benar;
- logo Danantara + PLN IP pada content master tidak tertutup;
- urutan slide konsisten dengan technical review report;
- documents reviewed dan revision tidak tertukar;
- methodology tidak mengklaim reference yang tidak digunakan;
- priority, status, dan confidence tidak tertukar;
- locator sumber tersedia untuk klaim teknis material;
- cross-discipline risks bukan sekadar duplikasi finding;
- setiap material open finding punya closure path atau gap yang jelas;
- angka / unit / dates match source;
- daftar sumber hanya berisi sumber yang benar-benar digunakan;
- closeout status tidak melebihi authority/evidence;
- tidak ada overflow / clipped text / overlap;
- closing Terima Kasih berada paling akhir.
