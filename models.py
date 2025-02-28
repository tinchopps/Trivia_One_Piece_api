from sqlalchemy import Column, Integer, String
from database import Base

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    points = Column(Integer, default=0)
