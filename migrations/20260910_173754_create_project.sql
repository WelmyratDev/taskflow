CREATE TABLE IF NOT EXISTS project(
    id BIGSERIAL PRIMARY KEY,
    account_id BIGINT 
        NOT NULL REFERENCES account(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    timesheet NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(100) NOT NULL DEFAULT 'active'
);