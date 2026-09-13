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
require_once __DIR__ . '/mailer.php';

$storageFile = __DIR__ . '/otp_store.json';
$registeredUsersFile = __DIR__ . '/users_registry.json';

$raw = file_get_contents('php://input');
$data = json_decode($raw, true) ?? [];
$action = $data['action'] ?? '';
$email = filter_var($data['email'] ?? '', FILTER_VALIDATE_EMAIL);

if (!$email) {
    echo json_encode(["status" => "error", "message" => "Format alamat email tidak valid."]);
    exit;
}

if ($action === 'send_otp') {
    if (file_exists($registeredUsersFile)) {
        $regUsers = json_decode(file_get_contents($registeredUsersFile), true) ?? [];
        if (in_array(strtolower($email), array_map('strtolower', $regUsers))) {
            echo json_encode([
                "status" => "already_registered",
                "message" => "Email ini sudah pernah terdaftar. Silakan gunakan tab Masuk ke Akun atau reset sandi."
            ]);
            exit;
        }
    }

    $name = htmlspecialchars($data['name'] ?? 'Pengguna GAEKS');
    $otp = strval(random_int(100000, 999999));
    
    $store = [];
    if (file_exists($storageFile)) {
        $store = json_decode(file_get_contents($storageFile), true) ?? [];
    }
    
    $store[strtolower($email)] = [
        'code' => $otp,
        'name' => $name,
        'expires' => time() + 600
    ];
    file_put_contents($storageFile, json_encode($store));

    $subject = "Kode Verifikasi Pendaftaran GAEKS Digital: $otp";
    $html = "
    <div style='max-width:520px;margin:auto;font-family:Arial,sans-serif;border:1px solid #e2e8f0;border-radius:12px;background:#ffffff;padding:28px 24px;'>
      <div style='text-align:center;margin-bottom:20px;'>
        <h2 style='color:#0f172a;margin:0;font-size:22px;'>GAEKS DIGITAL</h2>
        <p style='color:#64748b;font-size:12px;margin:4px 0 0;'>Verifikasi Pendaftaran Akun</p>
      </div>
      <p style='font-size:14px;color:#1e293b;'>Halo <strong>{$name}</strong>,</p>
      <p style='font-size:13px;color:#475569;'>Gunakan 6 digit kode verifikasi berikut untuk menyelesaikan pendaftaran akun Anda di GAEKS Digital:</p>
      <div style='background:#f1f5f9;border:1px dashed #cbd5e1;border-radius:10px;padding:16px;text-align:center;margin:24px 0;'>
        <span style='font-size:32px;font-weight:900;letter-spacing:6px;color:#2563eb;font-family:monospace;'>{$otp}</span>
      </div>
      <p style='font-size:12px;color:#64748b;'>Kode ini berlaku selama <strong>10 menit</strong>. Jangan bagikan kode ini kepada siapapun demi keamanan akun Anda.</p>
      <hr style='border:none;border-top:1px solid #f1f5f9;margin:20px 0;'>
      <p style='font-size:11px;color:#94a3b8;text-align:center;margin:0;'>Email ini dikirimkan otomatis oleh sistem resmi no-reply@gaeks.com.</p>
    </div>";

    $sendRes = sendHostingerSmtp($email, $name, $subject, $html);
    if ($sendRes['status'] === 'success') {
        echo json_encode(["status" => "success", "message" => "Kode verifikasi 6 digit telah dikirimkan ke " . $email]);
    } else {
        echo json_encode(["status" => "error", "message" => "Gagal mengirim email: " . $sendRes['message']]);
    }
    exit;
}

if ($action === 'verify_otp') {
    $code = trim($data['code'] ?? '');

    if (!file_exists($storageFile)) {
        echo json_encode(["status" => "error", "message" => "Kode verifikasi tidak ditemukan atau kedaluwarsa."]);
        exit;
    }

    $store = json_decode(file_get_contents($storageFile), true) ?? [];
    $entry = $store[strtolower($email)] ?? null;

    if (!$entry || time() > $entry['expires']) {
        echo json_encode(["status" => "error", "message" => "Kode verifikasi telah kedaluwarsa. Silakan minta kode baru."]);
        exit;
    }

    if ($entry['code'] !== $code) {
        echo json_encode(["status" => "error", "message" => "Kode verifikasi 6 digit yang Anda masukkan tidak cocok."]);
        exit;
    }

    $regUsers = [];
    if (file_exists($registeredUsersFile)) {
        $regUsers = json_decode(file_get_contents($registeredUsersFile), true) ?? [];
    }
    if (!in_array(strtolower($email), array_map('strtolower', $regUsers))) {
        $regUsers[] = strtolower($email);
        file_put_contents($registeredUsersFile, json_encode($regUsers));
    }

    $userName = $entry['name'];
    unset($store[strtolower($email)]);
    file_put_contents($storageFile, json_encode($store));

    echo json_encode([
        "status" => "success",
        "message" => "Pendaftaran berhasil diverifikasi!",
        "name" => $userName
    ]);
    exit;
}

echo json_encode(["status" => "error", "message" => "Aksi tidak dikenal."]);
