FROM python:3.10

WORKDIR /project
RUN apt-get update && \
    apt-get install -y gcc ffmpeg libsm6 libxext6 g++

WORKDIR /project

RUN python -m pip --no-cache-dir install pdm

ARG SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True

COPY src/api /project/api
COPY textures /project/textures
COPY images /project/images

COPY pyproject.toml pdm.lock .env /project

RUN pdm install --frozen-lockfile --no-editable -vv

EXPOSE 8000

ENTRYPOINT ["pdm", "run", "--", "python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD []
