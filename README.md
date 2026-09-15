# GAEKS Digital Products

Monorepo transisi untuk dua produk utama GAEKS:

- ATS CV Maker
- Presentation Maker

Dokumen produk dan urutan implementasi ada di [`prd.md`](prd.md). Panduan persiapan deployment Hostinger tersedia di [`docs/HOSTINGER_SETUP.md`](docs/HOSTINGER_SETUP.md).

## Status

Landing page dan halaman pricing baru telah disiapkan. Database schema, authentication server-side, isolasi data pengguna, dan billing masih harus diterapkan bertahap sesuai PRD sebelum production dianggap siap.

## Menjalankan frontend lokal

Gunakan web server statis dari root repository. Contoh:

```powershell
python -m http.server 8765
```

Kemudian buka `http://127.0.0.1:8765/`.

Jangan gunakan server PHP bawaan atau menjalankan script maintenance legacy pada data production sebelum containment dan backup selesai.
