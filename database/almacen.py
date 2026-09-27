from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from core.config import settings

UBICACION_ALMACEN = settings.DATABASE_URL

motor = create_engine(UBICACION_ALMACEN)
llaves = sessionmaker(bind=motor)


class miclaseBase(DeclarativeBase):
    pass


def abrir_puerta():
    
    try:
        db = llaves()
        yield db
    finally:
        db.close()