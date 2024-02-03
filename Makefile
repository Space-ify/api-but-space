.PHONY: run

run:
	pdm run -- uvicorn src.api.app:app --host 0.0.0.0 --reload
