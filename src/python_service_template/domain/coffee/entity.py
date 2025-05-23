import typing as t

from pydantic import BaseModel, BeforeValidator, Field, HttpUrl, RootModel


class CoffeeDrink(BaseModel):
    id: int
    title: str
    description: str
    image: HttpUrl
    ingredients: t.Annotated[list[str], BeforeValidator(lambda v: v.split(", ") if isinstance(v, str) else v)] = Field(
        default_factory=list
    )


class CoffeeDrinks(RootModel[list[CoffeeDrink]]):
    root: list[CoffeeDrink]
