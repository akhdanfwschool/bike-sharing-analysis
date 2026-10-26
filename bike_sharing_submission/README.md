# Bike Sharing — Analisis Data dan Dashboard

Proyek akhir kelas **Belajar Fundamental Analisis Data** menggunakan Bike Sharing Dataset dari UCI Machine Learning Repository. Data harian mencakup 1 Januari 2011–31 Desember 2012. Sumber: [UCI Bike Sharing](https://archive.ics.uci.edu/dataset/275/bike%2Bsharing%2Bdataset).

## Pertanyaan bisnis

1. Bagaimana perubahan rata-rata peminjaman sepeda per hari dari bulan ke bulan sepanjang 2011–2012, dan bulan mana yang perlu menjadi prioritas kesiapan armada atau promosi?
2. Seberapa besar perbedaan rata-rata peminjaman harian antara hari kerja dan akhir pekan/hari libur menurut musim dan kondisi cuaca selama 2011–2012, serta segmen mana yang perlu diprioritaskan dalam perencanaan kapasitas?

## Struktur proyek

```text
bike_sharing_submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   ├── hour.csv
│   └── Readme.txt
├── scripts/
│   └── download_data.py
├── notebook.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

**Penting untuk submission:** sertakan dataset asli yang digunakan (`day.csv`, `hour.csv`, dan `Readme.txt`) serta notebook yang sudah dijalankan dan disimpan bersama output-nya. **Jangan sertakan folder `.venv`** di ZIP submission karena berisi lingkungan Python lokal dan membuat ukuran ZIP membesar. Folder `.venv` boleh tetap ada selama proses kerja lokal; cukup keluarkan dari paket submission atau hapus setelah pengerjaan selesai.

## Menjalankan proyek di komputer lokal

Disarankan Python 3.12 untuk konsistensi deployment. Jika memakai versi Python lain yang sudah terpasang, pastikan semua library terinstal dan tidak ada error.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/download_data.py
jupyter notebook notebook.ipynb
```

Di Jupyter, jalankan **Run All**, pastikan sel selesai tanpa error, kemudian tekan `Ctrl+S` agar kode, tabel, dan grafik tersimpan ke `notebook.ipynb`.

Setelah notebook berhasil membuat `dashboard/main_data.csv`, jalankan dashboard dari root proyek:

```powershell
streamlit run dashboard/dashboard.py
```

## Dashboard publik

URL Streamlit Community Cloud:

https://bike-sharing-analysis-ab8xs7zfetrwy74ybvswev.streamlit.app/

URL yang sama disimpan pada `url.txt`.

## Ringkasan analisis dan integritas

- Notebook mendokumentasikan gathering, memahami data, assessing, cleaning, EDA, visualisasi/explanatory analysis, binning suhu, kesimpulan, dan rekomendasi.
- Kesimpulan dalam notebook ditulis langsung menggunakan Markdown dan disusun berurutan sesuai kedua pertanyaan bisnis.
- `day.csv` digunakan untuk analisis harian; jangan menjumlahkan total `day.csv` dan `hour.csv`, karena keduanya merepresentasikan aktivitas yang sama pada tingkat agregasi waktu berbeda.
- Variabel `temp`, `atemp`, `hum`, dan `windspeed` dalam dataset adalah nilai ternormalisasi. Jangan menginterpretasikan `temp` sebagai Celsius mentah.
- Outlier ditandai untuk pemeriksaan dan tidak otomatis dihapus, karena nilai ekstrem bisa mencerminkan puncak permintaan yang valid.
- Temuan merupakan deskripsi dataset historis 2011–2012 dan tidak membuktikan hubungan sebab-akibat.

## Checklist sebelum membuat ZIP submission

- [ ] `notebook.ipynb` sudah dijalankan dari awal hingga akhir tanpa error.
- [ ] Output tabel dan grafik sudah terlihat dan disimpan dengan `Ctrl+S`.
- [ ] Kesimpulan berbentuk Markdown dan menjawab pertanyaan bisnis 1 lalu 2.
- [ ] Dataset asli yang diperlukan tersedia di folder `data/`.
- [ ] `dashboard/main_data.csv` tersedia dan dashboard telah diuji.
- [ ] `url.txt` berisi URL publik Streamlit di atas.
- [ ] Folder `.venv` tidak masuk ke ZIP submission.
- [ ] README dan `requirements.txt` ikut disertakan.
