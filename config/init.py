import yaml
import json
from pathlib import Path
from typing import *

config = {}


def load_file(*args) -> Dict[str, Any]:
    global config
    for p in args:
        if p == "" or p is None:
            continue
        path = Path(p)
        if not path.exists():
            raise Exception(f"config didn't exist,path:[{str(path)}]")
        with open(str(path), 'r') as f:
            file_type = judge_file_type(str(path))
            if file_type == "json":
                deep_update_dict(config, json.load(f))
            elif file_type == "yaml":
                deep_update_dict(config, yaml.load(f, yaml.FullLoader))
    return config


def judge_file_type(path: str) -> str:
    # exts = [".json", ".yaml", ".yml"]
    prev_ext = path.split(".")[-1]
    if prev_ext == "yaml" or prev_ext == "yml":
        return "yaml"
    elif prev_ext == "json":
        return "json"
    else:
        raise Exception(f"Didn't support this kind of config file:{path}")


def deep_update_dict(d1: Dict, d2: Dict):
    for k, v in d2.items():
        if k in d1:
            if isinstance(v, dict):
                deep_update_dict(d1[k], d2[k])
            elif isinstance(v, list):
                # TODO MERGE
                d1[k] = v
            else:
                d1[k] = v
        else:
            d1[k] = v
