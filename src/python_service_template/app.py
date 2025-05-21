import asyncio
import sys
import structlog
import uvicorn
import uvloop
import logging
import typing as t
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from python_service_template.api.coffee import router as countries_router
from python_service_template.api.health import router as health_router
from python_service_template.dependencies import settings
from python_service_template.settings import LoggingConfig
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status


# Configure uvloop as the event loop policy
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

log = structlog.get_logger(__file__)
app = FastAPI(
    root_path="/api/v1",
    title="Python Service Template",
    description="Batteries-included starter template for Python backend services",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(countries_router)
app.include_router(health_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log.error("Unhandled exception", stack_info=True, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


def configure_logging(config: LoggingConfig) -> dict[str, t.Any]:
    log_level = logging._nameToLevel.get(config.level)
    if config.format == "JSON":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()
    
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    structlog.configure(
        processors=processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        stream=sys.stderr,
    )

    # Logging configuration for uvicorn which uses the standard logging module
    # The main goal is to render the logs the same way as structlog does
    # Source: https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
    std_logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structlog": {
                "()": "structlog.stdlib.ProcessorFormatter",
                "foreign_pre_chain": processors,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    renderer,
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
            "uvicorn": {"handlers": ["structlog"], "level": logging.getLevelName(log_level), "propagate": False},
            "uvicorn.error": {"level": logging.getLevelName(log_level)},
            "uvicorn.access": {"handlers": ["structlog"], "level": logging.getLevelName(log_level), "propagate": False},
        },
    }
    return std_logging_config


if __name__ == "__main__":
    app_settings = settings()
    std_logging_config = configure_logging(app_settings.logging)

    uvicorn.run(
        app,
        host=app_settings.host,
        port=app_settings.port,
        log_config=std_logging_config,
        access_log=True,
        reload=False,
    )
