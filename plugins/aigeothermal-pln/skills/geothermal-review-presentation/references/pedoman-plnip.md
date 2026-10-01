# Pedoman internal PLN IP (pelatihan presentasi 2023)

Ringkasan aturan dari materi pelatihan *PLN IP presentation skills* (13 Oktober 2023) yang dipakai
sebagai standar internal, ditulis ulang dengan kalimat sendiri. Bila isi dokumen ini bertentangan
dengan `aturan-slide.md`, **dokumen ini yang menang untuk hal-hal yang menyangkut standar PLN IP**
(palet, format resmi, lampu lalu lintas); untuk selebihnya `aturan-slide.md` tetap berlaku.

## 1. Tiga pertanyaan sebelum mendesain slide

Dijawab dulu sebelum menyentuh PowerPoint: **mengapa** paparan ini diberikan, **siapa** yang harus
diyakinkan, dan **berapa lama** waktunya. Jawaban ketiganya menentukan jumlah slide, kedalaman, dan
bentuk ceritanya.

## 2. Struktur piramida

Satu gagasan utama (*governing thought*) berupa jawaban atau rekomendasi, ditopang kelompok argumen,
lalu data pendukung di lapis bawah. Uji piramida:
- Gagasan utama harus tepat sasaran, mencakup keseluruhan, kuat, dan bisa dibuktikan.
- Argumen di satu lapis harus saling lepas dan bersama-sama lengkap (MECE), serta setara tingkatannya.
- Dibaca ke atas menjawab "jadi apa?", dibaca ke bawah menjawab "mengapa/bagaimana?".

Dua bentuk piramida, dipilih sesuai audiens:
- **Pengelompokan** (gagasan utama lalu "karena A, B, C") untuk audiens yang sudah sepaham, waktu
  sempit, atau perhatian pendek. Ini bentuk baku untuk komunikasi *top-down*.
- **Argumen** (situasi → komplikasi → implikasi, "ya… tetapi… maka") ketika penolakan diperkirakan,
  hubungan dengan lawan bicara belum kuat, atau menghadap manajemen yang lebih senior.

## 3. Storyboard

Alur kerjanya: piramida → daftar pesan berurutan (*storyline*) → draf kasar tiap halaman. Satu baris
alur menjadi satu slide, dan judul slide itulah barisnya. Ini sama dengan langkah "alur cerita dulu"
di `SKILL.md`.

## 4. Ringkasan bukan sintesis

