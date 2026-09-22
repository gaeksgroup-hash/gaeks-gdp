CREATE TABLE IF NOT EXISTS presentation_shares (
    presentation_id CHAR(36) PRIMARY KEY,
    owner_user_id CHAR(36) NOT NULL,
    public_token CHAR(48) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    revoked_at DATETIME(6) NULL,
    UNIQUE KEY uq_presentation_share_token (public_token),
    CONSTRAINT fk_presentation_share_presentation FOREIGN KEY (presentation_id) REFERENCES presentations(id) ON DELETE CASCADE,
    CONSTRAINT fk_presentation_share_owner FOREIGN KEY (owner_user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
INSERT IGNORE INTO schema_migrations (version) VALUES ('003_presentation_shares');
