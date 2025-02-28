from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./trivia.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    saga = Column(String, index=True)
    category = Column(String)
    difficulty = Column(String)
    type = Column(String)  # "multiple" o "boolean"
    question = Column(String)
    correct_answer = Column(String)
    incorrect_answers = Column(String)  # Guardamos las respuestas incorrectas separadas por "|"

Base.metadata.create_all(bind=engine)
