from typing import *
from enum import Enum
from pydantic import BaseModel


class EnvEnum(Enum):
    Dev = 'dev'
    Prev = 'prev'
    Prod = 'prod'


class AppConfig(BaseModel):
    env: EnvEnum = 'dev'
    version: str
    machine_id: str

    def is_dev(self) -> bool:
        return self.env == EnvEnum.Dev

    def is_prev(self) -> bool:
        return self.env == EnvEnum.Prev

    def is_prod(self) -> bool:
        return self.env == EnvEnum.Prod
