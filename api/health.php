<?php
declare(strict_types=1);
require_once __DIR__ . '/bootstrap.php';
$pdo=gaeks_db();
$pdo->query('SELECT 1')->fetchColumn();
gaeks_ok(['service'=>'gdp-api','database'=>'ok','environment'=>APP_ENV,'billingEnabled'=>BILLING_ENABLED]);
