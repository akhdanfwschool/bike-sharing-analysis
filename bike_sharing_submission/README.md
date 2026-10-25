# Bike Sharing — Analisis Data dan Dashboard

Proyek akhir kelas **Belajar Fundamental Analisis Data**. Proyek ini menggunakan **Bike Sharing Dataset** dari UCI Machine Learning Repository (Hadi Fanaee-T, 2013; lisensi CC BY 4.0). Dataset berisi catatan peminjaman harian dan per jam pada 2011–2012 beserta informasi cuaca dan musim.

## Pertanyaan bisnis (SMART)

1. **Tren permintaan:** Bagaimana perubahan rata-rata peminjaman sepeda per hari dari bulan ke bulan sepanjang 2011–2012, dan bulan mana yang perlu menjadi prioritas kesiapan armada atau promosi? Ukuran: rata-rata peminjaman harian per bulan; periode jelas 2011–2012; hasil dapat ditindaklanjuti dengan penjadwalan armada dan promosi.
2. **Kondisi operasional:** Seberapa besar perbedaan rata-rata peminjaman harian antara hari kerja dan akhir pekan/hari libur menurut musim dan kondisi cuaca selama 2011–2012, serta segmen mana yang perlu diprioritaskan dalam perencanaan kapasitas? Ukuran: rata-rata dan selisih peminjaman per kelompok; hasil dapat mengarahkan perencanaan staf, perawatan, dan kesiapan armada.

## Struktur proyek

```text
bike_sharing_submission/
├── dashboard/
│   └── dashboard.py
├── data/
│   └── (day.csv, hour.csv, Readme.txt dihasilkan oleh skrip pengunduh)
├── scripts/
│   └── download_data.py
├── notebook.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

## Instalasi dan menjalankan

Disarankan Python 3.10–3.12.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/download_data.py
```

Skrip mencoba mengunduh arsip resmi dari UCI, lalu mencoba tautan Google Drive dataset yang dicantumkan pada instruksi kelas jika UCI tidak tersedia. Dibutuhkan koneksi internet pada langkah ini. Data asli diekstrak ke folder `data/`; tidak ada data sintetis yang dibuat.

### Jalankan notebook

```bash
jupyter notebook notebook.ipynb
```

Jalankan seluruh sel dari atas ke bawah. Notebook melakukan gathering, assessing, cleaning, EDA, visualisasi, explanatory analysis, binning untuk analisis tambahan, serta menyimpan data yang telah dibersihkan ke `dashboard/main_data.csv`. Simpan notebook setelah semua sel selesai dijalankan agar hasil dan grafik terdokumentasi untuk submission.

### Jalankan dashboard

Dari root folder proyek:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard memiliki filter periode, tahun, musim, kondisi cuaca, dan tipe hari; empat visualisasi; KPI; insight yang dihitung dari filter aktif; tabel data dan tombol unduh CSV.

## Deploy ke Streamlit Community Cloud (opsional, direkomendasikan)

1. Push seluruh proyek ke repository GitHub. Sertakan dataset yang dipakai atau pastikan mekanisme pengunduh bekerja sesuai ketentuan kelas.
2. Di Streamlit Community Cloud, buat aplikasi dari repository tersebut.
3. Atur **Main file path** menjadi `dashboard/dashboard.py`.
4. Atur Python dependencies agar memakai `requirements.txt` pada root repository (atau salin daftar dependensi ke file yang ditentukan platform jika konfigurasi deployment mengharuskan).
5. Setelah aplikasi berhasil dibuka, tempel URL publik sebenarnya ke `url.txt`.

## Catatan analisis dan integritas

- `day.csv` dipakai sebagai dasar utama agar pertanyaan bisnis berfokus pada permintaan harian.
- Kolom `temp`, `atemp`, `hum`, dan `windspeed` pada dataset asli dinormalisasi; jangan menyebut `temp` sebagai derajat Celsius tanpa mengubahnya menggunakan rumus dan batas yang terdokumentasi.
- Outlier yang valid tidak otomatis dihapus. Hari dengan permintaan sangat tinggi bisa merupakan peristiwa penting; laporkan temuan dan lakukan investigasi sebelum menghapus nilai.
- Hasil analisis deskriptif menunjukkan asosiasi/pola, bukan bukti sebab-akibat.
- Label musim di sini mengikuti kode dataset: 1=Semi, 2=Panas, 3=Gugur, 4=Dingin. Verifikasi dengan `Readme.txt` yang menyertai dataset jika menggunakan terminologi dari sumber lain.

## Sumber data

Fanaee-T, H. (2013). *Bike Sharing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894. Lisensi: CC BY 4.0. Dataset aslinya dipublikasikan melalui UCI Machine Learning Repository dan juga disediakan pada tautan Google Drive di materi proyek Dicoding.
