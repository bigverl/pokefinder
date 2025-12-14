from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import UUIDBase
from advanced_alchemy.types import GUID
from uuid import UUID, uuid4
from typing import Optional


class TM(UUIDBase):
    __tablename__ = "tm"
    id: Mapped[UUID] = mapped_column(GUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(unique=True)
    machine_id: Mapped[Optional[str]] = mapped_column(unique=True)

# -- TM
# CREATE TABLE TM (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE,
#     machine_id TEXT  -- NULL if not a TM/HM
# );