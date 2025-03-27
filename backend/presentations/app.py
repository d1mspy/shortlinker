import time
from fastapi import FastAPI, Request, Response, status, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.short_link_service import ShortLinkService
from typing import Callable, Awaitable
from loguru import logger

app = FastAPI(
    title='Сервис генерации коротких ссылок',
    description='простенький тестовый сервис для создания коротких ссылок'
    )
short_link_service = ShortLinkService()

# разрешаем запросы
app.add_middleware(CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']             
    )

class PutLink(BaseModel):
    """
    ссылка 
    """
    link: str


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    мидлварь для записи времени выполнения запроса в хедеры
    """
    t0 = time.time()

    response = await call_next(request)

    elapsed_ms = round((time.time() - t0) * 1000, 2)
    response.headers["X-Latency"] = str(elapsed_ms)

    route_path = request.scope.get("route")
    if route_path:
        logger.debug("{} {} done in {}ms", request.method, route_path.path, elapsed_ms)
    else:
        logger.debug("{} [UNKNOWN_ROUTE] done in {}ms", request.method, elapsed_ms)

    return response


@app.put("/link")
async def put_link(long_link: PutLink) -> PutLink:
    """
    метод создания короткой ссылки по длинной ссылке
    """
    if long_link.link[:8] != "https://" and long_link.link[:7] != "http://":
        long_link.link = "https://" + long_link.link 
    if long_link.link.count('.') < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Некорректная ссылка {long_link.link}")

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


@app.get("/link/{short_link}/statistics")
async def get_statistics(short_link: str) -> Response:
    """
    метод получения статистики использования короткой ссылки
    """
    stats = await short_link_service.get_statistics(short_link)

    if stats == []:
        return "У этой ссылки еще нет статистики"

    return stats


@app.get("/link/list")
async def get_all_links() -> Response:
    """
    метод получения информации о всех ссылках
    """
    link_data = await short_link_service.get_all_links()
    
    if link_data == []:
        return "ссылок нету :("
    
    return link_data
