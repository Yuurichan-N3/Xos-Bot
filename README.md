# Xos-Bot

Alat otomatisasi berbasis Python untuk menghasilkan dompet Ethereum, menandatangani pesan, dan berinteraksi dengan API X.ink untuk mendapatkan token melalui referral.

## 🚀 Fitur
- **Pembuatan Dompet**: Membuat dompet Ethereum baru secara otomatis menggunakan `eth_account`.
- **Interaksi API**: Berkomunikasi dengan API WalletConnect dan X.ink untuk mengambil identitas, menandatangani pesan, dan memverifikasi tanda tangan.
- **Verifikasi Tanda Tangan**: Menandatangani pesan secara lokal dan memverifikasinya dengan server X.ink.
- **Penyimpanan Data**: Menyimpan detail dompet dan token ke `wallets.json` dan `tokens.json`.
- **Antarmuka Konsol Menarik**: Menampilkan banner berwarna dan tabel ringkasan menggunakan pustaka `rich`.
- **Penanganan Error**: Pencatatan log yang kuat dengan pesan error yang jelas.

## 📋 Prasyarat
- Python 3.8 atau lebih baru
- Modul yang diperlukan (pasang secara manual):
  - `requests`
  - `eth_account`
  - `web3`
  - `rich`

## 🛠 Instalasi
1. Kloning repositori:
   ```bash
   git clone https://github.com/Yuurichan-N3/Xos-Bot.git
   cd Xos-Bot
   ```
2. Pasang modul secara manual:
   ```bash
   pip install requests eth_account web3 rich
   ```
3. Jalankan bot:
   ```bash
   python bot.py
   ```

## 📖 Cara Penggunaan
1. Jalankan skrip, lalu masukkan kode referral (default: `9U25GX` jika dikosongkan).
2. Bot akan:
   - Membuat dompet Ethereum baru.
   - Mengambil data dompet dan identitas dari API.
   - Menandatangani pesan dan memverifikasinya dengan server X.ink.
   - Menyimpan detail dompet dan token ke file JSON.
   - Menampilkan tabel ringkasan setelah setiap iterasi.
3. Proses akan berulang setiap 2 detik hingga dihentikan (`Ctrl+C`).

## 📂 Keluaran
- `wallets.json`: Menyimpan alamat dompet, kunci pribadi, dan respons verifikasi.
- `tokens.json`: Menyimpan token yang diperoleh.

## ⚠️ Peringatan
- Gunakan dengan risiko Anda sendiri. Pastikan Anda memahami kode dan interaksi API.
- Kunci pribadi dibuat dan disimpan secara lokal; jaga keamanan file `wallets.json`.
- Alat ini berinteraksi dengan API pihak ketiga; periksa syarat layanan mereka.

## 📜 Lisensi
Script ini didistribusikan untuk keperluan pembelajaran dan pengujian. Penggunaan di luar tanggung jawab pengembang.

Untuk update terbaru, bergabunglah di grup **Telegram**: [Klik di sini](https://t.me/sentineldiscus).

---

## 💡 Disclaimer
Penggunaan bot ini sepenuhnya tanggung jawab pengguna. Kami tidak bertanggung jawab atas penyalahgunaan skrip ini.
