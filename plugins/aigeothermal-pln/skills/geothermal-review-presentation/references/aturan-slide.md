# Aturan slide (versi lengkap)

Dokumen ini adalah acuan utama. Bila ada yang bertentangan dengan dokumen lain, dokumen ini yang berlaku. Nomor aturan dirujuk dari file lain, jadi **jangan mengubah nomor; tambahkan aturan baru di akhir bagian**.

Baca juga `pedoman-plnip.md` (pedoman internal PLN IP: piramida, ringkasan vs sintesis, pemilihan chart, 8 tip exhibit, format resmi). Untuk hal yang menyangkut standar PLN IP, dokumen itu yang menang.

Urutan baca: §0 sebelum mulai → §1 kanvas → §2 judul → §3 larangan subjudul → §4 struktur → §5 warna & garis → §6 tabel → §7 chart → §8 bahasa → §9 QA.

**Istilah yang dipakai**
- **Judul aksi**: judul berbentuk kesimpulan dalam kalimat utuh.
- **Topik dan sub-topik**: dua bagian judul. Topik ("Analisis Biaya") dicetak biru, sub-topik ("Empat Skema Penyediaan") dicetak hitam.
- **Keterangan**: penjelasan singkat apa yang ditampilkan grafis/chart/tabel/gambar di slide, ditulis di badan slide (kolom kanan/kiri atau tepat di bawah konten), bukan di bawah judul.
- **Baris header**: bagian atas slide tempat judul (kiri) dan logo Danantara + PLN IP (kanan, sudah ada di template) berada.
- **Judul kolom**: satu baris bold dengan garis bawah PRIMARY di atas kolom atau chart.
- **Judul sumbu**: judul kolom khusus chart/tabel yang menyebut data + satuan + periode.
- **Bidang isi**: area antara bawah judul (y 1,3) dan nomor halaman (y 6,85).
- **Kata yatim**: 1–2 kata yang jatuh sendirian di baris terakhir.
- **Chevron**: bentuk panah bersambung untuk tahap atau periode.
- **Harvey ball**: lingkaran terisi sebagian (○ ◔ ◑ ◕ ●) untuk menunjukkan tingkat.

---

## 0. Sebelum mulai

1. **Pahami permintaan.** Siapa yang meminta, untuk rapat apa, siapa audiensnya, keputusan apa yang diharapkan, draf atau final. Tulis tujuan, bentuk keluaran, serta cakupan (termasuk/tidak termasuk) dalam 3–5 baris.
2. **Bila tujuan tidak jelas, jangan langsung membuat deck panjang.** Buat satu slide ringkasan masalah atau tanya satu hal terpenting. Makin banyak slide tanpa arah, makin banyak isi generik dan kesalahan.
3. **Baca bahan dari user dulu.** Jangan mengarang fakta, angka, nama proyek, atau kutipan. Fakta yang tidak ada di bahan ditandai sebagai asumsi.
4. **Isi lebih penting daripada tampilan.** Bila bahan tipis, katakan tipis. Jangan menutupinya dengan dekorasi atau kalimat panjang.
5. **Alur standar:** alur cerita (daftar judul) → pilih bentuk visual per judul → bangun → cek mesin → periksa visual → baca judul berurutan → review mata segar.

## 1. Kanvas

