# Katalog pola slide

Pola adalah bank ide tata letak, bukan cetakan yang harus diisi. Mulai dari **bentuk dasar A–D**. Pakai pola lanjutan hanya bila bentuk dasar tidak cocok. Bila tidak ada yang pas, susun sendiri dengan tetap mematuhi `aturan-slide.md`.

Cara memilih (diadaptasi dari katalog mckinsey-pptx): untuk setiap judul di alur cerita, sebutkan 1–3 kandidat pola, coret yang tertolak oleh kolom "Jangan dipakai bila", lalu pilih yang tersisa. Tulis alasan singkatnya di catatan kerja ("tabel bersumbu, bukan kartu, karena ada 4 opsi × 4 aspek").

Semua koordinat mengacu ke konstanta di `assets/plnip_deck.py` (`L`, `R`, `CW`, `BODY_TOP`, `LEFT_X`, `HALF_W`, dst.; inci, kanvas 13,333 × 7,5). Contoh kode lengkap ada di `assets/contoh-deck.py` (deck 6 slide) dan `assets/contoh-grafis.py` (galeri semua model grafis; pratinjau di `assets/galeri-grafis.jpg`). Deck selalu dibuka dengan `new_deck()` dari master native (`references/master-native.md`).

**Baris header berlaku untuk semua pola slide isi:** judul dua warna (topik biru + sub-topik hitam) di kiri, logo Danantara + PLN IP sudah ada di master di kanan, dan **tidak ada teks apa pun di bawah judul**. `add_slide(prs, topik, subtopik)` sudah mengaturnya; jangan menaruh judul dengan textbox sendiri dan jangan menambahkan kicker.

**Keterangan grafis selalu di badan slide**, isinya penjelasan singkat apa yang ditampilkan (data, satuan/periode, arti warna/garis/ukuran), **bukan implikasi tambahan**. Posisi per pola:
- **Kolom kanan** (grafis selebar ±7,4 in di kiri): `add_keterangan(s, teks, RIGHT_X, BODY_TOP, RIGHT_W)`; judul kolom opsional ("Keterangan"), bukan "Implikasi".
- **Kolom kiri**: bila grafis ada di kanan (mis. siklus, peta kecil), atau di bawah grafis kiri: `add_keterangan(s, teks, LEFT_X, y, LEFT_W)`.
- **Di bawah konten** (pola A, C, I, J, Y, Z, AA, AE, AI selebar penuh): `add_keterangan_bawah(s, teks)` setelah konten dibuat; posisinya otomatis 0,3 in di bawah konten terendah.
- Kolom kanan pola B dan D berisi isi dari materi user (syarat, rincian, konsekuensi yang user tulis), bukan implikasi karangan sendiri.
- Tanpa baris sumber dan tanpa footer teks; bawah slide hanya nomor halaman.

---

## Bentuk dasar

### A. Tabel bersumbu penuh
- **Dipakai bila:** ada beberapa item yang dinilai dari beberapa aspek yang sama (opsi × kriteria, proyek × status, risiko × mitigasi).
- **Jangan dipakai bila:** isinya deret waktu (pakai chart) atau hanya 2 item yang bisa jadi pola C.
- **Bangun:** `add_axis_table(s, header, rows, L, BODY_TOP, CW, col_w=[...])`. Kolom sumbu 2,0–2,4 in. Satu baris boleh disorot `{ text, highlight: true }` + legenda kecil tepat di bawah tabel.
- **Batas isi:** 3–7 baris, 3–5 kolom. Lebih dari itu, pecah menjadi 2 slide.

### B. Premis kiri → konsekuensi kanan
- **Dipakai bila:** fakta/data di kiri secara kuat menghasilkan kesimpulan di kanan ("karena X, maka Y").
- **Jangan dipakai bila:** kanan hanya penjelasan tambahan (pakai D tanpa segitiga).
- **Bangun:** kiri tabel atau bullet selebar `HALF_W - 0.2`; kanan `add_column_head(...)` + `add_bullets(...)`; satu `add_causal_triangle(...)` di tengah celah. Kedua kolom sama lebar dan sama tinggi.
- **Judul kolom kanan:** frasa yang menamai isi ("Syarat sebelum memilih skema"), bukan kata sambung ("Maka").

