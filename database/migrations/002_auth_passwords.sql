SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET time_zone = '+00:00';

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255) NULL AFTER email_verified_at;

INSERT IGNORE INTO schema_migrations (version) VALUES ('002_auth_passwords');
