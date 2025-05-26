from pydantic import BaseModel, HttpUrl


class CoffeeDrink(BaseModel):
    id: int
    title: str
    description: str
    image: HttpUrl
    ingredients: list[str]
