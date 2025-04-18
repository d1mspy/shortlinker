from persistend.db.link import Link, LinkUsage
from infrastructure.postgres.connect import pg_connection
from sqlalchemy import insert, select
from fastapi import Request

# взаимодействие с базой данных
class LinkRepository:

    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

    
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
        INSERT INTO link_usage(user_ip, user_agent, short_link) VALUES ({user_ip}, {user_agent}, {short_link})
        """
        using = insert(LinkUsage).values({
            "user_ip": request.client.host, 
            "user_agent": request.headers.get("User-Agent"), 
            "short_link": short_link
        })
        
        """
        SELECT long_link from link WHERE short_link = {short_link} LIMIT 1
        """
        stmp = select(Link.long_link).where(Link.short_link == short_link).limit(1)
        

        async with self._sessionmaker() as session:
            await session.execute(using)
            await session.commit()

            resp = await session.execute(stmp)
            
        row = resp.fetchone()
        if row is None:
            return None
        
        return row[0]


    async def get_statistics(self, short_link: str) -> list:
        """
        SELECT * from link_usage WHERE short_link = {short_link}
        """
        stmp = select(LinkUsage.id, LinkUsage.created_at, LinkUsage.updated_at, LinkUsage.user_ip, LinkUsage.user_agent).where(LinkUsage.short_link == short_link)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)

        row = list(resp.fetchall())
        keys = ["id", "created_at", "updated_at", "user_ip", "user_agent"]

        stats = [dict(zip(keys, item)) for item in row]
   
        return stats


    async def get_all_links(self) -> list[dict]:
        """
        SELECT * FROM link ORDER BY link.long_link
        """
        stmp = select(Link.id, Link.created_at, Link.updated_at, Link.long_link, Link.short_link).order_by(Link.long_link)
        
        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
        
        row = list(resp.fetchall())
        keys = ["id", "created_at", "updated_at", "long_link", "short_link"]
        
        links_data = [dict(zip(keys, item)) for item in row]
        
        return links_data
