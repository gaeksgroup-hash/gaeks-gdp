# PRD — GAEKS Digital Products

Versi: 1.0 · Tanggal: 15 September 2026 · Bahasa produk utama: Indonesia

Status: **baseline implementasi bertahap di repository**. Struktur fondasi dan frontend publik tahap awal telah dibuat; database Hostinger, authentication baru, isolasi data server, dan pembayaran belum diterapkan.

Konfirmasi pemilik saat penyusunan: target adalah **Hostinger Web Hosting Unlimited**. Nama paket/SKU di hPanel, batas resource, dan domain final belum diperiksa.

Repository: `gaeksgroup-hash/gaeks-gdp`

Baseline audit: `main`, commit `5e9f21b5c4f7a6226f84c1ef8ea28bbb6a7badc9`. HEAD lokal sama dengan `origin/main` yang diperiksa melalui remote pada saat audit.

## 1. Tujuan dan keputusan utama

Menjadikan **ATS CV Maker dan Presentation Maker** sebagai dua aplikasi yang dapat digunakan secara profesional: pengguna bisa mendaftar, masuk, membuat dokumen, menyimpan, membuka kembali dari perangkat lain, mengedit, dan mengekspor tanpa kehilangan data atau mengakses dokumen akun lain.

Istilah “kedua aplikasi” dalam dokumen ini berarti CV Maker dan Presentation Maker, sesuai isi repository dan rencana sebelumnya.

### 1.1 Arahan pemilik produk

- Pertahankan aplikasi/editor, tema CV, layout presentasi, dan fungsi produk yang sudah dibuat. Infrastruktur, autentikasi, data, routing, dan wiring tombol boleh direstrukturisasi untuk memperbaiki fungsi.
- Target deployment adalah Hostinger dengan database server yang persisten.
- Dua metode login dan registrasi: OTP email dan Sign in with Google. Konfigurasi Google yang sudah ada menjadi titik awal dan harus diverifikasi pada domain sebenarnya.
- Tambahkan CAPTCHA dengan validasi server.
- Semua dokumen privat secara default; memiliki URL atau mengetahui ID tidak memberikan hak akses.
- Buat ulang halaman depan dengan arah UI UX Pro Max: modern, halus, profesional, dan mudah dipakai.
- Rancang pembatasan pengguna Free dan langganan **PRO Rp33.000 per bulan, belum termasuk pajak**, yang membuka seluruh fitur CV dan presentasi.
- Midtrans menjadi payment gateway yang direncanakan. Implementasi dan aktivasi billing dilakukan setelah fungsi inti stabil.
- Deletion/refactor diperbolehkan untuk kode usang atau duplikasi yang telah diverifikasi. Data pengguna tetap harus dilindungi dan perubahan harus bisa dipulihkan.

### 1.2 Keputusan teknis untuk rancangan awal

| Area | Keputusan | Alasan |
| --- | --- | --- |
| Runtime | PHP yang masih didukung dan tersedia di paket Hostinger; PDO MySQL | Mengembangkan backend yang sudah ada dan cocok untuk deployment PHP |
| Database | MySQL/MariaDB terpisah untuk staging dan production | Sumber data akun dan dokumen yang sama lintas perangkat |
| Frontend | Pertahankan HTML/JavaScript; ekstrak modul bersama secara bertahap | Mempertahankan hasil editor yang sudah ada sambil memperbaiki strukturnya |
| CSS/dependensi | Build aset di lokal/CI, versi dikunci, hasil statis diunggah | Runtime tidak memerlukan Node atau CDN Tailwind compiler |
| Auth | Session server dengan cookie opaque; OTP email tanpa password dan Google | Menghapus login semu yang ada saat ini |
| CAPTCHA | Cloudflare Turnstile sebagai pilihan rancangan awal | Widget dan verifikasi server; provider bisa diganti lewat adapter |
| Data | Server sebagai sumber kebenaran; cache browser opsional untuk pemulihan | Cache bukan identitas, permission, atau bukti cloud save |
| Media | File privat di luar document root; metadata dan owner di database | Foto, slide, thumbnail, dan export mengikuti otorisasi dokumen |
| Billing | Adapter Midtrans, feature flag mati sampai gate billing lulus | Infrastruktur siap tanpa menagih sebelum produk siap |
| Sharing | Ditutup saat peluncuran pertama; private owner-only | Menutup akses lintas akun sebelum menambah kolaborasi |

Keputusan PHP/MySQL adalah **rancangan untuk Web Hosting Unlimited yang dikonfirmasi pemilik**, bukan hasil pemeriksaan akun Hostinger. Versi database, SSH/Composer, cron, batas resource, dan document root belum diverifikasi. Label paket “Unlimited” tidak dipakai sebagai asumsi kapasitas CPU, RAM, database, atau proses tanpa batas. Domain `gdp.gaeks.com` muncul di kode email; domain final, status DNS, SSL, dan deployment aktifnya belum diverifikasi.

## 2. Ruang lingkup dan ukuran keberhasilan

### 2.1 Rilis A — fungsi inti dan deployment

1. Konfigurasi aman, staging, database, migrasi, dan backup.
2. Login/registrasi OTP email + Google + CAPTCHA, logout, dan pengelolaan session.
3. Otorisasi owner pada seluruh operasi dokumen dan media.
4. Penyimpanan server, penanganan konflik, serta pemulihan data lama yang aman.
5. Seluruh alur dan tombol CV Maker berfungsi; PDF A4 diuji.
6. Seluruh alur dan tombol Presentation Maker berfungsi; playback, PDF, dan PPTX diuji.
7. Halaman depan, auth, dashboard, profil, dan pricing konsisten.
8. Pengujian keamanan/fungsi, deployment staging, lalu production.

### 2.2 Rilis B — monetisasi setelah Rilis A stabil

- Entitlement Free/PRO, quota server, status langganan, checkout Midtrans, pembayaran terverifikasi, invoice, renewal, expiry, dan rekonsiliasi.
- Angka limit Free belum diputuskan. Dokumen ini menyiapkan modelnya, bukan menetapkan kuota bisnis secara sepihak.
- Paket tahunan, diskon, trial berbayar, serta biaya tambahan belum disetujui. Angka tahunan dan Rp49.000 dari UI lama bukan dasar harga baru.

### 2.3 Di luar ruang lingkup awal

- ERP, website korporat, toko e-book, layanan SMM, dan produk lain di landing lama.
- Kolaborasi realtime, public gallery dokumen, public share link, dan editor pengganti total.
- Layanan AI berbayar baru. Fitur terjemahan lokal yang ada tidak boleh dipasarkan seolah memakai backend AI yang belum tersedia.
- Migrasi framework menyeluruh, Kubernetes, Redis, atau worker permanen sebagai prasyarat.

### 2.4 Kriteria keberhasilan rilis

| Hasil | Kriteria penerimaan |
| --- | --- |
| Auth | OTP dan Google menghasilkan session server yang valid; kredensial palsu ditolak |
| Privasi | Akun A tidak bisa membaca/mengubah/menghapus/mengunduh data B lewat UI, URL, API, cache, maupun media |
| Persistensi | Dokumen yang dinyatakan tersimpan muncul identik setelah refresh, logout/login, dan di perangkat/browser kedua |
| Interaksi | Seluruh tombol penting dalam matriks pengujian lulus; tidak ada fungsi hilang, loader permanen, atau error JavaScript pada alur utama |
| Export | PDF dapat dibuka dan teksnya diperiksa; PPTX terbuka tanpa repair warning dan elemen yang dijanjikan editable memang dapat diedit |
| Operasional | Backup dan restore diuji pada staging; deployment serta rollback terdokumentasi |
| Rilis | Tidak ada temuan kritis/tinggi yang belum diselesaikan pada jalur auth, owner, data, dan export |

Angka performa pada bagian 12 adalah target pengujian, belum merupakan hasil benchmark.

## 3. Hasil telaah repository

### 3.1 Metode dan batas pemeriksaan

- Inventaris dan pemindaian statis mencakup **65 file terlacak**, termasuk file tersembunyi, dokumentasi, backend, frontend, serta generator/skrip lama.
- Alur aktif diperiksa pada 8 halaman HTML, `auth.js`, 8 file PHP, dan `.htaccess`.
- JavaScript inline aktif dan `auth.js` diperiksa sintaksnya tanpa mengeksekusi aplikasi produksi. Sintaks yang lulus tidak membuktikan fungsi runtime lulus.
- Lima file Python diperiksa menggunakan parser, tanpa menjalankan generator atau perintah deployment di dalamnya.
- Rekursi dashboard presentasi direproduksi dengan fungsi asli dan DOM tiruan dalam Node; hasil `RangeError: Maximum call stack size exceeded`.
- Referensi UI UX Pro Max dan dokumentasi resmi Hostinger, Google, Turnstile, serta Midtrans ditelaah.
- Belum dilakukan pengujian browser menyeluruh, login akun asli, pengiriman email, akses database Hostinger, atau transaksi pembayaran. PHP executable tidak tersedia pada PATH lokal saat pemeriksaan; validasi PHP dan integrasi database masih harus dilakukan pada tahap implementasi.

### 3.2 Temuan yang menjadi dasar pekerjaan

Nomor baris mengacu pada baseline di atas. “Terbukti di kode” berbeda dari “telah dieksploitasi di production”; audit ini tidak menguji eksploitasi pada production.

