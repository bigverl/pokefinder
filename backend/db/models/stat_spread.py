from __future__ import annotations

from sqlalchemy import String, Column, Table, Integer
from litestar.plugins.sqlalchemy import UUIDBase

stat_spread = Table(
    "stat_spread",
    UUIDBase.metadata,
    Column("stat_name", String, primary_key=True),
    Column("percentile_20", Integer),
    Column("percentile_40", Integer),
    Column("percentile_60", Integer),
    Column("percentile_80", Integer),
    Column("percentile_100", Integer),
    Column("median", Integer)
)

# CREATE TABLE stat_quintiles (
#     stat_name TEXT PRIMARY KEY,
#     percentile_20 INTEGER NOT NULL,  -- D-tier threshold
#     percentile_40 INTEGER NOT NULL,  -- C-tier threshold
#     percentile_60 INTEGER NOT NULL,  -- B-tier threshold
#     percentile_80 INTEGER NOT NULL,  -- A-tier threshold
#     percentile_100 INTEGER NOT NULL, -- S-tier / max
#     median INTEGER NOT NULL
# );