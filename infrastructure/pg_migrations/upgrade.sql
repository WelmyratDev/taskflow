\set ON_ERROR_STOP on
BEGIN;

\ir 0001_create_account.up.sql
\ir 0002_create_permission.up.sql
\ir 0003_create_account_permission.up.sql
\ir 0004_create_project.up.sql
\ir 0005_create_task.up.sql
\ir 0006_create_timesheet.up.sql

COMMIT;
