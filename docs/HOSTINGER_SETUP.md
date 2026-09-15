# Setup Hostinger Web Hosting Unlimited — GAEKS GDP

Dokumen ini memisahkan dua kegiatan:

1. **Deploy tampilan/fondasi repository sekarang** — halaman depan baru dan folder arsitektur.
2. **Aktivasi database/auth baru nanti** — dilakukan setelah backend implementasi tersedia dan migration diuji di staging.

Jangan memasukkan credential ke Git, `prd.md`, tiket publik, atau file di dalam `public_html`.

## A. Sebelum deploy source terbaru

1. Masuk ke hPanel dan buka website GDP.
2. Catat domain yang benar, document root, versi PHP, serta apakah Git Deployment digunakan. Kode saat ini mengindikasikan `gdp.gaeks.com`, tetapi domain final harus dipastikan.
3. Buat backup penuh dari file website dan database/data aktual. Unduh salinannya ke lokasi privat.
4. Rotasi password SMTP yang pernah tertulis di repository. Setelah rotasi, jangan menaruh password baru pada `api/config.php` atau file Git.
5. Jangan menjalankan script root bernama `safe_deploy.sh`, `deploy_*`, `update_*`, atau `run_deploy_fix.py`; beberapa menimpa source dan melakukan force-push.

## B. Menampilkan landing page baru

### Jika memakai Git Deployment hPanel

1. Buka **Websites → Manage → Git**.
2. Pastikan repository adalah `https://github.com/gaeksgroup-hash/gaeks-gdp` dan branch `main`.
3. Pastikan deploy path menunjuk ke document root GDP saja, bukan root website lain.
4. Pull/deploy commit terbaru setelah backup selesai.
5. Pastikan file berikut tersedia dari browser:
   - `/index.html`
   - `/pricing.html`
   - `/public/assets/css/landing.css`
   - `/public/assets/js/landing.js`
6. Buka halaman dalam private/incognito window dan lakukan hard refresh.

### Jika memakai File Manager/SFTP

1. Unduh source dari commit yang akan dirilis.
2. Upload hanya file runtime yang diperlukan. Untuk tahap transisi ini, pertahankan halaman `.html`, `auth.js`, folder `api`, folder `public/assets`, dan `.htaccess`.
3. Jangan upload `.git`, `.env`, `prd.md`, `app`, `config`, `database`, `docs`, `scripts`, `tests`, backup, dump, atau file log ke area publik.
4. Verifikasi permission file normal dan jangan membuat directory runtime world-writable.

## C. Membuat staging

1. Buat subdomain staging, misalnya `staging-gdp.gaeks.com`, pada website/directory yang terpisah. Nama final boleh berbeda.
2. Aktifkan SSL dan paksa HTTPS.
3. Buat database dan user staging terpisah dari production.
4. Gunakan akun/email testing. Jangan mengirim OTP kepada daftar pengguna production selama uji.
5. Atur origin Google dan hostname CAPTCHA untuk staging setelah backend auth baru tersedia.
6. Lindungi staging dari indexing dan akses umum sesuai fasilitas hPanel. Jangan memakai HTTP Basic Auth pada endpoint webhook Midtrans ketika fase billing diuji karena webhook harus dapat dijangkau provider.

## D. Membuat database MySQL/MariaDB

1. Buka **Websites → Manage → Databases → Management** (nama menu dapat berubah di hPanel).
2. Buat database `gdp_staging` dan user kuat khusus staging; hPanel biasanya menambahkan prefix akun.
3. Buat database production terpisah, misalnya `gdp_production`, hanya setelah staging lulus.
4. Simpan host, port, nama database, username, dan password pada password manager. Jangan mengirimkannya melalui Git.
5. Periksa versi MySQL/MariaDB dan dukungan InnoDB, foreign key, `utf8mb4`, `DATETIME(6)`, serta PDO MySQL.
6. Buka phpMyAdmin untuk database staging, pilih database yang benar, lalu import `database/migrations/001_initial_schema.sql`.
7. Verifikasi tabel dibuat dan `schema_migrations` berisi `001_initial_schema`.
8. Jangan import migration ke production sampai backend auth baru tersedia, backup/restore diuji, dan data lama diinventaris.

