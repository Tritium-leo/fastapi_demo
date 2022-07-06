from unittest import TestCase

from config import model as config_model
# to create test db
from pkg import model
from pkg.dao import db
from root import PROJECT_ROOT_PATH

config = config_model.Config.load_dir(f"{PROJECT_ROOT_PATH}/config/file/default.yaml",
                                      f"{PROJECT_ROOT_PATH}/config/file/local.yaml",
                                      f"{PROJECT_ROOT_PATH}/config/file/test.yaml")

db.init_db(config.struct_map("db", db.DBConfig))


class DBSetUpTearDown(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        model.Base.metadata.create_all(db.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        model.Base.metadata.drop_all(db.engine)
