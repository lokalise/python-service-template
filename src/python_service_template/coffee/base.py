import abc
import typing as t
from pydantic import (
    BeforeValidator,
    Field,
    HttpUrl,
    RootModel,
    BaseModel,
)


class CoffeeDrink(BaseModel):
    id: int
    title: str
    description: str
    image: HttpUrl
    ingredients: t.Annotated[
        list[str], BeforeValidator(lambda v: v.split(", ") if isinstance(v, str) else v)
    ] = Field(default_factory=list)


class CoffeeDrinks(RootModel[list[CoffeeDrink]]):
    root: list[CoffeeDrink]


class CoffeeClient(abc.ABC):
    @abc.abstractmethod
    async def get_all(self) -> list[CoffeeDrink]:
        """Get all countries"""
        pass

    @abc.abstractmethod
    async def get_hot(self) -> list[CoffeeDrink]:
        """Get all hot drinks"""
        pass

    @abc.abstractmethod
    async def get_iced(self) -> list[CoffeeDrink]:
        """Get all iced drinks"""
        pass


class CoffeeService(abc.ABC):
    @abc.abstractmethod
    async def recommend(self) -> CoffeeDrink | None:
        """Recommend a drink from a list of drinks"""
        pass
