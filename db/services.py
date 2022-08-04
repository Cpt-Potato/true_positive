from datetime import date, timezone

from sqlalchemy import select

from db.base import get_session
from db.models import Statistics


async def write_to_db(data: Statistics):
    session = await get_session()
    session.add(data)
    await session.commit()


async def get_statistics() -> str:
    statistics = ""
    session = await get_session()
    statement = select(Statistics).where(Statistics.create_date >= date.today())
    result = await session.execute(statement)
    for stat in result.scalars().all():
        statistics += f"{stat.user_id}, {stat.url}, {stat.create_date.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%d-%m-%Y_%H:%M:%S')}"
        statistics += "\n"
    return statistics or "Статистика за сегодня пуста"