| ID | Prioritas | Bukti | Dampak dan tindakan wajib |
| --- | --- | --- | --- |
| SEC-01 | P0 | `api/config.php:6`; kandidat credential juga pada `update_credentials_and_push.sh:14` | Credential SMTP tertulis di repository publik. Rotasi/revoke di provider, pindah ke konfigurasi privat, audit salinan/history; jangan menyalin nilainya ke dokumen/log |
| AUTH-01 | P0 | `login.html:305` → `processLoginSuccess` | Email/password masuk tanpa verifikasi backend. Ganti jalur ini dengan OTP login yang diverifikasi server |
| AUTH-02 | P0 | `login.html:285` | Token Google hanya di-decode di browser. Server wajib memverifikasi signature dan claims sebelum membuat session |
| AUTH-03 | P0 | `api/db.php:33` | Header/cookie JSON dengan email dianggap authenticated; user ID dibentuk dari email. Pemeriksaan owner dapat dilewati dengan identitas palsu |
| AUTH-04 | P0 | `auth.js:5`, `auth.js:104`, `login.html:237` | Admin/PRO dihitung dari whitelist email dan browser state. Pindahkan role dan entitlement ke database |
| AUTH-05 | P0 | `api/auth_otp.php:15`, `:28`, `:81` | OTP plaintext dalam JSON; tidak ada throttle/attempt counter/CAPTCHA, hanya registrasi, dan verifikasi tidak menghasilkan session server |
| MAIL-01 | P0 | `api/mailer.php:69`, `api/test_mail.php:5`, `api/send_welcome_email.php:11` | Endpoint email dapat dipanggil langsung tanpa session/role. Jadikan layanan internal; endpoint tester dikeluarkan dari production |
| DATA-01 | P0 | `cv-dashboard.html:156`, `cv.html:1181`, `presentation.html:384` | Halaman aktif tidak memanggil API dokumen. Backend PHP sudah ada, tetapi operasi UI masih lokal |
| DATA-02 | P0 | `cv-dashboard.html:149` vs `cv.html:970` | Dashboard memakai email + versi v19, editor memakai ID + v18 atau key khusus. Membuka dari dashboard dapat memunculkan dokumen kosong baru |
| DATA-03 | P0 | `presentation.html:351`, `:403` | Key detail presentasi hanya memakai ID, tidak scope akun; list yang terpisah tidak melindungi isi dokumen pada browser bersama |
| DATA-04 | P0 | `cv.html:1190`, `:974` | Guest data otomatis diadopsi akun berikutnya; dua akun khusus memakai key CV sama. Hentikan adopsi otomatis dan key bersama |
| UI-01 | P0 | `presentation.html:760`, `:1418` | `loadDashboard()` memanggil `switchView('dashboard')`, yang memanggil `loadDashboard()` lagi. Stack overflow sudah direproduksi lokal |
| UI-02 | P1 | `editor.html:220` dan akhir file | Halaman lama memiliki banyak handler tanpa implementasi script. Jadikan route kompatibilitas menuju editor kanonis dengan query yang tervalidasi |
| UI-03 | P1 | `cv.html:251`, `:2351`; `index.html:39`; `cv-dashboard.html:168` | `showDashboardView`, `openAdminModal`, dan `getDenyTriawanSampleData` dipanggil tetapi tidak ditemukan definisinya di source aktif |
| UI-04 | P1 | `cv.html:1428`, `:1548`, `:1575` | History diinisialisasi tetapi perubahan input tidak menambah snapshot; undo/redo tidak punya riwayat baru |
| UI-05 | P1 | `presentation.html:485` | Adapter `google.script.run` hanya membungkus localStorage. `try/catch` di luar callback timer tidak menangkap error yang muncul di callback; loader/tombol dapat tertinggal |
| EXP-01 | P1 | `presentation.html:1595` | `writeFile()` tidak di-await; cleanup berjalan sebelum export selesai dan rejection tidak tertangkap catch luar |
| EXP-02 | P1 | `cv.html:188`, `:506`; export presentasi mulai `:1490` | PDF CV masih print browser; pagination panjang dan fidelity PDF/PPTX perlu validasi file nyata |
| SEC-02 | P0 | `cv-dashboard.html:267`, `cv.html:2293`, `presentation.html:1074` | Input pengguna dirangkai ke HTML/atribut/link tanpa escaping konsisten. Risiko XSS harus ditutup sebelum konten server ditampilkan |
| SEC-03 | P0 | `.htaccess`; `api/db.php:2`; `api/auth_otp.php:15` | Tidak ada deny rule di repo untuk data/OTP/registry/backup/script. Potensi paparan bila direktori deploy mengikuti repo; keadaan hosting belum diuji |
| API-01 | P1 | `api/cv.php`, `api/presentation.php` | Action mutasi menerima query GET, CORS wildcard, belum ada CSRF, validasi payload/version, dan penanganan error seragam |
| DB-01 | P1 | `api/db.php:8`, `:31` | SQLite/JSON fallback; error ditelan, penulisan JSON tanpa transaksi/locking. Kegagalan database bisa mengalihkan sumber data tanpa diketahui |
| UX-01 | P1 | `presentation.html` head; gambar lewat `FileReader` | Meta viewport belum ada; media base64 membebani localStorage; tombol hover-only perlu akses sentuh/keyboard |
| BILL-01 | P2 | `pricing.html`; `auth.js:149` | Rp49.000/bulan, paket tahunan, CTA WhatsApp dan plan lokal tidak sesuai arahan Rp33.000 + pajak; belum ada Midtrans |
| OPS-01 | P1 | Root `deploy_*`, `safe_deploy.sh`, `update_*`, `run_deploy_fix.py` | Banyak generator menimpa file dan beberapa melakukan force-push. Bukan pipeline deployment yang layak dijalankan ulang |
| OPS-02 | P1 | `deploy_codespaces.py:759`; `run_deploy_fix.py:320` | Parser Python menemukan syntax error; dua script singkat lain hanya import/print. Nama script tidak menjamin dapat dipakai |
| DOC-01 | P2 | `docs/GDP_FULL_AUDIT.md` | Dokumen lama menyebut `api/server.js` dan editor identik yang tidak sesuai checkout saat ini. Gunakan bukti source terbaru |

P0 = penghalang keamanan/fungsi inti; P1 = wajib sebelum rilis; P2 = tahap berikutnya atau perbaikan konsistensi.

### 3.3 Inventaris dan keputusan per kelompok

| Kelompok | File | Keputusan |
| --- | --- | --- |
| Halaman publik | `index.html`, `pricing.html` | Bangun ulang landing/pricing sesuai produk dan harga yang disetujui |
| Akun | `login.html`, `profile.html`, `auth.js` | Ganti sumber identitas dan session; pertahankan integrasi Google sebagai konfigurasi awal |
| CV | `cv-dashboard.html`, `cv.html`, `editor.html` | Pertahankan mesin CV; satukan data/API dan route; editor lama menjadi adapter redirect |
| Presentasi | `presentation.html` | Pertahankan layout/playback/export; perbaiki rekursi, async, data, keamanan rendering |
| Data/API | `api/db.php`, `api/cv.php`, `api/presentation.php` | Migrasi adapter ke MySQL, session terpercaya, authorization, transaksi dan validation |
| Auth/mail | `api/auth_otp.php`, `api/config.php`, `api/mailer.php`, `api/send_welcome_email.php`, `api/test_mail.php` | Pisahkan endpoint dari layanan; credential privat; hapus akses publik pengiriman/test email |
| Server rules | `.htaccess` | Routing eksplisit, perlindungan private paths, HTTPS dan security headers |
| Dokumentasi | `README.md`, delapan file `docs/GDP_*.md`, empat backup markdown di direktori tersembunyi | Sinkronkan sesudah implementasi; backup tidak masuk artifact publik |
| Generator | 34 file `.sh`/`.py` di root | Bekukan sebagai legacy; inventaris target tulis, arsipkan di luar production, hapus bertahap setelah pengganti teruji |

File generator yang diperiksa melalui inventaris/pemindaian: `deploy_auth_and_subscriptions.sh`, `deploy_codespaces.py`, `deploy_login_and_otp.sh`, `deploy_master.py`, `deploy_redirect_fix.sh`, `fix_ajax_test_mail.sh`, `fix_cv_now.py`, `fix_mail_test.sh`, `fix_mime_and_render.sh`, `run_deploy_fix.py`, `safe_deploy.sh`, `setup_and_push.sh`, `setup_auth_and_ecosystem.py`, `setup_cv_page.sh`, `update_15_themes_and_clean_sample.sh`, `update_500_professions_cv.sh`, `update_ats_cv_pro.sh`, `update_ats_cv_ultimate.sh`, `update_blank_cv_and_clean_contact.sh`, `update_credentials_and_push.sh`, `update_cv_dashboard.sh`, `update_cv_maker.sh`, `update_cv_pdf_fix.sh`, `update_cv_sample_deny.sh`, `update_cv_themes.sh`, `update_deny_triawan_full_cv.sh`, `update_executive_density_cv.sh`, `update_full_architecture_cv.sh`, `update_modern_ats_cv.sh`, `update_prestige_perfect_cv.sh`, `update_standardized_cv.sh`, `update_target_roles_and_clean_cv.sh`, `update_universal_ats_cv.sh`, `upgrade_pro_cv.sh`.

Tidak semua kode legacy perlu dipindahkan ke arsitektur baru. Beberapa berisi versi lengkap aplikasi lama, data sampel pribadi, atau source yang dibuat ulang; bukan fitur tambahan yang wajib dipertahankan.

## 4. Arsitektur target dan struktur deployment

### 4.1 Aliran sistem

