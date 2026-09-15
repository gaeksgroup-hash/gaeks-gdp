<?php
declare(strict_types=1);
require_once __DIR__ . '/bootstrap.php';

// Compatibility aliases for code that still includes db.php.
function getPdoConnection(): PDO { return gaeks_db(); }
function getAuthenticatedUser(): ?array { return gaeks_current_user(false); }
