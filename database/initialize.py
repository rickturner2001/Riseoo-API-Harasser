from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"


# Create engine
engine = create_engine(f'sqlite:///{DATABASE_DIR}/data.sqlite', echo=True)

Base = declarative_base()
Base.metadata.create_all(engine)


# Define models


# Create tables
Base.metadata.create_all(engine)
