import os
from root import PROJECT_ROOT_PATH

# DEV PREV RELEASE
pod_type = os.environ.get("POD_TYPE", "DEV")
# TODO
file_list = os.listdir(f"{PROJECT_ROOT_PATH}/db/migration")
if pod_type == "DEV":
    pass
elif pod_type == "PREV":
    pass
elif pod_type == "RELEASE":
    raise Exception("RELEASE CAN NOT MIGRATE")
else:
    raise Exception("UNKNOWN ENV")
