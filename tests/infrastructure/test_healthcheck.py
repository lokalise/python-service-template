import os

import pytest

from python_service_template.infrastructure.healthcheck import HealthIndicator, PrivateHealthcheck, PublicHealthcheck


class MockCoffeeClient:
    def __init__(self, healthy: bool) -> None:
        self._healthy: bool = healthy

    async def healthcheck(self) -> bool:
        return self._healthy


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_healthy,expected_status",
    [
        (True, HealthIndicator.HEALTHY),
        (False, HealthIndicator.UNHEALTHY),
    ],
)
async def test_private_healthcheck_status(client_healthy: bool, expected_status: HealthIndicator) -> None:
    client = MockCoffeeClient(client_healthy)
    healthcheck = PrivateHealthcheck(client)  # type: ignore
    response = await healthcheck.check()
    assert response.heartbeat == expected_status
    assert response.checks["coffee"] == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_healthy,expected_status",
    [
        (True, HealthIndicator.HEALTHY),
        (False, HealthIndicator.UNHEALTHY),
    ],
)
async def test_public_healthcheck_status(client_healthy: bool, expected_status: HealthIndicator) -> None:
    client = MockCoffeeClient(client_healthy)
    healthcheck = PublicHealthcheck(client)  # type: ignore
    response = await healthcheck.check()
    assert response.heartbeat == expected_status


@pytest.mark.asyncio
async def test_private_healthcheck_git_commit_sha():
    os.environ["GIT_COMMIT_SHA"] = "testsha123"
    client = MockCoffeeClient(True)
    healthcheck = PrivateHealthcheck(client)
    response = await healthcheck.check()
    assert response.git_commit_sha == "testsha123"
    del os.environ["GIT_COMMIT_SHA"]


@pytest.mark.asyncio
async def test_public_healthcheck_git_commit_sha():
    os.environ["GIT_COMMIT_SHA"] = "testsha456"
    client = MockCoffeeClient(True)
    healthcheck = PublicHealthcheck(client)
    response = await healthcheck.check()
    assert response.git_commit_sha == "testsha456"
    del os.environ["GIT_COMMIT_SHA"]
