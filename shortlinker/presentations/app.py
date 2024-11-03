import time
from fastapi import FastAPI, Request, Response, status, Path, HTTPException
from pydantic import BaseModel
from services.short_link_service import ShortLinkService
from re import fullmatch
from typing import Callable, Awaitable
from loguru import logger

app = FastAPI(
    title='Сервис генерации коротких ссылок',
    description='простенький тестовый сервис для создания коротких ссылок'
    )
short_link_service = ShortLinkService()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    мидлварь для записи времени выполнения запроса в хедеры
    """
    t0 = time.time()

    response = await call_next(request)

    elapsed_ms = round((time.time() - t0) * 1000, 2)
    response.headers["X-Latency"] = str(elapsed_ms)

    try:
        route_path = request.scope.get("route", {}).path
        logger.debug("{} {} done in {}ms", request.method, route_path, elapsed_ms)
    except Exception:
        logger.exception("exception.raised")

    return response


@app.get("/health")
def hello_world() -> str:
    """
    тестовый эндпоинт
    """
    return "ok"


class PutLink(BaseModel):
    """
    ссылка 
    """
    link: str


@app.put("/link")
async def put_link(long_link: PutLink) -> PutLink:
    """
    метод создания короткой ссылки по длинной ссылке
    """
    if long_link.link[:8] != "https://":
        long_link.link = "https://" + long_link.link 
    if not(fullmatch("https://\w{1,}\.\w{1,}", long_link.link)):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Некорректная ссылка")

    short_link = await short_link_service.put_link(long_link.link)

    return PutLink(link=f'http://localhost:8000/short/{short_link}')


@app.get("/short/{short_link}")
async def get_link(request: Request, short_link: str = Path(...)) -> Response:
    """
    метод переадресации с короткой ссылки на длинную
    """
    long_link = await short_link_service.get_link(short_link, request)

    if long_link is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Упс, мы не нашли эту ссылочку")
    
    return Response(
        content=None, 
        headers={"Location": long_link}, 
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
