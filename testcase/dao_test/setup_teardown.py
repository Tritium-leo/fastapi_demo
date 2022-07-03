from unittest import TestCase

from config import init
# to create test db
from pkg import model
from pkg.dao import db
from root import PROJECT_ROOT_PATH

init.load_file(f"{PROJECT_ROOT_PATH}/config/file/default.yaml", f"{PROJECT_ROOT_PATH}/config/file/local.yaml",
               f"{PROJECT_ROOT_PATH}/config/file/test.yaml")

db.init_db(db.DBConfig(**init.config["db"]))


class DBSetUpTearDown(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        model.Base.metadata.create_all(db.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        model.Base.metadata.drop_all(db.engine)
