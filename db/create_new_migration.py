import os
import time
from pathlib import Path

project_root_path = os.environ.get("PROJECT_ROOT")
project_root_path = project_root_path if project_root_path != "" and project_root_path != None else os.path.abspath(".")

present_time = int(time.time())

prev_file_name = input("please input file name to continue: \n")

file_dir = Path(f"{project_root_path}/db/migration")
file_paths = [
    file_dir.joinpath(Path(f"{present_time}_{prev_file_name}_up.sql")),
    file_dir.joinpath(Path(f"{present_time}_{prev_file_name}_down.sql"))
]

if not file_dir.exists():
    logger.info(f"File Dir Didn't exist Dir : [ {str(file_dir)} ]")
elif any([x.exists() for x in file_paths]):
    logger.info(f"File Already exist. Path: [ {str(file_paths)} ] ")
else:
    for file_path in file_paths:
        with open(str(file_path), 'w') as f:
            f.write("")
        logger.info(f"Success create file :{file_path}")
