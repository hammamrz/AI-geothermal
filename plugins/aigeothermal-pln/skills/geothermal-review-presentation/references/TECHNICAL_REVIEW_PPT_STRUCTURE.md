# Technical Review PowerPoint Structure

This presentation structure is the PowerPoint counterpart of the formal `Geothermal Technical Review / Comment Sheet Report`.

The PPT must preserve the same review logic and traceability while compressing document-style front matter into presentation-native slides.

## Mapping from Word report to PowerPoint

| Formal technical review report | PowerPoint equivalent |
|---|---|
| Cover | Cover |
| Document Control + Revision History | Review Control & Revision slide when metadata is supplied |
| Executive Summary | Executive Review Summary |
| Table of Contents | Review Structure / Agenda |
| List of Figures / List of Tables | Omit as dedicated slides; caption and source each visual/table where used |
| 1. Tujuan, Lingkup, dan Basis Review | Objectives, Scope & Review Basis |
| 2. Dokumen yang Diperiksa | Documents Reviewed register |
| 3. Metodologi Review dan Klasifikasi Komentar | Review Methodology & Comment Classification |
| 4. Data Eksisting dan Komentar Review | Item Review overview + one detail slide per item (existing data → review comment → resolution steps) |
| 5. Key Risks and Cross-Discipline Interfaces | Key Risks & Cross-Discipline Interfaces |
| 6. Data Gaps, Clarifications, and Assumptions | Data Gap and steps to complete it |
| 7. Langkah Penyelesaian Item Review | Langkah Penyelesaian per Item Review |
| 8. Kesimpulan dan Langkah Selanjutnya | Kesimpulan dan Langkah Selanjutnya |
| Appendix / references | Sources Used & Review Traceability |
| Penutup | Terima Kasih |

## Default slide sequence

1. Cover
2. Executive Review Summary
3. Review Structure / Agenda
4. Review Control & Revision, if useful
5. Objectives, Scope & Review Basis
6. Documents Reviewed
7. Review Methodology & Comment Classification
8. Findings distribution by discipline and priority
9. Item Review: Data Eksisting dan Komentar Review
10. One detail slide per material item: existing data → review comment → resolution steps
11. Key Risks & Cross-Discipline Interfaces
12. Data Gap and steps to complete it
13. Langkah Penyelesaian per Item Review
14. Kesimpulan dan Langkah Selanjutnya
15. Sources Used & Review Traceability
16. Terima Kasih

Do not force empty slides. If a chapter has no evidence, merge it with the nearest logical slide or mark it clearly as not provided.

## Content rules

### Review items
Every item is shown in a fixed reading order: **existing data → review comment → resolution steps**. Keep the same semantic fields as the Word report:
- Finding ID
- Discipline
- exact target document / location
- existing data (`existing`): what the document states now, as-is, without judgement
- review comment (`finding`, plus `comment`): the reviewer's assessment of that data
- technical basis / reference
- priority
- resolution steps (`resolution_steps`): numbered, concrete, verb-first, with a checkable output

Optional when available:
- confidence
- potential impact
- PIC, target date, evidence of completion (never guessed)
- document owner response

### Key risks and interfaces
Prioritize cross-discipline issues such as:
- resource confirmation vs development capacity
- well deliverability vs plant staging
- chemistry vs scaling/corrosion and material selection
- reservoir model vs well targeting
- drilling design vs subsurface uncertainty
- well integrity vs operating envelope
- reinjection strategy vs reservoir sustainability

### Data gaps
Show:
- Gap ID
- missing/unclear data
- impact if unresolved
- steps to complete the data
- owner

### Resolution steps
Show per item, ordered by priority:
- item ID and short title
- numbered resolution steps
- PIC / owner, target date, evidence of completion (only when known)

### Conclusion and next steps
Show the conclusion, the review recommendation (`overall_status`), and 3–5 ordered next steps (`next_steps`). Do not show completion status, progress bars, or percentages. Do not invent a stronger technical approval than the review evidence or governance supports.
