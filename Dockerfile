FROM python:3.10

WORKDIR /project
RUN apt-get update && \
    apt-get install -y gcc ffmpeg libsm6 libxext6 g++

WORKDIR /project

RUN python -m pip --no-cache-dir install pdm

ARG SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True
ARG CLIENT_ID
ARG CLIENT_SECRET
ARG REDIRECT_URI
ARG CODE

ENV CLIENT_ID=${CLIENT_ID}
ENV CLIENT_SECRET=${CLIENT_SECRET}
ENV REDIRECT_URI=${REDIRECT_URI}
ENV CODE=${CODE}

COPY src/api /project/api
COPY textures /project/textures
COPY images /project/images

COPY pyproject.toml pdm.lock /project

RUN pdm install --frozen-lockfile --no-editable -vv

EXPOSE 8000

ENTRYPOINT ["pdm", "run", "--", "python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD []
