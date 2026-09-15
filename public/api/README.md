# Public API facade

Direktori ini disiapkan sebagai satu-satunya entry point HTTP untuk backend baru. Implementasi berikutnya harus meneruskan request ke service di `app/`, mengambil secret dari konfigurasi privat, dan tidak menyimpan data pengguna di document root.

Endpoint legacy pada root `api/` dipertahankan sementara untuk compatibility, tetapi tidak boleh dianggap sebagai model keamanan final.
