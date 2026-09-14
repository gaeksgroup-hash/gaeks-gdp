# GAEKS DIGITAL PLATFORM (GDP) â€” FULL CODEBASEF & PRODUCT AUDIT
 *Level Audit:* Arsitektur, Alur Data, Keamanan, dan Inventaris Sistem  
 *Target:* Repositori `gaeksgroup-hash/gaeks-gdp`  
 *Prioritas Modul Saat Ini:* (A) ATS CV Maker & (B) Presentation Maker

---

## 1. Inventaris Repositori (Repository Inventory)

### 1.1 Berkas Antarmuka & Halaman Utama (Frontend Pages)
- `bindex.html` (~19 KB):*
  Landing page publik ekosistem GAEKS Digital. Berisi hero section, katalog alat digital, review testimoni, dan tautan routing ke modul CV Maker serta Presentation Maker.
- `blogin.html` (~20 KB):*
  Portal otentikasi mandiri. Mengintegrasikan tombol login Google Identity Services (GIS) dan formulir login email dengan fallback simulasi OTP.
- `cv-dashboard.html` (~29 KB):*
  Dashboard pengelolaan resume ATS. Mengelola tab resume aktif, tab tempat sampah (*trash 3 hari*), kartu preview, tombol `+Buat Resume Baru`, duplikasi CV, dan kalkulator persentase kelengkapan.
- `vcv.html`, (~97 KB):*
  Studio Editor CV ATS utama. Terdiri atas formulir input data riwayat hidup bertahap, pemilihan 15 tema ATS, 2-way live preview lembar A4, tombol simpan progress, dan modul cetak PDF.
- ``editor.html` (~97 KB):*
  Berkas mirror/duplikat identik dari `cv.html`. Disimpan sementara untuk mengegah broken link dari riwayat tautan lama.
- ``presentation.html`, (~131 KB):*
  Studio Presentasi & Meeting deck. Mencakup pengelola daftar dek meeting, editor slide interaktif, presenter playback mode (layar penuh, canvas pena/laser pointer, timer), serta ekspor slide.
- ``profile.html` (~9 KB):*
  Halaman manajemen profil akun, ringkasan keanggotaan, dan identitas pengguna.
- ``pricing.html` (~7 KB):*
  Halaman katalog komparasi paket Free vs GAEKS PRO VIP.
- ``test_logos.html`, ``test_logos_render.html`, (< 1 KB):*
  Berkas uji visual statis (non-kritis).

