import os

# DEV PREV RELEASE
pod_type = os.environ.get("POD_TYPE", "DEV")
# TODO
file_list = os.listdir("/db/migration")
if pod_type == "DEV":
    pass
elif pod_type == "PREV":
    pass
elif pod_type == "RELEASE":
    file_list = filter(lambda x: "_down.sql" not in x, file_list)
