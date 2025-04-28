from typing import Annotated

from fastapi import Depends
from python_service_template.coffee.client import AsyncCoffeeClient
from python_service_template.coffee.service import SimpleCoffeeService
from python_service_template.coffee.base import CoffeeClient, CoffeeService


def coffee_client() -> CoffeeClient:
    return AsyncCoffeeClient()


def coffee_service(
    client: Annotated[CoffeeClient, Depends(coffee_client)],
) -> CoffeeService:
    return SimpleCoffeeService(client=client)