### C. Perbandingan dalam tabel
- **Dipakai bila:** membandingkan 2–4 opsi, skema, lokasi, atau vendor.
- **Jangan dipakai bila:** menaruh Opsi A dan Opsi B dalam dua kotak berdampingan. Itu dilarang (aturan 4.11).
- **Bangun:** pola A dengan baris = aspek, kolom = opsi. Sorotan pada sel pihak yang unggul per aspek. Wajib ada aspek di mana opsi yang tidak direkomendasikan unggul.

### D. Analisis kiri → makna kanan
- **Dipakai bila:** satu chart atau tabel analisis membuktikan judul, dan pembaca perlu tahu cara membacanya.
- **Jangan dipakai bila:** chart terbaca sendiri dan makna sudah tuntas di judul (chart boleh lebar penuh).
- **Bangun:** kiri `add_column_head(s, 'data', LEFT_X, BODY_TOP, LEFT_W, unit='satuan, periode')` + chart di `LEFT_X, LEFT_W`; kanan `add_column_head(...)` + bullet 3–5 butir. Poin di kanan yang merujuk batang tertentu, batangnya disorot di chart.

---

## Pola lanjutan

### E. Ringkasan eksekutif
- **Dipakai bila:** deck ≥ 6 slide isi. Diletakkan setelah cover.
- **Bentuk 1 (tabel 2 kolom):** kolom kiri aspek/bab (sama dengan topik judul slide pendalaman), kolom kanan satu kalimat temuan. Satu baris terpenting bold. Lihat slide 2 contoh.
- **Bentuk 2 (teks bertingkat):** tiga tingkat indentasi "kondisi → alasan → konsekuensi", tanpa kotak.
- **Jangan:** tiga kartu berwarna berisi "Tantangan / Solusi / Dampak".

### F. Chart satu sorotan (bar horizontal urut)
- **Dipakai bila:** membandingkan nilai beberapa item (biaya per skema, kapasitas per unit, capaian per wilayah).
- **Bangun:** `add_bar_chart(s, kategori, nilai, LEFT_X, y, LEFT_W, tinggi, highlight=idx)`. Urutkan nilai. Tambahkan anotasi selisih di kanan bila pesannya selisih.

### G. Tren waktu
- **Dipakai bila:** nilai berubah dari tahun ke tahun (produksi GWh, EAF, beban puncak).
- **Bangun:** `add_bar_chart(..., horizontal=False)` untuk ≤ 10 periode; untuk lebih banyak periode atau beberapa seri pakai `add_line_chart(s, kategori, [(nama, nilai), ...], x, y, w, h, highlight=0, proyeksi_mulai=idx)`: seri sorotan PRIMARY berlabel, seri lain abu, proyeksi putus-putus. Sebutkan batas aktual/proyeksi di judul sumbu.
- **Jangan:** menaruh angka tahunan dalam tabel.

### H. Komposisi dan perubahannya
- **Dipakai bila:** bauran energi, struktur biaya, porsi per unit dan perubahannya antar-periode.
- **Bangun:** `add_stacked_chart(s, kategori, [(nama, nilai), ...], x, y, w, h, persen=False, colors=[...])` (kolom bertumpuk; `horizontal=True` untuk batang), maksimal 4 segmen (PRIMARY, abu `#C0C0C0`, A1, A4 — ingat batas 3 warna), label posisi `ctr`. Urutan segmen sama di semua kolom dan sama dengan urutan legenda.

### I. Waterfall (kontribusi naik-turun)
- **Dipakai bila:** menjelaskan dari angka awal ke angka akhir (EBITDA 2025 → 2026, biaya rencana → realisasi).
- **Bangun:** `add_waterfall(s, label, nilai, x, y, w, h, total=(0, -1), satuan='')`: nilai total di indeks `total`, selisih +/− di sisanya. Kenaikan PRIMARY, penurunan NEG, total DARK, garis penghubung putus-putus, label +/− di atas batang. Judul sumbu di atasnya (`add_column_head`).

### J. Peta jalan (chevron + tabel)
- **Dipakai bila:** rencana beberapa periode dengan kegiatan, pelaksana, keluaran.
- **Bangun:** chevron di atas mulai dari `G.L + lebarSumbu` (`add_chevrons`), lalu `add_axis_table(s, None, rows, ...)` dengan baris Kegiatan / Pelaksana / Keluaran. Lihat slide 6 contoh.
- **Jangan:** chevron dengan kotak-kotak mengambang di bawahnya.

### K. Alur langkah vertikal + komentar
- **Dipakai bila:** proses 3–6 langkah yang perlu penjelasan atau catatan per langkah.
- **Bangun:** kiri (±45%) kotak nomor PRIMARY kecil + teks langkah, dipisah segitiga kecil mengarah ke bawah; judul sumbu selebar penuh di atas kedua kolom ("Alur persetujuan pengadaan"); kanan bullet tanpa judul kolom (judul sumbu sudah melintasi dua kolom).

