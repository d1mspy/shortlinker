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
        assert response.status_code == 200
        
        data = response.json()
        assert data == "ссылок нету :("


@pytest.mark.asyncio(loop_scope="session")
async def test_put_link():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        default_input = {"link": "test.com"}
        full_input = {"link": "https://test.com"}
        err_input = {"link": "https://incorrect_link"}
        
        default_response = await ac.put("/link", json=default_input)
        full_response = await ac.put("/link", json=full_input)
        err_response = await ac.put("/link", json=err_input)

        assert default_response.status_code == 200
        assert full_response.status_code == 200
        assert err_response.status_code == 422
        
        default_data = default_response.json()
        full_data = full_response.json()
        err_data = err_response.json()
        
        assert "link" in default_data
        assert "link" in full_data
        
        assert default_data["link"].startswith("http://localhost/api/short/")
        assert full_data["link"].startswith("http://localhost/api/short/")
        
        assert err_data["detail"] == "Некорректная ссылка https://incorrect_link"


@pytest.mark.asyncio
async def test_get_link():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        
        all_links = await ac.get("link/list")
        assert all_links.status_code == 200
        
        all_links_data = all_links.json()
        assert isinstance(all_links_data, list)
        assert len(all_links_data) == 2
        
        assert all_links_data[0]["long_link"] == "https://test.com"
        assert all_links_data[1]["long_link"] == "https://test.com"
        
        short_link = all_links_data[0]["short_link"]
        short_link_err = "non_existent_link"
        
        response = await ac.get(f"/short/{short_link}")
        response_err = await ac.get(f"/short/{short_link_err}")
        err_data = response_err.json()
        
        assert response.status_code == 301
        assert response_err.status_code == 404
        assert err_data["detail"] == "Упс, мы не нашли эту ссылочку"

@pytest.mark.asyncio
async def test_get_statistics():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        all_links = await ac.get("link/list")
        assert all_links.status_code == 200
        
        all_links_data = all_links.json()
        assert isinstance(all_links_data, list)
        assert len(all_links_data) == 2
        
        assert all_links_data[0]["long_link"] == "https://test.com"
        assert all_links_data[1]["long_link"] == "https://test.com"
        
        short_link_1 = all_links_data[0]["short_link"]
        short_link_2 = all_links_data[1]["short_link"]
        
        response_1 = await ac.get(f"/link/{short_link_1}/statistics")
        response_2 = await ac.get(f"/link/{short_link_2}/statistics")
        
        assert response_1.status_code == 200
        assert response_2.status_code == 200
        
        data_2 = response_2.json()
        assert data_2 == "У этой ссылки еще нет статистики"
