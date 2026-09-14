<?php
// GAEKS ATS CV API - STRICT BACKEND OWNERSHIP & DATABASE PERSISTENCE
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Gaeks-Auth');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }

require_once __DIR__ . '/db.php';

$user = getAuthenticatedUser();
if (!$user) {
    http_response_code(401);
    echo json_encode(["status" => "error", "message" => "Unauthorized: Sesi tidak valid atau telah berakhir."]);
    exit;
}

$authUserId = $user['id'];
$pdo = getPdoConnection();
$raw = file_get_contents('php://input');
$postData = json_decode($raw, true) ?? [];
$action = $_GET['action'] ?? $postData['action'] ?? 'list';

if ($action === 'list') {
    $tab = $_GET['tab'] ?? 'active';
    $results = [];

    if ($pdo) {
        if ($tab === 'trash') {
            $stmt = $pdo->prepare("SELECT * FROM cvs WHERE user_id = :uid AND deleted_at IS NOT NULL ORDER BY updated_at DESC");
        } else {
            $stmt = $pdo->prepare("SELECT * FROM cvs WHERE user_id = :uid AND deleted_at IS NULL ORDER BY updated_at DESC");
        }
        $stmt->execute([':uid' => $authUserId]);
        foreach ($stmt->fetchAll() as $r) {
            $results[] = [
                'id' => $r['id'],
                'title' => $r['title'],
                'isDraft' => (bool)$r['is_draft'],
                'completeness' => (int)$r['completeness'],
                'updatedAt' => (int)$r['updated_at'],
                'deletedAt' => $r['deleted_at'] ? (int)$r['deleted_at'] : null,
                'data' => json_decode($r['data_json'], true) ?? []
            ];
        }
    } else {
        $store = getJsonStore($cvStoreFile);
        $userCvs = $store[$authUserId] ?? [];
        foreach ($userCvs as $c) {
            if ($tab === 'trash' && !empty($c['deletedAt'])) $results[] = $c;
            elseif ($tab !== 'trash' && empty($c['deletedAt'])) $results[] = $c;
        }
        usort($results, fn($a, $b) => ($b['updatedAt'] ?? 0) <=> ($a['updatedAt'] ?? 0));
    }

    echo json_encode(["status" => "success", "data" => $results]);
    exit;
}

if ($action === 'get') {
    $id = $_GET['id'] ?? $postData['id'] ?? '';
    if (!$id) { http_response_code(400); echo json_encode(["status" => "error", "message" => "ID diperlukan."]); exit; }

    if ($pdo) {
        $checkStmt = $pdo->prepare("SELECT user_id FROM cvs WHERE id = :id");
        $checkStmt->execute([':id' => $id]);
        $ownerRow = $checkStmt->fetch();
        if ($ownerRow) {
            if ($ownerRow['user_id'] !== $authUserId) {
                http_response_code(403);
                echo json_encode(["status" => "error", "message" => "Forbidden: Anda tidak memiliki akses ke resume ini."]);
                exit;
            }
            $stmt = $pdo->prepare("SELECT * FROM cvs WHERE id = :id AND user_id = :uid");
            $stmt->execute([':id' => $id, ':uid' => $authUserId]);
            $r = $stmt->fetch();
            if ($r) {
                echo json_encode(["status" => "success", "data" => [
                    'id' => $r['id'], 'title' => $r['title'], 'isDraft' => (bool)$r['is_draft'],
                    'completeness' => (int)$r['completeness'], 'updatedAt' => (int)$r['updated_at'],
                    'deletedAt' => $r['deleted_at'] ? (int)$r['deleted_at'] : null,
                    'data' => json_decode($r['data_json'], true) ?? []
                ]]);
                exit;
            }
        }
    } else {
        $store = getJsonStore($cvStoreFile);
        foreach ($store as $otherUid => $otherList) {
            if ($otherUid !== $authUserId) {
                foreach ($otherList as $oc) {
                    if ($oc['id'] === $id) {
                        http_response_code(403);
                        echo json_encode(["status" => "error", "message" => "Forbidden: Anda tidak memiliki akses ke resume ini."]);
                        exit;
                    }
                }
            }
        }
        foreach ($store[$authUserId] ?? [] as $c) {
            if ($c['id'] === $id) { echo json_encode(["status" => "success", "data" => $c]); exit; }
        }
    }

    http_response_code(404);
    echo json_encode(["status" => "error", "message" => "Resume tidak ditemukan."]);
    exit;
}

