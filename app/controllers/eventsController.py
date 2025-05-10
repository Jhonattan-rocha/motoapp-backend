from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.eventsModel import Events
from app.schemas.eventsSchema import EventBase, EventCreate
from app.utils import apply_filters_dynamic
from fastapi import HTTPException

async def create_event(db: AsyncSession, event: EventBase):
    # Verifica conflitos de datas com eventos abertos
    stmt = select(Events).where(
        Events.closed == False,
        or_(
            and_(
                event.date_init <= Events.date_final,
                event.date_final >= Events.date_init
            ),
            and_(
                event.date_final >= Events.date_init,
                event.date_init <= Events.date_final
            )
        )
    )

    result = await db.execute(stmt)
    conflicting_event = result.scalars().first()

    if conflicting_event:
        raise HTTPException(
            status_code=409,
            detail="Já existe um evento em aberto que conflita com as datas informadas."
        )

    # Cria o evento se não houver conflito
    db_event = Events(**event.model_dump(exclude_none=True))
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def get_events(db: AsyncSession, skip: int = 0, limit: int = 10, filters: Optional[List[str]] = None,
                    model: str = ""):
    query = select(Events)

    if filters and model:
        query = apply_filters_dynamic(query, filters, model)
    result = await db.execute(
        query
        .offset(skip)
        .options(joinedload(Events.cars), joinedload(Events.user))
        .limit(limit if limit > 0 else None)
    )
    return result.scalars().unique().all()


async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(
        select(Events)
        .options(joinedload(Events.cars), joinedload(Events.user))
        .where(Events.id == event_id)
    )
    event = result.scalars().unique().first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid id, not found",
        )
    return event


async def update_event(db: AsyncSession, event_id: int, updated_event: EventCreate):
    result = await db.execute(select(Events).where(Events.id == event_id))
    event = result.scalars().first()
    if event is None:
        return None

    for key, value in updated_event.model_dump(exclude_none=True).items():
        if str(value):
            setattr(event, key, value)

    await db.commit()
    await db.refresh(event)
    return event


async def delete_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Events).where(Events.id == event_id))
    event = result.scalars().first()
    if event is None:
        return None
    await db.delete(event)
    await db.commit()
    return event
