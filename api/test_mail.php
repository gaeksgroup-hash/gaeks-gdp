<?php
require_once __DIR__ . '/mailer.php';
$to = $_GET['to'] ?? 'gaeks.group@gmail.com';
echo "<h2>Menguji Pengiriman Email via Hostinger SMTP (no-reply@gaeks.com)...</h2>";
echo "<p>Penerima: <strong>$to</strong></p>";
$res = sendHostingerSmtp($to, "Admin GAEKS", "Uji Coba Sistem no-reply@gaeks.com", "<p>Koneksi Hostinger SMTP (smtp.hostinger.com:465) berhasil!</p>");
echo "<pre>"; print_r($res); echo "</pre>";
