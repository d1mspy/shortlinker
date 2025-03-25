from persistend.db.base import Base, WithId, WithCreatedAt, WithUpdatedAt
from sqlalchemy import Column, Text


# таблица link
class Link(Base, WithId, WithCreatedAt, WithUpdatedAt):
    __tablename__ = "link"
    
    short_link = Column(Text, nullable=False, unique=True)
    long_link = Column(Text, nullable=False)


# таблица link_usage
class LinkUsage(Base, WithId, WithCreatedAt, WithUpdatedAt):
    __tablename__ = "link_usage"

    user_ip = Column(Text, nullable=False, unique=False)
    user_agent = Column(Text, nullable=False, unique=False)
    short_link = Column(Text, nullable=False, unique=False)