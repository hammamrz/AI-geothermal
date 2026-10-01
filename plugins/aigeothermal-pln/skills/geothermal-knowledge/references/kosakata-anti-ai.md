# Kosakata dan gaya "rasa AI" dalam Bahasa Indonesia

Tujuan: menghapus kesan "ditulis AI" dari slide, email pengantar, dan catatan. Tulisan AI mudah dikenali bukan karena satu kata, tetapi karena kombinasi: kata besar yang kosong, struktur kalimat berulang, dan kerapian yang terlalu seragam.

Dipakai: saat menulis, lalu sekali lagi sebelum menyerahkan (swa-periksa 30 detik di bagian akhir). Kata dengan keyakinan tinggi juga diperiksa oleh `scripts/check_deck.py` sebagai WARN. Konteks tetap menentukan: "berkelanjutan" dalam "energi berkelanjutan" sebagai istilah teknis tidak masalah.

## 1. Kata dan frasa yang dihapus atau diganti

| Rasa AI | Ganti dengan |
|---|---|
| komprehensif, holistik, menyeluruh (tanpa bukti) | sebut cakupannya: "mencakup 4 unit dan 2 skema" |
| sinergi, bersinergi | sebut kerja samanya: "tim operasi dan perencanaan memakai data beban yang sama" |
| optimalisasi, mengoptimalkan | sebut apa yang naik/turun dan berapa: "menurunkan biaya bahan bakar 6%" |
| memberdayakan, mendorong, mengakselerasi, memperkuat | kata kerja biasa: memakai, menambah, mempercepat X bulan |
| transformasi, transformatif, revolusioner, inovatif, terobosan | sebut perubahannya secara konkret |
| krusial, esensial, sangat penting, memainkan peran penting, menjadi kunci | buang; bila penting, tunjukkan akibatnya bila tidak dilakukan |
| lanskap, ekosistem (sebagai kiasan), paradigma | pasar, sistem, pihak-pihak yang terlibat |
| secara signifikan (tanpa angka) | angkanya |
| solusi terintegrasi, end-to-end, seamless, robust, leverage | jelaskan komponennya |
| di era digital / di tengah dinamika / seiring perkembangan zaman | buang |
| dalam rangka, guna mewujudkan, adapun, yang mana | untuk, agar; atau pecah kalimat |
| pentingnya X, peran strategis X | kesimpulan tentang X |
| langkah strategis, inisiatif strategis (tanpa isi) | nama langkahnya |
| key takeaway, insight utama, kesimpulan utama (sebagai kotak) | hapus; cukup keterangan singkat apa yang ditampilkan grafis (bagian 1b) |
| mari kita, perlu dicatat bahwa, penting untuk dicatat | buang |

## 1a. Padanan Indonesia yang tidak umum: pakai istilah Inggris

Di lingkungan PLN IP banyak istilah Inggris lebih cepat dipahami daripada padanan resminya. Padanan yang jarang dipakai membuat slide terasa kaku dan "hasil terjemahan mesin". Pakai kolom kanan. (`check_deck.py` memberi WARN untuk kolom kiri.)

| Jangan | Pakai |
|---|---|
| tonggak, tonggak capaian | milestone |
| linimasa | timeline |
| daring / luring | online / offline |
| larik | array |
| surel | email |
| pranala, tautan (di slide) | link |
| peladen | server |
| gawai | gadget / device |
| tetikus | mouse |
| tagar / warganet / swafoto | hashtag / netizen / selfie |
| dasbor, papan pemuka | dashboard |
| pelantar | platform |
| perisian | software |
| rintisan (usaha) | startup |
| mahadata / komputasi awan / rantai blok | big data / cloud / blockchain |
| salindia, tayangan salindia | slide |
| narahubung | contact person |
| sangkil / mangkus | efisien / efektif |

Tetap pakai istilah Indonesia yang memang lazim di PLN IP (pembangkit, gardu induk, beban puncak, pengadaan, perizinan, kajian). Ukurannya: istilah mana yang dipakai rekan kerja dalam rapat dan dokumen internal.

## 1b. Teks pendamping grafis: keterangan, bukan implikasi

Teks di samping atau di bawah grafik, chart, tabel, atau gambar cukup menjelaskan **apa yang ditampilkan** dan cara membacanya. Jangan menambahkan implikasi, rekomendasi, atau "jadi apa" yang tidak diminta dan tidak ada di materi user.

