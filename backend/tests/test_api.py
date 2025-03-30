import pytest
from httpx import AsyncClient, ASGITransport
from presentations.app import app

@pytest.mark.asyncio
async def test_get_all_links():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
        ) as ac:
        response = await ac.get("/link/list")
        print(response)