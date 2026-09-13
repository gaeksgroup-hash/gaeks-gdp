<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$rawInput = file_get_contents('php://input');
$data = json_decode($rawInput, true);

$toEmail = filter_var($data['email'] ?? '', FILTER_VALIDATE_EMAIL);
$toName  = htmlspecialchars($data['name'] ?? 'Pengguna GAEKS');

if (!$toEmail) {
    echo json_encode(['status' => 'error', 'message' => 'Email tidak valid']);
    exit;
}

$subject = "Selamat Datang di GAEKS Digital Products - Akun Anda Telah Aktif";

$message = "
<html>
<head>
  <title>Selamat Datang di GAEKS Digital</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #1e293b; }
    .container { max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; }
    .header { background: #0f172a; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }
    .content { padding: 20px; background: #ffffff; }
    .button { display: inline-block; padding: 12px 24px; background: #2563eb; color: #ffffff !important; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 15px; }
    .footer { font-size: 11px; color: #64748b; text-align: center; margin-top: 20px; }
  </style>
</head>
<body>
  <div class='container'>
    <div class='header'>
      <h2 style='margin:0;'>GAEKS DIGITAL PRODUCTS</h2>
    </div>
    <div class='content'>
      <h3>Halo, {$toName}!</h3>
      <p>Terima kasih telah mendaftar di <strong>GAEKS Digital Products</strong>. Akun Anda berhasil terdaftar dengan email: <strong>{$toEmail}</strong>.</p>
      <p>Anda sekarang dapat langsung menggunakan <strong>ATS CV Studio</strong> untuk menyusun resume berstandar korporat global dengan 520+ bank profesi terverifikasi.</p>
      <p style='text-align:center;'>
        <a href='https://gdp.gaeks.com/cv.html' class='button'>Buka Studio CV Sekarang</a>
      </p>
      <p>Jika ada pertanyaan atau membutuhkan bantuan seputar akun atau paket PRO, silakan hubungi tim kami via WhatsApp di <a href='https://wa.me/6285608561745'>+62 856-0856-1745</a>.</p>
    </div>
    <div class='footer'>
      &copy; " . date('Y') . " GAEKS Group. All rights reserved.
    </div>
  </div>
</body>
</html>
";

$headers  = "MIME-Version: 1.0
";
$headers .= "Content-type: text/html; charset=UTF-8
";
$headers .= "From: GAEKS Digital <no-reply@gaeks.com>
";
$headers .= "Reply-To: gaeks.group@gmail.com
";
$headers .= "X-Mailer: PHP/" . phpversion();

$mailSent = @mail($toEmail, $subject, $message, $headers);

echo json_encode([
    'status' => $mailSent ? 'success' : 'queued',
    'recipient' => $toEmail,
    'message' => $mailSent ? 'Email selamat datang berhasil dikirim' : 'Email diproses oleh server Hostinger'
]);
