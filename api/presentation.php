<?php
// GAEKS PRESENTATION API - STRICT BACKEND OWNERSHIP & PERSISTENCE
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
    $results = [];
    if ($pdo) {
        $stmt = $pdo->prepare("SELECT id, name, date, status, updated_at, deleted_at FROM presentations WHERE user_id = :uid ORDER BY updated_at DESC");
        $stmt->execute([':uid' => $authUserId]);
        foreach ($stmt->fetchAll() as $r) {
            $results[] = [
                'id' => $r['id'], 'name' => $r['name'], 'date' => $r['date'],
                'status' => $r['status'], 'updatedAt' => (int)$r['updated_at'],
                'deletedAt' => $r['deleted_at'] ? (int)$r['deleted_at'] : null
            ];
        }
    } else {
        $store = getJsonStore($presStoreFile);
        foreach ($store[$authUserId] ?? [] as $p) {
            $results[] = [
                'id' => $p['id'], 'name' => $p['meetingName'] ?? $p['name'] ?? 'Presentasi',
                'date' => $p['meetingDate'] ?? $p['date'] ?? date('Y-m-d'),
                'status' => $p['status'] ?? 'active', 'updatedAt' => $p['updatedAt'] ?? time() * 1000,
                'deletedAt' => $p['deletedAt'] ?? null
            ];
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
        $checkStmt = $pdo->prepare("SELECT user_id FROM presentations WHERE id = :id");
        $checkStmt->execute([':id' => $id]);
        $ownerRow = $checkStmt->fetch();
        if ($ownerRow) {
            if ($ownerRow['user_id'] !== $authUserId) {
                http_response_code(403);
                echo json_encode(["status" => "error", "message" => "Forbidden: Anda tidak memiliki akses ke presentasi ini."]);
                exit;
            }
            $stmt = $pdo->prepare("SELECT * FROM presentations WHERE id = :id AND user_id = :uid");
            $stmt->execute([':id' => $id, ':uid' => $authUserId]);
            $r = $stmt->fetch();
            if ($r) {
                $pres = json_decode($r['data_json'], true) ?? [];
                $pres['id'] = $r['id']; $pres['meetingName'] = $r['name'];
                $pres['meetingDate'] = $r['date']; $pres['status'] = $r['status'];
                echo json_encode(["status" => "success", "data" => $pres]);
                exit;
            }
        }
    } else {
        $store = getJsonStore($presStoreFile);
        foreach ($store as $otherUid => $otherList) {
            if ($otherUid !== $authUserId) {
                foreach ($otherList as $op) {
                    if ($op['id'] === $id) {
                        http_response_code(403);
                        echo json_encode(["status" => "error", "message" => "Forbidden: Anda tidak memiliki akses ke presentasi ini."]);
                        exit;
                    }
                }
            }
        }
        foreach ($store[$authUserId] ?? [] as $p) {
            if ($p['id'] === $id) { echo json_encode(["status" => "success", "data" => $p]); exit; }
        }
    }
    http_response_code(404);
    echo json_encode(["status" => "error", "message" => "Presentasi tidak ditemukan."]);
    exit;
}