| Hal | Nilai |
|---|---|
| Rasio | Selalu 16:9. PPTX 13.333 × 7.5 in (`LAYOUT_WIDE`), sama dengan master native PLN IP. |
| Font | **Helvetica** untuk semua teks baru (judul, isi, tabel, chart, label; `FONT` di `plnip_deck.py`). Jangan mengganti diam-diam ke Calibri/Arial/Aptos. Bila Helvetica tidak terpasang di lingkungan render, pertahankan definisi Helvetica di PPTX dan sebutkan keterbatasan render ke user. Tidak berganti font di tengah deck. |
| Warna | Hanya palet PLN IP + netral (lihat SKILL.md), maksimal 3 warna PLN IP per dokumen; lampu lalu lintas dikecualikan. |
| Logo | Pada jalur utama logo sudah ada di **master native** (`assets/masters/`), jadi tidak ditempel ke slide. Pada jalur cadangan pptxgenjs: Danantara dan PLN IP di kanan atas slide isi (dan cover), dari file resmi di `assets/logos/` (terpasang otomatis oleh `T.newDeck()`). Rata kanan di x 13,13 (bukan margin isi 12,833 — baris header boleh lebih dekat tepi). Danantara tinggi 0,35 in, PLN IP 0,44 in (sengaja tidak disamakan; mengikuti proporsi lockup resminya), jarak antar-logo 0,12 in, tengah vertikal y 0,58 in. Logo ada di semua slide isi atau tidak sama sekali. Jangan menggambar ulang, mewarnai ulang, meregangkan, atau mengubah proporsi logo untuk memberi tempat judul |
| Berkas awal | **Selalu** mulai dari pustaka master native `assets/masters/PLN_IP_Master_Library.pptx` lewat `new_deck()` di `plnip_deck.py` (lihat `references/master-native.md`). Logo, latar, cover, dan pembatas ikut dari master; jangan menempel logo sendiri, jangan membangun dari kanvas kosong, jangan menutup latar master dengan kotak putih penuh. `Template_PLNIP.pptx` hanya dipakai bila user memintanya (`new_deck(dasar='template')`). |
| Template | Satu deck, satu gaya: posisi judul, margin, posisi keterangan, ukuran huruf sama di semua slide. Bawah slide hanya berisi nomor halaman: tanpa footer teks "PT PLN Indonesia Power \| …" dan tanpa baris sumber. Bila menggabungkan bahan dari beberapa sumber, samakan semua ke gaya ini. |

## 2. Judul

1. **Judul berbentuk label topik + sub-topik**, bukan kalimat kesimpulan. Contoh: "Latar Belakang Proyek PLTMG Minahasa", "Analisis Biaya Empat Skema Penyediaan", "Prasyarat Keputusan Ambang Utilisasi BESS". Topik memakai kosakata yang lazim di PLN IP: Latar Belakang, Maksud dan Tujuan, Kondisi Eksisting, Analisis Biaya, Analisis Risiko, Prasyarat Keputusan, Peta Jalan, Langkah Berikutnya, Ringkasan Eksekutif, Lampiran.
2. **Pewarnaan dua bagian wajib**: bagian topik biru (`#008AAC`), bagian sub-topik hitam. Ini penanda khas dokumen PLN IP; tanpa itu slide terasa bukan produk internal. `add_slide(prs, topik, subtopik)` sudah mengurus warnanya.
3. **Kesimpulan tidak masuk ke judul, dan tidak ditulis sebagai teks kecil di bawah judul.** Baris subjudul/narasi abu-abu di bawah judul adalah ciri deck buatan AI. Teks pendamping ditulis di badan slide: kolom kanan atau kiri di samping konten (`add_keterangan`), atau tepat di bawah konten selebar bidang isi (`add_keterangan_bawah`). Isinya **keterangan singkat apa yang ditampilkan** grafis/chart/gambar (data apa, satuan/periode, cara membaca warna/garis/ukuran), bukan implikasi, rekomendasi, atau "jadi apa" yang tidak diminta. Kesimpulan hanya ditulis bila berasal dari materi user atau diminta.
4. **Ukuran dan posisi**: x 0,5 in, y 0,28 in, **28pt bold Helvetica**, lebar berhenti 0,25 in sebelum blok logo master (8,61 in pada desain isi 1; dihitung otomatis per desain oleh `add_slide`). Jangan dilebarkan.
5. **Maksimal 2 baris, idealnya 1.** Judul yang tidak muat diringkas, bukan dikecilkan hurufnya. `add_slide` punya jaring pengaman (turun ke 26/24pt) dan mencetak `PERINGATAN`; bila peringatan itu muncul, persingkat sub-topik. Bila tetap 2 baris, pecah di jeda makna; jangan ada satu kata yatim di baris kedua.
6. **Tanpa kicker.** Tidak ada label topik kecil di kiri atas atau kanan atas. Topik sudah menjadi bagian biru pada judul.
7. **Tanpa titik di akhir judul**, tanpa tanda seru, tanpa awalan penanda ("Tahap 1 – ...").
8. **Judul menandai alur.** Bila deretan judul dibaca berurutan, yang terbentuk adalah kerangka dokumen (latar belakang → analisis → prasyarat → langkah). Keterangan per slide tidak dipakai untuk membangun cerita tambahan; ia hanya membantu membaca grafisnya. Keduanya diperiksa sebelum menyerahkan.
9. **Bila judul menyebut jumlah, isi slide harus cocok** ("Tiga Keputusan Hari Ini" berarti ada tiga butir, bukan empat).
10. **Sub-topik spesifik, bukan umum.** "Proyek PLTMG Minahasa 150 MW" lebih baik daripada "Proyek Pembangkit".

