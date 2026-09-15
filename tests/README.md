# Tests

- `unit/`: normalisasi data, pricing, status, dan validator murni.
- `integration/`: database, session, OTP, ownership, media, dan webhook.
- `e2e/`: alur pengguna CV/presentasi serta isolasi dua akun.
- `fixtures/`: data fiktif untuk CV, presentasi, export, dan migration.

Fixture tidak boleh berisi data pengguna production atau credential.

`e2e/backend_flow.mjs` menjalankan alur dua akun terhadap server PHP lokal dengan
SQLite fixture. Mode test mematikan pengiriman email nyata dan memakai OTP tetap;
kedua fitur tersebut tidak dapat aktif ketika `APP_ENV=production`.
