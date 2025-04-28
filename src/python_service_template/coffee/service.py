from python_service_template.coffee.base import CoffeeClient, CoffeeDrink, CoffeeService


class SimpleCoffeeService(CoffeeService):
    def __init__(self, client: CoffeeClient) -> None:
        self.client = client
    
    async def turnover(self) -> float:
        drinks = await self.client.get_all()
        return sum(drink.price * drink.total_sales for drink in drinks)

    async def recommend(self) -> CoffeeDrink | None:
        drinks = await self.client.get_hot()
        espresso = next(drink for drink in drinks if drink.title == "Espresso")
        return espresso if espresso else None
