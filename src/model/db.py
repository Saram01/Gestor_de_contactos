from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.model.base import Base
import traceback

DATABASE_URL = "postgresql://mamau:postgres@localhost:5432/Contactos"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crear_tablas():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("[ERROR] No se pudo conectar con la base de datos al iniciar.")
        traceback.print_exc()
        raise e