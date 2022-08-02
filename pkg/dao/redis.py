from contextlib import contextmanager
from typing import *

import loguru
import redis
from loguru import logger
from pydantic import *

from pkg import constant
from vender import jsonplus


class RedisConfig(BaseModel):
    host: str
    port: int
    password: Union[str, None]
    db: int
    max_open_conn: int


def format_key(key: str) -> str:
    return f"{constant.base.RedisKeyPrev}|{key}"


def format_value(value: str):
    # list dict set tuple
    if isinstance(value, dict):
        value = jsonplus.dumps(value)
    elif isinstance(value, list):
        value = jsonplus.dumps(value)
    else:
        value = str(value)
    return value


class RedisCli:
    # TODO CODE @SET_PREF @GET_AFTER

    def __init__(self, conf: RedisConfig):
        self.pool = redis.ConnectionPool(host=conf.host, port=conf.port, password=conf.password, db=conf.db,
                                         max_connections=conf.max_open_conn)

    def close(self):
        try:
            self.pool.disconnect(inuse_connections=True)
        except Exception as e:
            logger.error(f"redis closed Failed,err:{e}")
        else:
            logger.info("redis closed Successfully")

    @staticmethod
    def try_parse_dict(v):
        try:
            v = jsonplus.loads(v)
        except Exception as e:
            loguru.logger.error(f"REDIS PARSE ERROR,data:[{v}],err:[{e}]")
        return v

    @property
    def cli(self):
        return redis.Redis(connection_pool=self.pool)

    @contextmanager
    def get_cli(self) -> redis.Redis:
        cli = None
        try:
            cli = redis.Redis(connection_pool=self.pool)
            yield cli
        finally:
            cli.close() if cli is not None else None
    #
    # def get(self, k: str):
    #     k = format_key(k)
    #     with self.get_cli() as cli:
    #         # cli = self.get_cli()
    #         res = RedisCli.try_parse_dict(cli.get(k))
    #     return res
    #
    # def set(self, k, v, px=-1, nx=False, xx=False):
    #     k = format_key(k)
    #     v = format_value(v)
    #     # ex：过期时间（秒），时间到了后redis会自动删除
    #     # px：过期时间（毫秒），时间到了后redis会自动删除。ex、px二选一即可
    #     # nx：如果设置为True，则只有name不存在时，当前set操作才执行
    #     # xx：如果设置为True，则只有name存在时，当前set操作才执行
    #     cli = self.get_cli()
    #     if px != -1:
    #         cli.set(k, v, nx=nx, xx=xx)
    #     else:
    #         cli.set(k, v, px=px, nx=nx, xx=xx)
    #
    # def hset(self, k, k1, v) -> int:
    #     k = format_key(k)
    #     v = format_value(v)
    #     with self.get_cli() as cli:
    #         res = cli.hset(k, k1, v)
    #     return res
    #
    # def hmset(self, k, data: Dict[str, Any]):
    #     k = format_key(k)
    #     with self.get_cli() as cli:
    #         res = cli.hmset(k, data)
    #     return res
    #
    # def hget(self, k, k1) -> str:
    #     k = format_key(k)
    #     with self.get_cli() as cli:
    #         res = RedisCli.try_parse_dict(cli.hget(k, k1))
    #     # cli = self.get_cli()
    #     return res
    #
    # def hmget(self, k, *k1) -> List[Any]:
    #     k = format_key(k)
    #     cli = self.get_cli()
    #     return RedisCli.try_parse_dict(cli.hmget(k, *k1))
    #
    # def delete(self, *args):
    #     args = [format_key(x) for x in args]
    #     cli = self.get_cli()
    #     v = cli.delete(*args)
    #     return v
    #
    # def exists(self, k: str):
    #     k = format_key(k)
    #     cli = self.get_cli()
    #     return cli.exists(k)
    #
    # def rename(self, k: str, n_k: str) -> bool:
    #     k = format_key(k)
    #     cli = self.get_cli()
    #     return cli.rename(k, n_k)
    #
    # def move(self, k: str, db: int) -> bool:
    #     k = format_key(k)
    #     cli = self.get_cli()
    #     return cli.move(k, db)
    #
    # def setnx(self, k, v, px):
    #     k = format_key(k)
    #     v = format_value(v)
    #     self.set(k, v, px, nx=True)
    #
    # def lock(self, k, v, px) -> bool:
    #     k = format_key(k)
    #     self.setnx(k, v, px)
    #
    # def unlock(self, k) -> bool:
    #     k = format_key(k)
    #     v = self.delete(k)
    #     return v == 1
    #
    # def decr(self, k):
    #     k = format_key(k)
    #     cli = self.get_cli()
    #     cli.decr(k)
    #
    # def incr(self, k):
    #     k = format_key(k)
    #     cli = self.get_cli()
    #     cli.incr(k)
    #
    # def lpush(self, k, *args):
    #     k = format_key(k)
    #     cli = self.get_cli()
    #     cli.lpush(k, *args)


client: RedisCli


def init_redis(conf: RedisConfig):
    global client
    client = RedisCli(conf)
