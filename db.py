from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///spotify.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db(drop: bool = False) -> None:
    if drop:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)