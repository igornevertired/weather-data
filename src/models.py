import logging
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import yaml

Base = declarative_base()

DIALECTS_MAP = {'Postgres': "postgresql"}
DBMS = "Postgres"


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    temperature = Column(Float)
    wind_direction = Column(String)
    wind_speed = Column(Float)
    pressure = Column(Float)
    precipitation_type = Column(String)
    precipitation_amount = Column(Float)


with open("./src/configs/db_config.yaml", "r", encoding="utf_8") as file:
    config = yaml.safe_load(file)
    url_object = URL.create(
        DIALECTS_MAP[DBMS],
        host=config[DBMS]["host"],
        username=config[DBMS]["username"],
        password=config[DBMS]["password"],
        database=config[DBMS]["database"]
    )

engine = create_engine(url_object)
if not database_exists(engine.url):
    logging.warning(f"Database {config[DBMS]['database']} doesn't exist")
    create_database(engine.url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
