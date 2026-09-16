CREATE TABLE IF NOT EXISTS task(
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL
        REFERENCES project(id) ON DELETE CASCADE,
    created_by BIGINT
        REFERENCES account(id) ON DELETE SET NULL,
    assigned_to BIGINT
        REFERENCES account(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    priority VARCHAR(50) NOT NULL DEFAULT 'normal',
    due_date TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);