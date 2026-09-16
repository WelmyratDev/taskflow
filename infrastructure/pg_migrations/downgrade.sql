\set ON_ERROR_STOP on
BEGIN;

\ir 0001_create_account.down.sql
\ir 0002_create_permission.down.sql
\ir 0003_create_account_permission.down.sql
\ir 0004_create_project.down.sql
\ir 0005_create_task.down.sql
\ir 0006_create_timesheet.down.sql

COMMIT;