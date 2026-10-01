# PLN IP Lite Master for Geothermal Review Decks

This is a deliberately compact extraction of only the PLN Indonesia Power presentation identity needed for geothermal technical-review decks. It does **not** carry the full `skill-pptplnip` library.

## Mandatory 3-layout master system

Use only these three bundled master backgrounds in `references/master_assets/`:

1. `MASTER_COVER.jpg`
   - derived from the approved PLN IP Belt & Road / Hong Kong cover master;
   - Danantara Indonesia at top-left and PLN Indonesia Power at top-right;
   - use only for the opening slide.

2. `MASTER_CONTENT.jpg`
   - white-space content master;
   - Danantara Indonesia + PLN Indonesia Power logos at top-right;
   - subtle power-plant silhouette along the bottom;
   - use for **all normal content slides**. Do not invent additional slide masters.

3. `MASTER_CLOSING.jpg`
   - derived from the approved PLN IP closing / Thank You reference;
   - localized to `Terima Kasih`;
   - use only for the last slide.

`PLN_IP_GEOTHERMAL_3_SLIDE_MASTER_REFERENCE.pptx` is a lightweight visual reference containing exactly these three slide types.

The rasterized backgrounds are intentional: they preserve the approved corporate master appearance without embedding the large source decks and their unused media. All review content placed on top must remain editable.

## Typography

- Canvas: 16:9 widescreen.
- Typeface: **Helvetica** for all newly created editable text.
- Cover title: Helvetica Bold, dark teal / PLN blue as appropriate to the background.
- Content title: left aligned and kept clear of the logo zone at the top-right.
- Body: Helvetica Regular; labels / metrics may use Helvetica Bold.
- Do not bundle font files.

## Palet (mengikuti skill presentasi-pln-ip)

| Token | Hex | Pakai |
|---|---|---|
| PRIMARY | `#008AAC` | Bagian topik pada judul, garis judul kolom/header tabel, seri chart yang disorot |
| DARK | `#05365B` | Angka kunci, seri chart kedua, teks beraksen |
| TINT | `#D1EDF3` | Latar panel tanpa garis tepi, sel "—", seri pembanding |
| A1 / A4 | `#1B4F60` / `#29537B` | Seri chart tambahan |
| Abu / Outline | `#4D4D4D` / `#C0C0C0` | Keterangan, nomor halaman / garis antarbaris |
| Lampu lalu lintas | `#22B44A` `#EFCF06` `#E00102` | **Hanya** penanda status (selesai / dalam proses / terbuka) di satu kolom, dengan legenda |
| Tingkat risiko | `#1B7F3B` `#22B44A` `#EFCF06` `#F08C00` `#E00102` | **Hanya** matriks risiko 5×5 |

Prioritas temuan ditulis sebagai teks (Tinggi/Sedang/Rendah). Teks tidak diwarnai merah/kuning, karena warna lampu lalu lintas khusus untuk kolom status.

## Content-slide safe area

Because the logo lockup occupies the upper-right area, keep normal titles and content inside approximately:
- title: x `0.55–8.7 in`, y `0.30–0.95 in`;
- main content: x `0.55–12.75 in`, y `1.20–6.80 in`;
- source / page number: y `6.95–7.25 in`.

Do not cover the top-right logos or the subtle bottom master artwork.

## Relevant frameworks only

1. Ringkasan eksekutif: deret 2–4 angka kunci tanpa kartu berwarna (`add_kpi_row`) + 3–5 pesan utama.
2. Scope / evidence basis: scope, coverage, basis, revision.
3. Findings overview: ID, issue, priority, confidence, target locator, KB basis.
4. Detailed finding: finding, potential impact, evidence/comparator, recommendation.
5. Technical evidence: annotated well schematic, casing section, geological section, conceptual model, BHA, PT plot, drilling curve, table.
6. Data gaps / clarification items.
7. Action plan / timeline / stage-gate.
8. Sources / traceability appendix.

Avoid business-development frameworks such as market sizing, partner proposition, portfolio map, or financial waterfall unless the review content genuinely requires them.

## Storytelling

- One dominant message per content slide.
- Use an action title only when evidence supports the conclusion.
- Observation, interpretation, risk, and recommendation must remain distinguishable.
- Every material technical claim should include a target-document locator and/or KB locator.
- Preserve technical units, datum, conditions, revision and applicability.

## Closing rule

The final slide must always use `MASTER_CLOSING.jpg`. Do not add findings, sources, or action items on top of the closing slide.
