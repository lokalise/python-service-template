import aiohttp
from python_service_template.coffee.base import CoffeeClient, CoffeeDrink, CoffeeDrinks


class AsyncCoffeeClient(CoffeeClient):
    def __init__(self, base_url: str = "https://api.sampleapis.com/coffee/") -> None:
        self.base_url = base_url

    async def get_all(self) -> list[CoffeeDrink]:
        return await self.get_hot() + await self.get_iced()

    async def get_hot(self) -> list[CoffeeDrink]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/hot") as response:
                if response.status == 200:
                    deserialized = await response.json()
                    countries = CoffeeDrinks.model_validate(deserialized)
                    return countries.root
                else:
                    raise Exception(f"Error fetching data: {response.status}")

    async def get_iced(self) -> list[CoffeeDrink]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/iced") as response:
                if response.status == 200:
                    deserialized = await response.json()
                    countries = CoffeeDrinks.model_validate(deserialized)
                    return countries.root
                else:
                    raise Exception(f"Error fetching data: {response.status}")