### 1.2 Berkas Logika Otentikasi & State (`auth.js`)
- `auth.js` (~8 KB):*
  Menyediakan objek global `window.GaeksAuthP. Mengelola persistensi sesi ganda (`localStorage` key `gaeks_user_session_v3` dan cookie `gaieks_session_v3`), decoding payload Google JWT di client, registrasi pengguna ke database lokal `gaieks_users_db_v3`, dan penentuan tier VIP secara hardcoded.

### 1.3 Berkas Layanan Backend & REST API (`api/`)
- `api/db.php` (~2.5 KB):*
  Adapter database terpusat. Menginisialisasi koneksi SQLite PDO ke `api/data/gaeks.sqlite`, membuat tabel `cvs` dan `presentations` secara otomatis jika belum ada, menyediakan fungsi fallback JSON store (`*_store.json`), serta mengurai header sesi `X-Gaeks-Auth` dan cookie.
- `api/cv.php` (~6 KB):*
  REST handler untuk siklus hidup CV: `list`, `get`, `save`, `delete` (soft delete ke trash), `restore`, dan `delete_permanent`. Memvalidasi kepemilikan record berdasarkan `user_id`.
- `api/presentation.php`, (~3.6 KB):*
  REST handler untuk materi presentasi: `list`, `get`, `save`, dan perubahan status (`active`, `trashed`, `delete_permanent`).
- `api/mailer.php`, (~5.3 KB):*
  Endpoint pengirim notifikasi email transaksional pendaftaran dan status upgrade via PHP `mail()` / wrapper SMTP.
- `api/auth_otp.php`, (~5 KB):*
  Pengelola siklus OTP email berbasis JSON store sementara (`api/otp_store.json`).
- `api/server.js` (~12.5 KB):*
  Server HTTP Node.js mandiri. Berfungsi sebagai runtime alternatif pengujian lokal untuk menangani rute `/api/cv.php` dan `/api/presentation.php` di lingkungan tanpa PHP.
- `api/data/` (Directory):*
  Direktori penyimpanan persistent database `gaeks.sqlite` dan backup JSON.

### 1.4 Berkas Utilitas Root (Patch & Deployment Scripts)
- Berkas utilitas seperti `deploy_codespaces.py`, `update_gaeks.py`, dan `apply_all_fixes.py` di root direktori merupakan artefak sinkronisasi multi-tahap yang tidak boleh dieksekusi sembarangan agar tidak menimpa kode produksi.

---

## 2. Arsitektur Aktual Sistem (Actual Architecture)

Aplikasi saat ini mengusung pola **Multi-Page Application (MPA) Statis Berbasis Komponen Vanilla JavaScript**, dengan persistensi hibrida antara penyimpanan lokal browser dan REST API backend:



---

## 3. Peta Penyimpanan & API (Storage & API Map)

| Storage Key / Endpoint | Tipe | Komponen Pengguna | Deskripsi & Tujuan |
|---|---|---|---|
| `gaeks_user_session_v3` | localStorage & Cookie | `auth.js`, Semua Halaman | Menyimpan objek profil user yang aktif login (id, email, name, plan). |
| `gaieks_users_db_v3` | localStorage | `auth.js` | Mock user database client-side untuk fallback offline. |
| `gaeks_cv_user{hash}_v20` | localStorage | `cv-dashboard.html`, `cv.html` | Cache array dokumen CV milik pengguna aktif di perangkat lokal. |
| `gaeks_pres_list_{uid}_v2` | localStorage | `presentation.html` | Cache ringkasan metadata dek presentasi aktif dan tempat sampah. |
| `GAEKS_PRES_ITEM_{id}` | localStorage | `presentation.html` | Cache isi lengkap slide dan konten presentasi per ID materi. |
| `/api/cv.php?action=list` | GET REST | `cv-dashboard.html` | Mengambil seluruh daftar CV aktif atau trash milik `authUserId`. |
| `/api/cv.php?action=get` | GET REST | `cv.html` | Mengambil 1 dokumen CV spesifik berdasarkan query parameter `id`. |
| `/api/cv.php?action=save` | POST REST | `cv.html`, `cv-dashboard` | Menyimpan perubahan formulir CV atau inisialisasi resume baru. |
| `/api/cv.php?action=delete` | POST REST | `cv-dashboard.html` | Memindahkan CV ke tempat sampah (`deleted_at = timestamp`). |
| `/api/presentation.php` | GET/POST REST | `presentation.html` | Sinkronisasi materi presentasi ke tabel `presentations`ÔLite. |

---

## 4. Matriks Risiko Komprehensif (Ranked Risk Assessment)

### [CRITICAL] 1. Otorisasi Tingkat Fitur Berada di Sisi Client (Client-Side Entitlement)
- *Bukti:* Pada `auth.js`:
  ```javascript
  const VIP_WHITELIST = ["gaeks.group@gmail.com", "triawan25@gmail.com", "ranesath@gmail.com"];
  user.isPro = VIP_WHITELIST.includes[ãleanEmail);
  ```
- *Dampak:* Pengguna dapat memcodifikasi state `user.isPro = true` melalui Developer Tools console dan membuka batasan UI premium tanpa otentikasi server.
- *Mitigasi:* Verifikasi status langganan wajib dilakukan di endpoint backend saat memproses fitur PRO.

### [CRITICAL] 2. Desinkronisasi Dual-Persistence & Ancaman Kehilangan Data (Data-Loss Risk)
- *Bukti:* Pada `cv.html` dan `presentation.html`, proses penyimpanan menulis ke `localStorage` dan melakukan `fetch()` non-blocking ke backend.
-(*Dampak:* Jika fetch backend gagal (misal koneksi terputus atau session header tidak lolos), user menerima feedback "Tersimpan" di layar padahal data hanya ada di cache lokal. Saat user berpindah perangkat, dokumen tidak ditemukan.
-$*Mitigasi:* Standarsisasi mekanisme sync dengan status jelas: `Tersimpan di Cloud`, `Tersimpan di Perangkat (Offline)`, atau `Gagal Menyimpan`.

### [HIGH] 3. Duplikasi Berkas `editor.html`, dan `cv.html`, (Code Drift Risk)
-*Bukti:* Kedua berkas berukuran ~97 KB dengan fungsionalitas editor CV ATS yang sama.
-*Dampak:* Perubahan layout atau logika pada salah satu file berisiko tidak tercermin pada file lainnya, menimbulkan inkonsistensi perilaku.
-*Mitigasi:* Pertahankan `editor.html` sebagai wrapper redirect permanen ke `cv.html`, setelah dependensi diverifikasi.

### [HIGH] 4. Ketergantungan Cetak PDF pada Dialog Browser (`media print`)
- *Bukti:* Tombol ekspor PDF pada `cv.html` memanggil fungsi native `window.print()`.
- *Dampak:* Format tata letak A4 sangat rentan terpotong di tengah baris teks jika pengguna menggunakan margin non-standar atau mencetak dari perangkat mobile.
- *Mitigasi:* Perkuat aturan CSS` @page { size: A4 portrait; margin: 0; }` dan `page-break-inside: avoid` pada section pengalaman dan pendidikan.

### [MEDIUM] 5. Risiko Batas Kuota LocalStorage pada Slide Gambar Presentasi
- *Bukti:* `presentation.html` mengizinkan upload gambar slide via FileReader `readAsDataURL` ke dalam state JSON slide deck.
- *Dampak:* Gambar resolusi tinggi dapat melampaui batas 5MB `localStorage`, menyebabkan eksekusi simpan gagal melempar `QuotaExceededError`.
- *Mitigasi:* Terapkan kompresi Canvas otomatis sebelum menyimpan data URL gambar ke dalam objek slide.

### [LOW] 6. Ketergantungan Eksternal CDN (Tailwind CSS & Google Fonts)
- *Bukti:* Berkas HTML memuat stylesheet dark `cdn.tailwindcss.com` dan `fonts.googleapis.com`.
- *Dampak:* Halaman bergantung pada koneksi internet publik saat pertama kali dimuat.