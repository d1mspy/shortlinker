from persistend.db.base import Base, WithId
from sqlalchemy import Column, Text

"""
create table link(
    id text primary key
    short_link text not null unique
    long_link text not null
);
"""

class Link(Base, WithId):
    __tablename__ = "link"
    
    short_link = Column(Text, nullable=False, unique=True)
    long_link = Column(Text, nullable=False)