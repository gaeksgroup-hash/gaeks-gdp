# GAEKS Digital Products

Monorepo transisi untuk dua produk utama GAEKS:

- ATS CV Maker
- Presentation Maker

Dokumen produk dan urutan implementasi ada di [`prd.md`](prd.md). Panduan persiapan deployment Hostinger tersedia di [`docs/HOSTINGER_SETUP.md`](docs/HOSTINGER_SETUP.md).

## Status

Landing page, pricing, authentication server-side, OTP email, Google Sign-In,
Turnstile, penyimpanan CV/presentasi, session HttpOnly, CSRF, versioning, dan
isolasi data pengguna sudah diterapkan. Infrastruktur tabel billing disiapkan,
namun pembayaran dan limitasi tetap dinonaktifkan sampai implementasi Midtrans
sandbox selesai.

## Menjalankan aplikasi lokal

Gunakan PHP 8.3 dengan PDO MySQL dan isi `.env` privat berdasarkan `.env.example`.
Contoh server development:

```powershell
php -S 127.0.0.1:8765
```

Kemudian buka `http://127.0.0.1:8765/`.

Jangan menjalankan server development PHP sebagai server production. Panduan
cutover Hostinger ada di [`docs/HOSTINGER_SETUP.md`](docs/HOSTINGER_SETUP.md).