## 3. Keterangan dan label lain

1. **Tidak ada teks apa pun di antara judul dan konten.** Tidak ada narasi, subjudul, atau kalimat pengantar di bawah judul. Konten (judul kolom, tabel, chart, grafis) langsung mulai di `BODY_TOP`.
1a. **Keterangan di badan slide**: 13pt biasa, hitam, satu sampai dua kalimat (atau 2–4 butir pendek). Posisinya konsisten dalam satu deck: di kolom kanan untuk pola kiri-kanan, di bawah konten untuk grafis/tabel selebar slide. Tidak perlu keterangan pada slide yang isinya sudah teks yang menjelaskan diri sendiri (ringkasan eksekutif, daftar keputusan), daftar isi, pembatas, dan lampiran.
1b. **Tanpa implikasi atau penjelasan yang tidak dibutuhkan.** Tidak ada kolom "Implikasi", "Arti bagi keputusan", "Insight", "So what", dan tidak ada kalimat "Hal ini menunjukkan …" / "Artinya …" kecuali user memberi atau meminta kesimpulannya.
1c. **Istilah**: pakai istilah Inggris yang lebih lazim daripada padanan Indonesia yang jarang dipakai (milestone, timeline, online, offline, array, email, dashboard; daftar di `kosakata-anti-ai.md` bagian 1a).
2. **Tidak ada subjudul lain**, tidak ada kalimat pembuka tambahan, dan tidak ada kicker.
3. **Tidak ada label nama di atas gambar/tabel dan tidak ada keterangan di bawah gambar.** Yang menjelaskan tabel adalah judul kolom atau judul sumbu.
4. **Judul sumbu** tetap diizinkan: satu baris "data + satuan + periode" tepat di atas chart/tabel dengan garis bawah PRIMARY selebar chart.

## 4. Struktur dan tata letak

**Indeks cepat:** satu pesan (4.1, 4.19) · dua kolom (4.2–4.7) · bawah slide & objek mengambang (4.8–4.9, 4.20) · kartu vs tabel (4.10–4.12) · proses (4.13–4.14) · struktur deck (4.15–4.18, 4.24–4.27) · urutan baca (4.21–4.23)

