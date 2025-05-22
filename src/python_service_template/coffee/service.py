import structlog

from python_service_template.coffee.base import CoffeeClient, CoffeeDrink, CoffeeService


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
