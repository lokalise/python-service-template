import typing as t
from functools import lru_cache

from fastapi import Depends

from python_service_template.coffee.base import CoffeeClient, CoffeeService
from python_service_template.coffee.client import AsyncCoffeeClient
from python_service_template.coffee.service import SimpleCoffeeService
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
