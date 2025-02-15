from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.core.users import User


class Role(BaseModel, table=True):
    name: str = Field(index=True, unique=True)
    users: list["User"] = Relationship(back_populates="role")


# Similar para Status, Currency, PaymentMethod, etc...