### L. Matriks 2 × 2 atau prioritas
- **Dipakai bila:** menempatkan 4–12 item pada dua sumbu (dampak × kemudahan, urgensi × kepentingan).
- **Bangun:** `add_matrix_2x2(s, items, x, y, w, h, sumbu_x=('Rendah','Tinggi','Kemudahan'), sumbu_y=(..., 'Dampak'), kuadran=[4 nama], rekomendasi=1)`. Item `{'label','x':0–1,'y':0–1,'sorot':True,'nilai':ukuran}`; kuadran rekomendasi berlatar TINT. Sisakan kolom kanan untuk dasar penilaian.
- **Jangan:** empat kotak berwarna berbeda.

### M. Tabel penilaian (harvey ball)
- **Dipakai bila:** menilai kecukupan/kesesuaian beberapa opsi terhadap kriteria kualitatif.
- **Bangun:** `add_harvey_table(s, header, rows, x, y, w, col_w=[...])`: sel berupa angka 0–4 otomatis menjadi harvey ball, sel teks tetap teks; legenda ○…● ikut otomatis. Kolom terakhir boleh berisi catatan singkat.
- **Jangan:** warna lampu lalu lintas.

### N. Angka besar tunggal
- **Dipakai bila:** satu angka adalah seluruh pesan slide (misalnya kebutuhan investasi total). Maksimal satu kali per deck.
- **Bangun:** `add_big_number(s, '410', 'Kebutuhan investasi ...', LEFT_X, y, LEFT_W, satuan='Rp miliar')` di kolom kiri, kolom kanan berisi rincian pembentuk angka dalam tabel kecil.
- **Jangan:** 3–4 kartu angka besar berjajar.

### O. Isu → penyebab (issue tree)
- **Dipakai bila:** menguraikan masalah menjadi penyebab (keterlambatan COD, penurunan EAF).
- **Bangun:** `add_issue_tree(s, akar, [{'teks', 'anak': [...], 'utama': True}], x, y, w, h)`: akar DARK, cabang TINT, cabang terbukti PRIMARY + garis PRIMARY, sub-penyebab/bukti sebagai bullet di kanan. Juga untuk pohon *value driver* (EBITDA → pendapatan/biaya → pendorong).


### S. Daftar butir berikon + ilustrasi (pola resmi PLN IP)
- **Dipakai bila:** 3–5 butir setara yang tidak punya sumbu bersama (maksud dan tujuan, ruang lingkup, prasyarat, permintaan keputusan, langkah berikutnya) dan tiap butir satu kalimat + satu keterangan pendek.
- **Jangan dipakai bila:** butir-butirnya punya aspek yang sama (itu tabel bersumbu, pola A/T), lebih dari 5 butir, atau butirnya butuh angka pendukung.
- **Bangun:** `add_icon_list(s, [{'icon':…, 'text':…, 'sub':…}], L, BODY_TOP + 0.3, 7.0, row_h=1.15)` lalu `fit_illustration(s, nama, RIGHT_X + 0.3, BODY_TOP + 0.3, RIGHT_W - 0.3, 4.6)`. Kolom kanan **wajib** diisi ilustrasi yang nyambung dengan pesan slide; baru dibiarkan kosong bila tidak ada satu pun yang nyambung.

### T. Tabel kualitatif dengan ikon di kolom sumbu
- **Dipakai bila:** tabel 3–7 baris yang barisnya kategori berbeda sifat (aspek hukum/teknis/finansial, jenis risiko, pihak yang terlibat, tema strategis) dan isinya kalimat, bukan angka.
- **Jangan dipakai bila:** baris berisi angka untuk dibandingkan, lebih dari 7 baris, atau baris-barisnya sejenis (daftar proyek, daftar tahun). Ikon yang dipaksakan pada baris sejenis hanya jadi hiasan.
- **Bangun:** `add_axis_table(s, header, rows, L, BODY_TOP, CW, col_w=[…], row_h=0.8, row_icons=['regulasi', 'lokasi', 'biaya'])`. `row_h` harus cukup untuk teks terpanjang agar ikon tetap sejajar; cek di render.

