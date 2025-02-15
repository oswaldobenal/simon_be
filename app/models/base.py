from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Index, func
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": func.now()},
    )
    is_deleted: bool = Field(default=False)
    deleted_at: datetime | None = None

    # __table_args__ = (
    #     Index("ix_active_records", "is_deleted"),  # Índice para registros activos
    # )
