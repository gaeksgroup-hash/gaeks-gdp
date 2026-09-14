<?php
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
    elseif (!empty($_SERVER['HTTP_AUTHORIZATION']) && preg_match('/Bearer\s+(.*)$/i', $_SERVER['HTTP_AUTHORIZATION'], $m)) $uJson = urldecode($m[1]);
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
