# Production Runbook — Hostinger GDP

Target: `https://gdp.gaeks.com` pada Hostinger Web Hosting, PHP 8.3, MySQL.
Staging tetap dipertahankan sebagai fallback, tetapi instruksi ini mengikuti
keputusan pemilik untuk cutover langsung ke production.

## 0. Gate keamanan wajib

Password yang pernah dikirim atau tersimpan di repository publik dianggap bocor.
Sebelum aplikasi live:

1. Ubah password user database production di hPanel dan simpan nilai baru di
   password manager.
2. Ubah password mailbox SMTP yang lama. Jangan gunakan password yang sama dengan
   database.
3. Rotasi Turnstile secret melalui Cloudflare karena secret lama pernah dibagikan
   dalam percakapan. Site key boleh tetap publik; secret key tidak boleh masuk Git.
4. Buat backup penuh file website dan database yang sedang live.

Jangan memakai kembali nilai lama dan jangan menaruh nilai baru di source, commit,
issue, atau chat.

## 1. Siapkan OAuth Google dan Turnstile

Di Google Cloud Console, pada OAuth Web Client yang digunakan:

- Authorized JavaScript origin: `https://gdp.gaeks.com`
- Authorized JavaScript origin opsional: `https://staging-gdp.gaeks.com`

Google Identity Services pada aplikasi mengirim ID token ke backend. Backend
memeriksa audience, issuer, expiry, status email, dan subject sebelum membuat sesi.

Di Cloudflare Turnstile, izinkan hostname:

- `gdp.gaeks.com`
- `staging-gdp.gaeks.com` bila staging masih digunakan

Masukkan hanya site key ke frontend. Secret hasil rotasi hanya masuk konfigurasi
privat server.

## 2. Import database production

1. Buka **Websites → gdp.gaeks.com → Databases → phpMyAdmin**.
2. Pilih database production yang sudah dibuat. Pastikan bukan database staging.
3. Ambil backup/export sebelum mengubah schema.
4. Import `database/migrations/001_initial_schema.sql`.
5. Import `database/migrations/002_auth_passwords.sql`.
6. Pastikan tabel berikut tersedia: `users`, `auth_identities`, `sessions`,
   `otp_challenges`, `rate_limit_buckets`, `cvs`, `presentations`,
   `document_revisions`, `audit_events`, serta tabel billing.
7. Pastikan `schema_migrations` memuat `001_initial_schema` dan
   `002_auth_passwords`.

Migration menggunakan `CREATE TABLE IF NOT EXISTS` dan kolom password memakai
`ADD COLUMN IF NOT EXISTS`, tetapi backup tetap wajib.

## 3. Buat konfigurasi privat

Buat file privat `gdp.env` di
`/home/u922552590/domains/gaeks.com/gdp.env`, yaitu **di luar** `public_html`.
Jangan menaruhnya di `/home/u922552590/domains/gaeks.com/public_html/.env`:
direktori itu dapat dilayani oleh website induk `gaeks.com`. Loader juga mendukung
`GAEKS_ENV_FILE` sebagai path absolut bila lokasi perlu diubah. File `.env` di
document root GDP hanya fallback dan tidak direkomendasikan untuk production.
Gunakan `.env.example` sebagai daftar variabel dan isi:

```dotenv
APP_ENV=production
APP_URL=https://gdp.gaeks.com
APP_SESSION_COOKIE=__Host-gaeks_session
APP_SESSION_TTL_SECONDS=604800
SESSION_SECRET=<random-minimum-32-bytes>

DB_HOST=localhost
DB_PORT=3306
DB_NAME=<production-database>
DB_USER=<production-user>
DB_PASSWORD=<rotated-production-password>

SMTP_HOST=smtp.hostinger.com
SMTP_PORT=465
SMTP_USER=<mailbox-sender>
SMTP_PASSWORD=<rotated-mailbox-password>
MAIL_TRANSPORT=auto
SMTP_FROM_NAME=GAEKS Digital Products
REPLY_TO_EMAIL=gdp@gaeks.com
ADMIN_NOTIFICATION_EMAIL=gdp@gaeks.com

GOOGLE_CLIENT_ID=<google-web-client-id>
TURNSTILE_SITE_KEY=<public-site-key>
TURNSTILE_SECRET_KEY=<rotated-secret-key>

BILLING_ENABLED=false
FREE_LIMITS_ENABLED=false
```

