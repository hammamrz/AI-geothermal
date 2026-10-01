# Aturan khusus TVV (menang atas aturan-slide.md bila bertentangan)

`aturan-slide.md` (disalin dari skill presentasi-pln-ip) tetap berlaku untuk bahasa, struktur, tabel, chart, dan QA.
Dokumen ini hanya mencatat bagian yang **berbeda** karena Template TVV. Nomor dalam kurung merujuk aturan-slide.md.

## 1. Berkas awal dan desain (menggantikan §1 "Berkas awal", "Logo", "Template")

1. Setiap deck TVV berangkat dari `assets/masters/TVV_Master.pptx` lewat `new_deck()` di `tvv_deck.py`. Logo
   Danantara + PLN IP ada di gambar latar master; jangan ditempel ulang, jangan ditutup kotak putih.
2. Cover selalu layout cover Template TVV (ilustrasi PLTA/PLTS, PROPER di kiri atas) lewat `set_cover`.
3. Desain isi default `'isi'` (latar biru muda + siluet pembangkit, dipakai mayoritas slide template). Satu deck,
   satu desain isi. Pilihan lain hanya bila user meminta: `'isi-putih'`, `'isi-gelombang'`, `'isi-polos'`.
4. `save()` membuang master dan layout yang tidak dipakai, jadi ukuran deck tetap kecil.

## 2. Judul (menggantikan §2.4)

1. Judul **20pt bold Helvetica** di x 0,4 in, y 0,26 in, lebar 8,71 in (berhenti 0,25 in sebelum logo). Turun ke
   18/16pt bila perlu; bila `add_slide` mencetak PERINGATAN, persingkat sub-topik.
2. Pola dua warna tetap: topik biru + sub-topik hitam. Untuk slide proyek, topik = bagian kajian dan sub-topik =
   nama proyek + kapasitas: `Profil Proyek` `PLTA Sulbagsel (Kuota) Tersebar Tambahan II 400 MW`,
   `Ringkasan KKO` `… (2/3)`, `Ringkasan KKF`, `Kajian Risiko`, `Indicative Timeline`.
3. Slide tabel bersambung memberi penanda halaman "(1/2)" di akhir sub-topik (otomatis di `add_tabel_bersambung`).

## 3. Narasi di bawah judul (menggantikan §2.3 dan §3.1)

Template TVV memakai satu kalimat ringkasan abu di bawah judul. Di skill ini itu **diizinkan** dengan syarat:

1. Hanya lewat `add_slide(..., narasi='...')` (14pt, abu `#4D4D4D`, maksimal 2 baris). Teks kecil lain di bawah
   judul tetap dilarang (checker FAIL).
2. Isinya **rangkuman isi slide dengan angka kunci**, bukan kalimat pengantar: "Dari 255 proyek alokasi RUPTL,
   54 proyek sudah masuk RKAP 2026 dan 32 proyek diusulkan pada RKAP 2027". Bukan "Berikut adalah progres …".
3. Angka di narasi harus sama persis dengan angka di tabel/grafis slide itu.
4. Tidak semua slide perlu narasi. Pakai pada slide yang pesannya bisa diringkas satu kalimat berangka (latar
   belakang, progres alokasi, asumsi, KKF, risiko, timeline). Slide tabel data murni (status dokumen, rekap
   proyek), outline, pembatas, dan profil proyek biasanya tanpa narasi.
5. Kesimpulan yang berasal dari dokumen user (mis. "Proyek layak secara finansial") boleh menjadi narasi. Kesimpulan
   karangan sendiri tetap dilarang (§3.1b).

## 4. Baris sumber (menggantikan §6 "Sumber" dan §1 "Template")

1. Baris sumber **diizinkan** di bawah bidang isi lewat `add_sumber(s, 'Sumber: …')` (11pt abu, y 6,9 in), untuk
   slide yang memuat parameter/angka acuan dari dokumen lain (asumsi keekonomian, rekap dari FIN).
