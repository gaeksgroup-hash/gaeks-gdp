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
