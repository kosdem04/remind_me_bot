from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from typing import Optional, List
import datetime

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=True)
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserORM(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

    events: Mapped[List["EventORM"]] = relationship(
        "EventORM",
        back_populates="user",
        cascade='all, delete'
    )


class EventORM(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL')
    )
    name: Mapped[str] = mapped_column(String(100))
    date: Mapped[datetime.date]

    user: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="events"
    )


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
