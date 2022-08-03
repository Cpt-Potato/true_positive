from datetime import date

from sqlalchemy import select

from db.base import get_session
from db.models import Statistic


async def write_to_db(data: Statistic):
    session = await get_session()
    session.add(data)
    await session.commit()


async def get_statistic():
    # res = []
    session = await get_session()
    statement = select(Statistic).where(Statistic.create_date >= date.today())
    result = await session.execute(statement)
    # return result.all()
    return result.scalars().all()
    # for stat in result.scalars().all():
    #     res.append(stat)
    # return res
