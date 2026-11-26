from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    source_type = Column(String(50), nullable=False)

    source_url = Column(String(500), nullable=True)

    local_path = Column(String(500), nullable=True)

    status = Column(String(50), default="uploaded")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
