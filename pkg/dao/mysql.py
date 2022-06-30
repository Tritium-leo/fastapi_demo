from config.init import config
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class MysqlConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    max_open_conn: int
    max_idle_conn: int
    log_mode: bool


conf = MysqlConfig(**config['mysql'])

engien = create_engine(
    f"mysql+pymysql://{conf.username}:{conf.password}@{conf.host}:{conf.port}?charset=utf-8&parseTime=True",
    pool_size=conf.max_open_conn,
    max_overflow=conf.max_idle_conn,
    pool_pre_ping=True,
    pool_recycle=-1,
    connect_args={"connect_timeout": 30},
    echo=conf.log_mode
)
Session = sessionmaker(bind=engien, autoflush=False, autocommit=False)


def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()
