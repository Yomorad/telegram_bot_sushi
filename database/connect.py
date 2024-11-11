import os
from dotenv import load_dotenv
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
POSTGRES_DB = Config.name_db
POSTGRES_USER = Config.name_db
POSTGRES_PASSWORD = Config.name_db
POSTGRES_HOST = Config.name_db

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Настройка подключения к БД
DATABASE_URL = "postgresql+psycopg2://user:password@localhost/dbname"  # Измените на ваши данные
engine = create_engine(DATABASE_URL)

# Создание таблиц
Base.metadata.create_all(engine)

# Настройка сессии
Session = sessionmaker(bind=engine)
session = Session()