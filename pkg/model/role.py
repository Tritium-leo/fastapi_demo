from . import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from pkg.model.constant import *


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    #
    uuid = Column(Integer)
    role_name = Column(String(20))

