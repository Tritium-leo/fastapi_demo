from sqlalchemy import Column,DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

Base.createtime = Column(DateTime, default=func.now, comment='创建时间')
Base.updatetime = Column(DateTime, default=func.now, onupdate=func.now, comment='修改时间')


def to_dict(self):
    return self.__dict__


Base.to_dict = to_dict
