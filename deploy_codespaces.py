#!/usr/bin/env python3
import os, sys, re, json, subprocess

print("===================================================================")
print("🚀 GAEKS ECOSYSTEM DEPLOYER & VERIFIER (GITHUB CODESPACES)")
print("===================================================================")

ROOT = os.path.dirname(os.path.abspath(__file__))

def safe_write(filename, content):
    path = os.path.join(ROOT, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_path, path)
    print(f"✓ Berhasil diperbarui: {filename} ({len(content)} bytes)")

# -----------------------------------------------------------------------------
# 1. SETUP BACKEND DATABASE & REST API (SQLite PDO + JSON Fallback)
# -----------------------------------------------------------------------------
print("\n[1/5] Membangun Backend API & Database SQLite Persistence...")
os.makedirs(os.path.join(ROOT, "api", "data"), exist_ok=True)

# api/db.php
safe_write("api/db.php", """<?php
// GAEKS DATABASE ADAPTER (SQLITE PDO WITH JSON BACKUP FALLBACK)
$dataDir = __DIR__ . '/data';
if (!file_exists($dataDir)) { @mkdir($dataDir, 0777, true); }

$sqliteFile = $dataDir . '/gaeks.sqlite';
$cvStoreFile = $dataDir . '/cvs_store.json';
$presStoreFile = $dataDir . '/presentations_store.json';

function getPdoConnection() {
    global $sqliteFile;
    try {
        if (class_exists('PDO') && in_array('sqlite', PDO::getAvailableDrivers())) {
            $pdo = new PDO('sqlite:' . $sqliteFile);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
            
            $pdo->exec("CREATE TABLE IF NOT EXISTS cvs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT,
                is_draft INTEGER DEFAULT 0,
                completeness INTEGER DEFAULT 0,
                data_json TEXT,
                created_at INTEGER,
                updated_at INTEGER,
                deleted_at INTEGER
            )");
            $pdo->exec("CREATE INDEX IF NOT EXISTS idx_cvs_user ON cvs(user_id)");

            $pdo->exec("CREATE TABLE IF NOT EXISTS presentations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT,
                date TEXT,
                status TEXT DEFAULT 'active',
                data_json TEXT,
                created_at INTEGER,
                updated_at INTEGER,
                deleted_at INTEGER
            )");
            $pdo->exec("CREATE INDEX IF NOT EXISTS idx_pres_user ON presentations(user_id)");

            return $pdo;
        }
    } catch (Exception $e) {}
    return null;
}

function getJsonStore($file) {
    if (file_exists($file)) {
        $raw = @file_get_contents($file);
        if ($raw) {
            $arr = json_decode($raw, true);
            if (is_array($arr)) return $arr;
        }
    }
    return [];
}

function saveJsonStore($file, $data) {
    @file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT));
}

function getAuthenticatedUser() {
    $userJson = null;
    if (!empty($_SERVER['HTTP_X_GAEKS_AUTH'])) {
        $userJson = urldecode($_SERVER['HTTP_X_GAEKS_AUTH']);
    } elseif (!empty($_SERVER['HTTP_AUTHORIZATION']) && preg_match('/Bearer\\s+(.*)$/i', $_SERVER['HTTP_AUTHORIZATION'], $m)) {
        $userJson = urldecode($m[1]);
    } elseif (!empty($_COOKIE['gaeks_session_v3'])) {
        $userJson = $_COOKIE['gaeks_session_v3'];
    } elseif (!empty($_COOKIE['gaeks_session'])) {
        $userJson = $_COOKIE['gaeks_session'];
    }

    if ($userJson) {
        $user = json_decode($userJson, true);
        if ($user && !empty($user['email'])) {
            $cleanEmail = strtolower(trim($user['email']));
            $userId = 'usr_' . preg_replace('/[^a-z0-9]/', '_', $cleanEmail);
            return ['id' => $userId, 'email' => $cleanEmail, 'name' => $user['name'] ?? $cleanEmail];
        }
    }
    return null;
}
""")

# api/cv.php
safe_write("api/cv.php", """<?php
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
""")

