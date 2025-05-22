from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from python_service_template.coffee.base import CoffeeDrink, CoffeeService
from python_service_template.dependencies import coffee_service

router = APIRouter(
    prefix="/coffee",
    tags=["beverages"],
)


@router.get("/recommend", response_model=CoffeeDrink)
async def get_recommended_coffee(
    service: Annotated[CoffeeService, Depends(coffee_service)],
) -> CoffeeDrink:
    recommendation = await service.recommend()
    if recommendation is None:
        raise HTTPException(status_code=404, detail="No recommendation available.")
    return recommendation
