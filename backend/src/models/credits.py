from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.database.connection import Base

class Credit(Base):
    __tablename__ = "credits"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    credits = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="credits")