# api/presentation.php
safe_write("api/presentation.php", """<?php
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

if ($action === 'get') {$id = $_GET['id'] ?? $postData['id'] ?? '';
    if (!$id) { http_response_code(400); echo json_encode(["status" => "error", "message" => "ID diperlukan."]); exit; }

    if ($pdo) {
        $checkStmt =$pdo->prepare("SELECT user_id FROM presentations WHERE id = :id");
        $checkStmt->execute([':id' =>$id]);
        $ownerRow =$checkStmt->fetch();
        if ($ownerRow) {
            if ($ownerRow['user_id'] !==$authUserId) {
                http_response_code(403);
                echo json_encode(["status" => "error", "message" => "Forbidden: Anda tidak memiliki akses ke presentasi ini."]);
                exit;
            }
            $stmt =$pdo->prepare("SELECT * FROM presentations WHERE id = :id AND user_id = :uid");
            $stmt->execute([':id' => $id, ':uid' =>$authUserId]);
            $r =$stmt->fetch();
            if ($r) {
                $pres = json_decode($r['data_json'], true) ?? [];
                $pres['id'] =$r['id']; $pres['meetingName'] =$r['name'];
                $pres['meetingDate'] =$r['date']; $pres['status'] =$r['status'];
                echo json_encode(["status" => "success", "data" => $pres]);
                exit;
            }
        }
    } else {
        $store = getJsonStore($presStoreFile);
        foreach ($store as $otherUid =>$otherList) {
            if ($otherUid !==$authUserId) {
                foreach ($otherList as$op) {
                    if ($op['id'] ===$id) {
                        http_response_code(403);
                        echo json_encode(["status" => "error", "message" => "Forbidden: Anda tidak memiliki akses ke presentasi ini."]);
                        exit;
                    }
                }
            }
        }
        foreach ($store[$authUserId] ?? [] as$p) {
            if ($p['id'] === $id) { echo json_encode(["status" => "success", "data" => $p]); exit; }
        }
    }
    http_response_code(404);
    echo json_encode(["status" => "error", "message" => "Presentasi tidak ditemukan."]);
    exit;
}

if ($action === 'save') {$pres = $postData['data'] ?? $postData;
    if (empty($pres['id'])) {$pres['id'] = 'MTG_' . round(microtime(true) * 1000); }
    $id =$pres['id'];
    $name =$pres['meetingName'] ?? $pres['name'] ?? 'Presentasi Baru';$date = $pres['meetingDate'] ?? $pres['date'] ?? date('Y-m-d');
    $status = $pres['status'] ?? 'active';$now = round(microtime(true) * 1000);
    $dataJson = json_encode($pres);

    if ($pdo) {
        $checkStmt =$pdo->prepare("SELECT user_id FROM presentations WHERE id = :id");
        $checkStmt->execute([':id' =>$id]);
        $existing =$checkStmt->fetch();
        if ($existing && $existing['user_id'] !==$authUserId) {
            http_response_code(403);
            echo json_encode(["status" => "error", "message" => "Forbidden."]);
            exit;
        }
        if ($existing) {
            $updateStmt =$pdo->prepare("UPDATE presentations SET name = :name, date = :date, status = :status, data_json = :data, updated_at = :now WHERE id = :id AND user_id = :uid");
            $updateStmt->execute([':name' =>$name, ':date' => $date, ':status' =>$status, ':data' => $dataJson, ':now' =>$now, ':id' => $id, ':uid' =>$authUserId]);
        } else {
            $insertStmt =$pdo->prepare("INSERT INTO presentations (id, user_id, name, date, status, data_json, created_at, updated_at) VALUES (:id, :uid, :name, :date, :status, :data, :created, :updated)");
            $insertStmt->execute([':id' => $id, ':uid' =>$authUserId, ':name' => $name, ':date' =>$date, ':status' => $status, ':data' =>$dataJson, ':created' => $now, ':updated' =>$now]);
        }
    } else {
        $store = getJsonStore($presStoreFile);
        foreach ($store as $otherUid =>$otherList) {
            if ($otherUid !==$authUserId) {
                foreach ($otherList as$op) {
                    if ($op['id'] ===$id) {
                        http_response_code(403);
                        echo json_encode(["status" => "error", "message" => "Forbidden."]);
                        exit;
                    }
                }
            }
        }
        if (!isset($store[$authUserId]))$store[$authUserId] = [];$idx = -1;
        foreach ($store[$authUserId] as $i =>$p) { if ($p['id'] ===$id) { $idx =$i; break; } }
        $pres['id'] =$id; $pres['updatedAt'] =$now;
        if ($idx >= 0) $store[$authUserId][$idx] =$pres;
        else array_unshift($store[$authUserId],$pres);
        saveJsonStore($presStoreFile,$store);
    }
    echo json_encode(["status" => "success", "message" => "Presentasi berhasil disimpan di database.", "data" => $pres]);
    exit;
}

if ($action === 'status') {$id = $postData['id'] ?? $_GET['id'] ?? '';
    $status =$postData['status'] ?? $_GET['status'] ?? 'trashed';$now = round(microtime(true) * 1000);
    if ($pdo) {
        $checkStmt =$pdo->prepare("SELECT user_id FROM presentations WHERE id = :id");
        $checkStmt->execute([':id' =>$id]);
        $existing =$checkStmt->fetch();
        if ($existing && $existing['user_id'] !==$authUserId) {
            http_response_code(403);
            echo json_encode(["status" => "error", "message" => "Forbidden."]);
            exit;
        }
        if ($status === 'delete_permanent') {
            $stmt =$pdo->prepare("DELETE FROM presentations WHERE id = :id AND user_id = :uid");
            $stmt->execute([':id' => $id, ':uid' =>$authUserId]);
        } else {
            $delAt = ($status === 'trashed') ?$now : null;
            $stmt =$pdo->prepare("UPDATE presentations SET status = :status, deleted_at = :del, updated_at = :now WHERE id = :id AND user_id = :uid");
            $stmt->execute([':status' =>$status, ':del' => $delAt, ':now' =>$now, ':id' => $id, ':uid' =>$authUserId]);
        }
    } else {
        $store = getJsonStore($presStoreFile);
        if (isset($store[$authUserId])) {
            if ($status === 'delete_permanent') {$store[$authUserId] = array_values(array_filter($store[$authUserId], fn($p) => $p['id'] !==$id));
            } else {
                foreach ($store[$authUserId] as &$p) {
                    if ($p['id'] === $id) {$p['status'] = $status; $p['deletedAt'] = ($status === 'trashed') ?$now : null; break; }
                }
            }
            saveJsonStore($presStoreFile,$store);
        }
    }
    echo json_encode(["status" => "success", "message" => "Status presentasi diperbarui."]);
    exit;
}
echo json_encode(["status" => "error", "message" => "Aksi tidak dikenal."]);
""")

