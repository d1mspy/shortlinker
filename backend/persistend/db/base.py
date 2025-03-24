from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, BigInteger, DateTime, Double, MetaData
import uuid
from datetime import datetime

Base = declarative_base()


def uuid4_as_str() -> str:
  return str(uuid.uuid4())


class WithId:
	__abstract__ = True

	id = Column(Text, default=uuid4_as_str, primary_key=True)


class WithCreatedAt:
  __abstract__ = True
  
  created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
  

class WithUpdatedAt:
	__abstract__ = True

	updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
