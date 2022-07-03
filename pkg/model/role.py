from . import Base
from sqlalchemy import Column, Integer, String


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    #
    uuid = Column(Integer)
    role_name = Column(String(20))

