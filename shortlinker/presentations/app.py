from fastapi import FastAPI, Response, status, Path, HTTPException
from pydantic import BaseModel
from services.short_link_service import ShortLinkService

app = FastAPI(
    title='Сервис генерации коротких ссылок',
    description='простенький тестовый сервис для создания коротких ссылок'
    )
short_link_service = ShortLinkService()


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
def put_link(long_link: PutLink) -> PutLink:
    """
    метод создания короткой ссылки по длинной ссылке
    """
    short_link = short_link_service.put_link(long_link.link)
    
    return PutLink(link=f'http://localhost:8000/short/{short_link}')


@app.get("/short/{short_link}")
def get_link(short_link: str = Path(...)) -> Response:
    """
    метод переадресации с короткой ссылки на длинную
    """
    long_link = short_link_service.get_link(short_link)
    if long_link is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Упс, мы не нашли эту ссылочку")
    return Response(
        content=None, 
        headers={"Location": long_link}, 
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
