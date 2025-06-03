import pytest
from aiohttp import web

from python_service_template.domain.coffee.repository import CoffeeClientError
from python_service_template.infrastructure.client.coffee import AsyncCoffeeClient


@pytest.fixture
def coffee_data():
    return [
        {
            "id": 1,
            "title": "Espresso",
            "description": "Strong coffee shot",
            "image": "https://example.com/espresso.jpg",
            "ingredients": ["coffee"],
        },
        {
            "id": 2,
            "title": "Latte",
            "description": "Coffee with milk",
            "image": "https://example.com/latte.jpg",
            "ingredients": "coffee, milk",
        },
    ]


@pytest.fixture
def coffee_app(coffee_data):
    async def hot_handler(request):
        return web.json_response(coffee_data)

    async def iced_handler(request):
        return web.json_response(coffee_data)

    app = web.Application()
    app.router.add_get("/hot", hot_handler)
    app.router.add_get("/iced", iced_handler)
    return app


@pytest.mark.asyncio
async def test_healthcheck(aiohttp_client, coffee_app):
    client = await aiohttp_client(coffee_app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    assert await coffee_client.healthcheck() is True


@pytest.mark.asyncio
async def test_get_hot(aiohttp_client, coffee_app, coffee_data):
    client = await aiohttp_client(coffee_app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    drinks = await coffee_client.get_hot()
    assert len(drinks) == len(coffee_data)
    assert drinks[0].title == coffee_data[0]["title"]


@pytest.mark.asyncio
async def test_get_iced(aiohttp_client, coffee_app, coffee_data):
    client = await aiohttp_client(coffee_app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    drinks = await coffee_client.get_iced()
    assert len(drinks) == len(coffee_data)
    assert drinks[1].title == coffee_data[1]["title"]


@pytest.mark.asyncio
async def test_get_all(aiohttp_client, coffee_app, coffee_data):
    client = await aiohttp_client(coffee_app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    drinks = await coffee_client.get_all()
    # get_all returns hot + iced, so double
    assert len(drinks) == 2 * len(coffee_data)


@pytest.mark.asyncio
async def test_get_hot_empty(aiohttp_client):
    async def hot_handler(request):
        return web.json_response([])

    async def iced_handler(request):
        return web.json_response([])

    app = web.Application()
    app.router.add_get("/hot", hot_handler)
    app.router.add_get("/iced", iced_handler)
    client = await aiohttp_client(app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    drinks = await coffee_client.get_hot()
    assert drinks == []


@pytest.mark.asyncio
async def test_get_hot_404(aiohttp_client):
    async def iced_handler(request):
        return web.json_response([])

    app = web.Application()
    app.router.add_get("/iced", iced_handler)
    client = await aiohttp_client(app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    with pytest.raises(CoffeeClientError):
        await coffee_client.get_hot()


@pytest.mark.asyncio
async def test_get_hot_malformed(aiohttp_client):
    async def hot_handler(request):
        return web.json_response({"not": "a list"})

    async def iced_handler(request):
        return web.json_response([])

    app = web.Application()
    app.router.add_get("/hot", hot_handler)
    app.router.add_get("/iced", iced_handler)
    client = await aiohttp_client(app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    with pytest.raises(CoffeeClientError):
        await coffee_client.get_hot()


@pytest.mark.asyncio
async def test_get_iced_404(aiohttp_client):
    async def hot_handler(request):
        return web.json_response([])

    app = web.Application()
    app.router.add_get("/hot", hot_handler)
    client = await aiohttp_client(app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    with pytest.raises(CoffeeClientError):
        await coffee_client.get_iced()


@pytest.mark.asyncio
async def test_get_iced_malformed(aiohttp_client):
    async def hot_handler(request):
        return web.json_response([])

    async def iced_handler(request):
        return web.json_response({"not": "a list"})

    app = web.Application()
    app.router.add_get("/hot", hot_handler)
    app.router.add_get("/iced", iced_handler)
    client = await aiohttp_client(app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    with pytest.raises(CoffeeClientError):
        await coffee_client.get_iced()


@pytest.mark.asyncio
async def test_get_all_one_fails(aiohttp_client):
    async def hot_handler(request):
        return web.json_response([])

    async def iced_handler(request):
        raise web.HTTPInternalServerError()

    app = web.Application()
    app.router.add_get("/hot", hot_handler)
    app.router.add_get("/iced", iced_handler)
    client = await aiohttp_client(app)
    coffee_client = AsyncCoffeeClient(base_url=str(client.make_url("")))
    with pytest.raises(CoffeeClientError):
        await coffee_client.get_all()