1. **Satu slide = satu pesan.** Dua pesan → dua slide.
2. **Baca kiri → kanan, bukan atas → bawah.** Isi yang tidak berhubungan tidak ditumpuk vertikal. Pengecualian: satu diagram alur vertikal yang memang berurutan.
3. **Satu tabel per slide.** Jangan menumpuk kartu di atas tabel.
4. **Slide berisi chart/diagram: kiri chart, kanan komentar.** Komentar tidak diletakkan di bawah chart. Chart boleh selebar penuh hanya bila makna sudah tuntas di judul dan chart terbaca tanpa penjelasan.
5. **Tepi bawah kolom kiri dan kanan sejajar.** Bila kolom kanan lebih pendek, tengahkan bullet-nya secara vertikal (judul kolom tetap di atas).
6. **Setiap kolom punya judul kolom yang bermakna berdiri sendiri** ("Biaya penyediaan per skema" / "Arti bagi keputusan investasi"). Hindari judul kolom yang baru bermakna bila dibaca bersambung ("Maka dari itu").
7. **Satu kolom, satu judul kolom.** Jangan menumpuk dua judul kolom dalam satu kolom; struktur di dalamnya dinyatakan dengan bullet bertingkat. Bila kolom kiri adalah tabel, header tabel itulah judulnya (tingginya disamakan dengan judul kolom kanan agar garis bawahnya sejajar).
8. **Tidak ada kotak kesimpulan berwarna** ("Key Takeaway", "Kesimpulan", "Insight") dan tidak ada label semacam itu. Keterangan di bawah konten ditulis sebagai kalimat biasa dengan garis tipis abu di atasnya (`add_keterangan_bawah`). Tidak ada baris sumber.
9. **Jangan boros kotak.** Teks ditulis langsung di latar. Kotak hanya untuk 1–2 hal yang benar-benar perlu ditonjolkan.
10. **Deretan kartu → tabel bersumbu.** Baris = item, kolom = aspek. Kategori besar di kolom kiri boleh digabung (merge) bila bermakna.
11. **Jangan meminta pembaca membandingkan dua kotak** (kotak Opsi A di kiri, Opsi B di kanan). Jadikan tabel: baris = aspek, kolom = opsi.
12. **Item sejajar harus seragam** ukuran kotaknya, jaraknya, sudut pandang, subjek, dan tingkat detailnya.
13. **Proses atau tahap yang berdiri sendiri: chevron.** Bila proses perlu komentar, gunakan alur langkah vertikal di kiri + komentar di kanan; jangan menumpuk dua kolom lain di bawah chevron.
14. **Tahap × cara mencapainya: tabel**, bukan kotak atas-bawah yang hubungannya harus ditebak. Peta jalan: chevron sebagai header waktu, tabel di bawahnya dengan baris Kegiatan / Pelaksana / Keluaran.
15. **Pisahkan ringkasan dan pendalaman.** Deck isi lebih dari 10 slide wajib punya ringkasan eksekutif di awal yang tiap barisnya merujuk halaman pendalaman; slide pendalaman memakai topik judul yang sama dengan nama barisnya. Deck isi lebih dari 10 slide juga wajib punya **daftar isi** setelah ringkasan eksekutif dan **pembatas bab** di awal setiap bab (3–7 bab, `add_section_slide`); nama bab sama dengan topik judul slide di dalamnya. Deck 10 slide atau kurang tidak perlu peta keseluruhan atau pembatas bab.
16. **Daftar isi satu kolom.**
17. **Risiko selalu bersama mitigasinya** di slide yang sama. "Alasan risiko rendah" dan "cara menangani risiko" adalah dua hal berbeda; jangan dicampur.
18. **Slide terakhir tanpa pesan.** Penutup cukup nama unit dan kontak, atau tidak ada sama sekali. Permintaan keputusan ("Direksi diminta menyetujui ...") ditaruh di slide isi sebelumnya dalam bentuk tabel/teks biasa.
19. **Slide yang terlalu padat dipecah bertahap** (2–3 slide dengan tata letak identik, elemen ditambah satu per satu). Syaratnya posisi elemen tidak bergeser sedikit pun antar-slide.
20. **Tidak ada objek mengambang.** Label, chip, atau ikon kecil harus berada di dalam struktur tabel, kolom, atau chart. Keterangan kategori dimasukkan sebagai header baris/kolom. Ikon di kolom sumbu tabel dan pada daftar berikon termasuk bagian struktur, bukan objek mengambang.
21. **Premis, definisi, dan alasan di kiri; contoh, hasil, dan pelaku di kanan.** Bila ragu, yang lebih "hulu" diletakkan di kiri. Hubungan sebab-akibat yang kuat boleh ditandai satu segitiga PRIMARY di tengah celah kolom (satu saja, bukan per baris, bukan panah blok).
22. **Poin di kolom kanan yang merujuk bagian chart ditandai pada chart** (sorotan warna atau label di batang yang sama). Bila kanan membahas sesuatu yang tidak ada di chart, tambahkan ke chart.
23. **Perbandingan kali lipat atau selisih ditunjukkan dari mana ke mana** (titik awal dan panah ke pembanding), bukan hanya ditulis "3 kali".
24. **Masalah diikuti penyelesaiannya.** Slide yang menunjukkan hambatan diikuti slide yang menyelesaikannya dengan judul berbentuk "Hambatan X dapat diatasi dengan Y".
25. **Cerita dalam satu bab maju satu langkah per slide.** Jangan memadatkan dua langkah argumen dalam satu slide.
26. **Nomor atau label hanya diberikan bila akan dirujuk lagi.** Nomor yang tidak pernah dirujuk adalah dekorasi.
27. **Cakupan yang dipersempit ditunjukkan pada gambar keseluruhan**: tampilkan semua komponen, beri bingkai pada bagian yang dibahas dengan catatan "Cakupan kajian ini".

