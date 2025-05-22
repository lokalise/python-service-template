from fastapi import APIRouter
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    # This should be dynamically set in a real implementation
    git_commit_sha: str = Field(default="sha", serialization_alias="gitCommitSha")
    heartbeat: str = "HEALTHY"
    version: str = "1"


class PrivateHealthResponse(HealthResponse):
    checks: dict[str, str]


router = APIRouter(tags=["system"])


async def check_openai() -> str:
    # TODO: Implement actual OpenAI health check
    return "HEALTHY"


async def check_anthropic() -> str:
    # TODO: Implement actual Anthropic health check
    return "HEALTHY"


@router.get("/")
async def public_health() -> HealthResponse:
    """Public health check endpoint."""
    return HealthResponse()


@router.get("/health")
async def private_health() -> PrivateHealthResponse:
    """Private health check endpoint with detailed system checks."""
    checks = {"openai": await check_openai(), "anthropic": await check_anthropic()}
    return PrivateHealthResponse(checks=checks)
