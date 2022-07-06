import json
import os
import typing
from collections import defaultdict
from pathlib import Path

import yaml
from pydantic import BaseModel


class Config(BaseModel):
    _instance = None
    data = dict()

    @classmethod
    def load_dir(cls, *paths):
        global config
        if config is None:
            config = Config()
        for p in paths:
            if p is None or p == "":
                continue
            path = Path(p)
            if not path.exists():
                raise Exception(f"config didn't exist,path:[{str(path)}]")
            with open(str(path), 'r') as f:
                file_type = Config.judge_file_type(str(path))
                if file_type == "json":
                    Config.deep_update_dict(config.data, json.load(f))
                elif file_type == "yaml":
                    Config.deep_update_dict(config.data, yaml.load(f, yaml.FullLoader))
        # 读取环境变量
        # 解析格式 = APP.PORT  8000   DB.DB_TYPE APP.SSO_CENTER
        for k, v in os.environ.items():
            if "." not in k:
                continue
            add_config = defaultdict(dict)
            prev_k = None
            for _k in k.split(".")[::-1]:
                _k = _k.lower()
                add_config[_k] = v
                v = add_config
                prev_k = _k
                add_config.pop(_k)
            Config.deep_update_dict(config.data, add_config)
        return config

    @staticmethod
    def judge_file_type(path: str) -> str:
        # exts = [".json", ".yaml", ".yml"]
        prev_ext = path.split(".")[-1]
        if prev_ext == "yaml" or prev_ext == "yml":
            return "yaml"
        elif prev_ext == "json":
            return "json"
        else:
            raise Exception(f"Didn't support this kind of config file:{path}")

    @staticmethod
    def deep_update_dict(d1: typing.Dict, d2: typing.Dict):
        for k, v in d2.items():
            if k in d1:
                if isinstance(v, dict):
                    Config.deep_update_dict(d1[k], d2[k])
                elif isinstance(v, list):
                    # TODO MERGE
                    d1[k] = v
                else:
                    d1[k] = v
            else:
                d1[k] = v

    def struct_map(self, root_name: str, config_cls: BaseModel):
        j_data = self.data.get(root_name, None)
        if j_data is None:
            raise Exception(f"this root doesn't exist,{root_name}")
        return config_cls(**j_data)


config: Config = None