## 5. Warna, kotak, dan garis

1. **Tidak ada sudut membulat.** Semua kotak bersudut siku. Pengecualian hanya label status kecil (tinggi < 0,4 in) atau bila template resmi mensyaratkan.
2. **Perbedaan warna harus bermakna dan diberi legenda di slide yang sama.** Tidak ada kotak gelap hanya supaya "terlihat menonjol".
3. **Kotak berisi warna tidak diberi garis tepi.** Garis tepi hanya untuk elemen tanpa isian.
4. **Garis hanya di tempat yang memisahkan sesuatu.** Tidak ada garis di bawah baris terakhir tabel atau di dasar slide (garis tipis di atas keterangan bawah adalah pemisah, bukan dekorasi).
5. **Sorotan pada tabel perbandingan diberikan pada pihak yang unggul** di aspek itu, bukan selalu pada kolom PLN IP.
6. **Perbandingan dengan pihak lain wajib memuat aspek di mana pihak lain unggul.** Tanpa itu perbandingan tidak kredibel.
7. **Angka hasil ukur internal disertai kondisinya** (periode, sampel, siapa yang mengukur).
8. **Palet selalu menyertakan abu-abu.** Nilai pembanding, netral, atau tidak disorot diberi abu (`#C0C0C0`); warna hanya untuk yang ingin ditonjolkan.
9. **Satu slide, satu sorotan.** Warna sorotan (YELLOW) maksimal satu kali per slide.
10. **Tidak ada bayangan, gradien, efek 3D, emoji.** Ikon dalam lingkaran berwarna DIIZINKAN sebagai pola resmi PLN IP, dengan syarat di aturan 15 di bawah.
11. **Tidak ada garis/pita dekoratif**: garis aksen di bawah judul, pita warna di tepi atas/bawah/samping slide, garis warna di satu sisi kartu.
12. **Isi mengisi minimal ±55% tinggi bidang isi.** Bila kosong, periksa: informasinya kurang (tambahkan makna/premis/catatan di kolom kanan), ukuran chart tidak disesuaikan, atau polanya salah. Jangan menutup ruang kosong dengan dekorasi atau meregangkan jarak baris. Bila isi memang sedikit (daftar 3–5 butir, tujuan, keputusan), taruh isi di kiri dan satu ilustrasi di kolom kanan (§5.16); bila bukan jenis slide itu, tengahkan isi secara vertikal.
13. **Tiga warna PLN IP untuk slide teks dan tabel** (di luar putih, abu `#4D4D4D`, outline `#C0C0C0`). Kombinasi bawaan: DARK `#05365B` + PRIMARY `#008AAC` + TINT `#D1EDF3`, ditambah satu warna sorotan bila perlu. **Chart, flowchart, matriks, peta jalan, dan diagram lain boleh memakai lebih banyak warna** (A1, A4, TEAL, YELLOW, MIST boleh bersamaan) selama setiap warna punya arti dan ada legendanya. Yang dilarang tetap: warna di luar palet, dan warna yang dipakai tanpa makna.
14. **Lampu lalu lintas dikecualikan** dari aturan 3 warna dan boleh dipakai untuk status: hijau `#22B44A`, kuning `#EFCF06`, merah `#E00102`. Syaratnya satu kolom status saja, ada legenda, teks status tetap ditulis (bukan hanya warna), dan baris tidak diwarnai seluruhnya.
15. **Ikon**: dari `assets/icons/` saja supaya tebal garisnya sama. Dua pemakaian yang sah: (a) **daftar berikon**, 3–5 butir setara, ikon putih dalam lingkaran PRIMARY diameter 0,55–0,7 in atau ikon polos 0,28–0,45 in; (b) **kolom sumbu tabel kualitatif** 3–7 baris, ikon putih dalam lingkaran PRIMARY diameter 0,38–0,45 in di kiri label baris (`add_axis_table(..., row_icons=[…])`), seperti tabel visi dan kajian risiko di materi pelatihan PLN IP. Satu ukuran dan satu gaya per slide. Ikon tidak menggantikan data dan tidak diletakkan di sel isi tabel, di judul kolom, atau di setiap judul kecil. Ikon yang sama tidak dipakai untuk dua baris berbeda dalam satu slide.
16. **Ilustrasi** ditempatkan menurut jenis slide:
    - **Wajib**: daftar isi dan setiap pembatas bab (deck > 10 slide); slide maksud-tujuan, ruang lingkup, prasyarat, permintaan keputusan, dan langkah berikutnya yang berbentuk daftar berikon 3–5 butir.
    - **Boleh**: slide isi yang kolom kanannya kosong ≥ 4 in karena isinya memang sedikit; penutup.
    - **Tidak pernah**: slide dengan chart, tabel selebar penuh, matriks, atau peta jalan; ringkasan eksekutif; lampiran. Ruang kosong di sana berarti informasinya kurang.
    - **Kerapatan**: minimal 1 slide berilustrasi per ±6 slide isi dan tidak ada 7 slide berturut-turut tanpa aset visual (ikon atau ilustrasi). Bila batas ini belum tercapai, perbaiki struktur deck (daftar isi, pembatas bab, slide tujuan berikon), bukan menempelkan ilustrasi ke slide analisis.
    - **Bentuk**: maksimal satu per slide, lebar paling banyak ±4,6 in, dimuat utuh di kolom kanan (`fit_illustration`), tidak di belakang teks, tidak dipotong, tidak menimpa logo. Satu ilustrasi tidak dipakai dua kali dalam satu deck.
    - **Pilihan**: dari `assets/illustrations/` saja; isinya harus nyambung dengan pesan slide (tabel tema di `KATALOG.md`, `saran_ilustrasi()`). Ilustrasi flat untuk topik pembangkit, unDraw untuk orang/rapat/dokumen/keuangan/hukum. Keduanya boleh dalam satu deck, tidak dalam satu slide.

