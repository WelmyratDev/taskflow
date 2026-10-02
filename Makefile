ifneq (,$(wildcard .env))
include .env
export
endif

freeze:
	pip freeze > requirements.txt

pg-login:
	psql -U taskflow_user -d taskflow_db -h localhost -p 5432


uvicorn-logger:
	uvicorn infrastructure.fastapi.main:app --reload --log-config shared/logging/uvicorn.json

uvicorn:
	uvicorn infrastructure.fastapi.main:app --reload

migrate-down:
	psql -h $(POSTGRES_HOST) -p $(POSTGRES_PORT) -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
	-f $(POSTGRES_MIGRATIONS_DIR)/downgrade.sql


migrate-up:
	psql -h $(POSTGRES_HOST) -p $(POSTGRES_PORT) -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
	-f $(POSTGRES_MIGRATIONS_DIR)/upgrade.sql

ps:
	tree -L 3