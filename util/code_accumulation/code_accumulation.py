import os
from next.next import BASE_DIR

exclude_folders = ["venv", "code_accumulation"]
out_file = os.path.join(BASE_DIR, "util", "code_accumulation", "aggregation_code.txt")

with open(out_file, "w") as f:
    pass

def code_accumulation(start_path, base_path=[]):
    if not base_path:
        base_path.append(start_path)
    for entity in os.listdir(path=start_path):
        if os.path.isdir(os.path.join(start_path, entity))\
                and entity not in exclude_folders:
            code_accumulation(os.path.join(start_path, entity))
        if entity.endswith(".py") and entity != "__init__.py":
            with open(out_file, "a") as f:
                with open(os.path.join(start_path, entity)) as source:
                    f.write("======================\n")
                    f.write(os.path.join(start_path, entity).replace(base_path[0], "") + "\n")
                    f.write(source.read())
                    f.write("======================\n\n\n")


code_accumulation(BASE_DIR)
