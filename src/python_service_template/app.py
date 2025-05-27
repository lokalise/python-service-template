import logging
import sys
import typing as t
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from python_service_template.api.health import router as health_router
from python_service_template.api.v1.coffee import router as coffee_router
from python_service_template.dependencies import settings
from python_service_template.settings import LoggingConfig

app = FastAPI(
    root_path="/api/v1",
    title="Python Service Template",
    description="Batteries-included starter template for Python backend services",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(coffee_router)
app.include_router(health_router)


log = structlog.get_logger("exception")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log.error("Unhandled exception", stack_info=True, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting application")
    yield
    log.info("Shutting down application")


def configure_structlog(config: LoggingConfig) -> None:
    log_level = logging._nameToLevel.get(config.level)

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer() if config.format == "JSON" else structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        stream=sys.stderr,
    )


def create_std_logging_config(config: LoggingConfig) -> dict[str, t.Any]:
    """
    Logging configuration for uvicorn which uses the standard logging module
    The main goal is to render the logs the same way as structlog does
    Source: https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structlog": {
                "()": "structlog.stdlib.ProcessorFormatter",
                "foreign_pre_chain": [
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.stdlib.add_log_level,
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.format_exc_info,
                ],
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.processors.JSONRenderer() if config.format == "JSON" else structlog.dev.ConsoleRenderer(),
                ],
            },
        },
        "handlers": {
            "structlog": {
                "formatter": "structlog",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["structlog"],
                "level": config.level.value,
                "propagate": False,
            },
            "uvicorn.error": {"level": config.level.value},
            "uvicorn.access": {
                "handlers": ["structlog"],
                "level": config.level.value,
                "propagate": False,
            },
        },
    }


if __name__ == "__main__":
    import argparse
    import asyncio

    import uvicorn
    import uvloop

    parser = argparse.ArgumentParser(description="Run the FastAPI service.")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development.",
    )
    args = parser.parse_args()

    app_settings = settings()
    configure_structlog(app_settings.logging)

    # Configure uvloop as the event loop policy
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    uvicorn.run(
        f"{__name__}:app",
        host=app_settings.host,
        port=app_settings.port,
        log_config=create_std_logging_config(app_settings.logging),
        access_log=True,
        reload=args.reload,
    )
