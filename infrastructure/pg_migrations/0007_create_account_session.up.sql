CREATE TABLE IF NOT EXISTS account_session(
    id BIGSERIAL PRIMARY KEY,
    account_id BIGINT NOT NULL
        REFERENCES account(id)
        ON DELETE CASCADE,
    session_token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_activity TIMESTAMPTZ NULL,
    ip_address INET NULL,
    user_agent TEXT NULL
);