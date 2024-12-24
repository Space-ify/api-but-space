.PHONY: run build up stop remove

run:
	pdm run -- uvicorn src.api.app:app --host 0.0.0.0 --reload

build:
	docker compose build --env-file .env

build-force:
	docker compose build --no-cache --env-file .env

up:
	docker compose up -d

stop:
	docker stop api-but-space

remove:
	docker remove api-but-space
