<?php
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
        $headers  = "MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8
From: " . SMTP_FROM_NAME . " <" . SMTP_USER . ">
Reply-To: " . REPLY_TO_EMAIL . "
";
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
    fputs($socket, "EHLO " . gethostname() . "
"); $read($socket);
    fputs($socket, "AUTH LOGIN
"); $read($socket);
    fputs($socket, base64_encode(SMTP_USER) . "
"); $read($socket);
    fputs($socket, base64_encode(SMTP_PASS) . "
");
    $authRes = $read($socket);

    if (substr($authRes, 0, 3) != "235") {
        fclose($socket);
        return ["status" => "error", "message" => "Autentikasi SMTP Gagal: $authRes"];
    }

    fputs($socket, "MAIL FROM: <" . SMTP_USER . ">
"); $read($socket);
    fputs($socket, "RCPT TO: <" . $toEmail . ">
"); $read($socket);
    fputs($socket, "DATA
"); $read($socket);

    $headers  = "MIME-Version: 1.0
";
    $headers .= "Content-Type: text/html; charset=UTF-8
";
    $headers .= "From: =?UTF-8?B?" . base64_encode(SMTP_FROM_NAME) . "?= <" . SMTP_USER . ">
";
    $headers .= "To: =?UTF-8?B?" . base64_encode($toName) . "?= <" . $toEmail . ">
";
    $headers .= "Reply-To: <" . REPLY_TO_EMAIL . ">
";
    $headers .= "Subject: =?UTF-8?B?" . base64_encode($subject) . "?=
";
    $headers .= "X-Mailer: GAEKS Executive Mailer
";

    $body = $headers . "
" . $htmlContent . "
.
";
    fputs($socket, $body);
    $sendRes = $read($socket);
    fputs($socket, "QUIT
");
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
