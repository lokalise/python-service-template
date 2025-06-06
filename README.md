# python-service-template

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Directory Structure](#directory-structure)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Project Lifecycle](#project-lifecycle)
- [Docker](#docker)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [CI/CD](#cicd)
- [License](#license)
- [Contributing](#contributing)

---

## Overview

`python-service-template` is a batteries-included template for building robust, production-ready Python backend services with FastAPI.

It comes with:
- [FastAPI](https://fastapi.tiangolo.com/) for high-performance APIs
- **Domain-Driven Design (DDD) structure** for clear separation of concerns
- Modular, domain-driven structure: `domain`, `infrastructure`, and `api` layers
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

- **Language:** Python 3.13+
- **Web Framework:** FastAPI
- **Async Runtime:** uvicorn, uvloop
- **Config:** pydantic, pydantic-settings
- **Logging:** structlog
- **HTTP Client:** aiohttp
- **Testing:** pytest, pytest-asyncio
- **Linting/Formatting:** ruff, mypy
- **Dependency Management:** [uv](https://github.com/astral-sh/uv)
- **Containerization:** Docker

## Directory Structure

```text
src/
  python_service_template/
    api/
      v1/
    domain/
      coffee/
    infrastructure/
      client/
  tests/
Dockerfile
pyproject.toml
README.md
uv.lock
LICENSE
```

---

## Project Structure

This project is organized according to Domain-Driven Design (DDD) principles, focusing on clear separation of concerns and business-centric architecture. The main layers are:

- **Domain Layer:** Contains the core business logic, including entities, value objects, aggregates, repositories (as interfaces), and domain services. This layer is independent of frameworks and external technologies.
- **Application Layer:** Coordinates domain logic to implement use cases. It orchestrates workflows, handles commands/queries, and interacts with the domain layer, but remains decoupled from infrastructure details.
- **Infrastructure Layer:** Provides technical implementations for things like databases, external APIs, and other integrations. It supplies concrete implementations for repository interfaces and other adapters required by the domain or application layers.
- **Interface Layer (API):** Handles HTTP requests and responses, validation, and serialization. This layer exposes the application's functionality to the outside world, typically via REST endpoints, and interacts with the application layer.

This structure ensures that business rules remain at the core of the project, with other concerns (like frameworks or external services) layered around them. Each layer has clear responsibilities and dependencies flow inward, keeping the domain model isolated and testable.

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

## Project Lifecycle

| Task                | Command                                      |
|---------------------|----------------------------------------------|
| Install deps        | `uv sync`                                    |
| Lint                | `ruff src/ tests/`                           |
| Format              | `ruff format src/ tests/`                    |
| Type check          | `mypy src/ tests/`                           |
| Run tests           | `pytest`                                     |
| Run dev server      | `python src/python_service_template/app.py --reload` |
| Run pre-commit      | `uvx pre-commit run --all-files`             |
| Build Docker image  | `docker buildx build ...`                    |
| Run Docker          | `docker run --env-file .env.default -p 8000:8000 python-service-template` |

---

## Docker

This project includes first-class Docker support for local and production use.

**Build the image:**
```sh
docker buildx build \
   --build-arg GIT_COMMIT_SHA=$(git rev-parse --short HEAD) \
   --tag python-service-template \
   .
```

**Run the container:**
```sh
docker run --env-file .env.default -p 8000:8000 python-service-template
```

- The container uses environment variables from `.env.default` (or your own `.env`).
- The default entrypoint runs the FastAPI app on port 8000.
- For local development, you can mount your code as a volume and override the command if needed.

---

## Configuration

All configuration is managed via environment variables. See `.env.default` for available options:

| Variable            | Description                        | Default         |
|---------------------|------------------------------------|-----------------|
| `HOST`              | Host to bind                       | `127.0.0.1`     |
| `PORT`              | Port to bind                       | `8000`          |
| `LOGGING__LEVEL`    | Logging level (`DEBUG`, `INFO`, etc.) | `INFO`       |
| `LOGGING__FORMAT`   | Logging format (`PLAIN` or `JSON`) | `PLAIN`         |
| `COFFEE_API__HOST`  | Base URL for the Coffee API        | *(none)*        |

---

## API Documentation

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **OpenAPI schema:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

All endpoints are organized under the `api/` layer, with versioning support (e.g., `api/v1/`).

---

## Code Quality

- **Lint:** `ruff check --fix`
- **Format:** `ruff format`
- **Type check:** `mypy`
- **Pre-commit hooks:** `uvx pre-commit run --all-files`

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

## CI/CD

Continuous Integration runs on every PR and push to `main`. See `.github/workflows/ci.yml` for details. The workflow checks lint, type checks, tests, and builds the Docker image.

---

## License

This project is licensed under the [Apache 2.0 License](LICENSE).

---

## Contributing

Contributions are welcome! Please open issues or pull requests.
