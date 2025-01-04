import gezondheid.config as config

from sqlalchemy import create_engine
from sqlalchemy import Date, Column, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()
engine = create_engine(config.DB_URL, echo=False)


class Health(Base):
    __tablename__ = "health"

    health_date = Column(Date, primary_key=True, nullable=False)
    health_sleep_score = Column(Integer, nullable=False)
    health_body_battery_max = Column(Integer, nullable=False)
    health_body_battery_min = Column(Integer, nullable=False)
    health_active_time = Column(Integer, nullable=False)
    health_defecation = Column(Integer, nullable=False)
