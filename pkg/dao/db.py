from contextlib import contextmanager
from enum import unique, Enum

import sqlalchemy
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.orm import close_all_sessions
from sqlalchemy.orm import sessionmaker

from pkg.errors import sql_error


@unique
class DBType(Enum):
    mysql = "mysql"
    postgres = "postgres"
    oracle = "oracle"


class DBConfig(BaseModel):
    db_type: DBType = DBType.mysql
    host: str
    port: int
    username: str
    password: str
    database: str
    max_open_conn: int
    max_idle_conn: int
    log_mode: bool = False


engine: sqlalchemy.engine = None
Session: sqlalchemy.orm.Session = None


def init_db(conf: DBConfig):
    global engine
    global Session

    if conf.db_type == DBType.mysql:
        conn_type = "mysql+pymysql"
    elif conf.db_type == DBType.postgres:
        conn_type = "postgres+psycopg2"
    elif conf.db_type == DBType.oracle:
        conn_type = "oracle+cx_oracle"
    else:
        raise Exception(f"Didn't support this kind db :{conf.db_type}")

    engine = sqlalchemy.create_engine(
        f"{conn_type}://{conf.username}:{conf.password}@{conf.host}:{conf.port}/{conf.database}",
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
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def session_scope() -> sqlalchemy.orm.Session:
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"【SQL ERROR】{str(e)}")
        raise sql_error.SqlException(e)
    finally:
        session.close()


def close():
    try:
        close_all_sessions()
        logger.info("DB closed Successfully")
    except Exception as e:
        logger.error(f"DB closed Failed,err:{e}")
