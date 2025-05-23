import abc

from python_service_template.domain.coffee.entity import CoffeeDrink


class CoffeeClient(abc.ABC):
    @abc.abstractmethod
    async def healthcheck(self) -> bool:
        """Check if the client is healthy"""
        pass

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
