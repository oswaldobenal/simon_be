from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.catalog.roles import Role


class User(BaseModel, table=True):
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    password_hash: str
    salt: str
    role_id: UUID = Field(foreign_key="role.id")
    last_login: datetime | None = None
    recovery_token: str | None = None

    # relashionships
    role: Optional["Role"] = Relationship(back_populates="users")
