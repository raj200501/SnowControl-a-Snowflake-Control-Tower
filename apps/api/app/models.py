from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    size: Mapped[str] = mapped_column(String)
    credit_per_hour: Mapped[float] = mapped_column(Float)


class WarehouseMetering(Base):
    __tablename__ = "warehouse_metering"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    warehouse_name: Mapped[str] = mapped_column(String)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    credits_used: Mapped[float] = mapped_column(Float)


class QueryHistory(Base):
    __tablename__ = "query_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    query_id: Mapped[str] = mapped_column(String)
    warehouse_name: Mapped[str] = mapped_column(String)
    user_name: Mapped[str] = mapped_column(String)
    role_name: Mapped[str] = mapped_column(String)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    total_elapsed_ms: Mapped[int] = mapped_column(Integer)
    bytes_scanned: Mapped[int] = mapped_column(Integer)
    rows_produced: Mapped[int] = mapped_column(Integer)
    query_text: Mapped[str] = mapped_column(Text)


class RoleGrant(Base):
    __tablename__ = "role_grants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String)
    grantee_name: Mapped[str] = mapped_column(String)
    grantee_type: Mapped[str] = mapped_column(String)
    privilege: Mapped[str] = mapped_column(String)
    granted_on: Mapped[str] = mapped_column(String)


class RoleUsage(Base):
    __tablename__ = "role_usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String)
    last_used_at: Mapped[datetime] = mapped_column(DateTime)


class ObjectAccess(Base):
    __tablename__ = "object_access"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    object_name: Mapped[str] = mapped_column(String)
    object_type: Mapped[str] = mapped_column(String)
    role_name: Mapped[str] = mapped_column(String)
    access_count: Mapped[int] = mapped_column(Integer)
