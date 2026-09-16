CREATE TABLE IF NOT EXISTS account_permission(
    account_id BIGINT NOT NULL
        REFERENCES account(id) ON DELETE CASCADE,
    permission_id BIGINT NOT NULL
        REFERENCES permission(id) ON DELETE CASCADE,
    PRIMARY KEY (account_id, permission_id)
);