```text
Browser
  ├─ Landing / Login / Profil
  ├─ Dashboard CV → Editor CV → Export
  └─ Dashboard Presentasi → Editor → Playback / Export
       │ HTTPS, cookie session, CSRF pada mutasi
       ▼
PHP API: Auth → Validasi → Owner/Entitlement → Layanan
       ├─ MySQL/MariaDB: akun, session, dokumen, versi, billing
       ├─ Private storage: gambar, thumbnail, export
       ├─ SMTP: OTP dan notifikasi akun
       ├─ Google verifier + Turnstile verifier
       └─ Midtrans adapter (fase B, default nonaktif)
```

Frontend dan API pada origin yang sama untuk menyederhanakan cookie dan CORS. Database tidak diakses langsung dari browser. Admin produk tidak otomatis mendapat hak membaca isi dokumen pengguna.

### 4.2 Struktur logis yang direncanakan

Struktur berikut **belum dibuat**; pemetaan fisiknya disesuaikan dengan document root paket Hostinger.

```text
project/
  prd.md
  README.md
  public/                   → hanya isi ini yang dapat dilayani web
    index.html, login.html, profile.html, pricing.html
    cv-dashboard.html, cv.html, editor.html, presentation.html
    assets/css/
    assets/js/{core,auth,cv,presentation}/
    api/                    → endpoint/facade kompatibel
    .htaccess
  app/
    Auth/, Documents/, Media/, Billing/, Mail/, Support/
  config/                   → schema config dan loader, tanpa secret di Git
  database/migrations/
  scripts/                  → deploy, migrasi, backup, health check teruji
  tests/{unit,integration,e2e,fixtures}/
  docs/

private-runtime/            → di luar document root dan artifact source
  environment-config
  uploads/, exports/, logs/, backups/
```

- Pemindahan ke `public/` dilakukan setelah asset path, link `.html`, clean URL, email link, dan domain root dipetakan.
- Jika hPanel menetapkan `public_html` tetap, tempatkan source privat sebagai sibling yang tidak disajikan HTTP; facade public membutuhkan path absolut/config tervalidasi.
- Tambahkan `.gitignore` untuk secret, runtime data, dependency vendor lokal, log, backup, dan file editor. `.gitignore` tidak menghapus secret dari history.
- Gunakan lockfile PHP/frontend dan build CSS lokal/CI; audit upgrade Tailwind terpisah dari perbaikan fungsi agar kelas lama tidak rusak.
- Pertahankan `api/cv.php`/`api/presentation.php` sebagai facade sementara; handler baru tidak boleh membuka jalur autentikasi lama.
- Hapus adapter palsu `google.script.run` dari runtime presentasi setelah semua call site memakai API client.

## 5. Database Hostinger dan migrasi

### 5.1 Persyaratan database