## 6. Tabel

| Hal | Aturan |
|---|---|
| Header | 2pt lebih besar dari isi, bold, warna INK, **tanpa isian warna**, garis bawah PRIMARY `#008AAC` 1.5pt |
| Baris | Tanpa zebra, tanpa latar baris. Antarbaris garis tipis RULE 0.75pt. Baris terakhir tanpa garis bawah |
| Kolom sumbu (paling kiri) | Bold, 2pt lebih besar dari isi. Label harus spesifik ("Pembangkit gas", bukan "Lainnya" atau "Umum") |
| Ukuran | Isi minimal 12pt, header 14pt. Label di dalam diagram minimal 9pt |
| Nama kolom | Kata benda konkret yang menyebut isi sel ("Capex PLN IP", "Mulai operasi"), bukan "Fakta", "Keterangan", "Lain-lain". Tanpa singkatan buatan |
| Isi sel | Satu kalimat boleh ditulis langsung. Dua kalimat atau lebih → bullet. Sel penjelasan (alasan, contoh, mitigasi) yang punya 2 hal atau lebih ditulis sebagai 2–3 bullet |
| Sel tidak relevan | "—" dengan latar TINT `#D1EDF3` dan teks GRAY, bukan sel kosong |
| Sel penting | Sel yang langsung memengaruhi keputusan diberi bold. Tidak semua sel sama tebal |
| Baris sesuai sumbu | Setiap baris harus anggota kategori yang didefinisikan kolom sumbu. Uji dengan membaca "Apakah [baris] termasuk [label sumbu]?" Fakta makro atau kesimpulan tidak disisipkan sebagai baris |
| Kolom sesuai pesan | Kolom yang tidak mendukung pesan dihapus. Isi setiap kolom punya sudut pandang dan tingkat detail yang sama |
| Hanya yang berubah | Tabel perubahan hanya memuat yang berubah; yang tetap cukup satu baris catatan |
| Sumber | Tidak dipakai (materi internal PLN IP). Asumsi penting ditulis sebagai bagian isi |
| Baris tinggi | Bila baris diregangkan agar tabel mengisi ruang, teks dirata-tengahkan vertikal |
| Daftar definisi pendek | 2–3 definisi cukup ditulis "Istilah: penjelasan" satu baris masing-masing |