# api/server.js
safe_write("api/server.js", """// =============================================================================
// GAEKS BACKEND SERVER & ACCEPTANCE TEST HARNESS (NODE.JS RUNTIME)
// =============================================================================
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const DATA_DIR = path.join(__dirname, 'data');
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const CVS_FILE = path.join(DATA_DIR, 'cvs_store.json');
const PRES_FILE = path.join(DATA_DIR, 'presentations_store.json');

function getStore(file) {
  try {
    if (fs.existsSync(file)) {
      return JSON.parse(fs.readFileSync(file, 'utf-8'));
    }
  } catch(e) {}
  return {};
}

function saveStore(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf-8');
}

function getAuthenticatedUser(req) {
  let userJson = null;
  const hAuth = req.headers['x-gaeks-auth'];
  if (hAuth) {
    userJson = decodeURIComponent(hAuth);
  } else if (req.headers.authorization && req.headers.authorization.startsWith('Bearer ')) {
    userJson = decodeURIComponent(req.headers.authorization.slice(7));
  } else if (req.headers.cookie) {
    const m = req.headers.cookie.match(/gaeks_session_v3=([^;]+)/) || req.headers.cookie.match(/gaeks_session=([^;]+)/);
    if (m) userJson = decodeURIComponent(m[1]);
  }

  if (userJson) {
    try {
      const u = JSON.parse(userJson);
      if (u && u.email) {
        const cleanEmail = u.email.toLowerCase().trim();
        const userId = 'usr_' + cleanEmail.replace(/[^a-z0-9]/g, '_');
        return {
          id: userId,
          email: cleanEmail,
          name: u.name || cleanEmail
        };
      }
    } catch(e) {}
  }
  return null;
}

function handleCvRequest(req, res, parsedUrl, postData) {
  const user = getAuthenticatedUser(req);
  if (!user) {
    res.writeHead(401, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'error', message: 'Unauthorized: Sesi tidak valid.' }));
  }

  const authUserId = user.id;
  const store = getStore(CVS_FILE);
  const action = parsedUrl.query.action || (postData && postData.action) || 'list';

  if (action === 'list') {
    const tab = parsedUrl.query.tab || 'active';
    const userCvs = store[authUserId] || [];
    let list = userCvs.filter(c => tab === 'trash' ? c.deletedAt : !c.deletedAt);
    list.sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'success', data: list }));
  }

  if (action === 'get') {
    const id = parsedUrl.query.id || (postData && postData.id);
    for (const otherUid of Object.keys(store)) {
      if (otherUid !== authUserId) {
        const otherList = store[otherUid] || [];
        if (otherList.some(c => c.id === id)) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({ status: 'error', message: 'Forbidden: Anda tidak memiliki akses ke resume ini.' }));
        }
      }
    }

    const myList = store[authUserId] || [];
    const item = myList.find(c => c.id === id);
    if (item) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ status: 'success', data: item }));
    }
    res.writeHead(404, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'error', message: 'Resume tidak ditemukan.' }));
  }

  if (action === 'save') {
    const cv = (postData && postData.cv) || postData || {};
    if (!cv.id) {
      cv.id = 'cv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4);
    }
    for (const otherUid of Object.keys(store)) {
      if (otherUid !== authUserId) {
        const otherList = store[otherUid] || [];
        if (otherList.some(c => c.id === cv.id)) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({ status: 'error', message: 'Forbidden: Anda tidak memiliki izin mengedit resume ini.' }));
        }
      }
    }

    if (!store[authUserId]) store[authUserId] = [];
    const now = Date.now();
    cv.updatedAt = now;
    cv.deletedAt = null;

    const idx = store[authUserId].findIndex(c => c.id === cv.id);
    if (idx >= 0) {
      store[authUserId][idx] = cv;
    } else {
      store[authUserId].unshift(cv);
    }
    saveStore(CVS_FILE, store);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'success', message: 'Resume berhasil disimpan.', data: cv }));
  }

  if (action === 'delete') {
    const id = (postData && postData.id) || parsedUrl.query.id;
    for (const otherUid of Object.keys(store)) {
      if (otherUid !== authUserId) {
        if ((store[otherUid] || []).some(c => c.id === id)) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({ status: 'error', message: 'Forbidden.' }));
        }
      }
    }

    if (store[authUserId]) {
      const item = store[authUserId].find(c => c.id === id);
      if (item) {
        item.deletedAt = Date.now();
        item.updatedAt = Date.now();
        saveStore(CVS_FILE, store);
      }
    }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'success', message: 'Dipindahkan ke sampah.' }));
  }

  if (action === 'restore') {
    const id = (postData && postData.id) || parsedUrl.query.id;
    for (const otherUid of Object.keys(store)) {
      if (otherUid !== authUserId) {
        if ((store[otherUid] || []).some(c => c.id === id)) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({ status: 'error', message: 'Forbidden.' }));
        }
      }
    }
    if (store[authUserId]) {
      const item = store[authUserId].find(c => c.id === id);
      if (item) {
        item.deletedAt = null;
        item.updatedAt = Date.now();
        saveStore(CVS_FILE, store);
      }
    }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'success', message: 'Berhasil dipulihkan.' }));
  }

  if (action === 'delete_permanent') {
    const id = (postData && postData.id) || parsedUrl.query.id;
    for (const otherUid of Object.keys(store)) {
      if (otherUid !== authUserId) {
        if ((store[otherUid] || []).some(c => c.id === id)) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          return res.end(JSON.stringify({ status: 'error', message: 'Forbidden.' }));
        }
      }
    }
    if (storeBerikut adalah skrip pembaruan yang ringkas, mandiri (*100% self-contained*), dan dirancang khusus untuk dieksekusi langsung di terminal GitHub Codespaces Anda pada repositori [gaeksgroup-hash/gaeks-gdp](https://github.com/gaeksgroup-hash/gaeks-gdp).

Skrip ini membaca langsung struktur berkas lokal repositori Anda, melakukan perbaikan secara *in-place*, menyusun backend database SQLite & REST API, serta mengaktifkan 15 tema ATS tanpa bergantung pada berkas sementara mana pun.

---

### Langkah 1: Buat dan Jalankan Skrip di Terminal Codespaces

Jalankan perintah berikut di terminal Codespaces Anda:

```bash
cat << 'EOF' > update_gaeks.py
#!/usr/bin/env python3
import os, sys, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))

def write_file(rel_path, content):
    p = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    os.replace(tmp, p)
    print(f"✓ Berhasil disimpan: {rel_path} ({os.path.getsize(p)} bytes)")

print("=== [1/4] Menyiapkan Backend API (SQLite PDO + JSON Fallback) ===")
os.makedirs(os.path.join(ROOT, "api", "data"), exist_ok=True)

write_file("api/db.php", """<?php
$dataDir = __DIR__ . '/data';
if (!file_exists($dataDir)) { @mkdir($dataDir, 0777, true); }
$sqliteFile = $dataDir . '/gaeks.sqlite';
$cvStoreFile = $dataDir . '/cvs_store.json';
$presStoreFile = $dataDir . '/presentations_store.json';

function getPdoConnection() {
    global $sqliteFile;
    try {
        if (class_exists('PDO') && in_array('sqlite', PDO::getAvailableDrivers())) {
            $pdo = new PDO('sqlite:' . $sqliteFile);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
            $pdo->exec("CREATE TABLE IF NOT EXISTS cvs (id TEXT PRIMARY KEY, user_id TEXT NOT NULL, title TEXT, is_draft INTEGER DEFAULT 0, completeness INTEGER DEFAULT 0, data_json TEXT, created_at INTEGER, updated_at INTEGER, deleted_at INTEGER)");
            $pdo->exec("CREATE INDEX IF NOT EXISTS idx_cvs_user ON cvs(user_id)");
            $pdo->exec("CREATE TABLE IF NOT EXISTS presentations (id TEXT PRIMARY KEY, user_id TEXT NOT NULL, name TEXT, date TEXT, status TEXT DEFAULT 'active', data_json TEXT, created_at INTEGER, updated_at INTEGER, deleted_at INTEGER)");
            $pdo->exec("CREATE INDEX IF NOT EXISTS idx_pres_user ON presentations(user_id)");
            return $pdo;
        }
    } catch (Exception $e) {}
    return null;
}
function getJsonStore($f) {
    if (file_exists($f)) {
        $raw = @file_get_contents($f);
        if ($raw) { $arr = json_decode($raw, true); if (is_array($arr)) return $arr; }
    }
    return [];
}
function saveJsonStore($f, $d) { @file_put_contents($f, json_encode($d, JSON_PRETTY_PRINT)); }

function getAuthenticatedUser() {
    $uJson = null;
    if (!empty($_SERVER['HTTP_X_GAEKS_AUTH'])) $uJson = urldecode($_SERVER['HTTP_X_GAEKS_AUTH']);
    elseif (!empty($_SERVER['HTTP_AUTHORIZATION']) && preg_match('/Bearer\\s+(.*)$/i', $_SERVER['HTTP_AUTHORIZATION'], $m)) $uJson = urldecode($m[1]);
    elseif (!empty($_COOKIE['gaeks_session_v3'])) $uJson = $_COOKIE['gaeks_session_v3'];
    elseif (!empty($_COOKIE['gaeks_session'])) $uJson = $_COOKIE['gaeks_session'];
    if ($uJson) {
        $u = json_decode($uJson, true);
        if ($u && !empty($u['email'])) {
            $clean = strtolower(trim($u['email']));
            return ['id' => 'usr_' . preg_replace('/[^a-z0-9]/', '_', $clean), 'email' => $clean, 'name' => $u['name'] ?? $clean];
        }
    }
    return null;
}
""")

write_file("api/cv.php", """<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Gaeks-Auth');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }

require_once __DIR__ . '/db.php';
$user = getAuthenticatedUser();
if (!$user) { http_response_code(401); echo json_encode(["status" => "error", "message" => "Unauthorized"]); exit; }
$authUserId = $user['id'];
$pdo = getPdoConnection();
$postData = json_decode(file_get_contents('php://input'), true) ?? [];
$action = $_GET['action'] ?? $postData['action'] ?? 'list';

if ($action === 'list') {
    $tab = $_GET['tab'] ?? 'active';
    $results = [];
    if ($pdo) {
        $sql = "SELECT * FROM cvs WHERE user_id = :uid AND " . ($tab === 'trash' ? "deleted_at IS NOT NULL" : "deleted_at IS NULL") . " ORDER BY updated_at DESC";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([':uid' => $authUserId]);
        foreach ($stmt->fetchAll() as $r) {
            $results[] = ['id' => $r['id'], 'title' => $r['title'], 'isDraft' => (bool)$r['is_draft'], 'completeness' => (int)$r['completeness'], 'updatedAt' => (int)$r['updated_at'], 'deletedAt' => $r['deleted_at'] ? (int)$r['deleted_at'] : null, 'data' => json_decode($r['data_json'], true) ?? []];
        }
    } else {
        $store = getJsonStore($cvStoreFile);
        foreach ($store[$authUserId] ?? [] as $c) {
            if ($tab === 'trash' && !empty($c['deletedAt'])) $results[] = $c;
            elseif ($tab !== 'trash' && empty($c['deletedAt'])) $results[] = $c;
        }
        usort($results, fn($a, $b) => ($b['updatedAt'] ?? 0) <=> ($a['updatedAt'] ?? 0));
    }
    echo json_encode(["status" => "success", "data" => $results]); exit;
}

if ($action === 'get') {
    $id = $_GET['id'] ?? $postData['id'] ?? '';
    if ($pdo) {
        $cStmt = $pdo->prepare("SELECT user_id FROM cvs WHERE id = :id");
        $cStmt->execute([':id' => $id]);
        $row = $cStmt->fetch();
        if ($row) {
            if ($row['user_id'] !== $authUserId) { http_response_code(403); echo json_encode(["status" => "error", "message" => "Forbidden"]); exit; }
            $stmt = $pdo->prepare("SELECT * FROM cvs WHERE id = :id AND user_id = :uid");
            $stmt->execute([':id' => $id, ':uid' => $authUserId]);
            $r = $stmt->fetch();
            if ($r) {
                echo json_encode(["status" => "success", "data" => ['id' => $r['id'], 'title' => $r['title'], 'isDraft' => (bool)$r['is_draft'], 'completeness' => (int)$r['completeness'], 'updatedAt' => (int)$r['updated_at'], 'deletedAt' => $r['deleted_at'] ? (int)$r['deleted_at'] : null, 'data' => json_decode($r['data_json'], true) ?? []]]); exit;
            }
        }
    } else {
        $store = getJsonStore($cvStoreFile);
        foreach ($store as $ouid => $olist) {
            if ($ouid !== $authUserId && array_filter($olist, fn($c) => $c['id'] === $id)) { http_response_code(403); echo json_encode(["status" => "error", "message" => "Forbidden"]); exit; }
        }
        foreach ($store[$authUserId] ?? [] as $c) { if ($c['id'] === $id) { echo json_encode(["status" => "success", "data" => $c]); exit; } }
    }
    http_response_code(404); echo json_encode(["status" => "error", "message" => "Not found"]); exit;
}

if ($action === 'save') {
    $cv = $postData['cv'] ?? $postData;
    if (empty($cv['id'])) $cv['id'] = 'cv_' . round(microtime(true)*1000) . '_' . substr(md5(random_bytes(4)), 0, 4);
    $id = $cv['id']; $title = $cv['title'] ?? 'CV Tanpa Judul';
    $isDraft = !empty($cv['isDraft']) ? 1 : 0; $comp = (int)($cv['completeness'] ?? 0);
    $now = round(microtime(true) * 1000); $dJson = json_encode($cv['data'] ?? []);
    if ($pdo) {
        $cStmt = $pdo->prepare("SELECT user_id FROM cvs WHERE id = :id");
        $cStmt->execute([':id' => $id]); $existing = $cStmt->fetch();
        if ($existing && $existing['user_id'] !== $authUserId) { http_response_code(403); echo json_encode(["status" => "error", "message" => "Forbidden"]); exit; }
        if ($existing) {
            $pdo->prepare("UPDATE cvs SET title=:t, is_draft=:d, completeness=:c, data_json=:dj, updated_at=:u WHERE id=:id AND user_id=:uid")->execute([':t'=>$title,':d'=>$isDraft,':c'=>$comp,':dj'=>$dJson,':u'=>$now,':id'=>$id,':uid'=>$authUserId]);
        } else {
            $pdo->prepare("INSERT INTO cvs (id, user_id, title, is_draft, completeness, data_json, created_at, updated_at) VALUES (:id, :uid, :t, :d, :c, :dj, :now, :now)")->execute([':id'=>$id,':uid'=>$authUserId,':t'=>$title,':d'=>$isDraft,':c'=>$comp,':dj'=>$dJson,':now'=>$now]);
        }
    } else {
        $store = getJsonStore($cvStoreFile);
        if (!isset($store[$authUserId])) $store[$authUserId] = [];
        $idx = -1; foreach ($store[$authUserId] as $i => $c) { if ($c['id'] === $id) { $idx = $i; break; } }
        $obj = ['id'=>$id,'title'=>$title,'isDraft'=>(bool)$isDraft,'completeness'=>$comp,'updatedAt'=>$now,'deletedAt'=>null,'data'=>$cv['data']??[]];
        if ($idx >= 0) $store[$authUserId][$idx] = $obj; else array_unshift($store[$authUserId], $obj);
        saveJsonStore($cvStoreFile, $store);
    }
    $cv['updatedAt'] = $now;
    echo json_encode(["status" => "success", "data" => $cv]); exit;
}

if ($action === 'delete') {
    $id = $postData['id'] ?? $_GET['id'] ?? ''; $now = round(microtime(true) * 1000);
    if ($pdo) $pdo->prepare("UPDATE cvs SET deleted_at = :del, updated_at = :now WHERE id = :id AND user_id = :uid")->execute([':del' => $now, ':now' => $now, ':id' => $id, ':uid' => $authUserId]);
    else {
        $store = getJsonStore($cvStoreFile);
        if (isset($store[$authUserId])) { foreach ($store[$authUserId] as &$c) { if ($c['id'] === $id) { $c['deletedAt'] = $now; break; } } saveJsonStore($cvStoreFile, $store); }
    }
    echo json_encode(["status" => "success"]); exit;
}
""")

write_file("api/presentation.php", """<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Gaeks-Auth');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }

require_once __DIR__ . '/db.php';
$user = getAuthenticatedUser();
if (!$user) { http_response_code(401); echo json_encode(["status" => "error", "message" => "Unauthorized"]); exit; }
$authUserId = $user['id'];
$pdo = getPdoConnection();
$postData = json_decode(file_get_contents('php://input'), true) ?? [];
$action = $_GET['action'] ?? $postData['action'] ?? 'list';

if ($action === 'list') {
    $results = [];
    if ($pdo) {
        $stmt = $pdo->prepare("SELECT id, name, date, status, updated_at, deleted_at FROM presentations WHERE user_id = :uid ORDER BY updated_at DESC");
        $stmt->execute([':uid' => $authUserId]);
        foreach ($stmt->fetchAll() as $r) {
            $results[] = ['id' => $r['id'], 'name' => $r['name'], 'date' => $r['date'], 'status' => $r['status'], 'updatedAt' => (int)$r['updated_at'], 'deletedAt' => $r['deleted_at'] ? (int)$r['deleted_at'] : null];
        }
    } else {
        $store = getJsonStore($presStoreFile);
        foreach ($store[$authUserId] ?? [] as $p) {
            $results[] = ['id' => $p['id'], 'name' => $p['meetingName'] ?? $p['name'] ?? 'Presentasi', 'date' => $p['meetingDate'] ?? $p['date'] ?? date('Y-m-d'), 'status' => $p['status'] ?? 'active', 'updatedAt' => $p['updatedAt'] ?? time() * 1000, 'deletedAt' => $p['deletedAt'] ?? null];
        }
    }
    echo json_encode(["status" => "success", "data" => $results]); exit;
}

if ($action === 'save') {
    $pres = $postData['data'] ?? $postData;
    if (empty($pres['id'])) $pres['id'] = 'MTG_' . round(microtime(true) * 1000);
    $id = $pres['id']; $name = $pres['meetingName'] ?? $pres['name'] ?? 'Presentasi';
    $date = $pres['meetingDate'] ?? $pres['date'] ?? date('Y-m-d'); $status = $pres['status'] ?? 'active';
    $now = round(microtime(true) * 1000); $dJson = json_encode($pres);
    if ($pdo) {
        $cStmt = $pdo->prepare("SELECT user_id FROM presentations WHERE id = :id");
        $cStmt->execute([':id' => $id]); $existing = $cStmt->fetch();
        if ($existing && $existing['user_id'] !== $authUserId) { http_response_code(403); echo json_encode(["status" => "error", "message" => "Forbidden"]); exit; }
        if ($existing) {
            $pdo->prepare("UPDATE presentations SET name=:n, date=:d, status=:s, data_json=:dj, updated_at=:u WHERE id=:id AND user_id=:uid")->execute([':n'=>$name,':d'=>$date,':s'=>$status,':dj'=>$dJson,':u'=>$now,':id'=>$id,':uid'=>$authUserId]);
        } else {
            $pdo->prepare("INSERT INTO presentations (id, user_id, name, date, status, data_json, created_at, updated_at) VALUES (:id, :uid, :n, :d, :s, :dj, :now, :now)")->execute([':id'=>$id,':uid'=>$authUserId,':n'=>$name,':d'=>$date,':s'=>$status,':dj'=>$dJson,':now'=>$now]);
        }
    } else {
        $store = getJsonStore($presStoreFile);
        if (!isset($store[$authUserId])) $store[$authUserId] = [];
        $idx = -1; foreach ($store[$authUserId] as $i => $p) { if ($p['id'] === $id) { $idx = $i; break; } }
        $pres['id'] = $id; $pres['updatedAt'] = $now;
        if ($idx >= 0) $store[$authUserId][$idx] = $pres; else array_unshift($store[$authUserId], $pres);
        saveJsonStore($presStoreFile, $store);
    }
    echo json_encode(["status" => "success", "data" => $pres]); exit;
}
""")

print("=== [2/4] Memperbarui cv-dashboard.html ===")
with open(os.path.join(ROOT, "cv-dashboard.html"), "r", encoding="utf-8") as f:
    dash = f.read()

if "function calculateCvCompleteness" not in dash:
    helper_code = """
    function calculateCvCompleteness(cv) {
      if (!cv) return 0;
      const d = cv.data || cv;
      let score = 0;
      if (d.name && d.name.trim().length >= 2) score += 15;
      if (d.title && d.title.trim().length >= 2) score += 10;
      if (d.email && d.email.includes('@')) score += 10;
      if (d.phone && d.phone.trim().length >= 5) score += 5;
      if (d.location && d.location.trim().length >= 2) score += 5;
      if (d.summary && d.summary.trim().length >= 20) score += 15;
      if (Array.isArray(d.experiences) && d.experiences.length > 0 && d.experiences.some(e => (e.company && e.company.trim()) || (e.position && e.position.trim()) || (e.role && e.role.trim()))) score += 20;
      if (Array.isArray(d.educations) && d.educations.length > 0 && d.educations.some(ed => (ed.school && ed.school.trim()) || (ed.degree && ed.degree.trim()))) score += 10;
      const hasSkills = (Array.isArray(d.skillGroups) && d.skillGroups.some(g => g.skills && g.skills.trim())) || (typeof d.skills === 'string' && d.skills.trim().length > 0);
      if (hasSkills) score += 10;
      return Math.min(100, Math.round(score));
    }
    if (typeof window !== 'undefined') window.calculateCvCompleteness = calculateCvCompleteness;

    function syncCvWithBackend(action, data = {}, params = '') {
      try {
        const u = (typeof GaeksAuth !== 'undefined' && GaeksAuth.getCurrentUser) ? GaeksAuth.getCurrentUser() : null;
        const headers = { 'Content-Type': 'application/json', 'X-Gaeks-Auth': encodeURIComponent(JSON.stringify(u || {})) };
        const url = '/api/cv.php?action=' + action + (params ? '&' + params : '');
        if (action === 'list' || action === 'get') return fetch(url, { method: 'GET', headers }).then(r => r.json()).catch(() => null);
        return fetch(url, { method: 'POST', headers, body: JSON.stringify(data) }).then(r => r.json()).catch(() => null);
      } catch(e) { return Promise.resolve(null); }
    }
    if (typeof window !== 'undefined') window.syncCvWithBackend = syncCvWithBackend;
"""
    dash = dash.replace("function loadCvList() {", helper_code + "\n    function loadCvList() {")

clean_create_cv = """function createNewBlankCV() {
      try {
        const lang = (typeof currentLang !== 'undefined' && currentLang) ? currentLang : 'id';
        const listLen = (typeof cvList !== 'undefined' && Array.isArray(cvList)) ? cvList.length : 0;
        const title = (lang === 'en' ? 'New Resume ' : 'CV Baru ') + (listLen + 1);
        const newCv = createBlankCvObject(title);
        newCv.isDraft = true;
        newCv.updatedAt = Date.now();
        if (typeof cvList === 'undefined' || !Array.isArray(cvList)) cvList = [];
        cvList.unshift(newCv);
        saveCvList();
        syncCvWithBackend('save', { cv: newCv });
        window.location.href = 'cv.html?id=' + encodeURIComponent(newCv.id);
      } catch(e) {
        window.location.href = 'cv.html?id=cv_' + Date.now();
      }
    }"""
dash = re.sub(r'function\s+createNewBlankCV\s*\(\)\s*\{[\s\S]*?window\.location\.href\s*=\s*[\'"]cv\.html\?id=[\s\S]*?\}\s*\}', lambda m: clean_create_cv, dash, count=1)
dash = re.sub(r'const\s+isDraft\s*=\s*Boolean\(cv\.isDraft\);', 'const comp = calculateCvCompleteness(cv);\n        const isDraft = Boolean(cv.isDraft || comp < 30);', dash)
write_file("cv-dashboard.html", dash)

print("=== [3/4] Memperbarui cv.html & editor.html (15 Tema ATS) ===")
with open(os.path.join(ROOT, "cv.html"), "r", encoding="utf-8") as f:
    cv = f.read()

fifteen_themes_css = """    /* 15 VARIAN TEMA VISUAL ATS LENGKAP */
    .style-apex, .style-modern-corporate { --accent: #1e3a8a; --accent-soft: #eff6ff; --accent-border: #bfdbfe; --tag-bg: #f1f5f9; --tag-text: #0f172a; }
    .style-swiss, .style-swiss-editorial { --accent: #0f172a; --accent-soft: #f8fafc; --accent-border: #cbd5e1; --tag-bg: #f8fafc; --tag-text: #1e293b; }
    .style-silicon, .style-silicon-tech { --accent: #047857; --accent-soft: #f0fdf4; --accent-border: #bbf7d0; --tag-bg: #f1f5f9; --tag-text: #065f46; }
    .style-prestige { --accent: #881337; --accent-soft: #fff1f2; --accent-border: #fecdd3; --tag-bg: #f8fafc; --tag-text: #4c0519; }
    .style-pure-ats { --accent: #1e293b; --accent-soft: #f8fafc; --accent-border: #94a3b8; --tag-bg: #f1f5f9; --tag-text: #0f172a; }
    .style-nordic-slate { --accent: #334155; --accent-soft: #f1f5f9; --accent-border: #94a3b8; --tag-bg: #f8fafc; --tag-text: #1e293b; }
    .style-emerald-horizon { --accent: #0f766e; --accent-soft: #f0fdfa; --accent-border: #99f6e4; --tag-bg: #f8fafc; --tag-text: #115e59; }
    .style-crimson-elegance { --accent: #991b1b; --accent-soft: #fef2f2; --accent-border: #fecaca; --tag-bg: #f8fafc; --tag-text: #7f1d1d; }
    .style-obsidian-minimal { --accent: #18181b; --accent-soft: #fafafa; --accent-border: #d4d4d8; --tag-bg: #f4f4f5; --tag-text: #27272a; }
    .style-oxford-navy { --accent: #172554; --accent-soft: #eff6ff; --accent-border: #93c5fd; --tag-bg: #f8fafc; --tag-text: #1e3a8a; }
    .style-imperial-gold { --accent: #b45309; --accent-soft: #fffbeb; --accent-border: #fde68a; --tag-bg: #fefce8; --tag-text: #78350f; }
    .style-azure-sky { --accent: #0284c7; --accent-soft: #f0f9ff; --accent-border: #bae6fd; --tag-bg: #f8fafc; --tag-text: #0369a1; }
    .style-metro-corporate { --accent: #475569; --accent-soft: #f8fafc; --accent-border: #cbd5e1; --tag-bg: #f1f5f9; --tag-text: #1e293b; }
    .style-boutique-creative { --accent: #4f46e5; --accent-soft: #eef2ff; --accent-border: #c7d2fe; --tag-bg: #f8fafc; --tag-text: #3730a3; }
    .style-apex-monolith { --accent: #1e1b4b; --accent-soft: #e0e7ff; --accent-border: #a5b4fc; --tag-bg: #f8fafc; --tag-text: #312e81; }"""

if "style-imperial-gold" not in cv:
    cv = re.sub(r'/\* VARIAN ARSITEKTUR TEMA \*/.*?(?=\.accent-color)', lambda m: fifteen_themes_css + '\n    ', cv, flags=re.DOTALL)

cv = re.sub(r'<!-- ================= VIEW 1: DASHBOARD LIST[\s\S]*?<!-- ================= VIEW 2: CV EDITOR STUDIO[^\n]*\n', '<!-- ================= CV EDITOR STUDIO (15 TEMA) ================= -->\n', cv)
cv = cv.replace('<section id="view-editor" class="hidden ', '<section id="view-editor" class="')

theme_select_html = """<div class="flex items-center gap-2">
          <label for="theme-selector" class="text-xs text-slate-400 font-medium hidden sm:inline">Pilihan Tema ATS (15 Preset):</label>
          <select id="theme-selector" onchange="setThemeLayout(this.value)" class="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:border-blue-500 focus:outline-none cursor-pointer font-medium">
            <option value="apex">Apex Blue (Eksekutif)</option>
            <option value="modern-corporate">Modern Corporate</option>
            <option value="swiss">Swiss Neutral (Monokrom)</option>
            <option value="swiss-editorial">Swiss Editorial</option>
            <option value="silicon">Silicon Tech (Emerald Modern)</option>
            <option value="silicon-tech">Silicon Tech Clean</option>
            <option value="prestige">Prestige Burgundy (Finansial)</option>
            <option value="pure-ats">Pure Minimalist ATS (Ultra Clean)</option>
            <option value="nordic-slate">Nordic Slate (Elegan & Tenang)</option>
            <option value="emerald-horizon">Emerald Horizon (Teal Profesional)</option>
            <option value="crimson-elegance">Crimson Elegance (Ruby Kontras)</option>
            <option value="obsidian-minimal">Obsidian Minimal (High Contrast)</option>
            <option value="oxford-navy">Oxford Navy (Akademik & Formal)</option>
            <option value="imperial-gold">Imperial Gold (Amber Luxury)</option>
            <option value="azure-sky">Azure Sky (Tech Vibrant)</option>
            <option value="metro-corporate">Metro Corporate (Cool Grey)</option>
            <option value="boutique-creative">Boutique Creative (Indigo Ungu)</option>
            <option value="apex-monolith">Apex Monolith (Midnight Blue)</option>
          </select>
        </div>"""
if '<select id="theme-selector"' not in cv:
    cv = re.sub(r'<div class="flex items-center space-x-1 bg-slate-900 p-1 rounded-lg border border-slate-800 text-xs font-semibold">[\s\S]*?id="btn-layout-prestige"[\s\S]*?</div>', theme_select_html, cv, count=1)

cv_js = """
    function saveCvProgress() {
      try {
        if (!currentEditingCv) return;
        currentEditingCv.data = extractFormData();
        currentEditingCv.updatedAt = Date.now();
        saveCvList();
        if (typeof syncCvWithBackend === 'function') syncCvWithBackend('save', { cv: currentEditingCv });
        const btn = document.getElementById('btn-save-progress');
        if (btn) {
          const old = btn.innerHTML; btn.innerHTML = '<span>✓ Tersimpan</span>';
          setTimeout(() => { btn.innerHTML = old; }, 1500);
        }
      } catch(e) {}
    }
    if (typeof window !== 'undefined') window.saveCvProgress = saveCvProgress;
"""
if "function saveCvProgress" not in cv:
    cv = cv.replace("function renderCV() {", cv_js + "\n    function renderCV() {")

if "btn-save-progress" not in cv:
    cv = cv.replace('<a href="cv-dashboard.html"', '<button type="button" id="btn-save-progress" onclick="saveCvProgress()" class="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-md shadow-emerald-500/20 cursor-pointer"><span>💾 Simpan Progress</span></button>\n        <a href="cv-dashboard.html"')

write_file("cv.html", cv)
write_file("editor.html", cv)

print("=== [4/4] Memperbarui presentation.html ===")
with open(os.path.join(ROOT, "presentation.html"), "r", encoding="utf-8") as f:
    pres = f.read()

pres_sync_helpers = """        // GAEKS PRESENTATION BACKEND SYNC
        function syncPresWithBackend(action, data = {}, params = '') {
            try {
                const u = (typeof GaeksAuth !== 'undefined' && GaeksAuth.getCurrentUser) ? GaeksAuth.getCurrentUser() : null;
                const headers = { 'Content-Type': 'application/json', 'X-Gaeks-Auth': encodeURIComponent(JSON.stringify(u || {})) };
                const url = '/api/presentation.php?action=' + action + (params ? '&' + params : '');
                if (action === 'list' || action === 'get') return fetch(url, { method: 'GET', headers }).then(r => r.json()).catch(() => null);
                return fetch(url, { method: 'POST', headers, body: JSON.stringify(data) }).then(r => r.json()).catch(() => null);
            } catch(e) { return Promise.resolve(null); }
        }
        if (typeof window !== 'undefined') window.syncPresWithBackend = syncPresWithBackend;
"""
if "function syncPresWithBackend" not in pres:
    pres = re.sub(r'const\s+GAEKS_PRES_LIST_KEY\s*=\s*\(\)\s*=>\s*\{', lambda m: pres_sync_helpers + '\n        ' + m.group(0), pres, count=1)

pres = re.sub(r'(localStorage\.setItem\(GAEKS_PRES_ITEM_KEY\(data\.id\),\s*JSON\.stringify\(data\)\);)', r'\1\n            syncPresWithBackend("save", { data: data });', pres)
write_file("presentation.html", pres)

print("\n🎉 Pembaruan Berhasil! Semua berkas telah diselaraskan dengan sempurna.")
