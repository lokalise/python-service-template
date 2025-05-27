from pydantic import BaseModel, HttpUrl


class CoffeeDrink(BaseModel):
    id: int
    title: str
    description: str
    image: HttpUrl | None
    ingredients: list[str]
