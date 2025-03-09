# Bike Sharing Dashboard
Dashboard ini dikembangkan menggunakan Streamlit dan dirancang untuk menampilkan analisis data penyewaan sepeda.

## Persyaratan
Sebelum menjalankan dashboard, pastikan Anda memiliki:

- Python yang terinstal di sistem 
- Paket-paket Python berikut.
  - `streamlit`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `numpy`

Jika belum menginstal paket-paket tersebut, jalankan perintah berikut di terminal atau command prompt:

```sh
pip install streamlit pandas matplotlib seaborn numpy
```

## Cara Menjalankan Dashboard
1. **Unduh Repository**
   Unduh berkas ke dalam sistem lokal.

2. **Pastikan Data Tersedia**
   - Pastikan file dataset `daily_clean.csv` dan `hourly_clean.csv` ada di direktori yang sama dengan skrip utama.
   - Pastikan gambar `logo.png` tersedia jika digunakan dalam sidebar.

3. **Jalankan Streamlit**
   Navigasikan ke direktori tempat file skrip Streamlit disimpan, lalu jalankan perintah berikut:

   ```sh
   streamlit run nama_file.py
   ```
   Gantilah `nama_file.py` dengan nama file yang berisi kode Streamlit (defaultnya adalah dashboard.py).

4. **Akses Dashboard**
   Setelah perintah dijalankan, Streamlit akan membuka dashboard di browser secara otomatis. Jika tidak terbuka, Anda bisa mengaksesnya secara manual dengan membuka URL berikut di browser:

   ```
   http://localhost:8501
   ```

