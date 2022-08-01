from datetime import date

from sqlalchemy import select

from db.base import get_session
from db.models import Statistic


async def write_row(data: Statistic):
    session = get_session()
    session.add(data)
    await session.commit()


async def get_statistic():
    session = get_session()
    statement = (
        select(Statistic)
        .where(Statistic.create_date > date.today())
    )
    return await session.execute(statement).scalars().all()
