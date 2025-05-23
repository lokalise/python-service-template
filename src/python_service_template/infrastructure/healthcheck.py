import enum

from pydantic import BaseModel, Field

from python_service_template.domain.coffee.repository import CoffeeClient


class HealthIndicator(str, enum.Enum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"


class PublicHealthResponse(BaseModel):
    git_commit_sha: str = Field(serialization_alias="gitCommitSha")
    heartbeat: HealthIndicator
    version: str


class PrivateHealthResponse(PublicHealthResponse):
    checks: dict[str, HealthIndicator]


class PrivateHealthcheck:
    def __init__(self, coffee_client: CoffeeClient) -> None:
        self.coffee_client = coffee_client

    async def check(self) -> PrivateHealthResponse:
        if not await self.coffee_client.healthcheck():
            coffee_status = HealthIndicator.UNHEALTHY
        else:
            coffee_status = HealthIndicator.HEALTHY
        checks = {"coffee": coffee_status}
        # More sophisticated checks can be added here
        status = HealthIndicator.HEALTHY if all(checks.values()) else HealthIndicator.UNHEALTHY
        return PrivateHealthResponse(
            git_commit_sha="sha",
            heartbeat=status,
            version="1",
            checks=checks,
        )


class PublicHealthcheck:
    def __init__(self, coffee_client: CoffeeClient) -> None:
        self.coffee_client = coffee_client

    async def check(self) -> PublicHealthResponse:
        if not await self.coffee_client.healthcheck():
            coffee_status = HealthIndicator.UNHEALTHY
        else:
            coffee_status = HealthIndicator.HEALTHY
        # More sophisticated checks can be added here
        status = coffee_status
        return PublicHealthResponse(
            git_commit_sha="sha",
            heartbeat=status,
            version="1",
        )
