import datetime
import functools
from typing import Any

from sqlalchemy import DateTime, String
from sqlalchemy.types import JSON
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


utcnow = functools.partial(datetime.datetime.now, datetime.UTC)


# Setup ORM's base model
class BaseModel(DeclarativeBase):
    # This map tells SQLAlchemy that any Mapped[dict] should use the JSON
    # column type
    type_annotation_map = {
        dict[str, Any]: JSON,
        list[dict[str, Any]]: JSON,
    }


class TimestampMixin(object):
    created_at = mapped_column(
        DateTime,
        nullable=False,
        default=utcnow,
    )
    modified_at = mapped_column(
        DateTime,
        nullable=True
    )


class City(BaseModel):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    title_en: Mapped[str] = mapped_column(String(50))
    title_fa: Mapped[str] = mapped_column(String(50))
    title_ar: Mapped[str] = mapped_column(String(50))
