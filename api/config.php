<?php
declare(strict_types=1);

function gaeks_load_env(): void
{
    $candidates = [dirname(__DIR__, 2) . DIRECTORY_SEPARATOR . '.env', dirname(__DIR__) . DIRECTORY_SEPARATOR . '.env'];
    foreach ($candidates as $path) {
        if (!is_file($path) || !is_readable($path)) continue;
        foreach (file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [] as $line) {
            $line = trim($line);
            if ($line === '' || str_starts_with($line, '#') || !str_contains($line, '=')) continue;
            [$key, $value] = array_map('trim', explode('=', $line, 2));
            if ($key === '' || getenv($key) !== false) continue;
            if (strlen($value) >= 2 && (($value[0] === '"' && str_ends_with($value, '"')) || ($value[0] === "'" && str_ends_with($value, "'")))) $value = substr($value, 1, -1);
            putenv($key . '=' . $value);
            $_ENV[$key] = $value;
        }
        break;
    }
}

function gaeks_env(string $key, ?string $default = null): ?string
{
    $value = getenv($key);
    return $value === false ? $default : $value;
}

gaeks_load_env();

define('APP_ENV', gaeks_env('APP_ENV', 'production'));
define('APP_URL', rtrim((string) gaeks_env('APP_URL', 'https://gdp.gaeks.com'), '/'));
define('APP_SESSION_COOKIE', gaeks_env('APP_SESSION_COOKIE', '__Host-gaeks_session'));
define('APP_SESSION_TTL_SECONDS', max(3600, (int) gaeks_env('APP_SESSION_TTL_SECONDS', '604800')));
define('SESSION_SECRET', (string) gaeks_env('SESSION_SECRET', ''));
define('DB_DSN', (string) gaeks_env('DB_DSN', ''));
define('DB_HOST', gaeks_env('DB_HOST', 'localhost'));
define('DB_PORT', (int) gaeks_env('DB_PORT', '3306'));
define('DB_NAME', (string) gaeks_env('DB_NAME', ''));
define('DB_USER', (string) gaeks_env('DB_USER', ''));
define('DB_PASSWORD', (string) gaeks_env('DB_PASSWORD', ''));
define('SMTP_HOST', gaeks_env('SMTP_HOST', 'smtp.hostinger.com'));
define('SMTP_PORT', (int) gaeks_env('SMTP_PORT', '465'));
define('SMTP_USER', (string) gaeks_env('SMTP_USER', ''));
define('SMTP_PASSWORD', (string) gaeks_env('SMTP_PASSWORD', ''));
define('MAIL_TRANSPORT', (string) gaeks_env('MAIL_TRANSPORT', 'auto'));
define('SMTP_FROM_NAME', gaeks_env('SMTP_FROM_NAME', 'GAEKS Digital Products'));
define('REPLY_TO_EMAIL', gaeks_env('REPLY_TO_EMAIL', 'gdp@gaeks.com'));
define('ADMIN_NOTIFICATION_EMAIL', gaeks_env('ADMIN_NOTIFICATION_EMAIL', 'gdp@gaeks.com'));
define('GOOGLE_CLIENT_ID', (string) gaeks_env('GOOGLE_CLIENT_ID', ''));
define('TURNSTILE_SITE_KEY', (string) gaeks_env('TURNSTILE_SITE_KEY', ''));
define('TURNSTILE_SECRET_KEY', (string) gaeks_env('TURNSTILE_SECRET_KEY', ''));
define('OTP_TTL_SECONDS', max(180, (int) gaeks_env('OTP_TTL_SECONDS', '600')));
define('OTP_MAX_ATTEMPTS', max(3, (int) gaeks_env('OTP_MAX_ATTEMPTS', '5')));
define('TEST_OTP_CODE', (string) gaeks_env('TEST_OTP_CODE', ''));
define('BILLING_ENABLED', filter_var(gaeks_env('BILLING_ENABLED', 'false'), FILTER_VALIDATE_BOOLEAN));
define('FREE_LIMITS_ENABLED', filter_var(gaeks_env('FREE_LIMITS_ENABLED', 'false'), FILTER_VALIDATE_BOOLEAN));
