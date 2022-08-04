from sqlalchemy import Column, DateTime, Integer, String, func

from db.base import Base


class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    url = Column(String(255))
    create_date = Column(DateTime, server_default=func.now())

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}
