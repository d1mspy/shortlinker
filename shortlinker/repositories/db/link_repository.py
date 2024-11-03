from persistend.db.link import Link, LinkUsage
from infrastructure.sqlite.connect import sqlite_connection
from sqlalchemy import insert, select
from fastapi import Request

class LinkRepository:
    def __init__(self) -> None:
        self._sessionmaker = sqlite_connection()

    async def put_link(self, short_link: str, long_link: str) -> None:
        """
        INSERT INTO Link(short_link, long_link) VALUES ({short_link}, {long_link})
        """

        stmp = insert(Link).values({"short_link": short_link, "long_link": long_link})

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()

    async def get_link(self, short_link: str, request: Request) -> str | None:
        """
        SELECT long_link from link WHERE short_link = {short_link} LIMIT 1
        """
        stmp = select(Link.long_link).where(Link.short_link == short_link).limit(1)
        """
        INSERT INTO link_usage(user_ip, user_agent, short_link) VALUES ({user_ip}, {user_agent}, {short_link})
        """
        using = insert(LinkUsage).values({"user_ip": request.client.host, "user_agent": request.headers.get('User-Agent'), "short_link": short_link})

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            await session.execute(using)
            await session.commit()

        row = resp.fetchone()
        if row is None:
            return None
        
        return row[0]
