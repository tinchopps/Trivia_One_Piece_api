from database import Base, engine
from models import Score

# Crear todas las tablas
Base.metadata.create_all(bind=engine)