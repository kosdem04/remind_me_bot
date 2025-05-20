from app.database.models import async_session
from app.database.models import UserORM, EventORM
from sqlalchemy import select, update, delete, desc
import datetime
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func



async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(UserORM).where(UserORM.tg_id == tg_id))
        
        if not user:
            session.add(UserORM(tg_id=tg_id))
            await session.commit()


async def get_user_events(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(UserORM).where(UserORM.tg_id == tg_id))

        query = (
            select(EventORM)
            .where(EventORM.user_id == user.id)
        )
        result_query = await session.execute(query)
        events = result_query.scalars().all()
        return events


async def events_with_start_today():
    async with async_session() as session:
        today_str = datetime.date.today().strftime("%m-%d")
        query = (
            select(EventORM)
            .options(selectinload(EventORM.user))
            .where(func.strftime("%m-%d", EventORM.date) == today_str)
        )
        result_query = await session.execute(query)
        events = result_query.scalars().all()
        return events


async def events_start_date_in_3_days():
    async with async_session() as session:
        target_date = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%m-%d")
        query = (
            select(EventORM)
            .options(selectinload(EventORM.user))
            .where(func.strftime("%m-%d", EventORM.date) == target_date)
        )
        result_query = await session.execute(query)
        events = result_query.scalars().all()
        return events


async def events_start_date_in_7_days():
    async with async_session() as session:
        target_date = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%m-%d")
        query = (
            select(EventORM)
            .options(selectinload(EventORM.user))
            .where(func.strftime("%m-%d", EventORM.date) == target_date)
        )
        result_query = await session.execute(query)
        events = result_query.scalars().all()
        return events



async def add_event(tg_id: int, name: str, date: datetime):
    async with async_session() as session:
        user = await session.scalar(select(UserORM).where(UserORM.tg_id == tg_id))
        query = (
                select(EventORM)
                .where(EventORM.user_id == user.id,
                       EventORM.name == name,
                       EventORM.date == date)
            )
        event = await session.scalar(query)
        if not event:
            session.add(EventORM(
                name=name,
                date=date,
                user_id=user.id,
            ))
            await session.commit()
        else:
            raise ValueError("Такое событие уже существует")

async def delete_event(event_id: int):
    async with async_session() as session:
        query = (
            delete(EventORM)
            .where(EventORM.id == event_id)
        )
        await session.execute(query)
        await session.commit()

