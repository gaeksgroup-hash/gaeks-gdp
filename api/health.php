<?php
declare(strict_types=1);
require_once __DIR__ . '/bootstrap.php';
$configuration = [
    'sessionSecretConfigured' => strlen(SESSION_SECRET) >= 32,
    'databaseNameConfigured' => DB_NAME !== '',
    'databaseUserConfigured' => DB_USER !== '',
    'databasePasswordConfigured' => DB_PASSWORD !== '',
];
try {
    $pdo = gaeks_db();
    $pdo->query('SELECT 1')->fetchColumn();
    gaeks_ok(['service'=>'gdp-api','database'=>'ok','environment'=>APP_ENV,'billingEnabled'=>BILLING_ENABLED, 'configuration'=>$configuration]);
} catch (Throwable $error) {
    http_response_code(503);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['ok'=>false, 'status'=>'degraded', 'service'=>'gdp-api', 'database'=>'unavailable', 'configuration'=>$configuration], JSON_UNESCAPED_SLASHES);
}