if ($action === 'save') {
    $pres = $postData['data'] ?? $postData;
    if (empty($pres['id'])) { $pres['id'] = 'MTG_' . round(microtime(true) * 1000); }
    $id = $pres['id'];
    $name = $pres['meetingName'] ?? $pres['name'] ?? 'Presentasi Baru';
    $date = $pres['meetingDate'] ?? $pres['date'] ?? date('Y-m-d');
    $status = $pres['status'] ?? 'active';
    $now = round(microtime(true) * 1000);
    $dataJson = json_encode($pres);

    if ($pdo) {
        $checkStmt = $pdo->prepare("SELECT user_id FROM presentations WHERE id = :id");
        $checkStmt->execute([':id' => $id]);
        $existing = $checkStmt->fetch();
        if ($existing && $existing['user_id'] !== $authUserId) {
            http_response_code(403);
            echo json_encode(["status" => "error", "message" => "Forbidden."]);
            exit;
        }
        if ($existing) {
            $updateStmt = $pdo->prepare("UPDATE presentations SET name = :name, date = :date, status = :status, data_json = :data, updated_at = :now WHERE id = :id AND user_id = :uid");
            $updateStmt->execute([':name' => $name, ':date' => $date, ':status' => $status, ':data' => $dataJson, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
        } else {
            $insertStmt = $pdo->prepare("INSERT INTO presentations (id, user_id, name, date, status, data_json, created_at, updated_at) VALUES (:id, :uid, :name, :date, :status, :data, :created, :updated)");
            $insertStmt->execute([':id' => $id, ':uid' => $authUserId, ':name' => $name, ':date' => $date, ':status' => $status, ':data' => $dataJson, ':created' => $now, ':updated' => $now]);
        }
    } else {
        $store = getJsonStore($presStoreFile);
        foreach ($store as $otherUid => $otherList) {
            if ($otherUid !== $authUserId) {
                foreach ($otherList as $op) {
                    if ($op['id'] === $id) {
                        http_response_code(403);
                        echo json_encode(["status" => "error", "message" => "Forbidden."]);
                        exit;
                    }
                }
            }
        }
        if (!isset($store[$authUserId])) $store[$authUserId] = [];
        $idx = -1;
        foreach ($store[$authUserId] as $i => $p) { if ($p['id'] === $id) { $idx = $i; break; } }
        $pres['id'] = $id; $pres['updatedAt'] = $now;
        if ($idx >= 0) $store[$authUserId][$idx] = $pres;
        else array_unshift($store[$authUserId], $pres);
        saveJsonStore($presStoreFile, $store);
    }
    echo json_encode(["status" => "success", "message" => "Presentasi berhasil disimpan di database.", "data" => $pres]);
    exit;
}

if ($action === 'status') {
    $id = $postData['id'] ?? $_GET['id'] ?? '';
    $status = $postData['status'] ?? $_GET['status'] ?? 'trashed';
    $now = round(microtime(true) * 1000);
    if ($pdo) {
        $checkStmt = $pdo->prepare("SELECT user_id FROM presentations WHERE id = :id");
        $checkStmt->execute([':id' => $id]);
        $existing = $checkStmt->fetch();
        if ($existing && $existing['user_id'] !== $authUserId) {
            http_response_code(403);
            echo json_encode(["status" => "error", "message" => "Forbidden."]);
            exit;
        }
        if ($status === 'delete_permanent') {
            $stmt = $pdo->prepare("DELETE FROM presentations WHERE id = :id AND user_id = :uid");
            $stmt->execute([':id' => $id, ':uid' => $authUserId]);
        } else {
            $delAt = ($status === 'trashed') ? $now : null;
            $stmt = $pdo->prepare("UPDATE presentations SET status = :status, deleted_at = :del, updated_at = :now WHERE id = :id AND user_id = :uid");
            $stmt->execute([':status' => $status, ':del' => $delAt, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
        }
    } else {
        $store = getJsonStore($presStoreFile);
        if (isset($store[$authUserId])) {
            if ($status === 'delete_permanent') {
                $store[$authUserId] = array_values(array_filter($store[$authUserId], fn($p) => $p['id'] !== $id));
            } else {
                foreach ($store[$authUserId] as &$p) {
                    if ($p['id'] === $id) { $p['status'] = $status; $p['deletedAt'] = ($status === 'trashed') ? $now : null; break; }
                }
            }
            saveJsonStore($presStoreFile, $store);
        }
    }
    echo json_encode(["status" => "success", "message" => "Status presentasi diperbarui."]);
    exit;
}
echo json_encode(["status" => "error", "message" => "Aksi tidak dikenal."]);
