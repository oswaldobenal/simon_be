from typing import Generator
from urllib.parse import urlparse, urlunparse

from sqlmodel import Session, SQLModel, create_engine


from app.core.config import settings

# Configuración para desarrollo
engine = create_engine(
    url=str(settings.SQLALCHEMY_DATABASE_URI),
    echo=settings.DEBUG,  # Mostrar queries en consola solo en desarrollo
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

# Configuración para testing
parsed_url = urlparse(str(settings.SQLALCHEMY_DATABASE_URI))
test_url = parsed_url._replace(path=f"/{settings.POSTGRES_TEST_DB}")
test_url_str = urlunparse(test_url)

test_engine = create_engine(
    url=test_url_str,
    echo=False,
    pool_size=5,
    pool_pre_ping=True,
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    # Importaciones de modelos
    from app.models.catalog.roles import Role
    from app.models.core.users import User

    # Crear tablas base primero
    Role.metadata.create_all(engine)
    User.metadata.create_all(engine)
    # SQLModel.metadata.create_all(engine)


def get_test_db():
    SQLModel.metadata.create_all(test_engine)
    return Session(test_engine)
