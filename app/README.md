# Application modules

Folder ini menjadi rumah layanan PHP yang tidak boleh dilayani langsung oleh web server.

- `Auth/`: OTP, Google identity verification, CAPTCHA, session, dan CSRF.
- `Documents/`: ownership, versioning, lifecycle CV dan presentasi.
- `Media/`: upload privat, validasi MIME, thumbnail, dan download terotorisasi.
- `Billing/`: plan, entitlement, order, webhook, dan adapter Midtrans (feature flag mati).
- `Mail/`: transport SMTP dan template email internal.
- `Support/`: database, konfigurasi, respons API, logging, dan rate limit.

Kode runtime baru masuk bertahap setelah migration dan test tersedia. Endpoint publik menjadi facade tipis di `public/api` atau root `api` selama masa kompatibilitas.