## 7. Chart dan diagram

1. **Tren, komposisi, dan distribusi selalu chart.** Jangan menaruh deret angka tahunan dalam tabel.
2. **Pilih bentuk dasar, jangan berkreasi.** Perbandingan item → bar horizontal urut; tren waktu → kolom atau garis; komposisi → kolom bertumpuk (pie hanya bila ≤4 bagian dan satu periode); distribusi → histogram/kolom; hubungan dua variabel → scatter; kontribusi naik-turun → waterfall.
3. **Satu chart, satu sorotan, satu makna.** Yang dibahas PRIMARY, lainnya abu `#C0C0C0`. Seri kedua bila benar-benar perlu: A1 `#1B4F60` (ingat batas 3 warna).
4. **Label nilai langsung pada data**, sumbu nilai disembunyikan, tanpa gridline, tanpa legenda untuk satu seri. Legenda bila ada diletakkan dekat data.
5. **Judul sumbu di atas chart**: "Data, satuan, periode".
6. **Indikator yang punya batas atas (persentase capaian, rasio) digambar dengan skala penuh** 0–100%, dengan garis acuan bila perlu. Jangan memotong sumbu sehingga perbedaan kecil terlihat besar.
7. **Chart native PowerPoint** (bisa diedit), bukan gambar, kecuali jenisnya tidak didukung.
8. **Orang dan dokumen dalam diagram digambar sebagai ikon satu warna sederhana** dengan label; bentuk tunggal ("Pengguna", bukan kerumunan).
9. **Tanda ○ ◑ ● (harvey ball) dibuat dari bentuk** (oval + pie), bukan karakter teks yang posisinya meleset.
10. **Urutan tabel dan chart yang menampilkan hal sama harus sama**, dan yang mendefinisikan urutan diletakkan di kiri.
11. **Baris yang punya urutan bermakna diberi sumbu arah** (panah/baji di kiri dengan label "makin besar kebutuhan").

## 8. Bahasa dan penulisan

