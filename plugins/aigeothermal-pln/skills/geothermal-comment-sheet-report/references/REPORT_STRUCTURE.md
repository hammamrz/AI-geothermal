# Geothermal Technical Review / Comment Sheet Report Framework

## Why this structure
For subsurface, drilling, and well reviews, a useful report must do three things at once:
1. show what was reviewed and against what basis;
2. make every technical comment traceable and actionable;
3. tell the document owner exactly how to resolve each review item.

Every review item is presented in the same order: **existing data → review comment → resolution steps**. The reader first sees what the document currently states (as-is), then the reviewer's assessment of it, then concrete, ordered steps to resolve it. A report that only has `finding -> comment` is hard to act on because the starting point and the concrete next steps are missing. Do not show completion status or completion percentages.

## Recommended chapters

### Front matter
- Cover
- Document Control
- Revision History
- Executive Summary
- Automatic Table of Contents
- Automatic List of Figures
- Automatic List of Tables
- Optional abbreviations / definitions for long reports

### 1. Tujuan, Lingkup, dan Basis Review
State:
- purpose of review
- review stage / gate
- included and excluded scope
- assumptions and limitations
- technical basis and references

### 2. Dokumen yang Diperiksa
Document register fields:
- title
- document number/code
- revision
- date
- discipline
- review scope

### 3. Metodologi Review dan Klasifikasi Komentar
Describe:
- evidence-based review approach
- retrieval/selective KB usage
- consistency checks across text/tables/figures
- severity/priority definitions
- the item structure: existing data → review comment → resolution steps

### 4. Data Eksisting dan Komentar Review
Minimum fields, in this order:
- Finding ID
- Discipline
- Target document / exact location
- **Existing data** (`existing`): what the document currently states, as-is: values, units, assumptions, method. Write "Tidak tersedia di dokumen" when absent. No judgement here.
- **Review comment** (`finding`, plus `comment` if needed): the reviewer's assessment of that existing data and why it is insufficient, inconsistent, or acceptable
- Technical basis / reference (KB ID + page)
- Priority
- **Resolution steps** (`resolution_steps`): numbered, concrete steps

Optional when the review is iterative:
- document owner response
- reviewer response to the revision

### 5. Key Risks and Cross-Discipline Interfaces
Use this for issues that cut across several comments or disciplines, for example:
- resource confirmation vs development capacity
- well deliverability vs plant staging
- chemistry vs scaling/corrosion and materials
- reservoir model vs well targeting
- drilling design vs subsurface uncertainty
- well integrity vs operating envelope
- reinjection strategy vs reservoir sustainability

### 6. Data Gaps, Clarifications, and Assumptions
Recommended fields:
- Gap ID
- missing/unclear data
- impact if unresolved
- steps to complete the data (`resolution_steps`, or `required` rendered as "Sediakan …")
- owner

### 7. Langkah Penyelesaian Item Review
One row per review item, ordered by priority:
- item ID and short title
- numbered resolution steps
- PIC/owner, target date, and evidence of completion, only when known (never guessed)

Good steps start with an action verb, name the specific object, and produce a checkable output. Avoid vague steps such as "perlu dikaji lebih lanjut". Example: "Hitung ulang beban *collapse* dan *burst* *production casing* 13⅜\" untuk kasus *shut-in* (BHST 280 °C); lampirkan perhitungan dan *grade* casing terpilih."

`actions` (legacy) is still accepted and used for an item that has no `resolution_steps`.

### 8. Kesimpulan dan Langkah Selanjutnya
State:
- conclusion on the reviewed document
- review recommendation (`overall_status`, shown as "Rekomendasi kajian"), without inventing a technical approval, e.g. "Perlu revisi", "Dapat dilanjutkan setelah langkah prioritas tinggi diselesaikan", "Dapat diterima tanpa komentar material"
- 3–5 ordered next steps (`next_steps`, alias `conditions_to_proceed`); when omitted, the generator takes the first step of the highest-priority items
- any limitations on the review conclusion

Do not report a completion status or percentage.

## Discipline-specific review coverage

### Subsurface
- source data quality and completeness
- geology / structural framework
- alteration / mineralogy when relevant
- geochemistry and fluid interpretation
- geophysics and inversion/interpretation basis
- conceptual model
- reservoir boundaries, temperature, permeability
- resource/reserve estimation method and uncertainty
- Monte Carlo / probabilistic assumptions
- resource classification and confidence
- well targeting and development concept
- production/reinjection concept

### Drilling / Well Design
- well objectives / success criteria
- offset-well lessons learned
- pore/formation pressure and temperature basis
- well trajectory / collision / target tolerance
- hole sizes and casing setting depths
- casing design load cases and material selection
- cementing program and TOC/barriers
- drilling-fluid program / hydraulics / ECD
- well-control philosophy, BOP, MAASP
- bit/BHA/directional/MWD-LWD plan
- lost-circulation strategy
- stuck-pipe / formation instability / H2S and other hazards
- logging / coring / testing / completion plan
- wellhead / completion / workover considerations
- well integrity and barrier verification
- contingency plans
- time/cost/NPT assumptions
- HSE / environmental controls

### Well / Reservoir Performance
- pressure-temperature survey quality
- feed zones and injectivity/productivity
- well test interpretation
- deliverability / decline assumptions
- scaling and corrosion risk
- production / reinjection allocation
- interference and connectivity
- make-up well assumptions
- monitoring plan

## JSON input supported by the bundled generator

```json
{
  "report_title": "TECHNICAL REVIEW & COMMENT SHEET REPORT",
  "project_name": "Project / Field Name",
  "report_no": "...",
  "revision": "0",
  "date": "30 September 2026",
  "prepared_by": "...",
  "reviewed_by": "...",
  "approved_by": "...",
  "executive_summary": "...",
  "objective": "...",
  "scope": ["..."],
  "review_basis": ["..."],
  "documents_reviewed": [
    {"title":"...","number":"...","revision":"...","date":"...","scope":"..."}
  ],
  "findings": [
    {
      "id":"F-001",
      "discipline":"Drilling",
      "location":"Doc A, Sec. 5.2, p. 34",
      "existing":"Production casing 13-3/8in K-55 designed for circulating load only; shut-in case not listed",
      "finding":"Review comment on the existing data",
      "comment":"Short recommendation (optional)",
      "basis":"KB source / standard actually used",
      "source":"GEO-0003, p. 45-47",
      "priority":"High",
      "resolution_steps":[
        "Recalculate ... (concrete step 1)",
        {"step":"Revise section 4.2 and attach the calculation","pic":"Drilling team","due":"...","evidence":"DP Rev. 2"}
      ]
    }
  ],
  "key_risks": ["..."],
  "data_gaps": [
    {"id":"DG-01","gap":"...","impact":"...","resolution_steps":["..."],"owner":"..."}
  ],
  "actions": [
    {"id":"A-01","finding_id":"F-009","action":"...","pic":"...","due":"...","evidence":"..."}
  ],
  "conclusion":"...",
  "overall_status":"Perlu revisi",
  "next_steps":["...","..."],
  "closing":"...",
  "references_used":["..."]
}
```