- **Ringkasan** hanya menyatakan ulang fakta secara padat ("PLN Mobile diunduh 10 juta kali, hanya 5%
  jadi pengguna aktif, penurunan terbesar di proses registrasi").
- **Sintesis** menyatakan artinya dan tindakannya ("mempermudah registrasi dan memperbaiki pengalaman
  pengguna akan menaikkan konversi").

Di format PLN IP (keputusan user), judul slide berisi label topik (misalnya "Analisis Biaya") dan
teks pendamping grafis hanya **keterangan singkat apa yang ditampilkan**, ditaruh di badan slide
(`add_keterangan`, `add_keterangan_bawah`). Sintesis dan rekomendasi hanya ditulis bila berasal dari
materi user atau diminta, biasanya di ringkasan eksekutif atau slide keputusan; jangan menambahkan
"jadi apa" sendiri di setiap slide.

## 5. Isi wajib sebuah deck

Halaman judul, ringkasan eksekutif, daftar isi/agenda, halaman isi berdata, slide jeda bila paparan
panjang, halaman langkah berikutnya, dan halaman penutup.

## 6. Memilih bentuk chart menurut tujuan

| Tujuan | Kata kunci pesan | Bentuk |
|---|---|---|
| Perbandingan antar-item | lebih besar, terbesar, setara | bar/kolom |
| Komposisi | porsi, bagian dari total | kolom bertumpuk, pie (maks 4 bagian), 100% |
| Deret waktu | naik, turun, berubah, tren | kolom atau garis |
| Korelasi | berhubungan dengan, meningkat seiring | scatter, bubble (3 variabel) |
| Sebaran | terkonsentrasi, pola, pusat | histogram |
| Penyebab naik-turun | kontribusi, selisih | waterfall |
| Jadwal dan proses | tahapan, tenggat | gantt/timeline |

Prinsipnya: isi menentukan bentuk, chart hanya dipakai bila memperjelas fakta secara visual,
dibatasi pada yang penting saja, dan menyatu dengan teks di sekitarnya.

## 7. Delapan tip membuat exhibit

1. Chart dibuat sesederhana mungkin.
2. Satu slide, satu ukuran huruf.
3. Objek sejenis dibuat berukuran sama.
4. Objek disejajarkan dan jaraknya dibuat rata, mendatar maupun tegak.
5. Tata letak seimbang; ruang kosong dimanfaatkan, bukan ditutupi.
6. Teks rata kiri; rata tengah hanya di dalam lingkaran atau bentuk tak beraturan.
7. Angka rata kanan dengan jumlah desimal yang sama.
8. Tanpa bayangan, tanpa 3D, tanpa warna berlebihan, tanpa animasi.

Tiga penentu exhibit yang baik: **akurasi** (tidak ada salah data), **konsistensi** (bahasa, jenis dan
ukuran huruf, skema warna, bentuk), dan **estetika** (koordinasi warna, tidak berjejal, tanpa bayangan).

## 8. Alasan paparan gagal diterima

Menurut data yang dikutip di pelatihan, keluhan terbesar audiens berturut-turut: pembicara membaca
slide, kalimat penuh alih-alih butir ringkas, teks terlalu kecil, pilihan warna membuat slide sulit
dibaca, dan diagram terlalu rumit. Empat dari lima keluhan itu soal slide, bukan soal isi.

## 9. Format standar PLN IP

- **Palet:** lihat tabel palet di `SKILL.md`. Pedoman menganjurkan 3 warna PLN IP per dokumen; di
  skill ini anjuran itu berlaku untuk slide teks dan tabel, sementara chart, flowchart, dan diagram
  boleh memakai lebih banyak asal setiap warna punya arti dan legenda. Warna lampu lalu lintas
  (hijau, kuning, merah) untuk status dikecualikan. Catatan pedoman: untuk teks, hitam lebih baik
  daripada abu.
- **Huruf template korporat:** judul 32pt Helvetica, kapitalisasi kalimat, abu gelap; isi 20pt Helvetica.
  Ukuran ini untuk deck yang harus persis mengikuti template korporat (misalnya materi sosialisasi
  atau paparan pimpinan dengan sedikit elemen per slide).
- **Deck analitis** (kajian, perbandingan skema, evaluasi proyek) memakai skala huruf skill ini
  (judul 28pt, isi 13–14pt, tabel 12pt), karena satu slide memuat tabel bersumbu atau chart plus
  kolom makna. Jangan mencampur dua skala dalam satu deck.
- Deck dibangun dari master native PLN IP (`assets/masters/`, lihat `master-native.md`) dengan
  python-pptx, bukan dari nol. `Template_PLNIP.pptx` hanya bila user memintanya.

## 10. Yang berbeda dari `aturan-slide.md`

Dua hal di skill ini dilonggarkan agar sesuai standar PLN IP:
- **Ikon dalam lingkaran berwarna** boleh, karena itu pola resmi PLN IP (`add_icon_list`).
  Syaratnya dipakai untuk daftar butir setara, ukuran seragam, bukan hiasan di tiap judul kecil.
- **Warna lampu lalu lintas** boleh untuk status (Done/Hold, hijau/kuning/merah), karena
  dikecualikan secara eksplisit oleh pedoman. Tetap pakai satu kolom status, ada legenda, dan
  jangan mewarnai seluruh baris.
