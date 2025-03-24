from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, BigInteger, DateTime, Double, MetaData
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class WithId:
	__abstract__ = True

	id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)


class WithCreatedAt:
  __abstract__ = True
  
  created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
  

class WithUpdatedAt:
	__abstract__ = True

	updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
