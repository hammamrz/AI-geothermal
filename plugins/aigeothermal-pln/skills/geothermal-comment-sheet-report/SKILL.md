---
name: geothermal-comment-sheet-report
description: Buat comment sheet / technical review report DOCX bergaya KKP PLN IP dari hasil review geothermal: TOC otomatis, tabel temuan, data gap, action plan, dan status closeout.
---

# Geothermal Comment Sheet Report

## Gaya bahasa (wajib)

Sebelum menulis jawaban, tabel, laporan, atau slide, baca `../geothermal-knowledge/references/GAYA_BAHASA.md` dan ikuti aturannya. Ringkasnya:
- Gunakan bahasa Indonesia baku yang natural, seperti laporan resmi seorang *engineer* senior. Jangan menyusun kalimat dengan pola terjemahan kata demi kata dari bahasa Inggris.
- Istilah Inggris yang padanannya kurang pas tetap dipakai dan **dicetak miring** dengan `*istilah*` (mis. *shut-in*, *casing*, *siting*, *reservoir engineer*, *data gap*). Akronim, nama dokumen, dan kata serapan baku tidak dimiringkan.
- Pakai padanan Indonesia yang lazim bila tepat: sumur (bukan *well*), pemboran, temuan, ahli geokimia.
- Nada lugas dan profesional, tanpa frasa pengisi ("Tentu!", "Berikut adalah …", "Penting untuk dicatat …").
- Contoh: "Apabila hasil ini digunakan sebagai dasar penentuan lokasi (*siting*) atau perencanaan sumur, perlu dilakukan verifikasi oleh ahli geokimia dan *reservoir engineer*."

## Purpose
Turn completed geothermal technical review findings into a formal, editable `.docx` report suitable for circulation, comment resolution, and management/technical review.

Use this skill **after** `geothermal-review` has produced evidence-based findings. Do not re-read the entire embedded KB just to create the report. Reuse the findings, evidence, source locations, and data gaps already established by the review.

## Output
Default output: editable Microsoft Word `.docx`.

When requested, also provide PDF after DOCX render/QA.

The report must contain real Word fields for:
- Table of Contents
- List of Figures
- List of Tables
- page numbers

Set Word `updateFields=true` so fields refresh when the document is opened. If fields remain stale in the user's Word client, instruct the user to press `Ctrl+A`, then `F9`.

## Visual identity
The report shell must use `references/PLN_IP_COMMENT_SHEET_REPORT_TEMPLATE.docx`.

This template is a stripped, lightweight reproduction of the supplied PLN IP KKP document shell. It intentionally preserves the KKP visual treatment for:
- the **cover page** (same artwork/composition)
- the **content-page header** (same PLN logo, PT PLN / PT PLN Indonesia Power text, address and horizontal rule)
- the **footer** (same top rule, left report/project block, centered automatic page number, right revision, ownership note, and copying restriction)
- KKP-style A4 spacing and typography

Do **not** redraw, reinterpret, modernize, or replace the cover/header/footer with a generic PLN-themed design. Do not load the full original KKP document at generation time; the lightweight shell already contains only the required visual elements.

Variable text may change only where needed for the generated report, such as report name, project/field/well name, document number, revision, and date. Layout and corporate geometry must remain unchanged.

Dense technical tables are allowed but must stay readable. Landscape sections may be used selectively for detailed finding/comment tables and action registers; they must inherit the same KKP header/footer.

## Default report architecture
Use this structure unless the user explicitly asks otherwise:

### Front matter
1. Cover
2. Document Control and Revision History
3. Executive Summary
4. Table of Contents - automatic
5. List of Figures - automatic
6. List of Tables - automatic

### Main report
1. Tujuan, Lingkup, dan Basis Review
2. Dokumen yang Diperiksa
3. Metodologi Review dan Klasifikasi Komentar
4. Technical Findings and Reviewer Comments
5. Key Risks and Cross-Discipline Interfaces
6. Data Gaps, Clarifications, and Assumptions
7. Action Plan and Comment Resolution Register
8. Kesimpulan and Closeout Status

