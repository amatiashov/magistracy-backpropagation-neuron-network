import os
import yaml
import uuid
from next.next import TESTS_RESOURCES_DIR

base_conf = dict(
    APPLICATION=[
        dict(name="log_level", value="DEBUG", sys_environment="APP_LOG_LEVEl", required=True),
        dict(name="log_folder", value="repository/logs", sys_environment="APP_LOG_FOLDER")
    ]
)

if not os.path.exists(TESTS_RESOURCES_DIR):
    os.makedirs(TESTS_RESOURCES_DIR)


def create_conf(*args, **kwargs):
    conf = dict()
    if kwargs.get("extend_base_conf", True):
        conf.update(base_conf)
    if kwargs.get("sections"):
        conf.update(kwargs.get("sections"))
    conf_name = kwargs.get("conf_name", str(uuid.uuid4()) + ".yml")
    print("Creating config file with name " + conf_name)
    if conf_name is None:
        raise RuntimeError("Fill in config name for saving!")
    print(yaml.dump(conf, default_flow_style=False))
    with open(os.path.join(TESTS_RESOURCES_DIR, conf_name), "w") as f:
        yaml.dump(conf, f, default_flow_style=False)
    return conf_name


def delete_conf(conf_name):
    print("deleting config file: " + os.path.join(TESTS_RESOURCES_DIR, conf_name))
    os.remove(os.path.join(TESTS_RESOURCES_DIR, conf_name))

