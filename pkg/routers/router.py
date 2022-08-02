import importlib
import os

from fastapi import APIRouter

from root import PROJECT_ROOT_PATH

v1 = APIRouter(prefix="/v1", tags=["v1"])
v2 = APIRouter(prefix="/v2", tags=["v2"])
# autoimport
SERVICE_ROOT = PROJECT_ROOT_PATH.joinpath("pkg/service/")
for file in os.listdir(SERVICE_ROOT):
    if not file.endswith("_service.py"):
        continue
    importlib.import_module(f"pkg.service.{file.split('.')[0]}")
