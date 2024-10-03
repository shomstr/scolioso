# mypy: ignore-errors

# Imports
from __future__ import annotations


from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)

    def to_dict(self, ignored_columns: list | None = None, relationships: bool = False) -> dict:
        if ignored_columns is None:
            ignored_columns = []
        result: dict = {}

        for c in self.__table__.columns:
            if c.name in ignored_columns:
                continue

            result[c.name] = getattr(self, c.name)
        if relationships:
            for relationship_name in self.__mapper__.relationships.keys():
                try:
                    relationship_value = getattr(self, relationship_name)
                except Exception:
                    continue

                if isinstance(relationship_value, list):
                    result[relationship_name] = [item.to_dict() for item in relationship_value]
                else:
                    result[relationship_name] = relationship_value.to_dict() if relationship_value is not None else None
        return result
