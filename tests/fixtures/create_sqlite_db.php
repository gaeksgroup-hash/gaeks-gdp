<?php
declare(strict_types=1);

$target = $argv[1] ?? '';
if ($target === '') {
    fwrite(STDERR, "Usage: php create_sqlite_db.php <database-path>\n");
    exit(2);
}

$schema = file_get_contents(__DIR__ . '/sqlite_schema.sql');
if ($schema === false) {
    throw new RuntimeException('SQLite fixture schema cannot be read.');
}

$pdo = new PDO('sqlite:' . $target, null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$pdo->exec($schema);
fwrite(STDOUT, "Test database ready.\n");
