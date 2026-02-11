from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    ObjectAccess,
    QueryHistory,
    RoleGrant,
    RoleUsage,
    Warehouse,
    WarehouseMetering,
)


def list_warehouses(session: Session, limit: int, offset: int) -> Sequence[Warehouse]:
    return session.execute(select(Warehouse).limit(limit).offset(offset)).scalars().all()


def list_warehouse_metering(
    session: Session,
    start_date: date | None,
    end_date: date | None,
    limit: int,
    offset: int,
) -> Sequence[WarehouseMetering]:
    query = select(WarehouseMetering)
    if start_date:
        query = query.where(
            WarehouseMetering.start_time >= datetime.combine(start_date, datetime.min.time())
        )
    if end_date:
        query = query.where(
            WarehouseMetering.start_time <= datetime.combine(end_date, datetime.max.time())
        )
    return session.execute(query.limit(limit).offset(offset)).scalars().all()


def list_queries(
    session: Session,
    limit: int,
    offset: int,
    warehouse_name: str | None,
    user_name: str | None,
    min_elapsed_ms: int | None,
) -> Sequence[QueryHistory]:
    query = select(QueryHistory)
    if warehouse_name:
        query = query.where(QueryHistory.warehouse_name == warehouse_name)
    if user_name:
        query = query.where(QueryHistory.user_name == user_name)
    if min_elapsed_ms is not None:
        query = query.where(QueryHistory.total_elapsed_ms >= min_elapsed_ms)
    return session.execute(query.limit(limit).offset(offset)).scalars().all()


def list_role_grants(session: Session) -> Sequence[RoleGrant]:
    return session.execute(select(RoleGrant)).scalars().all()


def list_role_usage(session: Session) -> Sequence[RoleUsage]:
    return session.execute(select(RoleUsage)).scalars().all()


def list_object_access(session: Session) -> Sequence[ObjectAccess]:
    return session.execute(select(ObjectAccess)).scalars().all()


def to_dicts(items: Iterable) -> list[dict]:
    rows: list[dict] = []
    for item in items:
        data = dict(item.__dict__)
        data.pop("_sa_instance_state", None)
        rows.append(data)
    return rows
