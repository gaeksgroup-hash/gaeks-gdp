<?php
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
    } elseif (!empty($_SERVER['HTTP_AUTHORIZATION']) && preg_match('/Bearer\s+(.*)$/i', $_SERVER['HTTP_AUTHORIZATION'], $m)) {
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
