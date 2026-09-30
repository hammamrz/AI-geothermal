# Geothermal Technical Review / Comment Sheet Report Framework

## Why this structure
For subsurface, drilling, and well reviews, a useful report must do three things at once:
1. show what was reviewed and against what basis;
2. make every technical comment traceable and actionable;
3. make closure status easy to manage after the review meeting.

A report that only has `finding -> comment` usually becomes hard to close because the owner, priority, due date, evidence, and review basis are separated or missing.

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
- status if multiple revisions are compared

### 3. Metodologi Review dan Klasifikasi Komentar
Describe:
- evidence-based review approach
- retrieval/selective KB usage
- consistency checks across text/tables/figures
- severity/priority definitions
- closure rules

### 4. Technical Findings and Reviewer Comments
Minimum fields:
- Finding ID
- Discipline
- Target document / exact location
- Finding / observation
- Reviewer comment / recommendation
- Technical basis / reference
- Priority
- Status

Optional fields when the review is iterative:
- document owner response
- reviewer closure comment
- closure evidence/reference

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
- evidence/deliverable required
- owner/status

### 7. Action Plan and Comment Resolution Register
Recommended fields:
- Action ID
- related finding(s)
- action required
- PIC/owner
- target date
- closure evidence
- status

### 8. Kesimpulan and Closeout Status
State:
- overall status of the reviewed document
- whether material comments remain open
- conditions to proceed to the next stage
- any limitations on the review conclusion

Suggested status wording, without inventing a technical approval:
- Open for Comment
- Revision Required
- Conditionally Acceptable subject to listed closure actions
- Closed / No Material Open Comments

Use a stronger approval phrase only if the user's governance explicitly supports it.

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
      "finding":"...",
      "comment":"...",
      "basis":"KB source / standard actually used",
      "priority":"High",
      "status":"Open"
    }
  ],
  "key_risks": ["..."],
  "data_gaps": [
    {"id":"DG-01","gap":"...","impact":"...","required":"...","status":"Open"}
  ],
  "actions": [
    {"id":"A-01","finding_id":"F-001","action":"...","pic":"...","due":"...","evidence":"...","status":"Open"}
  ],
  "conclusion":"...",
  "overall_status":"Revision Required",
  "closing":"...",
  "references_used":["..."]
}
```
