# python-service-template

## Overview

`python-service-template` is a batteries-included template for building robust, production-ready Python backend services with FastAPI.

It comes with:
- [FastAPI](https://fastapi.tiangolo.com/) for high-performance APIs
- Modular, domain-driven structure
- [Global error handler](src/python_service_template/app.py#L31) for consistent error responses
- Structured logging with [structlog](https://www.structlog.org/)
- Type-safe config management with [pydantic-settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
- Dependency injection via FastAPI's dependency system
- Async HTTP client ([aiohttp](https://docs.aiohttp.org/))
- Example integration with an external API (Coffee API)
- Health check endpoints (public and private)
- Docker support for local and production use
- Pre-commit hooks for linting, formatting, type checking and unit testing
- CI workflow for tests and code quality

---

## Tech Stack

- **Language:** Python 3.10+
- **Web Framework:** FastAPI
- **Async Runtime:** uvicorn, uvloop
- **Config:** pydantic, pydantic-settings
- **Logging:** structlog
- **HTTP Client:** aiohttp
- **Testing:** pytest, pytest-asyncio
- **Linting/Formatting:** ruff, mypy
- **Dependency Management:** [uv](https://github.com/astral-sh/uv)
- **Containerization:** Docker

---

## Getting Started

1. **Install dependencies:**
   ```sh
   uv sync
   ```
2. **Copy environment config:**
   ```sh
   cp .env.default .env
   ```
3. **Run the application:**
   ```sh
   python src/python_service_template/app.py --reload
   ```

### Running with Docker

```sh
docker buildx build -t python-service-template .
docker run --env-file .env -p 8000:8000 python-service-template
```

---

## Configuration

All configuration is managed via environment variables. See `.env.default` for available options:

- `HOST` - Host to bind (default: `127.0.0.1`)
- `PORT` - Port to bind (default: `8000`)
- `LOGGING__LEVEL` - Logging level (`DEBUG`, `INFO`, etc.)
- `LOGGING__FORMAT` - Logging format (`PLAIN` or `JSON`)
- `COFFEE_API__HOST` - Base URL for the Coffee API

---

## Project Structure

The codebase follows a modular, domain-driven structure. Main components include:
- API route definitions
- Domain modules (e.g., coffee)
- Dependency injection setup
- Configuration models
- Tests and CI/CD configuration

---

## Endpoints

This template uses FastAPI, which provides automatic and interactive API documentation at `/docs` when the service is running.

---

## Pre-commit Hooks

This template comes with a pre-configured set of pre-commit hooks for linting, formatting, type checking, and more. To enable them, run:

```sh
uvx pre-commit run --all-files
```

---

## Testing

Tests are located in the `tests/` directory and use [pytest](https://docs.pytest.org/) and [pytest-asyncio](https://pytest-asyncio.readthedocs.io/).

```sh
pytest
```

---

## Development

To run the FastAPI server in development mode with auto-reload:

```sh
python src/python_service_template/app.py --reload
```

---

## Troubleshooting

- If you encounter port conflicts, ensure no other process is using the configured port (default: 8000).
- For Docker issues, rebuild the image after dependency or config changes.

---

## License

This project is licensed under the [Apache 2.0 License](LICENSE).

---

## Contributing

Contributions are welcome! Please open issues or pull requests.
