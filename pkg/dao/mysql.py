from config.init import config
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class MysqlConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str
    max_open_conn: int
    max_idle_conn: int
    log_mode: bool


conf = MysqlConfig(**config['mysql'])

engien = create_engine(
    f"mysql+pymysql://{conf.username}:{conf.password}@{conf.host}:{conf.port}/{conf.database}",
    encoding='utf-8',
    pool_size=conf.max_open_conn,
    max_overflow=conf.max_idle_conn,
    pool_pre_ping=True,
    pool_recycle=-1,
    connect_args={"connect_timeout": 30},
    echo=conf.log_mode,
    query_cache_size=0,
    echo_pool=conf.log_mode
)
Session = sessionmaker(bind=engien, autoflush=False, autocommit=False)


def ping():
    res = engien.execute("select 1")


ping()


@contextmanager
def session_scope() -> Session:
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
