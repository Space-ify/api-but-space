.PHONY: run

run:
	pdm run -- uvicorn api.app:app --host 0.0.0.0 --reload
