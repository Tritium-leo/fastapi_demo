from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

Base.create_time = Column(DateTime, default=func.now(), comment='创建时间')
Base.update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment='修改时间')


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Base.to_dict = to_dict

from .user import *
from .role import *
