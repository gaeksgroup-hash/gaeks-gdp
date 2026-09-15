# Database

Migration MySQL/MariaDB tersimpan di `migrations/` dan dijalankan berurutan pada database staging sebelum production. Setiap perubahan schema harus memiliki langkah verifikasi dan strategi rollback atau forward-fix.

`001_initial_schema.sql` adalah fondasi baru. Jangan jalankan pada production sebelum backup dan inventaris data lama selesai.
