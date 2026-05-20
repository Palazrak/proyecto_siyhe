import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carga variables locales (.env) cuando corres en tu máquina
load_dotenv()

# Obtiene DATABASE_URL desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está configurada")

# Render entrega PostgreSQL como:
# postgresql://...
# SQLAlchemy con psycopg necesita:
# postgresql+psycopg://...
DATABASE_URL = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+psycopg://",
    1
)

# Crear engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Crear sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para modelos
Base = declarative_base()


# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