### Appendices
- Discipline-specific review coverage
- Reference / KB sources actually used
- Optional detailed evidence/excerpts when needed

Do **not** create sections with no useful content merely to fill the template. Optional sections may be omitted.

## Finding / comment schema
Every material finding should preserve:
- unique finding ID
- discipline
- target document and exact section/page/table/figure where possible
- finding / observation
- reviewer comment and recommended action
- technical basis / source reference actually used
- priority/severity
- status

Default priority taxonomy:
- `Critical / High`: safety, well integrity, resource-confidence, operability, or approval-gate issue that should be closed before proceeding
- `Major / Medium`: material design, cost, schedule, reliability, or decision-quality issue requiring action/clarification
- `Minor / Low`: consistency, completeness, or improvement issue without material effect on the main decision basis
- `Observation`: good-practice note or opportunity for improvement; no mandatory closeout unless requested

Never invent a severity solely to make the report look complete. If review output did not establish severity, use `Unrated` or ask for classification.

## Discipline-aware organization
For subsurface reviews, group findings when useful under:
- data quality / completeness
- geology and structural interpretation
- geochemistry
- geophysics
- conceptual model
- reservoir/resource assessment
- uncertainty and resource classification
- well targeting / development concept

For drilling/well reviews, group findings when useful under:
- well objectives and basis of design
- trajectory / anti-collision / drilling window
- hole and casing program
- cementing, barriers, and well integrity
- drilling fluids and hydraulics
- well control / BOP / MAASP
- bit, BHA, directional drilling, MWD/LWD
- lost circulation, stuck pipe, formation hazards, contingencies
- logging, testing, completion, workover
- HSE / environmental controls
- schedule, cost, NPT, lessons learned

For integrated geothermal reviews, explicitly surface cross-discipline interfaces such as:
- production/reinjection strategy
- steam/brine chemistry
- scaling/corrosion
- reservoir-well-surface interface
- confirmed resource vs installed capacity/staging
- well deliverability assumptions
- operability and reliability constraints

## Detailed comment table rule
If <=30 findings, the detailed finding/comment table may stay in Chapter 4.
If >30 findings, put a concise material-findings summary in Chapter 4 and move the full detailed register to an appendix to keep the body readable.

## Traceability rules
- Cite the target document location for every material finding when identifiable.
- Cite KB/reference evidence only when it was actually used.
- Keep `target document fact`, `reviewer inference`, and `external/KB basis` distinguishable.
- Never claim a standard or regulation applies unless that source is available or the user explicitly asked for external verification.

## Automatic tables / figures
Use Word captions with `SEQ` fields:
- Tables: label `Tabel`
- Figures: label `Gambar`

The List of Tables and List of Figures must be generated from those captions, not typed manually.

## Recommended workflow
1. Take structured output from `geothermal-review`.
2. Normalize findings into the schema above.
3. Decide whether Chapter 4 stays portrait or uses landscape detailed-comment pages.
4. Build the `.docx` using `scripts/build_comment_sheet.py` or equivalent document tooling.
5. Ensure all headings use Word Heading styles so TOC is automatic.
6. Ensure figures/tables have captions using SEQ fields.
7. Render the final DOCX to PNG/PDF and visually inspect every page.
8. Fix overflow, broken tables, clipped text, headers/footers, or stale fields before delivery.

## Generator
Run:

```bash
python scripts/build_comment_sheet.py input.json output.docx
```

See `references/REPORT_STRUCTURE.md` for the supported JSON schema and recommended chapter content.

## Non-negotiable rules
- Do not paste the whole reviewed document into the report.
- Do not paste the whole embedded KB into the report.
- Do not create unsupported technical conclusions.
- Do not lose page/section traceability from the review.
- Do not manually type page numbers into TOC/List of Figures/List of Tables.
- Do not make the report visually elaborate at the expense of technical readability.
- Keep the report as a review/closeout instrument, not a marketing brochure.