Gunakan generator password manager untuk `SESSION_SECRET`. Jangan menyalin teks
placeholder. Permission file privat disarankan `600` bila File Manager mendukung.

## 4. Konfigurasi PHP 8.3

Aktifkan atau pastikan tersedia: `pdo_mysql`, `openssl`, `curl`, `mbstring`,
`fileinfo`, dan `json`.

Nilai 2 GB yang saat ini dipakai untuk upload/post terlalu besar untuk aplikasi
ini dan memperbesar risiko kehabisan resource. Baseline production:

- `memory_limit`: 256M atau 512M
- `max_execution_time`: 120
- `max_input_time`: 120
- `max_input_vars`: 5000
- `post_max_size`: 32M
- `upload_max_filesize`: 25M
- `max_file_uploads`: 20
- `session.cookie_samesite`: Lax

Aplikasi menggunakan session token sendiri di database; PHP session file bukan
sumber otoritas login. HTTPS wajib agar cookie `__Host-` dikirim dengan aman.

## 5. Upload runtime

Upload ke document root production hanya:

- semua halaman `.html` runtime dan `auth.js`;
- folder `api/`;
- folder `public/assets/`;
- `.htaccess`;
- asset runtime lain yang benar-benar direferensikan halaman.

Jangan upload `.git`, `.env`, `prd.md`, `database`, `docs`, `tests`, `config`,
backup, dump, log, atau script deployment lama. Deployment lewat Git hPanel harus
memiliki aturan exclude yang setara; konfigurasi `.env` tetap berada di luar
checkout/document root.

## 6. Smoke test setelah cutover

1. Buka `https://gdp.gaeks.com/api/health.php`; respons harus `ok: true` dan nilai
   `data.database` harus `ok`.
2. Buka incognito, daftar dengan email test, selesaikan Turnstile dan OTP.
3. Pastikan email OTP dan welcome masuk ke pengguna.
4. Pastikan notifikasi pengguna baru masuk ke `gdp@gaeks.com`.
5. Logout, lalu login menggunakan password.
6. Uji Google Sign-In pada domain production.
7. Buat CV, refresh, logout/login, lalu pastikan data tetap ada.
8. Buat presentasi, edit, refresh, export PDF/PPTX, dan pastikan data tetap ada.
9. Uji dua akun: akun kedua harus menerima 404 saat meminta ID dokumen akun pertama.
10. Uji sampah, restore, dan hapus permanen pada kedua aplikasi.
11. Pastikan `/api/config.php`, `/api/bootstrap.php`, `.env`, `.sql`, `/database`,
    `/docs`, dan `/tests` menghasilkan 403/404.
12. Periksa error log tanpa menyalin credential ke tiket atau chat.

Jika health check, OTP, login, atau isolasi dua akun gagal, kembalikan file dari
backup dan hentikan pendaftaran sampai penyebab diperbaiki.

## 7. Email deliverability

Gunakan mailbox sender khusus, lalu pastikan SPF, DKIM, dan DMARC domain aktif.
Alamat admin notification default adalah `gdp@gaeks.com`. Endpoint mail tester
lama dinonaktifkan; pengujian dilakukan melalui pendaftaran test yang nyata.

## 8. Billing belum diaktifkan

Schema untuk paket Free dan PRO bulanan Rp33.000 sebelum pajak sudah tersedia.
Pertahankan `BILLING_ENABLED=false` dan `FREE_LIMITS_ENABLED=false` sampai Midtrans
sandbox, signature webhook, idempotency, refund, expiry, pajak, dan entitlement
lulus pengujian. Jangan memasukkan Server Key Midtrans production sekarang.
