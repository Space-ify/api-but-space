.PHONY: run build up stop remove

run:
	pdm run -- uvicorn src.api.app:app --host 0.0.0.0 --reload

build:
	docker compose build --no-cache

up:
	docker compose up -d

stop:
	docker stop api-but-space

remove:
	docker remove api-but-space
