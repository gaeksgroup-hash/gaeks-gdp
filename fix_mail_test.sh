#!/bin/bash
set -e

echo "=== 1. Memperbarui api/mailer.php ==="
cat << 'FILE_MAILER' > api/mailer.php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/config.php';

function sendHostingerSmtp($toEmail, $toName, $subject, $htmlContent) {
    $socket = @fsockopen("ssl://" . SMTP_HOST, SMTP_PORT, $errno, $errstr, 15);
    if (!$socket) {
        $headers  = "MIME-Version: 1.0\r\nContent-Type: text/html; charset=UTF-8\r\nFrom: " . SMTP_FROM_NAME . " <" . SMTP_USER . ">\r\nReply-To: " . REPLY_TO_EMAIL . "\r\n";
        @mail($toEmail, $subject, $htmlContent, $headers);
        return ["status" => "warning", "message" => "Sent via native fallback"];
    }

    $read = function($sock) {
        $res = "";
        while ($line = fgets($sock, 515)) {
            $res .= $line;
            if (substr($line, 3, 1) == " ") break;
        }
        return $res;
    };

    $read($socket);
    fputs($socket, "EHLO " . gethostname() . "\r\n"); $read($socket);
    fputs($socket, "AUTH LOGIN\r\n"); $read($socket);
    fputs($socket, base64_encode(SMTP_USER) . "\r\n"); $read($socket);
    fputs($socket, base64_encode(SMTP_PASS) . "\r\n");
    $authRes = $read($socket);

    if (substr($authRes, 0, 3) != "235") {
        fclose($socket);
        return ["status" => "error", "message" => "Autentikasi SMTP Gagal: $authRes"];
    }

    fputs($socket, "MAIL FROM: <" . SMTP_USER . ">\r\n"); $read($socket);
    fputs($socket, "RCPT TO: <" . $toEmail . ">\r\n"); $read($socket);
    fputs($socket, "DATA\r\n"); $read($socket);

    $headers  = "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $headers .= "From: =?UTF-8?B?" . base64_encode(SMTP_FROM_NAME) . "?= <" . SMTP_USER . ">\r\n";
    $headers .= "To: =?UTF-8?B?" . base64_encode($toName) . "?= <" . $toEmail . ">\r\n";
    $headers .= "Reply-To: <" . REPLY_TO_EMAIL . ">\r\n";
    $headers .= "Subject: =?UTF-8?B?" . base64_encode($subject) . "?=\r\n";
    $headers .= "X-Mailer: GAEKS Executive Mailer\r\n";

    $body = $headers . "\r\n" . $htmlContent . "\r\n.\r\n";
    fputs($socket, $body);
    $sendRes = $read($socket);
    fputs($socket, "QUIT\r\n");
    fclose($socket);

    if (substr($sendRes, 0, 3) == "250") {
        return ["status" => "success", "message" => "Email berhasil dikirim ke " . $toEmail];
    } else {
        return ["status" => "error", "message" => "Gagal kirim: " . $sendRes];
    }
}

if (realpath(__FILE__) === realpath($_SERVER['SCRIPT_FILENAME'] ?? '')) {
    $rawInput = file_get_contents('php://input');
    $data = json_decode($rawInput, true) ?? [];

    if (empty($data)) {
        $data = array_merge($_GET, $_POST);
    }

    $action  = $data['action'] ?? 'welcome';
    $toEmail = filter_var($data['email'] ?? $data['to'] ?? 'gaeks.group@gmail.com', FILTER_VALIDATE_EMAIL);
    $toName  = htmlspecialchars($data['name'] ?? 'Pengguna GAEKS');

    if ($action === 'welcome') {
        $subject = "Selamat Datang di GAEKS Digital Products - Akun Anda Telah Aktif";
        $html = "
        <div style='max-width:600px;margin:auto;font-family:Arial,sans-serif;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;background:#ffffff;'>
          <div style='background:#0f172a;padding:24px;text-align:center;'>
            <h2 style='color:#ffffff;margin:0;font-size:20px;'>GAEKS DIGITAL PRODUCTS</h2>
            <p style='color:#94a3b8;margin:4px 0 0 0;font-size:12px;'>Executive ATS CV Studio & Corporate Solutions</p>
          </div>
          <div style='padding:28px 24px;color:#1e293b;line-height:1.6;'>
            <h3 style='margin-top:0;'>Halo, {$toName}!</h3>
            <p>Terima kasih telah bergabung di <strong>GAEKS Digital Products</strong>. Akun Anda telah aktif menggunakan email: <strong>{$toEmail}</strong>.</p>
            <p>Anda dapat langsung menyusun resume ATS berstandar internasional dengan 520+ bank profesi.</p>
            <p style='text-align:center;margin:24px 0;'>
              <a href='https://gdp.gaeks.com/cv.html' style='display:inline-block;padding:12px 28px;background:#2563eb;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:13px;'>Buka ATS CV Studio &rarr;</a>
            </p>
            <p style='font-size:12px;color:#64748b;'>Balas email ini jika ada pertanyaan atau hubungi WhatsApp di <a href='https://wa.me/6285608561745' style='color:#2563eb;'>+62 856-0856-1745</a>.</p>
          </div>
          <div style='background:#f1f5f9;padding:16px;text-align:center;font-size:11px;color:#64748b;'>
            &copy; " . date('Y') . " GAEKS Group. All rights reserved.
          </div>
        </div>";
    } else {
        $subject = htmlspecialchars($data['subject'] ?? 'Pemberitahuan dari GAEKS Digital');
        $content = nl2br(htmlspecialchars($data['message'] ?? 'Terima kasih telah menggunakan layanan GAEKS.'));
        $html = "<p>{$content}</p>";
    }

    echo json_encode(sendHostingerSmtp($toEmail, $toName, $subject, $html));
    exit;
}
FILE_MAILER