- Buat database dan user khusus GDP melalui hPanel, terpisah dari ERP/website lain dan terpisah antara staging/production. Cara penyediaan mengikuti [panduan database Hostinger](https://www.hostinger.com/support/1583542-how-to-create-a-new-mysql-database-in-hostinger/).
- Kredensial disimpan melalui konfigurasi privat di host. Privilege dibatasi sesuai fasilitas paket; akun aplikasi tidak boleh memperoleh akses ke database produk lain.
- Gunakan InnoDB, `utf8mb4`, prepared statements, foreign key/index relevan, dan transaksi untuk operasi multi-tabel.
- ID internal acak/stabil; jangan membentuk identitas dari email yang dibersihkan karakter karena dapat berbenturan dan berubah.
- Timestamp disimpan UTC; tampilan menggunakan zona waktu yang sesuai pengguna. Tanggal meeting bertipe tanggal, bukan dikonversi sebagai instant UTC.
- Validasi JSON di aplikasi; pilih JSON native atau LONGTEXT tervalidasi setelah versi MySQL/MariaDB diketahui.
- Gunakan migration versioning; tidak membuat/mengubah tabel di setiap request.
- Database gagal → API mengembalikan kegagalan eksplisit; jangan beralih diam-diam ke JSON/SQLite di production.

### 5.2 Skema konseptual

Nama/kolom berikut adalah rancangan untuk migration berikutnya, bukan klaim tabel yang sudah ada.

| Tabel | Kolom inti | Constraint / penggunaan |
| --- | --- | --- |
| `users` | `id`, `email`, `email_normalized`, `email_verified_at`, `name`, `avatar_media_id`, `role`, `status`, timestamps | Unique email canonical dengan kebijakan case yang terdokumentasi; jangan menghapus titik/plus secara generik |
| `auth_identities` | `id`, `user_id`, `provider`, `provider_subject`, timestamps | Unique `(provider, provider_subject)`; Google memakai `sub` |
| `sessions` | `id`, `user_id`, `token_hash`, `csrf_secret`, `created_at`, `last_seen_at`, `expires_at`, `revoked_at` | Token acak; simpan hash token; expiry dan revoke diperiksa setiap request |
| `otp_challenges` | `id`, `email_normalized`, `purpose`, `code_hmac`, `attempts`, `expires_at`, `consumed_at`, `sent_at` | OTP sekali pakai; consume dan counter atomik; challenge lama dibatalkan saat resend |
| `rate_limit_buckets` | `scope_hash`, `action`, `window_start`, `count`, `blocked_until` | Increment atomik berdasarkan akun/IP/aksi; jangan bergantung localStorage |
| `cvs` | `id`, `user_id`, `title`, `data_json`, `schema_version`, `version`, `is_draft`, `completeness`, timestamps, `deleted_at` | FK owner; index `(user_id, deleted_at, updated_at)`; versi untuk konflik edit |
| `presentations` | `id`, `user_id`, `name`, `meeting_date`, `data_json`, `schema_version`, `version`, timestamps, `deleted_at` | FK owner; slide tetap JSON untuk menjaga editor; status lifecycle konsisten |
| `document_revisions` | `id`, `cv_id` atau `presentation_id`, `version`, `data_json`, `created_at` | Tepat satu document FK terisi; unique per dokumen + versi; retensi terukur |
| `media_assets` | `id`, `user_id`, `storage_key`, `mime`, `size_bytes`, `sha256`, dimensions, timestamps | Nama file acak, file privat, MIME diverifikasi |
| `document_media` | `media_id`, `cv_id` atau `presentation_id` | Owner media harus sama dengan owner dokumen; menjaga referensi dan cleanup |
| `audit_events` | `id`, `actor_id`, `action`, `target_type`, `target_id`, `request_id`, `created_at`, safe metadata | Jangan mencatat OTP/token/password atau isi CV/presentasi |
| `migration_batches` | `id`, `source_type`, `source_hash`, `status`, counts, timestamps | Jejak migrasi dan rerun yang aman |
| `legacy_owner_mappings` | `id`, `legacy_identifier`, `user_id`, `verification_status`, evidence reference | Mapping lama tidak langsung dipercaya; kasus ambigu dikarantina |
| `plans` | `id`, `code`, `name`, `price_idr`, `currency`, `interval_unit`, `interval_count`, `active` | `pro_monthly`: 33000 IDR, interval 1 bulan; hanya rancangan fase B |
| `plan_entitlements` | `plan_id`, `feature_key`, `enabled`, `limit_value`, `period` | Angka kuota configurable; NULL berarti tidak dibatasi quota produk, bukan tanpa batas keamanan |
| `subscriptions` | `id`, `user_id`, `plan_id`, `status`, `period_start`, `period_end`, `cancel_at_period_end`, provider refs | Period dan status server-authoritative; expiry tidak bergantung cron saja |
| `billing_orders` | `id`, `user_id`, `plan_id`, provider order ID, subtotal, tax snapshot, total, currency, status | Harga dan pajak dibekukan saat order dibuat; unique order/idempotency key |
| `payments` | `id`, `order_id`, provider transaction ID, amount, status, fraud status, paid_at | Unique provider transaction; cocokkan amount/currency/order |
| `webhook_events` | `id`, provider, event/dedup key, received_at, processing_status, safe payload hash | Durable sebelum acknowledge; replay tidak memberi masa PRO dua kali |
| `subscription_grants` | `id`, `subscription_id`, `payment_id`, `period_start`, `period_end` | Unique payment grant; mendukung rekonsiliasi/refund tanpa menimpa pembayaran lain |
| `usage_counters` | `user_id`, `feature_key`, period, count | Transaksi atomik saat limit diaktifkan |
| `export_jobs` | `id`, `user_id`, document ref, document version, format, status, result_media_id, timestamps | Disiapkan bila export resmi berpindah server pada fase entitlement |

Tabel billing/revision tambahan boleh masuk migration terpisah saat fasenya dimulai. Pilih implementasi constraint “tepat satu FK” yang didukung versi database; validasi layanan tetap wajib.

### 5.3 Migrasi data lama

1. Ambil backup file hosting dan database aktual lebih dahulu; inventaris apakah production memakai SQLite, JSON, file lain, atau kombinasi. Checkout Git tidak memuat database production.
2. Periksa jumlah record, ukuran, schema, key lama, referensi media, dan duplikasi tanpa mencetak konten pribadi.
3. Minta pengguna login dengan identitas baru yang diverifikasi. Jangan mempercayai `user_id`, email, role, atau plan dari session browser lama.
4. **Owner lama tidak otomatis dianggap sah.** Karena auth lama dapat dipalsukan, mapping akun harus menggunakan bukti kepemilikan/provenance. Record ambigu dikarantina untuk review terbatas, bukan dibagikan otomatis kepada email yang tercantum.
5. Data browser yang jelas milik pengguna dapat ditawarkan sebagai import opt-in setelah verifikasi ownership; tampilkan preview hanya jika asal akun dapat dipastikan. Cache guest/shared yang ambigu tidak boleh ditampilkan atau diadopsi oleh akun yang kebetulan login.
6. Import membuat ID baru dan menyimpan mapping; tidak boleh overwrite record server hanya dengan mengirim ID lama. Gunakan checksum/idempotency agar rerun tidak membuat duplikat.
7. Pertahankan field CV, urutan slide, gambar, tema, notes, judul, status trash, dan tanggal; catat field yang tidak dikenali untuk review.
8. Bandingkan counts/checksum, sampel render, hasil export, dan akses dua akun pada staging sebelum cutover.
9. Jangan purge cache browser atau backup sebelum keberhasilan import diverifikasi dan ada konfirmasi pemulihan yang jelas. Tidak semua data localStorage bisa dipulihkan dari perangkat yang tidak tersedia.
10. Cutover menggunakan maintenance singkat atau penghentian write lama; hindari dua sumber data aktif. Session lama dicabut, seluruh akun login ulang.

### 5.4 Backup dan pemulihan

- Rancangan awal: backup database harian, backup pra-deploy, media incremental, retensi 30 hari dengan akses terbatas; kemampuan/storage/biaya Hostinger harus diverifikasi.
- Target awal RPO ≤24 jam dan RTO ≤4 jam; ukur melalui restore drill, bukan hanya keberhasilan membuat file backup.
- Restore diuji pada database terpisah dan menjaga ownership. Jangan memulihkan seluruh production ke snapshot lama untuk rollback kode karena akan membuang write baru.
- Rollback aplikasi hanya ke versi yang kompatibel dengan migration dan tidak menghidupkan kembali auth rentan; bila tidak ada versi aman, gunakan maintenance.

## 6. Autentikasi, registrasi, CAPTCHA, dan session

### 6.1 OTP email untuk registrasi dan login

Keputusan produk awal: **passwordless OTP**. Ini memenuhi dua opsi yang diminta tanpa mempertahankan kolom password yang saat ini tidak diverifikasi.

1. Pengguna memilih “Lanjutkan dengan email”, memasukkan email dan, untuk profil baru, nama.
2. Frontend memperoleh token CAPTCHA dan mengirim permintaan challenge ke server.
3. Server memvalidasi email, CAPTCHA, origin/CSRF pra-login, dan rate limit. Respons tidak mengungkap apakah email sudah terdaftar.
4. Generate OTP 6 digit dari CSPRNG; simpan HMAC dengan server pepper dan challenge ID, bukan OTP plaintext. TTL rancangan 5 menit.
5. Kirim melalui SMTP yang credential-nya sudah dirotasi. Tantangan dibatalkan bila pengiriman gagal; UI tidak menyebut email terkirim jika provider menolak.
6. Verifikasi challenge + OTP + purpose dengan batas percobaan; konsumsi challenge secara atomik.
7. Buat akun baru atau login akun yang ada sesuai purpose/flow. Server membuat session baru dan mengembalikan profil minimal.
8. Redirect hanya menuju route internal yang diizinkan; query ID divalidasi dan owner dicek lagi saat membuka dokumen.

Default keamanan rancangan: resend paling cepat 60 detik; maksimal 5 percobaan per challenge; batas kirim 5/jam per email dan 20/jam per IP; throttle verifikasi per akun/IP. Nilai dikonfigurasi setelah uji pengguna di jaringan bersama. Resend tidak boleh mereset batas akun/IP sehingga brute force tetap mungkin.

OTP expired/salah/replayed menghasilkan error yang jelas dan generik. CAPTCHA yang gagal tidak boleh memiliki fallback login tanpa validasi. Hindari hard lock panjang yang mudah dipakai untuk memblokir korban.

### 6.2 Sign in with Google

- Pertahankan client ID yang sudah dikonfigurasi sebagai input konfigurasi; periksa Authorized JavaScript Origins, consent screen, mode publik/testing, dan domain staging/production pada akun Google.
- Frontend meneruskan credential Google ke endpoint server. Verifikasi signature, `aud`, `iss`, `exp`, dan status email; gunakan `sub` sebagai identitas provider. Ikuti [panduan verifikasi Google](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token).
- Terapkan nonce/login CSRF sesuai flow GIS yang dipilih, challenge singkat, dan pencegahan replay di aplikasi.
- Setelah verifikasi, buat session GDP yang sama dengan metode OTP; jangan menjadikan ID token Google sebagai cookie session aplikasi.
- Jika email sudah ada dari OTP, lakukan account linking dengan bukti kendali akun yang ada/reautentikasi. Jangan merge otomatis hanya berdasarkan email dari token tak terverifikasi.
- Pengguna bisa menggunakan dua identity pada satu akun setelah linking berhasil; dokumen dan entitlement tidak diduplikasi.
- CAPTCHA dan throttle tetap melindungi endpoint auth. Penolakan popup, token expired, callback duplikat, dan Google tidak tersedia memiliki jalur pemulihan yang jelas.

### 6.3 CAPTCHA

Gunakan Turnstile dengan site key public dan secret key privat; staging memakai konfigurasi yang sesuai lingkungan. Siteverify dilakukan server dan memeriksa success, hostname, serta action yang diharapkan. Token kedaluwarsa/terpakai ditolak; jangan menganggap tampilan widget sebagai bukti validasi. Dasar integrasi: [validasi server Turnstile](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/).

Jika provider timeout, tampilkan retry dan pertahankan data form. Endpoint auth sensitif gagal tertutup; tidak membuat session. Jangan memasang CAPTCHA pada setiap autosave atau webhook pembayaran.

### 6.4 Session dan authorization

- Cookie production `Secure; HttpOnly; SameSite=Lax; Path=/`, host-only; gunakan prefix `__Host-` bila sesuai konfigurasi HTTPS.
- Token opaque acak, disimpan sebagai hash server. Session baru setelah login; regenerate saat privilege berubah.
- Default rancangan: idle timeout 24 jam dan absolute timeout 7 hari, dapat dikonfigurasi. Admin memerlukan reautentikasi untuk aksi sensitif.
- Endpoint `/me` memeriksa session di server; browser menyimpan tampilan profil saja, bukan bukti login/PRO.
- Logout mencabut session server, membersihkan tampilan/cache akun, dan memberi sinyal ke tab lain. Logout semua perangkat mencabut seluruh session akun.
- Mutasi memakai CSRF token yang terikat session, validasi Origin/Referer, dan metode yang benar. CORS tidak wildcard; endpoint internal same-origin.
- Validasi owner pada query dan layanan untuk list/get/save/duplicate/trash/restore/delete/media/export. Client tidak boleh mengubah `user_id`, role, plan, atau harga.
- Resource bukan milik pengguna memberi 404 konsisten; unauthenticated memberi 401; role/entitlement terlarang 403.
- Race logout/switch-account: batalkan request tertunda, jangan render respons akun A setelah akun B aktif, dan kosongkan state memory editor.
- `Cache-Control: private, no-store` untuk data akun/dokumen; jangan memasukkan respons privat ke CDN/service worker cache umum.

## 7. Kontrak API dan perlindungan dokumen

Endpoint berikut adalah **kontrak target**, belum endpoint yang tersedia. Pilihan clean routes atau facade `.php?action=...` boleh mengikuti hosting, tetapi middleware dan semantik harus sama.

| Endpoint logis | Metode | Ketentuan |
| --- | --- | --- |
| `/api/auth/challenge` | POST | OTP + CAPTCHA + rate limit; CSRF pra-login |
| `/api/auth/verify-otp` | POST | Consume challenge atomik, session baru |
| `/api/auth/google` | POST | Verifikasi token Google + anti-replay + CAPTCHA |
| `/api/auth/me` | GET | Session tervalidasi, profil dan entitlement minimal |
| `/api/auth/logout`, `/api/auth/logout-all` | POST | CSRF dan revoke |
| `/api/cvs`, `/api/presentations` | GET / POST | List milik sendiri / create, paginasi, ID dari server |
| `/api/{type}/{id}` | GET / PATCH | Owner wajib; update memakai expected version |
| `/api/{type}/{id}/duplicate` | POST | Owner sumber wajib; server membuat ID dan owner baru |
| `/api/{type}/{id}/trash`, `/restore` | POST | Lifecycle valid, transaksi, CSRF |
| `/api/{type}/{id}` | DELETE | Penghapusan permanen eksplisit dengan konfirmasi UI dan pemeriksaan referensi media |
| `/api/media` | POST | Validasi file, owner, quota keamanan, CSRF |
| `/api/media/{id}` | GET | Owner/otorisasi dokumen termasuk thumbnail |
| `/api/exports` | POST | Fase export service: auth, owner, format/version, entitlement |
| `/api/billing/checkout` | POST | Fase B; harga server, CSRF, idempotency |
| `/api/billing/orders/{id}` | GET | Hanya pemilik order |
| `/api/billing/midtrans/webhook` | POST | Fase B; signature provider, durable event; tanpa login/CAPTCHA/CSRF browser |

JSON respons harus konsisten, misalnya `{ok, data, error: {code, message, fields}, request_id}`. Status yang diperlukan: 400 payload invalid, 401 unauthenticated, 403 permission, 404 resource tidak ditemukan, 405 metode salah, 409 konflik versi, 413 terlalu besar, 422 validasi field, 429 throttle, dan 5xx layanan gagal. Jangan selalu mengembalikan HTTP 200 untuk error.

### 7.1 Penyimpanan yang dapat dipercaya

- Draft dibuat server dan ID diterima sebelum navigasi editor. Direct URL dengan ID tidak dikenal menampilkan not-found; jangan menciptakan dokumen baru dengan ID tersebut.
- Autosave debounce rancangan 800–1.200 ms; save manual memaksa perubahan terakhir dikirim. Antrian save per dokumen mencegah respons lama menimpa state baru.
- Sertakan `version`; update atomik `WHERE id = ? AND user_id = ? AND version = ?`. Jika tidak cocok, tampilkan konflik dan pilihan muat versi server/simpan salinan milik sendiri, bukan silent overwrite.
- Idempotency untuk create/import/duplicate memastikan retry dan klik ganda tidak membuat dokumen tambahan.
- Pisahkan status **Draft/Siap** dari **Belum tersimpan/Menyimpan/Tersimpan di server/Gagal/Konflik**.
- “Tersimpan di server” hanya setelah transaksi berhasil dan versi/hash respons cocok dengan snapshot yang dikirim. Jika pengguna mengetik lagi ketika respons datang, perubahan baru tetap ditandai belum tersimpan.
- Gagal/offline: pertahankan draft di memory dan, bila diizinkan, cache terbatas milik akun; tampilkan “belum tersinkron”. Jangan menampilkan cloud success.
- Perubahan akun tidak boleh membaca cache akun sebelumnya. Draft recovery tidak dijadikan dasar ownership.
- Reload/perpindahan halaman mengingatkan perubahan belum tersimpan. Jangan mengandalkan `beforeunload`/beacon sebagai satu-satunya penyimpanan.
- Trash rancangan 30 hari agar pemulihan lebih aman dari auto-purge browser 3 hari. Retensi perlu dikonfirmasi; angka UI, server, dan job harus konsisten. Tidak ada auto-purge sebelum migrasi disahkan.

### 7.2 Media, XSS, dan sharing

- JPEG/PNG/WebP saja pada tahap awal; verifikasi MIME, decode/re-encode, dimensi, ukuran, dan batas jumlah file. Rancangan batas keamanan: 5 MB per upload dan 20 megapiksel; uji resource Hostinger sebelum final.
- Tolak script, HTML, SVG aktif, MIME palsu, ekstensi ganda, path traversal, dan nama file sebagai path penyimpanan.
- Hilangkan EXIF yang tidak diperlukan; media tidak disimpan base64 di database dokumen utama.
- External image URL bukan proxy bebas. Untuk tahap awal gunakan upload; jika importer URL dibuat, blok alamat privat/metadata/redirect berbahaya dan validasi hasil unduhan.
- Escape teks dan atribut sesuai konteks; gunakan `textContent` untuk teks. Rich text hanya melalui sanitizer allowlist yang teruji; batasi URL ke skema yang aman.
- CSP diterapkan bertahap setelah inline handler diekstrak; izinkan hanya origin yang diperlukan untuk GIS/Turnstile/Midtrans pada fase terkait. Sertakan `nosniff`, frame policy, dan referrer policy sesuai kebutuhan.
- Fase A tidak menyediakan public sharing. Link editor yang dikirim orang lain tetap membutuhkan login owner dan akan ditolak untuk akun lain.
- Jika sharing nanti disetujui: tabel grant terpisah dengan owner, recipient/hashed token, read-only default, expiry, revoke, audit; viewer tidak pernah mendapat akses list/trash/riwayat owner. Desain ini belum diaktifkan.

## 8. Alur dan fitur ATS CV Maker

Alur utama: landing → login → dashboard CV → buat CV → edit/live preview → simpan → buka kembali → PDF.

### 8.1 Dashboard dan route

- Daftar server milik akun aktif dengan empty/loading/error state yang jelas.
- Create, rename, duplicate, trash, restore, permanent delete, dan completeness memakai kontrak data yang sama dengan editor.
- Dashboard khusus `cv-dashboard.html` menjadi entry point; `cv.html?id=...` adalah editor kanonis.
- `cv.html` tanpa ID diarahkan ke dashboard atau flow create eksplisit, bukan memanggil fungsi yang hilang.
- `editor.html` dan clean `/editor` hanya adapter menuju route kanonis. Pertahankan ID yang valid; `action=new` tidak membuat berulang pada refresh.
- Hapus auto-injection sampel pribadi. Sampel produk opsional memakai data fiktif dan dibuat sebagai salinan baru milik pengguna yang memilihnya.

### 8.2 Editor yang dipertahankan

- Seluruh 15 tema tetap tercatat dalam registry tema; hak pengguna nanti ditentukan server.
- Pertahankan profil, kontak, target role, pengalaman, pendidikan, kategori skills, sertifikasi, informasi tambahan, foto opsional, bahasa ID/EN, dan preview.
- Satukan normalisasi schema: `targetRoles` vs `title`, data pendidikan, foto, layout dan completeness tidak boleh berbeda antara dashboard/API/editor.
- Semua tab dan tombol terhubung; undo/redo mencatat snapshot bermakna dan sinkron dengan save, bukan hanya merender ulang.
- Validasi input memberi pesan inline tanpa menghapus isian. Hindari nilai placeholder/sampel menjadi data pengguna.
- Perlindungan XSS berlaku pada form dan preview sekaligus.

### 8.3 PDF A4

- Ukuran A4, margin jelas, pemisahan halaman terukur; dukung CV 1–5 halaman dengan nama/jabatan panjang dan section berulang.
- Teks dapat dipilih/diekstrak; jangan menjadikan seluruh CV satu screenshot jika produk menjanjikan CV yang ramah ATS.
- Foto opsional, font, link, simbol, teks ID/EN, serta header tidak terpotong. Section panjang boleh berlanjut secara wajar tanpa halaman kosong.
- Print browser diberi petunjuk “Simpan sebagai PDF” yang jujur bila tetap dipakai pada fase A. Jangan menyebut unduhan otomatis jika membuka dialog cetak.
- Uji extraction order dan keterbacaan; jangan menjanjikan skor/lolos semua ATS tanpa bukti.

## 9. Alur dan fitur Presentation Maker

Alur utama: landing → login → dashboard presentasi → create/open → editor → save → playback / PDF / PPTX → kembali ke dashboard.

### 9.1 Dashboard dan editor

- Pisahkan fungsi perubahan view dari fungsi load data agar tidak terjadi rekursi.
- Replace seluruh adapter Apps Script lokal dengan API client Promise yang error-nya ditangani pada lokasi eksekusi.
- Global loader selalu ditutup melalui `finally`; timeout memunculkan error/retry. Tombol kembali aktif setelah gagal atau batal.
- Create/rename/duplicate/trash/restore/delete memakai server dan owner tervalidasi. Jangan membuat starter pribadi otomatis saat list kosong.
- Pertahankan metadata meeting, judul, tanggal, author, company, logo, cover, agenda, slide, notes/MOM, tabel, chart, gambar/caption, dan closing.
- Tambah/hapus slide dan poin, penggantian layout, serta pergantian view tidak menghilangkan isian yang belum dipull ke state.
- Pertahankan minimum satu slide atau berikan empty-state yang bisa dipulihkan; validasi tabel/chart rusak tanpa menghentikan seluruh editor.
- Save manual/autosave menampilkan status server dan version conflict; field “author” adalah metadata, bukan owner untuk authorization.

### 9.2 Playback

- Play, next/previous, agenda jump, fullscreen/exit, keyboard, zoom/lightbox, pena/pointer, dan catatan meeting diuji.
- Tolakan fullscreen browser tidak menggagalkan playback biasa.
- Shortcut tidak mengambil alih input teks/notes; kontrol dapat diakses sentuh dan keyboard.
- Ukuran layar kecil tidak menutupi tombol keluar; state editor pulih setelah playback/export.

### 9.3 PDF/PPTX

- Export menunggu save terakhir atau menawarkan versi draft yang jelas; hasil mengacu pada satu snapshot versi dokumen.
- Await seluruh proses asynchronous, termasuk `writeFile`, loading font/gambar, dan rendering chart. Error ditampilkan dan tidak ada success sebelum file selesai.
- Aturan pause/cancel sesuai kemampuan library: hentikan tahapan yang masih bisa dibatalkan dan cleanup; jangan mengklaim bisa membatalkan file yang sudah diserahkan ke browser.
- PDF landscape 16:9, teks/caption tidak overflow, tabel panjang serta MOM dipaginasi atau dipecah dengan aturan eksplisit.
- PPTX memakai teks editable; chart/tabel native diutamakan. Elemen yang sementara raster harus diinformasikan; dukungan lebih dari satu gambar per slide harus konsisten dengan editor.
- Uji PowerPoint dan LibreOffice; bandingkan editor → playback → PDF → PPTX dengan fixture yang sama, termasuk 1, 10, dan 30 slide.
- Tidak ada kebutuhan Node/headless browser pada server fase A. Jika export server diperlukan untuk entitlement/fidelity, kelayakan runtime dan biaya menjadi gate sebelum billing.

## 10. Halaman depan dan standar UI/UX

### 10.1 Referensi dan hasil pencarian desain

Referensi yang diminta adalah [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), sebuah skill/data panduan desain, bukan satu template website siap pasang. Panduan [SKILL.md](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/.claude/skills/ui-ux-pro-max/SKILL.md) dibaca dan mesin rekomendasinya dijalankan dari salinan sementara di luar repository GDP.

Commit referensi: `15de38fb70bc80ae9276fa7703b48ae861a672e6`.

- Query design system: `productivity SaaS professional modern` → pola **Hero + Features + CTA**, gaya glassmorphism, Plus Jakarta Sans, primary biru, background terang.
- Query stack: `responsive form button loading` pada `html-tailwind` → feedback loading, pencegahan klik ganda, label tombol ikon, dan ukuran tombol konsisten.
- Hasil sesuai tipe produk SaaS produktivitas. Panduan stack menyebut versi Tailwind yang lebih baru; itu bukan bukti versi aplikasi sekarang dan bukan instruksi upgrade otomatis.

Adaptasi untuk GDP: efek kaca hanya pada navigasi/aksen; area kerja editor tetap solid dan mudah dibaca. CTA utama biru dipilih untuk konsistensi merek yang ada; orange rekomendasi tidak wajib dipakai. Ini keputusan desain proyek, bukan hasil template yang sudah dirender.

### 10.2 Struktur landing

1. Navigasi ringkas: produk, cara kerja, harga, bantuan, masuk/profil.
2. Hero: manfaat dua aplikasi; CTA “Buat CV” dan “Buat Presentasi”; preview hasil nyata menggunakan data fiktif.
3. Dua panel produk yang menunjukkan hasil dan alur pengguna secara jelas.
4. Tiga langkah: masuk → buat dan simpan → ekspor/presentasikan.
5. Keunggulan yang sudah lulus uji: lintas perangkat, dokumen privat, template, dan format export.
6. Pricing Free/PRO; sebelum billing aktif gunakan status “Segera tersedia” untuk checkout, bukan tombol pembayaran palsu.
7. FAQ penyimpanan, privasi, login, export, harga + pajak, dan pembaruan langganan.
8. Footer kontak, privasi, ketentuan, dan kebijakan pembayaran ketika billing diluncurkan.

Jangan membuat statistik pengguna, testimonial, logo pelanggan, klaim ATS, atau jaminan keamanan tanpa bukti. Produk di luar dua aplikasi utama tidak mendominasi landing.

### 10.3 Sistem visual dan interaksi

| Elemen | Arahan rancangan |
| --- | --- |
| Tipografi | Plus Jakarta Sans untuk antarmuka; font dokumen tetap sesuai tema |
| Warna | Primary `#2563EB`, teks `#1E293B`, background `#F8FAFC`, surface putih; state success/error/warning semantik |
| Layout | Container maksimum sekitar 1200–1280 px, ruang putih cukup, kartu preview rapi |
| Motion | Feedback singkat sesuai komponen, umumnya 150–250 ms; reveal ringan; patuhi `prefers-reduced-motion` |
| Tombol | Ukuran sentuh target 44×44 px, label jelas, focus ring, busy/error state; tidak bergantung hover |
| Form | Label tetap, error dekat field, dukungan paste OTP, autocomplete yang sesuai, Enter dapat dipakai |
| Aksesibilitas | Target WCAG 2.2 AA, kontras teks biasa ≥4.5:1, navigasi keyboard, focus tidak tertutup, pembaca layar |
| Responsive | Uji 375, 768, 1024, 1440 px; tidak ada overflow horizontal halaman; preview dokumen boleh scroll dalam panel |
| Loading | Skeleton/status yang terukur; dekorasi dan overlay tidak menutupi kontrol aktif |

Artefak tahap awal yang sudah dibuat: design tokens CSS, landing page, pricing page, navigasi responsive, auth-aware CTA transisi, dan reduced-motion fallback. Auth states server-side, komponen aplikasi internal, serta visual regression lengkap kedua editor tetap menjadi pekerjaan berikutnya.

## 11. Free/PRO dan rancangan Midtrans

### 11.1 Aturan komersial

- Satu paket **PRO Monthly** untuk seluruh fitur CV Maker dan Presentation Maker.
- Harga dasar **Rp33.000 / bulan**, mata uang IDR, pajak belum termasuk.
- Tidak ada harga tahunan yang ditetapkan. Harga Rp49.000/Rp299.000 di source lama harus diganti saat pricing dirilis.
- Besaran, jenis, dasar pengenaan, dan kewajiban pajak belum dipastikan; gunakan konfigurasi yang disahkan pemilik bisnis/akuntansi. Jangan mengasumsikan persentase tertentu.
- Checkout menampilkan subtotal, pajak, total, dan periode sebelum pengguna menyetujui. Gateway fee tidak otomatis dianggap pajak atau diteruskan ke pembeli.
- “Semua fitur” tidak berarti storage/upload/request tanpa batas fisik. Batas keamanan/fair-use harus dinyatakan terpisah dari kuota Free.

### 11.2 Matrix entitlement yang disiapkan

| Fitur | Free | PRO Monthly |
| --- | --- | --- |
| Login, privasi, akses data sendiri | Selalu tersedia | Selalu tersedia |
| Editor dasar CV/presentasi | Tersedia; kuota perlu keputusan | Seluruh fitur produk |
| Tema CV | Daftar subset belum ditetapkan; 5 tema lama hanya referensi | Semua 15 tema yang tersedia |
| Jumlah CV/presentasi | Configurable, angka TBD | Tidak dibatasi kuota Free; fair-use berlaku |
| Export PDF/PPTX | Format/jumlah/periodenya TBD | Seluruh format produk yang telah dirilis |
| Upload/media | Kuota storage TBD | Kapasitas profesional TBD, batas file keamanan tetap |
| Riwayat/recovery | Kebijakan TBD | Fitur yang dirilis dibuka |
| Sharing/AI yang belum dibuat | Tidak dijanjikan | Tidak dijanjikan sebagai fitur tersedia |

Feature flag `BILLING_ENABLED=false` dan `FREE_LIMITS_ENABLED=false` selama stabilisasi. Akun tetap tercatat sebagai Free; mode beta ditampilkan eksplisit bila akses fitur dibuka sementara. Jangan memalsukan status paid PRO untuk membuka UI.

### 11.3 Batas teknis entitlement

- Server menghitung entitlement pada create/save/upload/export, bukan hanya menyembunyikan tombol.
- Kuota bertambah secara atomik hanya setelah operasi yang didefinisikan berhasil; retry tidak menggandakan pemakaian.
- Pengguna PRO yang expired tetap dapat masuk, melihat dan mengambil data miliknya. Jangan menghapus dokumen otomatis karena downgrade atau limit terlampaui.
- **Export/premium preview yang seluruhnya dirender di browser tidak bisa dijaga kuat hanya dengan endpoint izin.** Pengguna dapat mencetak atau mengubah JavaScript lokal.
- Sebelum menjual batas export/premium yang wajib dipaksakan, pilih jalur render/export resmi di server/layanan worker dan kirim hanya hasil yang diotorisasi. Jika paket Hostinger tidak mendukungnya, tetapkan layanan pendamping beserta biaya atau batasi janji bisnis pada operasi yang benar-benar dikendalikan server.
- Hindari klaim DRM: screenshot/penyalinan konten yang sudah sah ditampilkan tidak dapat dicegah sepenuhnya.

### 11.4 Checkout dan aktivasi

Rancangan awal menggunakan [Midtrans Snap](https://docs.midtrans.com/docs/snap-overview). Ketersediaan metode pembayaran mengikuti aktivasi merchant.

1. User login memilih PRO; server membuat order dengan harga plan dan tax snapshot, bukan nominal dari browser.
2. Server meminta token checkout menggunakan Server Key privat dan order ID unik/idempotency key.
3. Browser membuka Snap; cancel/pending/failure menampilkan status dan memungkinkan pemulihan order yang sama.
4. Redirect/callback frontend hanya memperbarui UI menjadi “memeriksa pembayaran”. Tidak memberi entitlement.
5. Webhook diterima di HTTPS public endpoint khusus yang memverifikasi signature serta mencocokkan order/amount/currency. Simpan event sebelum respons sukses.
6. Worker atau proses server menerapkan perubahan order/payment/grant dalam transaksi; success yang sah memberi satu periode PRO.
7. `/me` atau endpoint status langganan mengembalikan entitlement terbaru.

Dasar verifikasi notifikasi adalah [dokumentasi webhook Midtrans](https://docs.midtrans.com/docs/https-notification-webhooks): signature SHA-512 dari rangkaian `order_id + status_code + gross_amount + ServerKey`, dengan format nominal provider dipertahankan. Gunakan perbandingan aman dan Get Status bila perlu rekonsiliasi; browser bukan sumber status bayar.

### 11.5 Status, idempotency, renewal, dan expiry

- Status order internal: `created`, `pending`, `paid`, `failed`, `expired`, `cancelled`, `refunded`, `partially_refunded`, `chargeback`.
- Status langganan: `inactive`, `active`, `past_due` untuk recurring bila dipakai, `expired`, `suspended`. Pembatalan akhir periode disimpan terpisah agar sisa periode berbayar tetap berlaku.
- `settlement`, atau `capture` dengan pemeriksaan fraud yang memenuhi syarat metode tersebut, menjadi kandidat paid; petakan seluruh status sesuai dokumentasi saat integrasi. `pending` tidak membuka PRO.
- Webhook duplikat/terbalik, request ulang, dan dua worker bersamaan tidak boleh menggandakan masa aktif. Unique payment grant dan transaksi menjadi pengaman utama.
- Jika event tidak dapat disimpan, kembalikan kegagalan agar provider dapat retry; jika sudah tersimpan, proses yang gagal dapat diulang dari antrean database.
- Simpan status terminal yang lebih baru; jangan menurunkan paid menjadi pending karena notifikasi terlambat. Refund/chargeback memakai aturan kompensasi terdokumentasi.
- Renewal manual awal: pengguna membayar untuk memperpanjang satu bulan kalender. Jika masih aktif, hitung dari `period_end`; jika expired, dari waktu pembayaran sah. Tanggal akhir bulan dijepit ke tanggal valid dengan anchor yang konsisten.
- Expiry diperiksa pada request server, cron hanya untuk notifikasi/rekonsiliasi/cleanup. Kegagalan cron tidak membuat PRO berlaku selamanya.
- Default tidak ada grace period akses berbayar sebelum diputuskan; data tetap aman saat expired.
- Refund penuh, parsial, dan chargeback harus dipetakan terhadap payment grant yang bersangkutan. Kebijakan komersial refund belum ditetapkan; pengujian teknis wajib mencegah downgrade pengguna yang masih memiliki grant lain yang sah.

**Monthly bukan otomatis auto-debit.** [Subscription API Midtrans](https://docs.midtrans.com/reference/api-methods-1) memiliki dukungan metode tertentu, saat referensi diperiksa berupa kartu dan GoPay tokenization. Auto-renew baru ditambahkan setelah merchant eligibility, consent, tokenization, pembatalan, retry, dan notifikasi berulang siap. Jangan menganggap seluruh metode Snap dapat recurring.

### 11.6 Gate aktivasi billing

- Semua gate Rilis A lulus, limit Free disahkan, harga/pajak/ketentuan jelas.
- Sandbox lulus untuk paid/pending/cancel/expired/failure, invalid signature, amount mismatch, duplicate/reordered webhook, outage, late settlement, renewal dan refund.
- Server key sandbox/production terpisah, tidak tercetak di source/log/browser.
- Aktifkan production bertahap setelah merchant terverifikasi dan satu transaksi uji yang diotorisasi pemilik berhasil direkonsiliasi.

## 12. Nonfungsional dan pengujian

### 12.1 Target kualitas

- Landing mobile: target LCP ≤2,5 detik, CLS ≤0,1, INP ≤200 ms pada profil uji yang dicatat; verifikasi lapangan setelah ada trafik.
- API metadata/save dokumen wajar: target p95 ≤1 detik pada staging untuk payload sekitar ≤250 KB dan 10 pengguna bersamaan, di luar upload/OTP/provider/export.
- Gambar dan resource besar dimuat sesuai kebutuhan; batasi ukuran total dokumen serta slide berdasarkan benchmark, bukan asumsi “unlimited”.
- Error UI memiliki pesan yang bisa ditindaklanjuti dan request ID; log server memuat metadata yang cukup tanpa isi pribadi.
- Tidak ada secret/PII di console produksi, laporan CI publik, fixture, atau screenshot demo.
- Security QA dimulai sejak fondasi dan diulang sebagai gate rilis; bukan ditunda sampai akhir seluruh fitur.

### 12.2 Matriks acceptance test wajib

| ID | Skenario | Hasil yang harus diperiksa |
| --- | --- | --- |
| T-A01 | OTP registrasi baru dan login existing | Satu akun, session server, redirect internal benar |
| T-A02 | OTP salah/expired/replay/resend paralel | Batas dan consume atomik, tanpa session |
| T-A03 | CAPTCHA hilang/palsu/expired/provider timeout | Ditolak dengan retry UI, tanpa bypass |
| T-A04 | Google valid; signature/audience/expiry/nonce salah | Hanya token valid menghasilkan session |
| T-A05 | OTP + Google email sama; linking belum/sudah dibuktikan | Tidak ada takeover atau akun duplikat tak terkendali |
| T-A06 | Logout, logout-all, expiry, tab kedua | Session lama tidak valid; data UI tidak tertinggal |
| T-S01 | Header/cookie JSON auth lama atau localStorage `isAdmin/isPro` palsu | Tidak memberi identitas/role/entitlement |
| T-S02 | User B memakai ID CV/presentasi/media/export milik A | List/read/write/duplicate/trash/restore/delete/download ditolak |
| T-S03 | Akun berganti saat fetch/save A masih berjalan | Respons A tidak tampil atau tersimpan di state B |
| T-S04 | Input HTML/script/URL berbahaya di field, notes, judul, chart, caption | Ditampilkan sebagai data aman, script tidak berjalan |
| T-S05 | GET mutasi, CSRF hilang, origin asing | Ditolak tanpa perubahan database |
| T-S06 | Akses HTTP data/config/log/backup/script/test mail | 403/404; tidak mengirim mail atau mengungkap isi |
| T-D01 | Save → refresh → logout/login → perangkat B | Isi, tema, media dan versi sama |
| T-D02 | Offline, database down, storage denied, save timeout | Tidak ada cloud success palsu; perubahan bisa dipulihkan |
| T-D03 | Dua tab mengedit versi sama | Konflik 409 dan pemulihan, tanpa silent overwrite |
| T-D04 | Double click/create retry/import ulang | Satu efek sesuai idempotency |
| T-D05 | Migrasi legacy valid dan ambigu, rerun batch | Mapping sah, count/checksum cocok; ambigu tidak dibagikan |
| T-C01 | Semua tombol dashboard CV dan route legacy | Tidak ada handler hilang, create/edit record yang sama |
| T-C02 | Seluruh tab, input, role, foto, tema, bahasa, undo/redo | Preview/save akurat; tidak ada error console |
| T-C03 | PDF CV pendek/panjang, 15 tema, foto/no photo, teks panjang | A4 konsisten, tidak terpotong, teks bisa diekstrak |
| T-P01 | Dashboard presentasi → open/create → save/back | Tidak ada rekursi, loader macet, atau data hilang |
| T-P02 | Slide/poin/gambar/chart/tabel/MOM/rename/duplicate/trash | State tersimpan dan dapat dibuka ulang |
| T-P03 | Playback keyboard/touch/fullscreen ditolak/notes | Kontrol dan exit bekerja, input tidak terganggu |
| T-P04 | PDF/PPTX 1/10/30 slide, multi-image, tabel/notes panjang | Fidelity terverifikasi; error/cancel membersihkan state |
| T-U01 | 375/768/1024/1440 px, keyboard, reduced motion | Semua kontrol terjangkau, kontras dan focus lulus |
| T-B01 | Harga browser dimodifikasi; callback success palsu | Harga server tetap benar, PRO tidak aktif |
| T-B02 | Signature/amount salah; webhook ulang/terbalik/paralel | Hanya satu grant dari pembayaran yang sah |
| T-B03 | Renewal akhir bulan, expiry tanpa cron, downgrade/refund | Masa aktif benar; dokumen tidak dihapus |
| T-O01 | Backup/restore, deploy gagal, rollback kompatibel | Data dan privacy tetap benar; tidak kembali ke auth rentan |

Browser target: Chrome/Edge desktop, Firefox, Safari bila tersedia, Android Chrome dan iOS Safari. Catat platform yang benar-benar diuji; jangan menyatakan PASS untuk perangkat yang belum tersedia.

## 13. Urutan pekerjaan kritis dan deployment

### 13.1 Pemeriksaan awal yang sudah dijalankan

Pekerjaan pada sesi penyusunan PRD:

```powershell
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/main
git ls-files
```

Selain itu: pemindaian semua file terlacak, pencarian handler/storage/API, pemeriksaan sintaks JavaScript, parser lima file Python, dan reproduksi rekursi presentasi dengan data/DOM tiruan. Hasil dirangkum pada bagian 3.

Skrip `safe_deploy.sh`, `deploy_*`, `update_*`, dan `run_deploy_fix.py` lama tidak dijadikan langkah eksekusi karena hasil telaah menunjukkan penimpaan file, force-push, dan/atau syntax error. Penggantinya harus dibuat dan diuji terlebih dahulu.

### 13.2 Tahapan implementasi

| Tahap | Pekerjaan konkret | Gate untuk lanjut |
| --- | --- | --- |
| 00 — PRD/baseline | Dokumen ini, daftar risiko, target schema, acceptance matrix | PRD tersimpan lokal; status implementasi tidak ambigu |
| 01 — Containment/fondasi | Backup privat, rotasi credential provider, private config, deny private paths, tutup tester/mail publik, bekukan generator legacy, staging | Secret lama tidak berlaku; source baru tanpa secret; endpoint berisiko tertutup |
| 02 — Hostinger/database | Verifikasi paket, siapkan database/user staging, migration dasar users/session/OTP/document, runtime & SMTP adapter | Koneksi/transaksi/rollback migration staging lulus; backup bisa restore |
| 03 — Auth/authorization | OTP + Google + CAPTCHA + session/CSRF + role server + owner middleware | Semua T-A dan owner API lulus sebelum endpoint data digunakan pengguna |
| 04 — Data/migrasi | API client, normalisasi payload, version conflict, media privat, mapping legacy, import dry run | T-D dan T-S lulus; data ambigu tidak dibuka |
| 05 — CV | Satukan dashboard/editor, route legacy, missing handlers, undo/redo, server save, PDF | T-C lulus, fixture PDF terverifikasi |
| 06 — Presentasi | Putus rekursi, Promise API, save/recovery, loader, playback, PDF/PPTX | T-P lulus, file export terverifikasi |
| 07 — UI depan & akun | Landing UI UX Pro Max, auth/profile/pricing, responsive/accessibility | T-U lulus; klaim produk sesuai fungsi dan billing belum aktif |
| 08 — Release A | Security regression, deployment rehearsal, restore drill, production cutover, smoke test | Tidak ada blocker P0/P1; monitoring dan rollback siap |
| 09 — Entitlement | Konfirmasi limit Free, implement enforcement server dan jalur export yang layak | Bypass UI tidak membuka operasi premium; data downgrade aman |
| 10 — Midtrans sandbox | Checkout, webhook, grants, expiry/renewal/refund, rekonsiliasi | T-B lulus pada sandbox |
| 11 — Billing live | Merchant/pajak/ketentuan siap, production credentials, transaksi uji terotorisasi | Pembayaran dan grant cocok; lalu feature flag diaktifkan bertahap |

Tahap 03 memerlukan tabel auth minimal dari tahap 02; ini memperjelas urutan lama yang menempatkan seluruh auth sebelum fondasi database. Perbaikan UI yang independen dapat disiapkan sebelumnya, tetapi rilis integrasi tetap mengikuti gate keamanan/data. Kerjakan satu paket perubahan yang terukur, laporkan hasil, lalu lanjut dependency berikutnya.

### 13.3 Langkah deployment Hostinger

1. Verifikasi paket hosting, domain/subdomain staging, document root, PHP, PDO MySQL, OpenSSL, cURL, mbstring, fileinfo, image extension, memory/time/upload limit, Composer/SSH dan cron.
2. Buat database staging dan production terpisah; catat host/name/user secara privat. Jangan menebak nama host database atau menggunakan credential lama.
3. Atur environment/config di luar web root: DB, APP_URL, SMTP, Google client ID, Turnstile keys, session pepper/key, feature flags; Midtrans keys baru diperlukan fase B.
4. Bangun release artifact dari commit yang jelas; hanya allowlist file runtime. Exclude `.git`, `.env`, `prd.md`, docs, tests, scripts legacy, data, database dump, backup, serta log dari web artifact.
5. Jalankan lint PHP, test integration dengan database target, E2E/visual/export checks, dependency/secret scan, dan `git diff --check` pada perubahan source.
6. Upload ke staging; deploy migration versioned; periksa endpoint health non-sensitif dan kesiapan database privat. Secrets/schema lengkap tidak ditampilkan health endpoint publik.
7. Uji OTP pada inbox pengujian yang disetujui, Google pada origin staging, CAPTCHA, dua akun isolasi, media, serta export. Jangan mengirim email massal sebagai test.
8. Rehearsal migrasi/backup/restore; pastikan tidak menimpa data atau website lain di akun hosting.
9. Production cutover dengan backup dan maintenance singkat; jalankan migration forward-compatible, deploy artifact, invalidasi aset lama, lalu login ulang dan smoke test dua akun.
10. Pantau error auth/save/export, latensi API, kegagalan SMTP, dan job. Bila gagal, hentikan write berisiko dan rollback aman; jangan mengaktifkan generator lama.

Jika SSH/Composer/Node tidak tersedia di hosting, build dependency/artifact pada lokal/CI dan upload hasilnya. SQL migration melalui phpMyAdmin bisa menjadi fallback operasional terkontrol, dengan nomor versi dan verifikasi hasil. Tidak boleh menaruh installer/migration publik tanpa autentikasi.

### 13.4 Refactor dan deletion

- Arsipkan generator dan backup source di lokasi privat; keluarkan dari artifact sejak tahap 01.
- Hapus handler mock auth, whitelist admin/PRO, adapter Apps Script palsu, dan auto-import guest setelah replacement dan tesnya tersedia.
- Jadikan `editor.html` compatibility redirect dahulu; hapus hanya jika analytics/link inventory membuktikan route lama sudah tidak dipakai atau redirect server menggantikannya.
- Pindahkan fungsi mail ke service privat, bukan sekadar menghapus endpoint sementara caller OTP masih bergantung padanya.
- Hapus duplikasi source/theme/data sampel secara bertahap setelah fixture dan regression tersedia. Setiap deletion punya daftar target, alasan, dan cara pemulihan dari commit/backup.
- `api/db.php` dan `deploy_codespaces.py` memiliki catatan sebagai pekerjaan lama yang dilindungi. Refactor yang dibutuhkan boleh dilakukan dengan diff terarah dan snapshot; jangan overwrite wholesale.
- Database/user document tidak masuk scope cleanup source. Rewrite Git history untuk menghapus secret memerlukan rencana koordinasi khusus karena memengaruhi clone lain; rotasi secret tetap harus dilakukan lebih dahulu.

## 14. Informasi yang masih perlu diverifikasi

Informasi berikut tidak menghalangi penyusunan PRD, tetapi diperlukan pada gate implementasi terkait. Jangan mengirim secret melalui `prd.md`, Git, screenshot publik, atau chat biasa.

| Informasi | Default/asumsi rancangan | Diperlukan sebelum |
| --- | --- | --- |
| Paket Hostinger dan domain final | Pemilik mengonfirmasi Web Hosting Unlimited; SKU/batas perlu cek hPanel; domain terindikasi `gdp.gaeks.com` belum dikonfirmasi | Setup staging/database/deploy |
| Akses hPanel/deploy, document root, database version | Belum diverifikasi | Tahap 02 |
| Data pengguna aktual: SQLite/JSON/cache/browser lain | Belum diinventaris di host | Migrasi dan cutover |
| SMTP setelah rotasi, SPF/DKIM/DMARC, batas pengiriman | SMTP Hostinger dalam kode, belum diuji | Auth live |
| Google OAuth project/origins/consent | Client ID ditemukan; pengaturan console belum diverifikasi | Google login staging/live |
| Turnstile domain/site keys | Pilihan provider rancangan, belum provisioned | Auth staging/live |
| Retensi trash/revision/backup | Usulan 30 hari untuk trash/backup | Purge otomatis |
| Limit Free, kapasitas PRO, fair-use | TBD, enforcement belum aktif | Tahap 09 |
| Pajak, invoice, refund, terms, privacy | TBD; harga dasar Rp33.000 sudah ditentukan | Billing live |
| Midtrans merchant/methods/recurring eligibility | Snap manual monthly renewal sebagai tahap pertama | Tahap 10–11 |
| Jalur export server jika limit premium harus kuat | Evaluasi PHP library/worker terpisah sesuai fidelity dan hosting | Entitlement export berbayar |

## 15. Aturan pelaksanaan dan status

### 15.1 Acuan untuk sesi pengembangan berikutnya

- Baca `prd.md`, cek HEAD/worktree, dan cocokkan temuan dengan source terbaru sebelum mengubah kode.
- Gunakan dokumen ini sebagai acuan kebutuhan yang lebih baru dari audit lama; instruksi langsung pemilik produk tetap prioritas.
- Catat perubahan keputusan dengan tanggal, alasan, dan dampak terhadap schema/API/tes.
- Nama endpoint, direktori, tabel, flag, dan job pada bagian target adalah rencana sampai implementasi benar-benar ada.
- Sesudah setiap tahap, catat file berubah, migration, test PASS/WARN/FAIL, issue tersisa, risiko data, dan prosedur rollback.
- Untuk implementasi berikutnya gunakan branch `codex/...`, perubahan kecil yang bisa ditinjau, dan test yang menguji perilaku. Publishing/deployment mengikuti urutan dan gate di atas.

### 15.2 Checklist status implementasi

- [x] Repository lokal terhubung dan baseline diverifikasi.
- [x] Inventaris/pemindaian statis seluruh file terlacak dan telaah alur aktif.
- [x] Bug rekursi presentasi direproduksi lokal dengan fungsi asli.
- [x] Referensi desain dibaca dan rekomendasi design system/stack dijalankan.
- [x] PRD lokal mencakup auth, database, data safety, aplikasi, desain, billing, deployment, dan acceptance tests.
- [x] Struktur target `app`, `config`, `database`, `public`, `scripts`, `tests`, dan runtime privat lokal disiapkan.
- [x] Migration schema awal dan konfigurasi environment contoh disiapkan tanpa secret production.
- [x] Landing page dan pricing publik baru diimplementasikan secara responsive; checkout tetap dinonaktifkan.
- [ ] Credential provider dirotasi; containment production diterapkan.
- [ ] Database Hostinger dibuat dan migrasi diuji.
- [ ] OTP/Google/CAPTCHA/session baru diimplementasikan dan diuji.
- [ ] Isolasi dokumen/media dan penyimpanan server lulus pengujian dua akun.
- [ ] Seluruh tombol dan export kedua aplikasi diperbaiki serta diverifikasi.
- [ ] Seluruh frontend publik dan kedua editor lulus visual regression pada matriks viewport lengkap.
- [ ] Deployment Rilis A selesai.
- [ ] Limit Free/PRO dan Midtrans sandbox diselesaikan.
- [ ] Billing production diaktifkan.

**Langkah implementasi berikutnya: selesaikan tahap 01 pada environment Hostinger (rotasi credential, backup, staging, dan verifikasi konfigurasi), lalu setup database serta auth server-side. Fondasi repository sendiri belum menutup seluruh celah runtime legacy.**

### 15.3 Riwayat keputusan

| Tanggal | Keputusan | Dampak |
| --- | --- | --- |
| 15 September 2026 | PRD v1.0 lokal berdasarkan audit baseline source | Menetapkan urutan perbaikan, acceptance tests, dan status pekerjaan yang belum diimplementasikan |
| 15 September 2026 | Pemilik mengonfirmasi Hostinger Web Hosting Unlimited | Rancangan deploy PHP/MySQL dan aset statis; tidak mensyaratkan Node/worker permanen pada host; domain dan resource masih diverifikasi |
| 15 September 2026 | Fondasi repository, migration awal, panduan Hostinger, landing, dan pricing dibuat | Menyiapkan jalur implementasi tanpa mengaktifkan auth atau billing yang belum aman |
