# Asal dan lisensi pustaka presentasi

Folder ini berisi salinan pustaka dari skill **presentasi-pln-ip** dan **presentasi-tvv** milik pemilik repo. Isinya dipakai untuk model grafis dan tabel di deck review geothermal.

| File | Asal | Lisensi / catatan |
|---|---|---|
| `plnip_deck.py`, `plnip_grafis.py`, `tvv_deck.py`, `svg_render.py` | skill presentasi-pln-ip / presentasi-tvv | Kode milik pemilik skill. Pola diadaptasi dari `carnot-tech/consulting-pptx-skill` dan `seulee26/mckinsey-pptx` (MIT). Satu perubahan: `_fill_runs` di `plnip_deck.py` juga mengenali `**tebal**`. |
| `icons/` (63 ikon) | Tabler Icons | MIT (`icons/LICENSE-tabler.txt`) |
| `maps/indonesia.json` | Natural Earth 1:10m via `world-atlas` | Domain publik (Natural Earth), ISC (world-atlas) |

Yang **sengaja tidak disalin**:
- 770 ilustrasi unDraw (`undraw-pustaka.json`). Lisensi unDraw melarang pendistribusian ulang dalam paket, sedangkan repo ini publik.
- Master PLN IP (38 desain, ±15 MB) dan master TVV. Deck review memakai master geothermal sendiri di `references/master_assets/`, jadi fungsi `new_deck()`, `set_cover()`, dan `add_slide()` versi PLN IP/TVV tidak dipakai di sini.
