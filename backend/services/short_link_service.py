from utils.utils_random import random_alfanum
from repositories.db.link_repository import LinkRepository
from fastapi import Request

class ShortLinkService:
    def __init__(self):
        self.link_repository = LinkRepository()

    async def put_link(self, long_link: str) -> str:
        short_link = random_alfanum(10)

        await self.link_repository.put_link(short_link, long_link)

        return short_link
    
    async def get_link(self, short_link: str, request: Request) -> str | None:
        return await self.link_repository.get_link(short_link, request)
    
    async def get_statistics(self, short_link: str) -> list:
        return await self.link_repository.get_statistics(short_link)
    
    async def get_all_links(self) -> list[dict] | None:
        return await self.link_repository.get_all_links()