1. **Kalimat aktif dengan subjek dan predikat**, di judul maupun isi. "Tim operasi menyepakati pola dispatch" lebih jelas daripada "Penyepakatan pola dispatch". Untuk memendekkan, buang kata sifat, jangan buang subjek/predikat.
2. **Hindari pemadatan menjadi kata benda abstrak**: "peningkatan", "optimalisasi", "penguatan", "pengembangan" yang berderet tanpa pelaku. Tulis siapa melakukan apa.
3. **Bullet**: bullet asli PowerPoint (tingkat 1 "•", tingkat 2 "–"), jangan diketik manual. Satu bullet satu gagasan. Pernyataan tunggal tidak diberi bullet.
4. **Bentuk akhir bullet setingkat seragam**: semua kalimat dengan predikat, atau semua frasa kata benda. Tingkat 1 kalimat dan tingkat 2 frasa boleh, asal konsisten.
5. **Tanda kurung secukupnya.** Pemisah label pakai titik dua. Tanpa em dash (—) untuk menyambung kalimat.
6. **Istilah Inggris boleh** bila itu yang lazim dipahami di lingkungan PLN IP (*dispatch*, *take or pay*, *commercial operation date*, *reserve margin*, *build own operate*). Tulis miring; di `plnip_deck.py` apit dengan tanda bintang. Jangan menerjemahkan paksa istilah teknis yang justru asing bila diterjemahkan, dan jangan memakai Inggris untuk hal yang sudah lazim berbahasa Indonesia ("pembangkit", bukan "power plant"; "peta jalan" atau *roadmap*, pilih salah satu lalu konsisten).
7. **Satu konsep, satu istilah** di seluruh deck. Pilih salah satu dan konsisten: pemangku kepentingan/stakeholder, peta jalan/roadmap, belanja modal/capex, pembangkit/power plant. Istilah Inggris yang sudah baku di internal PLN (COD, EPC, PPA, capex) boleh, tetapi konsisten.
8. **Singkatan ditulis lengkap pada penggunaan pertama**: "Battery Energy Storage System (BESS)", "Pembangkit Listrik Tenaga Mesin Gas (PLTMG)", "Rencana Usaha Penyediaan Tenaga Listrik (RUPTL)". Singkatan internal yang tidak dikenal pembaca luar dijelaskan atau dihindari.
8. **Istilah kiasan diberi tanda petik dan didefinisikan** ("fat burning", "quick win").
9. **Hapus kosakata dan struktur "rasa AI"**. Daftar lengkap di `kosakata-anti-ai.md`.
10. **Deskripsi proses dimulai dari pelaku** ("Sistem menandai data ganjil; analis memverifikasi"). Untuk otomasi/AI, selalu sebutkan titik keputusan manusia.
11. **Istilah internal tidak dibawa ke dokumen eksternal** tanpa penjelasan.
12. **Pengulangan pola "Label: penjelasan"** di banyak sel/bullet adalah tanda struktur kurang: pisahkan menjadi kolom tabel atau tingkat bullet.
13. **Format angka Indonesia**: desimal koma (1,2), ribuan titik (2.450), "Rp 410 miliar" / "Rp 1,2 triliun", persen tanpa spasi (18%), rentang tahun dengan en dash (2026–2030), satuan teknis konsisten (MW, MWh, GWh, kV). Kode format chart `#,##0` mengikuti pengaturan regional komputer; periksa tampilannya.
14. **Ringkasan eksekutif mengikuti daftar judul**: tiap baris mewakili satu slide isi, satu baris terpenting boleh bold.
15. **Catatan satu kalimat di bawah chart dihapus bila tanpa itu slide tetap dipahami.**
16. **Empat bullet sejajar atau lebih yang bisa dikelompokkan**, dikelompokkan menjadi dua induk dengan anak masing-masing. Daftar yang memang satu sumbu (wilayah, kuartal, unit) tidak dipaksa dikelompokkan.
17. **Teks akhir dibaca ulang sebagai penutur Bahasa Indonesia.** Bila kalimat benar tetapi terasa terjemahan atau kaku, perbaiki. Judul adalah bagian paling rawan.

## 9. Pemeriksaan sebelum menyerahkan

**Mesin (wajib 0 FAIL):** `python3 scripts/check_deck.py deck.pptx`, lalu `validate.py` dari skill pptx.

**Visual (render semua slide, periksa satu per satu):**
- Judul tidak sebaris dengan logo, turun ke bawah logo, atau kotaknya menabrak logo; logo berbeda tinggi atau tidak segaris
- Teks terpotong, meluap dari kotak, atau tertimpa elemen lain
- Kata yatim di baris terakhir judul atau sel
- Tepi bawah kolom kiri-kanan tidak sejajar; garis bawah judul kolom kiri-kanan tidak sejajar
- Setengah bawah slide kosong; isi menempel di atas dengan ruang kosong besar di bawah
- Label chart bertumpuk; batang terlalu tipis; sorotan tidak pada data yang dibahas
- Legenda ada untuk setiap warna bermakna

**Isi (tidak bisa dicek mesin):**
- Judul dan chart/diagram di slide yang sama tidak saling bertentangan
- Kata penilaian ("signifikan", "memadai", "terbatas", "tidak masalah") punya bukti di slide itu
- Slide bagian akhir bukan pengulangan slide awal
- Jumlah di judul cocok dengan isi
- Angka yang diasumsikan ditandai

**Review mata segar:** ikuti `review-mata-segar.md`.

**Bila menerima koreksi:** pastikan dulu koreksi itu masih berlaku di versi terbaru (reviewer bisa melihat versi lama), lalu perbaiki, lalu tambahkan satu baris aturan di dokumen ini.
