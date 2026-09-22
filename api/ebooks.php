<?php
declare(strict_types=1);

require_once __DIR__ . '/bootstrap.php';

$pdo = gaeks_db();
$action = (string) ($_GET['action'] ?? $_POST['action'] ?? 'catalog');
$method = (string) ($_SERVER['REQUEST_METHOD'] ?? 'GET');

function ebook_admin(array $user): void {
    if (($user['role'] ?? '') !== 'admin') gaeks_error('forbidden', 'Akses admin diperlukan.', 403);
}

function ebook_row(array $row): array {
    return [
        'id' => $row['id'],
        'title' => $row['title'],
        'slug' => $row['slug'],
        'description' => $row['description'],
        'priceIdr' => (int) $row['price_idr'],
        'coverUrl' => $row['cover_path'] ? '/api/ebooks.php?action=cover&id=' . rawurlencode($row['id']) : null,
        'status' => $row['status'],
        'createdAt' => $row['created_at'],
        'updatedAt' => $row['updated_at'],
    ];
}

function ebook_upload(array $upload, string $kind): string {
    if (($upload['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK || !is_uploaded_file((string) ($upload['tmp_name'] ?? ''))) {
        gaeks_error('upload_failed', $kind === 'cover' ? 'Cover gagal diunggah.' : 'File e-book gagal diunggah.', 422);
    }
    $size = (int) ($upload['size'] ?? 0);
    $max = $kind === 'cover' ? 5 * 1024 * 1024 : 50 * 1024 * 1024;
    if ($size < 1 || $size > $max) {
        gaeks_error('invalid_file_size', $kind === 'cover' ? 'Cover maksimal 5 MB.' : 'File e-book maksimal 50 MB.', 422);
    }
    $path = (string) $upload['tmp_name'];
    $mime = (new finfo(FILEINFO_MIME_TYPE))->file($path);
    $ext = strtolower(pathinfo((string) ($upload['name'] ?? ''), PATHINFO_EXTENSION));
    if ($kind === 'cover') {
        $allowed = ['jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp'];
        $image = @getimagesize($path);
        if (!isset($allowed[$ext]) || $mime !== $allowed[$ext] || !is_array($image) || ($image['mime'] ?? '') !== $mime) {
            gaeks_error('invalid_cover', 'Cover harus berupa JPG, PNG, atau WebP yang valid.', 422);
        }
    } else {
        $magic = file_get_contents($path, false, null, 0, 5);
        $pdf = $ext === 'pdf' && $mime === 'application/pdf' && $magic === '%PDF-';
        $epub = $ext === 'epub' && in_array($mime, ['application/epub+zip', 'application/zip'], true) && str_starts_with((string) $magic, 'PK');
        if (!$pdf && !$epub) gaeks_error('invalid_ebook', 'File e-book harus berupa PDF atau EPUB yang valid.', 422);
    }
    return $ext;
}

if ($action === 'catalog') {
    if ($method !== 'GET') gaeks_error('method_not_allowed', 'Gunakan metode GET.', 405);
    $stmt = $pdo->query("SELECT * FROM ebooks WHERE status='published' ORDER BY created_at DESC");
    gaeks_ok(array_map('ebook_row', $stmt->fetchAll()));
}

if ($action === 'cover') {
    if ($method !== 'GET') gaeks_error('method_not_allowed', 'Gunakan metode GET.', 405);
    $stmt = $pdo->prepare("SELECT cover_path FROM ebooks WHERE id=:id AND status='published'");
    $stmt->execute([':id' => (string) ($_GET['id'] ?? '')]);
    $path = $stmt->fetchColumn();
    if (!$path || !is_file($path)) gaeks_error('not_found', 'Cover tidak ditemukan.', 404);
    $mime = (new finfo(FILEINFO_MIME_TYPE))->file($path);
    if (!in_array($mime, ['image/jpeg', 'image/png', 'image/webp'], true)) gaeks_error('not_found', 'Cover tidak ditemukan.', 404);
    header('Content-Type: ' . $mime);
    header('Cache-Control: public, max-age=300');
    readfile($path);
    exit;
}

$user = gaeks_current_user();
ebook_admin($user);

if ($action === 'admin_list') {
    if ($method !== 'GET') gaeks_error('method_not_allowed', 'Gunakan metode GET.', 405);
    $stmt = $pdo->query('SELECT * FROM ebooks ORDER BY created_at DESC');
    gaeks_ok(array_map('ebook_row', $stmt->fetchAll()));
}

if ($action === 'set_status') {
    if ($method !== 'POST') gaeks_error('method_not_allowed', 'Gunakan metode POST.', 405);
    gaeks_require_csrf($user);
    $input = gaeks_input();
    $id = (string) ($input['id'] ?? '');
    $status = (string) ($input['status'] ?? '');
    if (!preg_match('/^[a-f0-9-]{36}$/i', $id) || !in_array($status, ['draft', 'published', 'archived'], true)) {
        gaeks_error('invalid_input', 'Status e-book tidak valid.', 422);
    }
    $stmt = $pdo->prepare('UPDATE ebooks SET status=:status WHERE id=:id');
    $stmt->execute([':status' => $status, ':id' => $id]);
    $stmt = $pdo->prepare('SELECT * FROM ebooks WHERE id=:id');
    $stmt->execute([':id' => $id]);
    $row = $stmt->fetch();
    if (!$row) gaeks_error('not_found', 'E-book tidak ditemukan.', 404);
    gaeks_audit($pdo, $user['id'], 'ebook.status_changed', 'ebook', $id, ['status' => $status]);
    gaeks_ok(ebook_row($row), 200, 'Status e-book diperbarui.');
}

if ($action === 'create') {
    if ($method !== 'POST') gaeks_error('method_not_allowed', 'Gunakan metode POST.', 405);
    gaeks_require_csrf($user);
    $title = trim((string) ($_POST['title'] ?? ''));
    $description = trim((string) ($_POST['description'] ?? ''));
    $priceRaw = trim((string) ($_POST['priceIdr'] ?? ''));
    $status = (string) ($_POST['status'] ?? 'published');
    if ($title === '' || strlen($title) > 255 || $description === '' || strlen($description) > 10000 ||
        !preg_match('/^\d{1,10}$/', $priceRaw) || (float) $priceRaw > 2147483647 ||
        !in_array($status, ['draft', 'published'], true)) {
        gaeks_error('invalid_input', 'Periksa judul, deskripsi, harga, dan status e-book.', 422);
    }
    if (!isset($_FILES['file'])) gaeks_error('file_required', 'File e-book wajib dipilih.', 422);
    $fileExt = ebook_upload($_FILES['file'], 'file');
    $coverExt = isset($_FILES['cover']) && ($_FILES['cover']['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_NO_FILE
        ? ebook_upload($_FILES['cover'], 'cover') : null;

    $root = dirname(__DIR__, 3) . '/private-runtime/ebooks';
    if (!is_dir($root) && !mkdir($root, 0700, true)) throw new RuntimeException('Storage e-book tidak tersedia.');
    $id = gaeks_uuid();
    $file = $root . '/' . $id . '.' . $fileExt;
    $cover = $coverExt ? $root . '/' . $id . '-cover.' . $coverExt : null;
    if (!move_uploaded_file($_FILES['file']['tmp_name'], $file)) gaeks_error('upload_failed', 'File e-book gagal disimpan.', 500);
    @chmod($file, 0600);
    if ($cover !== null && !move_uploaded_file($_FILES['cover']['tmp_name'], $cover)) {
        @unlink($file);
        gaeks_error('upload_failed', 'Cover gagal disimpan.', 500);
    }
    if ($cover !== null) @chmod($cover, 0600);
    $base = substr(trim((string) preg_replace('/[^a-z0-9]+/', '-', strtolower($title)), '-'), 0, 160);
    $slug = ($base !== '' ? $base : 'ebook') . '-' . substr(str_replace('-', '', $id), 0, 8);
    try {
        $stmt = $pdo->prepare('INSERT INTO ebooks(id,title,slug,description,price_idr,cover_path,file_path,status,created_by) VALUES(:id,:title,:slug,:description,:price,:cover,:file,:status,:creator)');
        $stmt->execute([':id' => $id, ':title' => $title, ':slug' => $slug, ':description' => $description,
            ':price' => (int) $priceRaw, ':cover' => $cover, ':file' => $file, ':status' => $status, ':creator' => $user['id']]);
    } catch (Throwable $error) {
        @unlink($file);
        if ($cover !== null) @unlink($cover);
        throw $error;
    }
    gaeks_audit($pdo, $user['id'], 'ebook.created', 'ebook', $id, ['status' => $status]);
    gaeks_ok(['id' => $id, 'status' => $status], 201, 'E-book ditambahkan.');
}

gaeks_error('unknown_action', 'Aksi e-book tidak dikenal.', 404);
