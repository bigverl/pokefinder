from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from litestar.plugins.sqlalchemy import UUIDBase
from typing import Optional

class TM(UUIDBase):
    __tablename__ = "tm"
    name: Mapped[str] = mapped_column(unique=True)
    machine_id: Mapped[Optional[str]] = mapped_column(unique=True)

# -- TM
# CREATE TABLE TM (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE,
#     machine_id TEXT  -- NULL if not a TM/HM
# );