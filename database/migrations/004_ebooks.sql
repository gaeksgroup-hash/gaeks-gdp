CREATE TABLE IF NOT EXISTS ebooks (
 id CHAR(36) PRIMARY KEY, title VARCHAR(255) NOT NULL, slug VARCHAR(180) NOT NULL, description TEXT NOT NULL,
 price_idr INT UNSIGNED NOT NULL, cover_path VARCHAR(512) NULL, file_path VARCHAR(512) NOT NULL,
 status ENUM('draft','published','archived') NOT NULL DEFAULT 'draft', created_by CHAR(36) NOT NULL,
 created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6), updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
 UNIQUE KEY uq_ebook_slug(slug), KEY idx_ebook_catalog(status,created_at), CONSTRAINT fk_ebook_creator FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS ebook_purchases (
 id CHAR(36) PRIMARY KEY, ebook_id CHAR(36) NOT NULL, user_id CHAR(36) NOT NULL, billing_order_id CHAR(36) NULL, status ENUM('pending','paid','refunded','cancelled') NOT NULL DEFAULT 'pending', created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6), paid_at DATETIME(6) NULL,
 UNIQUE KEY uq_ebook_purchase(ebook_id,user_id), CONSTRAINT fk_ebook_purchase_ebook FOREIGN KEY(ebook_id) REFERENCES ebooks(id) ON DELETE RESTRICT, CONSTRAINT fk_ebook_purchase_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
INSERT IGNORE INTO schema_migrations(version) VALUES ('004_ebooks');
