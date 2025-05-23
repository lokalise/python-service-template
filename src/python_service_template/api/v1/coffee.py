import typing as t

from fastapi import APIRouter, Depends, HTTPException

from python_service_template.dependencies import coffee_service
from python_service_template.domain.coffee.entity import CoffeeDrink
from python_service_template.domain.coffee.service import CoffeeService

router = APIRouter(
    prefix="/coffee",
    tags=["beverages"],
)


@router.get("/recommend", response_model=CoffeeDrink)
async def get_recommended_coffee(
    service: t.Annotated[CoffeeService, Depends(coffee_service)],
) -> CoffeeDrink:
    recommendation = await service.recommend()
    if recommendation is None:
        raise HTTPException(status_code=404, detail="No recommendation available.")
    return recommendation
