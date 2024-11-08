import multiprocessing as mp

from loguru import logger 
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Postgres(BaseModel):
	database: str = "db_main"
	host: str = "localhost"
	port: int = 5432
	username: str = "postgres"
	password: str = "postgresuper"


class Uvicorn(BaseModel):
	host: str = "localhost"
	port: int = 8000
	workers: int = mp.cpu_count() * 2 + 1


class _Settings(BaseSettings):
	pg: Postgres = Postgres()
	uvicorn: Uvicorn = Uvicorn()

	model_config = SettingsConfigDict(env_file=".env", evn_prefix="app_", env_nested_delimiter="__")


settings = _Settings()
logger.info("settings.inited {}", settings.model_dump_json())
