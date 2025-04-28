import abc
from pydantic import AliasPath, Field, HttpUrl, RootModel, BaseModel


class CoffeeDrink(BaseModel):
    id: int
    title: str
    price: float = Field(ge=0.0)
    description: str
    image: HttpUrl
    ingredients: list[str] = Field(default_factory=list)
    total_sales: int = Field(validation_alias=AliasPath("totalSales"))


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
    async def turnover(self) -> float:
        """Calculate the turnover of a list of drinks"""
        pass

    @abc.abstractmethod
    async def recommend(self) -> CoffeeDrink | None:
        """Recommend a drink from a list of drinks"""
        pass
