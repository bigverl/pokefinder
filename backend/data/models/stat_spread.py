from __future__ import annotations

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from litestar.plugins.sqlalchemy import UUIDBase


class StatSpread(UUIDBase):
    __tablename__ = "stat_spread"
    stat_name: Mapped[str] = mapped_column(String, primary_key=True)
    percentile_20: Mapped[int] = mapped_column(Integer)
    percentile_40: Mapped[int] = mapped_column(Integer)
    percentile_60: Mapped[int] = mapped_column(Integer)
    percentile_80: Mapped[int] = mapped_column(Integer)
    percentile_100: Mapped[int] = mapped_column(Integer)
    median: Mapped[int] = mapped_column(Integer)

# CREATE TABLE stat_quintiles (
#     stat_name TEXT PRIMARY KEY,
#     percentile_20 INTEGER NOT NULL,  -- D-tier threshold
#     percentile_40 INTEGER NOT NULL,  -- C-tier threshold
#     percentile_60 INTEGER NOT NULL,  -- B-tier threshold
#     percentile_80 INTEGER NOT NULL,  -- A-tier threshold
#     percentile_100 INTEGER NOT NULL, -- S-tier / max
#     median INTEGER NOT NULL
# );