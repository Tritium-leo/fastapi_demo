from . import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from pkg.model.constant import *


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    #
    uuid = Column(Integer)
    username = Column(String(20))
    _password_hash_ = Column(String(256))

    @property
    def password(self):
        return Exception("password can't be get")

    @password.setter
    def password_setter(self, value):
        self._password_hash_ = generate_password_hash(value)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self._password_hash_, password)

    @classmethod
    def check_username(cls, username: str) -> bool:
        if len(username) < UserNameMinLen or len(username) >= UsernameMaxLen:
            return False
        return True
