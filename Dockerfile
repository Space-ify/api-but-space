FROM python:slim

WORKDIR /project
RUN apt-get update && \
    apt-get install -y gcc

WORKDIR /project

RUN python -m pip --no-cache-dir install pdm

ARG SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

COPY src/api /project/api
COPY pyproject.toml pdm.lock .env /project

RUN pdm install --frozen-lockfile --no-editable -vv


EXPOSE 5000

ENTRYPOINT ["pdm", "run", "--", "python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"]
CMD []
