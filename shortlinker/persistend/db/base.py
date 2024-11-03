from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text
import uuid

Base = declarative_base()


def uuid4_as_str() -> str:
    return str(uuid.uuid4())


class WithId:
	__abstract__ = True

	id = Column(Text, default=uuid4_as_str, primary_key=True)