### U. Isi sedikit di kiri + ilustrasi di kanan
- **Dipakai bila:** slide isi yang pesannya cukup dengan 3–6 bullet atau satu tabel kecil (≤ 7 in lebar), sehingga kolom kanan kosong ≥ 4 in.
- **Jangan dipakai bila:** kolom kanan seharusnya berisi makna/implikasi (pola B dan D). Makna lebih penting daripada gambar; ilustrasi hanya mengisi ruang yang memang tidak dibutuhkan isi.
- **Bangun:** isi di `LEFT_X`, `LEFT_W`; `fit_illustration(s, nama, RIGHT_X + 0.3, BODY_TOP + 0.3, RIGHT_W - 0.3, 4.6)`.

## Model grafis tambahan (V–AK) — `assets/plnip_grafis.py`

Semua model di bawah dibangun dari bentuk/chart asli PowerPoint (bisa diedit) dan dikelompokkan dalam satu group `Grafik <jenis>`. Lihat hasil render semuanya di `assets/galeri-grafis.jpg`; kode contoh lengkap di `assets/contoh-grafis.py`. Setiap grafis tetap butuh judul sumbu (`add_column_head`) bila menampilkan data, dan pesan di badan slide (kolom samping atau di bawah grafis).

### V. Angka kunci (KPI) berjajar
- **Dipakai bila:** proposisi investasi atau ringkasan kinerja yang pesannya memang 2–4 angka (kapasitas, nilai investasi, IRR, COD). Maksimal satu slide seperti ini per deck.
- **Jangan dipakai bila:** angkanya hanya hiasan pembuka atau lebih dari 4 (pakai tabel).
- **Bangun:** `add_kpi_row(s, [{'nilai':'1,1','satuan':'GW','label':'Kapasitas','ket':'…'}, …], L, BODY_TOP + 0.3, CW)`. Tanpa kartu berwarna: garis atas PRIMARY, angka DARK. Sisa bidang di bawahnya untuk asumsi atau tabel kecil.

### W. Sensitivitas: tornado dan matriks
- **Dipakai bila:** business case perlu menunjukkan faktor mana yang paling menggerakkan IRR/NPV/LCOE (tornado), atau hasil untuk kombinasi dua variabel (matriks).
- **Bangun:** `add_tornado(s, faktor, nilai_rendah, nilai_tinggi, dasar, x, y, w, h, satuan='%')` (urut otomatis dari rentang terbesar). `add_sensitivity_table(s, label_baris, label_kolom, matriks, x, y, w, judul_baris='Tarif', judul_kolom='Capex', dasar=(1,1), ambang=8.5)`: sel dasar PRIMARY, sel ≥ ambang (mis. WACC) TINT; tulis arti arsiran di bawahnya.

### X. Timeline milestone terstruktur
- **Dipakai bila:** 4–8 milestone proyek menuju COD/financial close, dengan fase dan penanda "saat ini".
- **Jangan dipakai bila:** ada banyak kegiatan paralel dengan pelaksana (pakai Y atau J).
- **Bangun:** `add_timeline(s, [{'t':2027.25,'label':'Financial close','ket':'Apr 2027','status':'selesai'|'rencana'|'kunci'}], L, y, CW, 2026, 2030, fase=[{'mulai','selesai','label'}], hari_ini=2026.73)`. Waktu dalam tahun desimal. Label otomatis turun ke baris kedua bila terlalu rapat. Separuh bawah slide boleh diisi tabel risiko jadwal atau prasyarat tiap milestone.

### Y. Gantt / rencana kerja
- **Dipakai bila:** 5–12 kegiatan dengan durasi, kelompok, status, dan milestone (rencana kerja 12–24 bulan, progress report).
- **Bangun:** `add_gantt(s, ['Q3 26','Q4 26',…], [{'label','mulai','selesai','status':'selesai'|'berjalan'|'rencana'|'kritis','milestone':t,'grup':True}], L, BODY_TOP, CW, hari_ini=0.8)`. Posisi dalam satuan kolom. Legenda status otomatis. Maksimal ±12 baris; lebih dari itu pecah per kelompok.

### Z. Stage-gate / rantai nilai
- **Dipakai bila:** tahapan berurutan dengan titik keputusan (identifikasi → pra-FS → FS → pengadaan → konstruksi), atau rantai nilai tanpa gerbang.
- **Bangun:** `add_stage_gate(s, [{'judul','butir':[…]}], L, y, CW, h, gerbang=['G1','G2',…], aktif=1)`. Chevron di atas, butir sejajar di bawah tiap tahap, gerbang belah ketupat DARK di sambungan, tahap sesudah `aktif` abu. `gerbang=None` untuk rantai nilai.

