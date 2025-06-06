import typing as t

import aiohttp
import structlog
from pydantic import BaseModel, BeforeValidator, Field, HttpUrl, RootModel

from python_service_template.domain.coffee.entity import CoffeeDrink
from python_service_template.domain.coffee.repository import CoffeeClient, CoffeeClientError


class CoffeeDrinkDTO(BaseModel):
    id: int
    title: str
    description: str
    image: t.Annotated[HttpUrl | None, BeforeValidator(lambda v: v if "https://" in v else None)]
    ingredients: t.Annotated[list[str], BeforeValidator(lambda v: v.split(", ") if isinstance(v, str) else v)] = Field(
        default_factory=list
    )

    def to_domain(self) -> CoffeeDrink:
        return CoffeeDrink(
            id=self.id,
            title=self.title,
            description=self.description,
            image=self.image,
            ingredients=self.ingredients,
        )


class CoffeeDrinksDTO(RootModel[list[CoffeeDrinkDTO]]):
    root: list[CoffeeDrinkDTO]


class AsyncCoffeeClient(CoffeeClient):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.log = structlog.get_logger(__name__).bind(class_name=self.__class__.__name__)

    async def healthcheck(self) -> bool:
        await self.log.adebug("Performing healthcheck")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/hot") as response:
                return response.status == 200

    async def get_all(self) -> list[CoffeeDrink]:
        await self.log.adebug("Fetching all coffee drinks")
        return await self.get_hot() + await self.get_iced()

    async def get_hot(self) -> list[CoffeeDrink]:
        await self.log.adebug("Fetching hot coffee drinks")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/hot") as response:
                if response.status == 200:
                    deserialized = await response.json()
                    try:
                        drinks = CoffeeDrinksDTO.model_validate(deserialized)
                    except Exception as exc:
                        raise CoffeeClientError("Malformed data from /hot endpoint") from exc
                    return [drink.to_domain() for drink in drinks.root]
                else:
                    raise CoffeeClientError(f"Error fetching data: {response.status}")

    async def get_iced(self) -> list[CoffeeDrink]:
        await self.log.adebug("Fetching iced coffee drinks")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/iced") as response:
                if response.status == 200:
                    deserialized = await response.json()
                    try:
                        drinks = CoffeeDrinksDTO.model_validate(deserialized)
                    except Exception as exc:
                        raise CoffeeClientError("Malformed data from /iced endpoint") from exc
                    return [drink.to_domain() for drink in drinks.root]
                else:
                    raise CoffeeClientError(f"Error fetching data: {response.status}")
