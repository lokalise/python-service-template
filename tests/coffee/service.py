from unittest.mock import AsyncMock, MagicMock

import pytest

from python_service_template.coffee.base import CoffeeClient, CoffeeDrink
from python_service_template.coffee.service import SimpleCoffeeService


@pytest.mark.asyncio
async def test_recommend_returns_espresso():
    mock_client = MagicMock(spec=CoffeeClient)
    espresso = CoffeeDrink(title="Espresso", ingredients=["coffee"])
    mock_client.get_hot = AsyncMock(return_value=[espresso])
    service = SimpleCoffeeService(mock_client)
    result = await service.recommend()
    assert result == espresso


@pytest.mark.asyncio
async def test_recommend_returns_none_if_no_espresso():
    mock_client = MagicMock(spec=CoffeeClient)
    mock_client.get_hot = AsyncMock(return_value=[CoffeeDrink(title="Latte", ingredients=["coffee", "milk"])])
    service = SimpleCoffeeService(mock_client)
    result = await service.recommend()
    assert result is None
