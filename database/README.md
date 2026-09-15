# Database

Migration MySQL/MariaDB tersimpan di `migrations/` dan dijalankan berurutan. Setiap perubahan schema harus memiliki langkah verifikasi dan strategi rollback atau forward-fix.

Untuk database baru, import `001_initial_schema.sql` lalu `002_auth_passwords.sql`.
Jangan menjalankan migration production tanpa backup dan verifikasi target database.
