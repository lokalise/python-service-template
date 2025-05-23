import abc

import structlog

from python_service_template.domain.coffee.entity import CoffeeDrink
from python_service_template.domain.coffee.repository import CoffeeClient


class CoffeeService(abc.ABC):
    @abc.abstractmethod
    async def recommend(self) -> CoffeeDrink | None:
        """Recommend a drink from a list of drinks"""
        pass


class SimpleCoffeeService(CoffeeService):
    def __init__(self, client: CoffeeClient) -> None:
        self.client = client
        self.log = structlog.get_logger(__name__).bind(class_name=self.__class__.__name__)

    async def recommend(self) -> CoffeeDrink | None:
        await self.log.adebug("Recommending a drink")
        drinks = await self.client.get_hot()
        espresso = [drink for drink in drinks if drink.title == "Espresso"]
        if espresso:
            await self.log.adebug("Recommending espresso")
            return espresso[0]
        await self.log.awarn("Espresso not found")
        return None
