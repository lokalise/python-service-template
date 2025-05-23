import typing as t
from functools import lru_cache

from fastapi import Depends

from python_service_template.domain.coffee.repository import CoffeeClient
from python_service_template.domain.coffee.service import CoffeeService, SimpleCoffeeService
from python_service_template.infrastructure.client.coffee import AsyncCoffeeClient
from python_service_template.infrastructure.healthcheck import PrivateHealthcheck, PublicHealthcheck
from python_service_template.settings import Settings


@lru_cache
def settings() -> Settings:
    return Settings()


def coffee_client(settings: t.Annotated[Settings, Depends(settings)]) -> CoffeeClient:
    return AsyncCoffeeClient(base_url=settings.coffee_api.host)


def coffee_service(
    client: t.Annotated[CoffeeClient, Depends(coffee_client)],
) -> CoffeeService:
    return SimpleCoffeeService(client=client)


def private_healthcheck(coffee_client: t.Annotated[CoffeeClient, Depends(coffee_client)]) -> PrivateHealthcheck:
    return PrivateHealthcheck(coffee_client)


def public_healthcheck(coffee_client: t.Annotated[CoffeeClient, Depends(coffee_client)]) -> PublicHealthcheck:
    return PublicHealthcheck(coffee_client)