2. Satu baris, menyebut dokumen asal, bukan kalimat penjelasan. Tanpa footer teks lain.

## 5. Tabel (tambahan untuk §6)

1. **Gaya sumbu** (default `add_tabel`) untuk tabel kualitatif 3–10 baris: header tanpa isian bergaris bawah
   PRIMARY, kolom sumbu bold navy. Sama dengan aturan PLN IP.
2. **Gaya data** (`gaya='data'`) khusus tabel angka padat ≥ 8 kolom (status dokumen, rekap proyek): header berisi
   PRIMARY dengan teks putih bold, antarbaris garis tipis, tanpa zebra. Ini pengecualian §6 "Header" yang mengikuti
   kebutuhan keterbacaan template.
3. Ukuran isi tabel data minimal **10pt** (menggantikan batas 12pt/11pt). Tabel yang butuh < 10pt dipecah ke
   beberapa slide (`add_tabel_bersambung`), bukan dikecilkan.
4. Kolom angka rata kanan, kolom kode/status rata tengah (`rata=[...]`). Satuan ditulis di header kolom.
5. Sel "—" (`{'na': True}`) berlatar TINT; kolom usulan tahun berjalan boleh disorot seluruhnya (`sorot_kolom`).
6. Kelompok baris (mis. "Regulasi dan kebijakan PLN" untuk lima dokumen) memakai sel gabungan di kolom sumbu
   (`gabung=[0]`, sel lanjutan `None`), dengan ikon di kolom sumbu bila kategorinya 2–4 (`ikon={baris: 'nama'}`).

## 6. Status, risiko, dan timeline (tambahan untuk §5.14)

1. **Status dokumen** memakai penanda bulat lampu lalu lintas (hijau lengkap, kuning dalam proses, merah belum ada)
   di banyak kolom dokumen sekaligus. Ini pengecualian §5.14 "satu kolom status": matriks kelengkapan dokumen
   memang satu sumbu status. Syaratnya legenda selalu ada (`legenda='status'`) dan tidak memakai emoji.
2. **Matriks risiko 5×5** memakai lima warna tingkat risiko (Low hijau tua, Low to Moderate hijau, Moderate kuning,
   Moderate to High oranye, High merah) dengan legenda. Warna ini hanya untuk matriks risiko.
3. **Timeline proyek**: batang kegiatan navy, milestone belah ketupat PRIMARY, pita tahap bergantian abu terang.
   Kolom per semester (SM1/SM2). Tanggal kegiatan hanya dari user; `TAHAP_BAKU` hanya urutan labelnya.

## 7. Aset visual (menggantikan §5.16 "Kerapatan")

Deck TVV adalah deck data. Kuota ilustrasi (1 per 6 slide) **tidak berlaku** dan checker tidak memeriksanya.
Aset visual berasal dari struktur: ikon di kolom sumbu tabel latar belakang, ikon analisis KKO, peta lokasi,
waterfall, matriks risiko, dan timeline. Ilustrasi flat (`assets/illustrations/svg/`: plta, plts, pltb, pltu,
bess, transmisi, pipa-gas, kota-jaringan, alur-tahapan) boleh dipakai di slide permohonan persetujuan atau penutup
bila user menginginkan, maksimal satu per slide.

## 8. Struktur deck (menggantikan §4.15)

1. Deck TVV > 10 slide dibuka dengan **Outline Pembahasan** (`add_outline`), bukan ringkasan eksekutif + daftar isi
   gaya PLN IP. Judul bab di outline sama dengan topik biru di judul slide bab itu.
2. Pembatas bagian (`add_divider`) memisahkan rekap portofolio dari pengembangan bisnis proyek; pembatas proyek
   (`add_divider_proyek`) membuka setiap blok proyek.
3. Urutan dan isi baku ada di `struktur-deck-tvv.md`.