| Jangan | Pakai |
|---|---|
| "Implikasi: kenaikan harga gas menghapus manfaat efisiensi, sehingga manajemen perlu …" | "Perubahan EBITDA dari RKAP ke prognosa 2026 per faktor; merah = penurunan, biru = kenaikan." |
| "Hal ini menunjukkan bahwa …", "Artinya, …", "Dengan demikian, …" | langsung sebut isi grafis: data, satuan, periode, arti warna/garis |
| Judul kolom "Implikasi", "Arti bagi keputusan", "Insight", "So what" | tanpa judul kolom, atau "Keterangan" |

## 2. Struktur kalimat yang dirombak

- **"Tidak hanya X, tetapi juga Y"** berulang. Tulis dua kalimat pendek atau pilih yang paling penting.
- **Tiga serangkai**: "efisien, andal, dan berkelanjutan", "cepat, tepat, dan akurat". Pilih satu yang bisa dibuktikan.
- **Pola judul seragam**: semua judul "X: Y" atau "Mewujudkan ... melalui ...". Variasikan secara alami sesuai isi.
- **Deret kata benda abstrak**: "Penguatan tata kelola pengelolaan aset untuk peningkatan kinerja". Tulis siapa melakukan apa.
- **Kalimat pasif beruntun**: "telah dilakukan", "akan dilaksanakan", "perlu dilakukan". Sebut pelakunya.
- **"Hal ini"** di awal banyak kalimat. Sebut bendanya.
- **Kata sambung di tiap awal kalimat**: selain itu, lebih lanjut, oleh karena itu, dengan demikian, di sisi lain. Sebagian besar bisa dihapus.
- **Rangka "Pertama, kedua, terakhir" dan "Terdapat 3 poin utama"** sebagai struktur default.
- **Em dash (—)** untuk menyambung atau menyisipkan. Pakai titik, koma, atau titik dua.
- **Penghalus berlebihan**: "dapat dikatakan", "cenderung", "berpotensi untuk dapat". Katakan seberapa yakin dan apa dasarnya.
- **Campur Inggris–Indonesia tanpa pola**: "melakukan improvement untuk meng-enhance performance". Pilih satu bahasa per istilah dan konsisten.

## 3. Nada dan penutup

- Pembuka ramah yang kosong: "Dalam era transisi energi yang dinamis ini, ..."
- Penutup template: "Demikian yang dapat kami sampaikan", "Semoga bermanfaat", "Mari bersama wujudkan ...". Di slide tidak ada; di email cukup satu baris konkret tentang tindak lanjut.
- Slogan di akhir slide atau deck ("Bersama Menuju Net Zero").
- Semua kalimat sama panjang dan sama sempurna. Tulisan manusia punya variasi.
- Optimisme tanpa dasar: "dengan langkah ini target pasti tercapai".

## 4. Tampilan yang terasa AI

- Emoji dan simbol sebagai penanda (🚀 ✅ 📊 ⚡ 👉 ▪).
- Bold di banyak frasa per paragraf. Bold hanya untuk satu hal terpenting.
- Semua isi dijadikan bullet, termasuk pernyataan tunggal.
- Tabel lampu lalu lintas merah-kuning-hijau.
- Ikon dalam lingkaran berwarna di samping setiap judul kecil.
- Garis aksen di bawah judul, pita warna di tepi slide atau kartu.
- Kartu bersudut bulat dengan bayangan.
- Setiap slide memakai pola yang sama (judul + 3 kartu).

## 5. Tanda tulisan manusia yang baik

- Pendek, satu kalimat satu gagasan.
- Angka, tanggal, nama unit, dan nama opsi disebut spesifik.
- Berani menyimpulkan, dan jujur bila data belum cukup ("data realisasi 2026 belum tersedia; perkiraan memakai tren 2023–2025").
- Istilah yang dipakai sehari-hari di unit kerja pembaca.

## 6. Swa-periksa 30 detik

1. Sudah menghapus kata dari tabel bagian 1 dan kata sambung yang tidak perlu?
2. Sudah menghapus emoji, simbol, dan bold berlebih?
3. Judul berbentuk label topik + sub-topik, dan tidak ada teks kecil di bawahnya?
4. Setiap kata penilaian ("signifikan", "memadai") punya angka atau bukti?
5. Bila dibacakan keras, apakah terdengar seperti orang di unit ini berbicara?
6. Tidak ada padanan Indonesia yang jarang dipakai (tonggak, linimasa, daring, luring, larik, surel …)? Lihat bagian 1a.
7. Teks pendamping grafis hanya menjelaskan apa yang ditampilkan, tanpa implikasi tambahan? Lihat bagian 1b.

## Perawatan

Setiap kali ada kata atau kalimat yang dikomentari "kok kayak AI", tambahkan satu baris di sini dan, bila kata itu jelas, tambahkan ke `AI_SMELL` di `scripts/check_deck.py`.
