from sqlalchemy import Column, DateTime, Integer, Text, func

from db.base import Base


class Statistic(Base):
    __tablename__ = "statistic"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    url = Column(Text)
    create_date = Column(DateTime, server_default=func.now())

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}
