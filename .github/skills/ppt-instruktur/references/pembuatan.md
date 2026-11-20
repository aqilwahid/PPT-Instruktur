# Membuat PPTX editable

## Jalur tercepat

Dengan editor PowerPoint atau alat yang bisa mengimpor PPTX, buka salinan `assets/Template-Instruktur.pptx`. Pilih komposisi yang diperlukan, duplikasi bila perlu, isi ulang teks dan speaker notes, lalu periksa hasil ekspor. Template berisi 14 **contoh slide editable**. Komposisinya dibentuk dengan objek per slide yang dapat diduplikasi.

## Jalur Python

Dari direktori yang memuat SKILL.md, dengan Python 3.10+:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/build_deck.py assets/contoh.json hasil.pptx
```

Contoh itu menghasilkan materi rekonsiliasi. Untuk kelas lain, simpan brief JSON baru, tulis seluruh konten dan notes sesuai tugas, lalu ganti argumen pertama. Generator dapat bekerja tanpa jaringan setelah dependensi tersedia. Jalur gambar relatif dihitung dari folder JSON. Gunakan gambar lokal PNG/JPEG, termasuk untuk logo. `@kelas` merujuk pada foto fasilitasi di paket. Ketika menyalin contoh JSON ke folder lain, salin juga folder `icons` di sebelahnya atau ubah jalur gambar.

**Struktur dokumen.** `meta` opsional memuat `title`, `organization`, `logo`, `logo_light` untuk latar gelap, dan `credit`. `slides` adalah array berurutan. Tiap slide membutuhkan `role`, `title`, dan `notes` berupa teks yang akan masuk ke catatan presenter. `tag` opsional pada slide isi. Beri `alt` deskriptif untuk tiap foto/ikon bermakna.

| role | Isi tambahan | Fungsi |
| --- | --- | --- |
| cover, hook | subtitle dan image opsional | Sampul luas atau pertanyaan pemantik. Pada cover berjudul dua baris, accent_last_line bernilai true memberi warna sian pada baris akhir. Tambahkan atribusi yang telah dicek untuk kutipan. |
| roadmap | rows berisi key, title, text | 1–4 modul per slide. Lanjutkan huruf pada slide berikutnya. |
| day, divider | subtitle opsional | Sampul modul atau transisi bab. |
| goals | items, array 1–5 string | Hasil belajar yang dapat diperiksa. |
| compare | left dan right, masing-masing dengan title, items; image dan alt opsional | Perbandingan dengan kriteria sejajar. |
| process | stages (2–5), masing-masing berisi title dan text; image, alt, dan cue akhir opsional | Tahap berurutan. cue berada pada tingkat slide. |
| cards | cards (2–6), masing-masing berisi title, text; image dan alt opsional | Konsep sejajar atau pilihan. |
| teach_lab | items untuk konsep kiri; lab untuk tugas kanan | Konsep bersama latihan. |
| lab | items untuk stimulus singkat; lab untuk tugas mandiri | Aktivitas satu layar dengan urutan tugas. |
| takeaway | subtitle; image dan alt opsional | Pesan yang perlu diingat. |
| project | setup, work dan evidence; work_title dan evidence_title opsional | Daftar tugas dan bukti praktik akhir. |
| close | subtitle opsional | Penutup atau pertanyaan refleksi. |

Objek `lab` memuat `badge` (teks singkat seperti “LAB 2”), `name` (nama aktivitas), `time` (misalnya “12 menit · berpasangan”), `steps` (array instruksi), dan `output` (satu hasil yang bisa diperiksa). Untuk role `lab`, gunakan nama aktivitas sebagai `title` slide; bidang `name` terutama dipakai pada panel `teach_lab`. Kedua role mendukung gambar opsional. Contoh lengkap seluruh role tersedia di `assets/contoh.json`.

Gunakan `lab.output_label` untuk menyesuaikan label hasil dengan bahasa kelas, misalnya `Hasil` atau `Deliverable`.

## Pemeriksaan hasil

Generator menolak bidang teks yang melampaui perkiraan ruang, slide tanpa notes, dan gambar yang tak dapat dibuka. Ukuran huruf dapat berbeda antarplatform. Tinjau hasil render dengan alat yang tersedia, lalu buka dalam mode presentasi jika ada efek atau media. Untuk materi padat, pindahkan rincian ke notes dan sisakan bukti atau contoh minimum di slide; bila masih padat, pecah menjadi dua slide. Sesuaikan komposisi dengan editor presentasi bila brief memerlukan grafik, animasi, tabel besar, foto tambahan, atau template resmi pengguna.
