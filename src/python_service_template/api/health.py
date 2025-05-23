import typing as t

from fastapi import APIRouter, Depends

from python_service_template.dependencies import (
    private_healthcheck,
    public_healthcheck,
)
from python_service_template.infrastructure.healthcheck import (
    PrivateHealthcheck,
    PrivateHealthResponse,
    PublicHealthcheck,
    PublicHealthResponse,
)

router = APIRouter(tags=["system"])


@router.get("/")
async def public_health(
    public_healthcheck: t.Annotated[PublicHealthcheck, Depends(public_healthcheck)],
) -> PublicHealthResponse:
    """Public health check endpoint."""
    return await public_healthcheck.check()


@router.get("/health")
async def private_health(
    private_healthcheck: t.Annotated[PrivateHealthcheck, Depends(private_healthcheck)],
) -> PrivateHealthResponse:
    """Private health check endpoint with detailed system checks."""
    return await private_healthcheck.check()