if ($action === 'save') {
    $cv = $postData['cv'] ?? $postData;
    if (empty($cv['id'])) {
        $cv['id'] = 'cv_' . round(microtime(true) * 1000) . '_' . substr(md5(random_bytes(6)), 0, 4);
    }
    $id = $cv['id'];
    $title = $cv['title'] ?? 'CV Tanpa Judul';
    $data = $cv['data'] ?? [];
    $isDraft = !empty($cv['isDraft']) ? 1 : 0;
    $completeness = (int)($cv['completeness'] ?? 0);
    $now = round(microtime(true) * 1000);
    $dataJson = json_encode($data);

    if ($pdo) {
        $checkStmt = $pdo->prepare("SELECT user_id FROM cvs WHERE id = :id");
        $checkStmt->execute([':id' => $id]);
        $existing = $checkStmt->fetch();
        if ($existing && $existing['user_id'] !== $authUserId) {
            http_response_code(403);
            echo json_encode(["status" => "error", "message" => "Forbidden: Anda tidak memiliki izin mengedit resume ini."]);
            exit;
        }
        if ($existing) {
            $updateStmt = $pdo->prepare("UPDATE cvs SET title = :title, is_draft = :draft, completeness = :comp, data_json = :data, updated_at = :now WHERE id = :id AND user_id = :uid");
            $updateStmt->execute([':title' => $title, ':draft' => $isDraft, ':comp' => $completeness, ':data' => $dataJson, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
        } else {
            $insertStmt = $pdo->prepare("INSERT INTO cvs (id, user_id, title, is_draft, completeness, data_json, created_at, updated_at) VALUES (:id, :uid, :title, :draft, :comp, :data, :created, :updated)");
            $insertStmt->execute([':id' => $id, ':uid' => $authUserId, ':title' => $title, ':draft' => $isDraft, ':comp' => $completeness, ':data' => $dataJson, ':created' => $now, ':updated' => $now]);
        }
    } else {
        $store = getJsonStore($cvStoreFile);
        foreach ($store as $otherUid => $otherList) {
            if ($otherUid !== $authUserId) {
                foreach ($otherList as $oc) {
                    if ($oc['id'] === $id) {
                        http_response_code(403);
                        echo json_encode(["status" => "error", "message" => "Forbidden: Anda tidak memiliki izin mengedit resume ini."]);
                        exit;
                    }
                }
            }
        }
        if (!isset($store[$authUserId])) $store[$authUserId] = [];
        $idx = -1;
        foreach ($store[$authUserId] as $i => $c) { if ($c['id'] === $id) { $idx = $i; break; } }
        $savedObj = ['id' => $id, 'title' => $title, 'isDraft' => (bool)$isDraft, 'completeness' => $completeness, 'updatedAt' => $now, 'deletedAt' => null, 'data' => $data];
        if ($idx >= 0) $store[$authUserId][$idx] = $savedObj;
        else array_unshift($store[$authUserId], $savedObj);
        saveJsonStore($cvStoreFile, $store);
    }

    $cv['updatedAt'] = $now;
    echo json_encode(["status" => "success", "message" => "Resume berhasil disimpan di database.", "data" => $cv]);
    exit;
}

if ($action === 'delete') {
    $id = $postData['id'] ?? $_GET['id'] ?? '';
    $now = round(microtime(true) * 1000);
    if ($pdo) {
        $checkStmt = $pdo->prepare("SELECT user_id FROM cvs WHERE id = :id");
        $checkStmt->execute([':id' => $id]);
        $existing = $checkStmt->fetch();
        if ($existing && $existing['user_id'] !== $authUserId) {
            http_response_code(403);
            echo json_encode(["status" => "error", "message" => "Forbidden."]);
            exit;
        }
        $stmt = $pdo->prepare("UPDATE cvs SET deleted_at = :del, updated_at = :now WHERE id = :id AND user_id = :uid");
        $stmt->execute([':del' => $now, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
    } else {
        $store = getJsonStore($cvStoreFile);
        if (isset($store[$authUserId])) {
            foreach ($store[$authUserId] as &$c) { if ($c['id'] === $id) { $c['deletedAt'] = $now; break; } }
            saveJsonStore($cvStoreFile, $store);
        }
    }
    echo json_encode(["status" => "success", "message" => "Resume dipindahkan ke tempat sampah."]);
    exit;
}

if ($action === 'restore') {
    $id = $postData['id'] ?? $_GET['id'] ?? '';
    $now = round(microtime(true) * 1000);
    if ($pdo) {
        $checkStmt = $pdo->prepare("SELECT user_id FROM cvs WHERE id = :id");
        $checkStmt->execute([':id' => $id]);
        $existing = $checkStmt->fetch();
        if ($existing && $existing['user_id'] !== $authUserId) {
            http_response_code(403);
            echo json_encode(["status" => "error", "message" => "Forbidden."]);
            exit;
        }
        $stmt = $pdo->prepare("UPDATE cvs SET deleted_at = NULL, updated_at = :now WHERE id = :id AND user_id = :uid");
        $stmt->execute([':now' => $now, ':id' => $id, ':uid' => $authUserId]);
    } else {
        $store = getJsonStore($cvStoreFile);
        if (isset($store[$authUserId])) {
            foreach ($store[$authUserId] as &$c) { if ($c['id'] === $id) { $c['deletedAt'] = null; break; } }
            saveJsonStore($cvStoreFile, $store);
        }
    }
    echo json_encode(["status" => "success", "message" => "Resume berhasil dipulihkan."]);
    exit;
}

if ($action === 'delete_permanent') {
    $id = $postData['id'] ?? $_GET['id'] ?? '';
    if ($pdo) {
        $checkStmt = $pdo->prepare("SELECT user_id FROM cvs WHERE id = :id");
        $checkStmt->execute([':id' => $id]);
        $existing = $checkStmt->fetch();
        if ($existing && $existing['user_id'] !== $authUserId) {
            http_response_code(403);
            echo json_encode(["status" => "error", "message" => "Forbidden."]);
            exit;
        }
        $stmt = $pdo->prepare("DELETE FROM cvs WHERE id = :id AND user_id = :uid");
        $stmt->execute([':id' => $id, ':uid' => $authUserId]);
    } else {
        $store = getJsonStore($cvStoreFile);
        if (isset($store[$authUserId])) {
            $store[$authUserId] = array_values(array_filter($store[$authUserId], fn($c) => $c['id'] !== $id));
            saveJsonStore($cvStoreFile, $store);
        }
    }
    echo json_encode(["status" => "success", "message" => "Resume dihapus permanen."]);
    exit;
}

echo json_encode(["status" => "error", "message" => "Aksi tidak dikenal."]);