### AA. Swimlane lintas pihak
- **Dipakai bila:** proses melibatkan 2–5 pihak (PLN, PLN IP, EPC, lender, regulator) dan pertanyaannya "siapa melakukan apa, kapan".
- **Bangun:** `add_swimlane(s, ['PLN','PLN IP','EPC'], [{'lajur':1,'kolom':0,'teks':'…'}, …], n_kolom, L, BODY_TOP, CW, h, kolom=[label fase], sorot=[indeks keputusan])`. Panah otomatis urut daftar, atau atur lewat `alur=[(a,b),…]`. Maksimal ±10 langkah.

### AB. Alur proses / aliran energi
- **Dipakai bila:** 3–6 langkah atau komponen berurutan: aliran energi (PLTS → BESS → gardu → beban), rantai pasok gas, alur dokumen.
- **Bangun:** `add_flow(s, [{'judul','sub','ikon'}], x, y, w, h=1.4, arah='h'|'v', sorot=idx)`. Kotak TINT tanpa garis tepi, langkah sorotan PRIMARY, panah segitiga. Ikon dari `assets/icons/`.

### AC. Siklus
- **Dipakai bila:** proses berulang: cadence rapat transformasi, PDCA, siklus operasi harian BESS, siklus pemeliharaan.
- **Bangun:** `add_cycle(s, [{'judul','sub'}], cx, cy, r, sorot=idx)`. 3–6 langkah; teks di luar cincin, jadi sisakan ±2,6 in di kiri-kanan pusat.

### AD. Struktur organisasi / kepemilikan
- **Dipakai bila:** struktur JV/SPV dan porsi saham, struktur tata kelola proyek, organisasi tim. Maksimal 3 tingkat.
- **Bangun:** `add_org_chart(s, {'teks','sub','anak':[{'teks','sub','label':'51%','sorot':True}, …]}, x, y, w, h)`. `label` tampil di garis (porsi saham, jenis kontrak).

### AE. Rumah strategi (pilar)
- **Dipakai bila:** aspirasi → 3–5 pilar inisiatif → fondasi enabler (RJPP, strategi transisi energi, proposisi mitra).
- **Jangan dipakai bila:** pilar-pilar sebenarnya item yang dinilai dari aspek sama (itu tabel bersumbu).
- **Bangun:** `add_pillars(s, atap, [{'judul','butir':[…]}], L, BODY_TOP, CW, h, fondasi='…')`. Pilar tanpa isian warna.

### AF. Corong pipeline
- **Dipakai bila:** penyaringan bertahap (potensi → tersaring → siap lelang → konstruksi → COD; prospek mitra → LOI → kontrak).
- **Bangun:** `add_funnel(s, [{'label','nilai','ket'}], x, y, w, h, satuan='GW')`. Batang terpusat sebanding nilai, persentase lolos dari tahap sebelumnya di kanan.

### AG. Progres per proyek
- **Dipakai bila:** progress report beberapa proyek/paket terhadap target (fisik, serapan anggaran, capaian KPI).
- **Bangun:** `add_progress(s, [{'label','nilai':72,'target':80,'status':'kuning'}], x, y, w, header=('Proyek','Progres fisik','Status'), status=True)`. Garis tegak = target; batang DARK bila sudah ≥ target. Kolom status lampu lalu lintas hanya satu kolom dan butuh legenda.

### AH. Komposisi satu waktu (donat)
- **Dipakai bila:** porsi 2–6 bagian dari satu total (komposisi capex, bauran satu tahun) dan totalnya perlu ditonjolkan.
- **Jangan dipakai bila:** membandingkan komposisi antar-periode (pakai H) atau bagian > 6.
- **Bangun:** `add_donut(s, label, nilai, x, y, d, highlight=0, tengah='18,0', tengah_sub='Rp triliun')`. Legenda-tabel (nilai + %) otomatis di kanan.

