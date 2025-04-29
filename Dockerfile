# Heavily inspired by: https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile
ARG PYTHON_VERSION=3.10
ARG DEBIAN_VERSION=bookworm
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-${DEBIAN_VERSION}-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:${PYTHON_VERSION}-slim-${DEBIAN_VERSION}

COPY --from=builder --chown=app:app /app /app
ARG PORT=8000
ENV PATH="/app/.venv/bin:$PATH" \
    PORT=${PORT} \
    PYTHONUNBUFFERED=1

EXPOSE ${PORT}
SHELL ["/bin/bash", "-c"]
CMD fastapi run --port ${PORT} /app/src/python_service_template/app.py
