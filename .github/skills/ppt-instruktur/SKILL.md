---
name: ppt-instruktur
description: Buat atau revisi PowerPoint instruktur yang siap dibawakan di kelas. Gunakan bila pengguna menyebut PPT Instruktur, slide pengajar, deck fasilitator, modul training, micro-lab, workshop, atau meminta materi ajar yang mengikuti contoh cover program dan modul harian. Hasilkan PPTX editable dengan pola visual, alur praktik, dan speaker notes yang sesuai audiens.
---

# PPT Instruktur

Hasilkan PowerPoint yang dapat langsung dibawakan instruktur. Gunakan bahasa pengguna, secara default bahasa Indonesia. Gunakan istilah teknis yang dikenal peserta dan kasus yang sesuai pekerjaan mereka.

## Pilih alur mengajar

1. Ambil topik, profil peserta, kompetensi akhir, durasi, bahan, dan format keluaran dari permintaan. Baca seluruh file yang dirujuk, termasuk tabel, gambar, dan instruksi praktik. Pertahankan urutan lab, angka, jadwal, dan istilah yang diberikan. Jika informasi ringan belum tersedia, gunakan asumsi yang masuk akal dan sebutkan saat menyerahkan hasil. Tanyakan hanya keputusan yang sungguh mengubah isi.
2. Pilih cakupan. **Pengantar program** berisi cover foto, pemantik, dan peta modul berhuruf. **Modul harian** dibuka dengan cover bab dan tujuan, dilanjutkan dengan rangkaian konsep, demonstrasi, latihan, dan penutup. **Paket beberapa hari** memiliki satu pengantar dan modul harian sesuai permintaan. Untuk sesi singkat, pilih satu siklus konsep–contoh–praktik–umpan balik. Sesuaikan jumlah slide dengan kegiatan dan waktu.
3. Tentukan hasil kerja peserta sebelum menulis slide. Buat pemetaan internal sederhana untuk tiap tujuan: aksi peserta, contoh, praktik, bukti keberhasilan. Jumlahkan waktu penjelasan, demonstrasi, latihan, debrief, dan jeda sesuai jadwal. Jangan mengarang jam atau mengubah durasi sumber.
4. Susun storyboard berdasarkan fungsi. Gunakan **micro-lab mandiri** ketika peserta harus berhenti dan mengerjakan tugas. Gunakan **konsep kiri + lab kanan** jika aturan perlu terlihat selama praktik. Pilih perbandingan, alur, kartu, demonstrasi layar, atau foto besar sesuai hubungan yang diterangkan. Lihat [pola mengajar dan visual](references/pola.md).
5. Tulis apa yang perlu dilihat kelas di slide. Beri instruktur pertanyaan, alokasi waktu, langkah demo, jawaban yang diharapkan, dan cara menanggapi kesalahan di speaker notes sesuai kebutuhan. Untuk pertanyaan evaluasi, simpan kunci di notes sampai sesi pembahasan.

## Bangun file

- Gunakan [template PowerPoint](assets/Template-Instruktur.pptx) dan [lembar pratinjau](assets/Pratinjau.jpg) sebagai patokan proporsi, kontras, penempatan judul, dan panel latihan. Template berisi contoh lengkap; pilih slide yang diperlukan. Ganti seluruh topik contoh beserta teks kecil, gambar, catatan, dan metadata materi. Bila pengguna memberi template resmi untuk tugas saat ini, kerjakan di salinannya dan pertahankan master, logo, font, serta efek yang diminta.
- Untuk lingkungan Python, salin [contoh brief](assets/contoh.json), lalu isi materi baru dan jalankan [generator](scripts/build_deck.py). Lihat [kontrak input dan perintah](references/pembuatan.md) sebelum menjalankannya. Generator memakai objek teks dan bentuk PowerPoint native serta gambar yang disematkan.
- Jika menggunakan alat presentasi lain, terapkan geometri dan urutan dalam panduan lalu ekspor PPTX. Tambahkan layout khusus bila materi memerlukannya, misalnya demonstrasi screenshot, matriks keputusan, potongan kode, grafik data asli, atau kuis bertahap. Gunakan kotak teks, tabel, chart, dan shape editable. Gambar layar, foto, serta ikon tetap menjadi objek gambar tersendiri. Jika lingkungan hanya mendukung teks, jelaskan keterbatasan ekspor dan hasilkan brief lengkap yang dapat dijalankan.
- Rencanakan visual sejak storyboard: sebutkan apa yang peserta perlu lihat dan di slide mana. Untuk modul penuh, tunjukkan setidaknya satu benda, dokumen, tampilan, atau situasi kerja yang khas topiknya. Misalnya, pada inventaris perpustakaan tampilkan label nomor buku dan cuplikan register yang akan dicocokkan. Jika foto belum tersedia, buat contoh register editable dari data latihan. Beri label “contoh” bila datanya ilustratif.
- Ambil visual spesifik materi dari lampiran. Pilih foto untuk situasi kerja, ikon untuk membedakan kategori, dan screenshot nyata untuk langkah antarmuka. Bila alat mendukung pembuatan gambar, buat ilustrasi baru yang sesuai objek dan peserta. Tempatkan gambar di slide yang sedang membahasnya. Cantumkan sumber aset eksternal di notes bila diperlukan. Sertakan logo/kredit yang diberikan untuk tugas itu. Untuk topik baru, pilih ulang visual pembelajaran dan nama organisasi.

## Uji sebagai instruktur

- Baca tiap slide dalam urutan presentasi. Pastikan judul menyampaikan ide, contoh konkret mendahului latihan sulit, dan peserta tahu apa yang harus dilakukan, berapa lama, dengan siapa, dan bukti apa yang harus diserahkan.
- Periksa kesesuaian tujuan dengan latihan, keakuratan angka dan contoh, kecocokan nama file/data, urutan demo, dan total waktu. Untuk kerja teknis, uji input kecil dan cocokkan output dengan kunci di notes.
- Buka kembali PPTX. Render **semua** slide dan periksa slide padat pada ukuran proyeksi. Cek baris paling bawah di panel latihan, kontras label, gambar gepeng, jarak gambar dengan teks, urutan baca, notes, dan logo. Pecah slide atau ringkas isi jika meluap. Ulangi render setelah koreksi. Jika alat render atau pemutaran efek tidak tersedia, sebutkan pemeriksaan yang berhasil dilakukan.
- Serahkan file PPTX final. Sertakan PDF, handout, atau file peserta hanya jika diminta. Untuk revisi, pertahankan konten dan urutan yang sudah disetujui pengguna.