echo "=== 2. Memperbarui api/test_mail.php (Antarmuka Visual Uji Kirim Email) ==="
cat << 'FILE_TEST' > api/test_mail.php
<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/mailer.php';

$target = filter_var($_GET['to'] ?? $_GET['email'] ?? 'gaeks.group@gmail.com', FILTER_VALIDATE_EMAIL);
if (!$target) $target = 'gaeks.group@gmail.com';

$result = null;
if (isset($_GET['send']) && $_GET['send'] === '1') {
    $subject = "Uji Coba Pengiriman no-reply@gaeks.com - " . date('d M Y H:i:s');
    $body = "
    <div style='font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:20px;border:1px solid #cbd5e1;border-radius:10px;'>
      <h2 style='color:#0f172a;'>Uji Coba Hostinger SMTP Berhasil!</h2>
      <p>Halo Admin GAEKS,</p>
      <p>Email ini dikirimkan langsung dari server Hostinger menggunakan alamat resmi <strong>no-reply@gaeks.com</strong>.</p>
      <p>Sistem notifikasi pendaftaran akun dan konfirmasi pembelian kini telah aktif 100%.</p>
      <hr style='border:none;border-top:1px solid #e2e8f0;margin:20px 0;'>
      <p style='font-size:12px;color:#64748b;'>Waktu server: " . date('Y-m-d H:i:s') . "</p>
    </div>";
    $result = sendHostingerSmtp($target, "Admin GAEKS", $subject, $body);
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Tes Pengiriman Email Hostinger | GAEKS Digital</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px 20px; }
    .card { max-width: 500px; margin: auto; background: #1e293b; padding: 30px; border-radius: 16px; border: 1px solid #334155; }
    h2 { margin-top: 0; color: #60a5fa; }
    p { font-size: 14px; color: #94a3b8; }
    input[type=email] { width: 100%; box-sizing: border-box; padding: 12px; background: #0f172a; border: 1px solid #475569; border-radius: 8px; color: white; margin: 10px 0 20px 0; font-size: 14px; }
    button { width: 100%; padding: 14px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px; }
    button:hover { background: #1d4ed8; }
    .alert { padding: 12px; border-radius: 8px; margin-bottom: 20px; font-size: 13px; }
    .success { background: #064e3b; border: 1px solid #059669; color: #a7f3d0; }
    .error { background: #881337; border: 1px solid #be123c; color: #fecdd3; }
  </style>
</head>
<body>
  <div class="card">
    <h2>🧪 Uji Pengiriman Email Hostinger</h2>
    <p>Pengirim: <strong>no-reply@gaeks.com</strong><br>Server: <strong>smtp.hostinger.com:465 (SSL)</strong></p>

    <?php if ($result): ?>
      <?php if ($result['status'] === 'success'): ?>
        <div class="alert success">
          <strong>✓ Sukses!</strong> <?php echo htmlspecialchars($result['message']); ?>.<br>
          Silakan periksa inbox atau folder spam email tujuan Anda sekarang.
        </div>
      <?php else: ?>
        <div class="alert error">
          <strong>✕ Gagal:</strong> <?php echo htmlspecialchars($result['message']); ?>
        </div>
      <?php endif; ?>
    <?php endif; ?>

    <form method="GET" action="">
      <input type="hidden" name="send" value="1">
      <label style="font-size: 12px; font-weight: bold; color: #cbd5e1;">Kirim Email Uji Coba Ke:</label>
      <input type="email" name="to" value="<?php echo htmlspecialchars($target); ?>" required>
      <button type="submit">Kirim Email Sekarang &rarr;</button>
    </form>
  </div>
</body>
</html>
FILE_TEST

echo "=== 3. Mem-push pembaruan ke GitHub ==="
git add api/mailer.php api/test_mail.php
git commit -m "fix: resolve email parameter parsing and add visual interactive tester for Hostinger SMTP" || true
git push origin main

echo "=== Selesai! Buka https://gdp.gaeks.com/api/test_mail.php di browser ==="