### AI. Peta Indonesia / wilayah dengan titik proyek
- **Dipakai bila:** sebaran aset/proyek/lokasi kandidat, portofolio per wilayah, konteks lokasi proyek.
- **Bangun:** `h = add_map(s, [{'nama','lon','lat','jenis','nilai','sorot','posisi'}], x, y, w, wilayah='indonesia'|'sumatera'|'jawa-bali'|'jawa'|'kalimantan'|'sulawesi'|'nusa-tenggara'|'maluku-papua'|'papua', ukuran_nilai=False, satuan='MW')`. Tinggi mengikuti proporsi (`map_height(w, wilayah)`); peta nasional selebar ±11,5 in setinggi ±4,3 in. Warna per `jenis` otomatis + legenda. Daratan TINT, negara tetangga abu terang. Koordinat dari user atau sumber resmi; jangan mengarang koordinat, dan tandai "lokasi indikatif" bila perkiraan.
- **Catatan:** batas dari Natural Earth 1:10m (domain publik), disederhanakan; bukan peta resmi batas negara. Untuk peta tapak/lahan yang presisi, pakai gambar peta dari user.

### AJ. Legenda manual
- `add_legend(s, [(label, warna, 'kotak'|'garis'|'bulat'|'belah'|'kotak-garis')], x, y)` untuk grafis bentuk yang butuh keterangan warna tambahan.

### AK. Memilih model grafis (ringkas)

| Pertanyaan audiens | Model |
|---|---|
| Berapa angkanya, dan dari mana? | V angka kunci, N angka besar, I waterfall |
| Apa yang paling menggerakkan hasil? | W tornado / matriks sensitivitas |
| Kapan dan apa yang kritis? | X timeline, Y gantt, J roadmap |
| Siapa melakukan apa? | AA swimlane, AD struktur |
| Bagaimana prosesnya berjalan? | AB alur, Z stage-gate, AC siklus, K alur vertikal |
| Mengapa masalah terjadi? | O pohon isu |
| Mana yang didahulukan? | L matriks 2×2, M harvey |
| Di mana lokasinya? | AI peta |
| Seberapa jauh kemajuannya? | AG progres, AF corong |
| Apa strateginya? | AE pilar, Z rantai nilai |

### P. Cover
- `set_cover(prs, judul, unit, tanggal, desain=12, subjudul='')` membuat cover dari master native yang bertema dengan isi (daftar desain cover di `master-native.md`). Judul 34pt rata kiri (boleh berupa kesimpulan utama deck), subjudul satu baris (jenis bahan / rapat), meta di bawah (unit, bulan tahun). Logo resmi di baris header yang sama dengan slide isi (kanan atas, tengah y 0,58). Latar DARK `#05365B` dengan teks putih bila ada logo versi putih (`logosOnDark`) atau tidak ada logo; bila hanya logo berwarna, latar putih dengan judul DARK. Tanpa pita warna dekoratif.
- Jalur utama (master native): cover sudah berilustrasi/berfoto, jangan ditambah. Jalur cadangan pptxgenjs: ruang kosong di sisi berlawanan judul boleh diisi **satu** ilustrasi (`addIllustration`), lebar ±4–5 in, tidak menimpa judul maupun logo.

### Q. Daftar isi dan pembatas bab (content tracker)
- **Wajib** untuk deck isi > 10 slide: satu daftar isi setelah ringkasan eksekutif, lalu satu pembatas bab di awal setiap bab (3–7 bab).
- **Bangun:** `add_section_slide(prs, bab, ilustrasi=…, subtopik='Lima Bab Kajian')` untuk daftar isi; untuk pembatas bab n pilih salah satu gaya dan pakai konsisten: `add_section_slide(prs, bab, aktif=n, ilustrasi=…)` (content tracker di slide isi) atau `add_divider(prs, nama_bab, nomor=n, desain=20)` (pembatas master penuh: 20, 29, 34, 17, 18, 37). Daftar bab satu kolom di kiri (bab aktif DARK tebal dengan pita TINT, bab lain abu), satu ilustrasi di kanan yang bertema bab itu. Nama bab sama persis dengan topik judul slide di bab tersebut.

### R. Lampiran
- Setelah slide penutup atau setelah slide permintaan keputusan. Kicker "Lampiran". Aturan sama dengan slide isi. Rekap tanggapan reviewer dan pertanyaan terbuka ditaruh di sini, bukan di badan deck.

---

## Pola yang tidak disediakan dengan sengaja

Karena menjadi ciri deck buatan AI: grid kartu ikon, "Tantangan–Solusi–Dampak" dalam tiga kotak warna, timeline horizontal dengan lingkaran dan teks mengambang bergantian di atas-bawah, kotak kutipan besar, slide "Terima kasih" bergambar, dan slide "Agenda" berisi 4 kotak bernomor. (Daftar isi satu kolom dengan satu ilustrasi, pola Q, bukan pola terlarang ini. Timeline terstruktur pola X, dengan pita tahun sebagai sumbu dan label pada baris tetap, juga bukan.)
