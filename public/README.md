# Future public document root

Target akhir deployment adalah menjadikan folder ini satu-satunya document root. Selama transisi, halaman aktif masih berada di root repository agar URL production yang ada tidak terputus.

Saat cutover, salin hanya halaman, aset terbangun, facade API, dan `.htaccess` yang diperlukan. Jangan memasukkan `app`, `config`, `database`, `docs`, `scripts`, `tests`, backup, atau secret.
