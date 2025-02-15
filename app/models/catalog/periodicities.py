# from typing import TYPE_CHECKING

# from sqlmodel import Field, Relationship, SQLModel

# from app.models.base import BaseModel

# if TYPE_CHECKING:
#     from app.models.core.users import User


# class Periodicity(BaseModel, table=True):
#     name: str = Field(index=True, unique=True)
#     users: list["Plan"] = Relationship(back_populates="periodicity")
