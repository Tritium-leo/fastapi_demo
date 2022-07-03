from typing import *

from pydantic import *

import redis
from pkg import constant
from vender import jsonplus


class RedisConfig(BaseModel):
    host: str
    port: int
    password: Union[str, None]
    db: int
    max_open_conn: int


class RedisCli:
    # TODO CODE @SET_PREF @GET_AFTER

    def __init__(self, conf: RedisConfig):
        self.pool = redis.ConnectionPool(host=conf.host, port=conf.port, password=conf.password, db=conf.db,
                                         max_connections=conf.max_open_conn)

    def close(self):
        self.pool.disconnect(inuse_connections=True)

    def format_key(self, key: str) -> str:
        return f"{constant.base.RedisKeyPrev}|{key}"

    def format_value(self, value: str):
        # list dict set tuple
        if isinstance(value, dict):
            value = jsonplus.dumps(value)
        elif isinstance(value, list):
            value = jsonplus.dumps(value)
        else:
            value = str(value)
        return value

    @staticmethod
    def try_parse_dict(v):
        try:
            v = jsonplus.loads(v)
        except:
            pass
        return v

    def get_conn(self):
        return redis.Redis(connection_pool=self.pool)

    def get(self, k: str):
        k = self.format_key(k)
        conn = self.get_conn()
        return RedisCli.try_parse_dict(conn.get(k))

    def set(self, k, v, px=-1, nx=False, xx=False):
        k = self.format_key(k)
        v = self.format_value(v)
        # ex：过期时间（秒），时间到了后redis会自动删除
        # px：过期时间（毫秒），时间到了后redis会自动删除。ex、px二选一即可
        # nx：如果设置为True，则只有name不存在时，当前set操作才执行
        # xx：如果设置为True，则只有name存在时，当前set操作才执行
        conn = self.get_conn()
        if px != -1:
            conn.set(k, v, nx=nx, xx=xx)
        else:
            conn.set(k, v, px=px, nx=nx, xx=xx)

    def hset(self, k, k1, v):
        k = self.format_key(k)
        v = self.format_value(v)
        conn = self.get_conn()
        conn.hset(k, k1, v)
        return

    def hmset(self, k, data: Dict[str, Any]):
        k = self.format_key(k)
        conn = self.get_conn()
        conn.hmset(k, data)
        return

    def hget(self, k, k1) -> str:
        k = self.format_key(k)
        conn = self.get_conn()
        return RedisCli.try_parse_dict(conn.hget(k, k1))

    def hmget(self, k, *k1) -> List[Any]:
        k = self.format_key(k)
        conn = self.get_conn()
        return RedisCli.try_parse_dict(conn.hmget(k, *k1))

    def delete(self, *args):
        args = [self.format_key(x) for x in args]
        conn = self.get_conn()
        v = conn.delete(*args)
        return v

    def exists(self, k: str):
        k = self.format_key(k)
        conn = self.get_conn()
        return conn.exists(k)

    def rename(self, k: str, n_k: str) -> bool:
        k = self.format_key(k)
        conn = self.get_conn()
        return conn.rename(k, n_k)

    def move(self, k: str, db: int) -> bool:
        k = self.format_key(k)
        conn = self.get_conn()
        return conn.move(k, db)

    def setnx(self, k, v, px):
        k = self.format_key(k)
        v = self.format_value(v)
        self.set(k, v, px, nx=True)

    def lock(self, k, v, px) -> bool:
        k = self.format_key(k)
        self.setnx(k, v, px)

    def unlock(self, k) -> bool:
        k = self.format_key(k)
        v = self.delete(k)
        return v == 1

    def decr(self, k):
        k = self.format_key(k)
        conn = self.get_conn()
        conn.decr(k)

    def incr(self, k):
        k = self.format_key(k)
        conn = self.get_conn()
        conn.incr(k)

    def lpush(self, k, *args):
        k = self.format_key(k)
        conn = self.get_conn()
        conn.lpush(k, *args)


client: RedisCli


def init_redis(conf: RedisConfig):
    global client
    client = RedisCli(conf)
