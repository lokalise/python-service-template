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

WORKDIR /app
COPY --from=builder /app /app

# Create non-root user
RUN groupadd -r app && \
    useradd -r -g app app && \
    chown -R app:app /app

ARG PORT=8000
ENV PATH="/app/.venv/bin:$PATH" \
    PORT=${PORT} \
    PYTHONUNBUFFERED=1

EXPOSE ${PORT}
USER app
SHELL ["/bin/bash", "-c"]

# Add healthcheck using Python's http.client
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python3 -c "import http.client; conn = http.client.HTTPConnection('localhost', ${PORT}); conn.request('GET', '/api/v1/health'); response = conn.getresponse(); exit(0 if response.status == 200 else 1)"

CMD fastapi run --port ${PORT} /app/src/python_service_template/app.py
