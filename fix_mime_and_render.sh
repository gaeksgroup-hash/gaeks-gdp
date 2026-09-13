#!/bin/bash
set -e

echo "=== Memperbarui api/test_mail.php agar Browser Merender Tampilan Visual ==="

cat << 'FILE_TEST' > api/test_mail.php
<?php
header('Content-Type: text/html; charset=UTF-8');
require_once __DIR__ . '/config.php';

$target = filter_var($_GET['to'] ?? $_GET['email'] ?? 'gaeks.group@gmail.com', FILTER_VALIDATE_EMAIL);
if (!$target) $target = 'gaeks.group@gmail.com';

$result = null;
if (isset($_GET['send']) && $_GET['send'] === '1') {
    $subject = "Uji Coba Pengiriman no-reply@gaeks.com - " . date('d M Y H:i:s');
    $htmlContent = "
    <div style='font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:24px;border:1px solid #cbd5e1;border-radius:12px;background:#ffffff;'>
      <div style='background:#0f172a;padding:16px;border-radius:8px;text-align:center;margin-bottom:20px;'>
        <h2 style='color:#ffffff;margin:0;'>GAEKS DIGITAL PRODUCTS</h2>
      </div>
      <h3 style='color:#0f172a;margin-top:0;'>Uji Coba Hostinger SMTP Berhasil!</h3>
      <p>Halo Admin GAEKS,</p>
      <p>Email ini dikirimkan langsung dari server Hostinger melalui alamat resmi <strong>no-reply@gaeks.com</strong>.</p>
      <p>Sistem notifikasi pendaftaran dan langganan telah aktif 100%.</p>
      <hr style='border:none;border-top:1px solid #e2e8f0;margin:20px 0;'>
      <p style='font-size:12px;color:#64748b;'>Waktu server: " . date('Y-m-d H:i:s') . "</p>
    </div>";

    $socket = @fsockopen("ssl://" . SMTP_HOST, SMTP_PORT, $errno, $errstr, 15);
    if (!$socket) {
        $result = ["status" => "error", "message" => "Gagal terhubung ke Hostinger SMTP: $errstr ($errno)"];
    } else {
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
            $result = ["status" => "error", "message" => "Autentikasi SMTP Gagal: $authRes. Periksa kata sandi."];
        } else {
            fputs($socket, "MAIL FROM: <" . SMTP_USER . ">\r\n"); $read($socket);
            fputs($socket, "RCPT TO: <" . $target . ">\r\n"); $read($socket);
            fputs($socket, "DATA\r\n"); $read($socket);

            $headers  = "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
            $headers .= "From: =?UTF-8?B?" . base64_encode(SMTP_FROM_NAME) . "?= <" . SMTP_USER . ">\r\n";
            $headers .= "To: <" . $target . ">\r\n";
            $headers .= "Reply-To: <" . REPLY_TO_EMAIL . ">\r\n";
            $headers .= "Subject: =?UTF-8?B?" . base64_encode($subject) . "?=\r\n";
            $headers .= "X-Mailer: GAEKS Executive Mailer\r\n";

            $body = $headers . "\r\n" . $htmlContent . "\r\n.\r\n";
            fputs($socket, $body);
            $sendRes = $read($socket);
            fputs($socket, "QUIT\r\n");
            fclose($socket);

            if (substr($sendRes, 0, 3) == "250") {
                $result = ["status" => "success", "message" => "Email berhasil dikirim ke " . $target];
            } else {
                $result = ["status" => "error", "message" => "Gagal kirim: " . $sendRes];
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tes Pengiriman Email Hostinger | GAEKS Digital</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px 20px; margin: 0; }
    .card { max-width: 480px; margin: auto; background: #1e293b; padding: 32px; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
    h2 { margin-top: 0; color: #60a5fa; font-size: 20px; }
    p { font-size: 13px; color: #94a3b8; line-height: 1.5; }
    input[type=email] { width: 100%; box-sizing: border-box; padding: 12px; background: #0f172a; border: 1px solid #475569; border-radius: 8px; color: white; margin: 8px 0 20px 0; font-size: 14px; }
    input[type=email]:focus { outline: none; border-color: #3b82f6; }
    button { width: 100%; padding: 14px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 14px; transition: background 0.2s; }
    button:hover { background: #1d4ed8; }
    .alert { padding: 14px; border-radius: 8px; margin-bottom: 20px; font-size: 13px; line-height: 1.4; }
    .success { background: #064e3b; border: 1px solid #059669; color: #a7f3d0; }
    .error { background: #881337; border: 1px solid #be123c; color: #fecdd3; }
    .info { background: #0f172a; border: 1px solid #334155; padding: 12px; border-radius: 8px; font-size: 12px; color: #cbd5e1; margin-bottom: 20px; }
  </style>
</head>
<body>
  <div class="card">
    <h2>🧪 Uji Pengiriman Email Hostinger</h2>
    
    <div class="info">
      <div><strong>Pengirim:</strong> no-reply@gaeks.com</div>
      <div><strong>Server:</strong> smtp.hostinger.com:465 (SSL)</div>
      <div><strong>Balasan (Reply-To):</strong> gaeks.group@gmail.com</div>
    </div>

    <?php if ($result): ?>
      <?php if ($result['status'] === 'success'): ?>
        <div class="alert success">
          <strong>✓ Sukses!</strong> <?php echo htmlspecialchars($result['message']); ?>.<br>
          Silakan periksa kotak masuk (atau folder spam) di akun Gmail Anda sekarang.
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
    
    <p style="text-align: center; margin-top: 24px; margin-bottom: 0;">
      <a href="/cv.html" style="color: #60a5fa; text-decoration: none; font-size: 12px;">&larr; Kembali ke Studio CV</a>
    </p>
  </div>
</body>
</html>
FILE_TEST

git add api/test_mail.php
git commit -m "fix: enforce text/html header on test_mail.php so browsers render UI properly" || true
git push origin main

echo "=== SELESAI! Buka kembali https://gdp.gaeks.com/api/test_mail.php ==="