## E. Konfigurasi privat server

1. Gunakan `.env.example` hanya sebagai daftar nama variabel.
2. Simpan nilai sebenarnya di luar document root. Jika paket tidak menyediakan environment variables, gunakan file PHP privat sebagai sibling `public_html` dan permission minimum; jangan menyimpannya di Git.
3. Isi `APP_URL`, database, SMTP hasil rotasi, Google client ID, serta Turnstile site/secret key.
4. Pertahankan `BILLING_ENABLED=false` dan `FREE_LIMITS_ENABLED=false`.
5. Jangan isi/aktifkan Midtrans production sebelum modul billing dan sandbox selesai.
6. Pastikan error display mati di production dan log berada di lokasi privat.

## F. Pemeriksaan PHP yang diperlukan

Pilih versi PHP yang masih mendapat security updates dan didukung aplikasi. Aktifkan/periksa:

- PDO dan `pdo_mysql`
- OpenSSL
- cURL
- mbstring
- fileinfo
- JSON
- GD atau Imagick untuk validasi/re-encode gambar pada fase media

Catat `memory_limit`, `max_execution_time`, `post_max_size`, `upload_max_filesize`, batas database, inode, cron, dan proses. Label paket “Unlimited” tidak berarti resource komputasi tanpa batas.

## G. Google, OTP, dan CAPTCHA

Bagian ini dijalankan setelah endpoint auth server baru selesai.

1. Google Cloud Console: tambahkan origin HTTPS staging dan production yang tepat ke OAuth/GIS client yang digunakan.
2. Pastikan consent screen dan status publishing cocok untuk pengguna target.
3. Backend harus memverifikasi ID token Google; callback browser tidak boleh langsung membuat session.
4. Buat Turnstile widget untuk domain staging/production. Site key boleh ke frontend; secret key hanya di server.
5. Verifikasi token Turnstile melalui server pada permintaan OTP dan Google login.
6. SMTP: gunakan akun hasil rotasi dan periksa SPF, DKIM, DMARC, sender, serta batas pengiriman.
7. Uji OTP salah, expired, replay, resend, throttling, dan kegagalan SMTP.
8. Uji login Google valid dan token dengan audience/expiry salah.

## H. Checklist sesudah deploy tampilan

- [ ] HTTPS aktif dan tidak ada mixed content.
- [ ] Landing dan pricing memuat CSS/JS baru tanpa 404.
- [ ] Navigasi desktop/mobile dan focus keyboard bekerja.
- [ ] Tombol CV/presentasi mengarah ke login saat belum masuk.
- [ ] Halaman tidak menampilkan tombol pembayaran aktif.
- [ ] URL lama CV dan presentasi masih dapat dibuka.
- [ ] Request langsung ke `/app`, `/config`, `/database`, `/docs`, `/scripts`, `/tests`, backup tersembunyi, `.sql`, `.env`, dan file log menghasilkan 403/404.
- [ ] Endpoint mail tester tidak digunakan pada production.
- [ ] Error log diperiksa tanpa membocorkan credential atau data pengguna.

## I. Data/production cutover berikutnya

1. Inventaris database/file production aktual sebelum migrasi.
2. Implementasikan auth server, API document, dan migrator di branch terpisah.
3. Uji dua akun pada staging: akun B harus gagal membuka ID/media akun A.
4. Uji save, refresh, logout/login, dan browser kedua untuk kedua aplikasi.
5. Jalankan backup/restore rehearsal.
6. Lakukan cutover dengan maintenance singkat, migration yang kompatibel, session lama dicabut, lalu smoke test.

Ikuti detail gate dan acceptance test di `prd.md`. Jangan menyatakan cloud save/auth aman hanya karena tabel sudah dibuat.
