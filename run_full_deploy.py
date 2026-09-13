import os, json, subprocess

print("=== 1. Membuat direktori api dan konfigurasi SMTP Hostinger ===")
os.makedirs("api", exist_ok=True)

# .htaccess
with open(".htaccess", "w") as f:
    f.write("DirectoryIndex index.html index.php cv.html\nAddDefaultCharset UTF-8\n")

# api/config.php
with open("api/config.php", "w") as f:
    f.write('''<?php
// GAEKS DIGITAL SMTP CONFIGURATION (HOSTINGER)
define('SMTP_HOST', 'smtp.hostinger.com');
define('SMTP_PORT', 465); // SSL
define('SMTP_USER', 'no-reply@gaeks.com');
define('SMTP_PASS', 'Adagagap499!');
define('SMTP_FROM_NAME', 'GAEKS Digital Products');
define('REPLY_TO_EMAIL', 'gaeks.group@gmail.com');
define('ADMIN_NOTIFICATION_EMAIL', 'gaeks.group@gmail.com');
''')

# api/mailer.php
with open("api/mailer.php", "w") as f:
    f.write('''<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
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

$rawInput = file_get_contents('php://input');
$data = json_decode($rawInput, true) ?? [];

$action  = $data['action'] ?? 'welcome';
$toEmail = filter_var($data['email'] ?? '', FILTER_VALIDATE_EMAIL);
$toName  = htmlspecialchars($data['name'] ?? 'Pengguna GAEKS');

if (!$toEmail) {
    echo json_encode(["status" => "error", "message" => "Email tidak valid."]);
    exit;
}

if ($action === 'welcome') {
    $subject = "Selamat Datang di GAEKS Digital Products - Akun Anda Telah Aktif";
    $html = "
    <div style='max-width:600px;margin:auto;font-family:Arial,sans-serif;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;background:#ffffff;'>
      <div style='background:#0f172a;padding:24px;text-align:center;'>
        <h2 style='color:#ffffff;margin:0;font-size:20px;letter-spacing:1px;'>GAEKS DIGITAL PRODUCTS</h2>
        <p style='color:#94a3b8;margin:4px 0 0 0;font-size:12px;'>Executive ATS CV Studio & Corporate Solutions</p>
      </div>
      <div style='padding:28px 24px;color:#1e293b;line-height:1.6;'>
        <h3 style='margin-top:0;'>Halo, {$toName}!</h3>
        <p>Terima kasih telah mendaftar di <strong>GAEKS Digital Products</strong>. Akun Anda telah aktif menggunakan email: <strong>{$toEmail}</strong>.</p>
        <p>Sekarang Anda dapat langsung menyusun resume berstandar korporat global dengan 520+ bank profesi.</p>
        <p style='text-align:center;margin:24px 0;'>
          <a href='https://gdp.gaeks.com/cv.html' style='display:inline-block;padding:12px 28px;background:#2563eb;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:13px;'>Buka ATS CV Studio &rarr;</a>
        </p>
        <p style='font-size:12px;color:#64748b;'>Balas email ini jika ada pertanyaan atau hubungi WhatsApp kami di <a href='https://wa.me/6285608561745' style='color:#2563eb;'>+62 856-0856-1745</a>.</p>
      </div>
      <div style='background:#f1f5f9;padding:16px;text-align:center;font-size:11px;color:#64748b;'>
        &copy; " . date('Y') . " GAEKS Group. All rights reserved.
      </div>
    </div>";
} else {
    $subject = htmlspecialchars($data['subject'] ?? 'Pemberitahuan dari GAEKS Digital');
    $content = nl2br(htmlspecialchars($data['message'] ?? 'Terima kasih telah menggunakan layanan GAEKS.'));
    $html = "
    <div style='max-width:600px;margin:auto;font-family:Arial,sans-serif;border:1px solid #e2e8f0;border-radius:12px;padding:24px;background:#ffffff;'>
      <div style='border-bottom:2px solid #0f172a;padding-bottom:12px;margin-bottom:16px;'>
        <h3 style='margin:0;color:#0f172a;'>GAEKS Digital Products</h3>
      </div>
      <div style='color:#1e293b;line-height:1.6;font-size:13px;'>
        <p>Halo {$toName},</p>
        <p>{$content}</p>
        <p style='margin-top:20px;'>Salam hangat,<br><strong>Tim GAEKS Digital</strong></p>
      </div>
    </div>";
}

echo json_encode(sendHostingerSmtp($toEmail, $toName, $subject, $html));
''')

# api/test_mail.php
with open("api/test_mail.php", "w") as f:
    f.write('''<?php
require_once __DIR__ . '/mailer.php';
$to = $_GET['to'] ?? 'gaeks.group@gmail.com';
echo "<h2>Menguji Pengiriman Email via Hostinger SMTP (no-reply@gaeks.com)...</h2>";
echo "<p>Penerima: <strong>$to</strong></p>";
$res = sendHostingerSmtp($to, "Admin GAEKS", "Uji Coba Sistem no-reply@gaeks.com", "<p>Koneksi Hostinger SMTP (smtp.hostinger.com:465) berhasil!</p>");
echo "<pre>"; print_r($res); echo "</pre>";
''')

print("=== 2. Memperbarui auth.js dengan Google Client ID Resmi ===")
with open("auth.js", "r") as f:
    auth_text = f.read()

# Masukkan Client ID resmi
auth_text = auth_text.replace(
    'const GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com";',
    'const GOOGLE_CLIENT_ID = "41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com";'
)

with open("auth.js", "w") as f:
    f.write(auth_text)

print("=== 3. Memeriksa index.html & cv.html ===")
if os.path.exists("index.html"):
    with open("index.html", "r") as f: idx = f.read()
    if "https://accounts.google.com/gsi/client" not in idx:
        idx = idx.replace("</head>", "  <script src=\"https://accounts.google.com/gsi/client\" async defer></script>\n</head>")
        with open("index.html", "w") as f: f.write(idx)

if os.path.exists("cv.html"):
    with open("cv.html", "r") as f: cv = f.read()
    if "https://accounts.google.com/gsi/client" not in cv:
        cv = cv.replace("</head>", "  <script src=\"https://accounts.google.com/gsi/client\" async defer></script>\n</head>")
        with open("cv.html", "w") as f: f.write(cv)

print("=== 4. Menjalankan Git Add, Commit & Push ke GitHub ===")
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "fix: deploy full index, api mailer with credentials, and Google GIS client"])
push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print(push_res.stdout)
if push_res.stderr:
    print(push_res.stderr)

print("=== DEPLOYMENT SELESAI! ===")
