import os
import sys
import yaml
import json
import logging
from configparser import ConfigParser
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
TESTS_RESOURCES_DIR = os.path.join(BASE_DIR, "tests", "resources")


if sys.version_info >= (3, 0):
    import builtins
    _global_object = builtins
else:
    import __builtin__
    _global_object = __builtin__


class Next(object):
    _config = None
    _logger = None
    _instance = None
    _config_path = None
    _current_dir = None
    _external_check_folder = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self, config_path=None, external_check=True, external_check_folder="external_checks"):
        self._current_dir = os.path.dirname(os.path.abspath(__file__))
        self._external_check = external_check
        self._external_check_folder = external_check_folder
        self._config_path = config_path
        self._logger = logging.getLogger(__name__)
        self._config = ConfigParser()
        self._config.read(os.environ.get("CONFIG_PATH", os.path.join(self._current_dir, "descriptors", "config.ini")))
        self._config = {s: dict(self._config.items(s)) for s in self._config.sections()}
        self._check_config_health()
        self._configure_logging()
        # check configuration
        if external_check:
            self._do_external_checks()

    def get(self, section_name=None):
        if not section_name:
            return self._config
        return self._config.get(section_name, dict())

    def _check_config_health(self):
        default_conf = self._get_default_config()
        for section in default_conf:
            parameters = default_conf.get(section)
            if not self._config.get(section):
                self._config[section] = dict()
            config = self._config[section]
            for param in parameters:
                name = param["name"]
                default = param.get("value", None)
                required = param.get("required", True)
                config[name] = config.get(name, default)
                environment = param.get("sys_environment", None)
                if environment:
                    config[name] = os.environ.get(environment, config[name])
                    self._check_int(config, name)
                    self._check_boolean_value(config, name)
                if config[name] is None and required:
                    msg = "\n%s\n" % json.dumps(config, indent=4)
                    msg += "You have to define the '%s' variable in the '%s' section!" % (name, section)
                    if environment:
                        msg = msg[:-1] + " or define the '%s' system variable!" % environment
                    raise ValueError(msg)

    def _get_default_config(self):
        if not self._config_path:
            self._config_path = os.path.join(self._current_dir, "descriptors", "config.yml")
        if self._config_path.endswith(".json"):
            return self._get_default_config_from_json()
        if self._config_path.endswith(".yaml") or self._config_path.endswith(".yml"):
            return self._get_default_config_from_yaml()
        # if file is not supported throw exception
        error_msg = "Default config must be json or yaml!"
        self._logger.error(error_msg)
        raise RuntimeError(error_msg)

    def _get_default_config_from_yaml(self):
        # try to get default config from yaml file
        with open(self._config_path) as stream:
            self._logger.info("Found file config.yml")
            return yaml.load(stream)

    def _get_default_config_from_json(self):
        # try to get default config from json file
        with open(self._config_path, encoding="utf-8") as f:
            self._logger.info("Found file config.json")
            return json.loads(f.read())

    def _configure_logging(self):
        log_folder = os.path.join(BASE_DIR, self.get("APPLICATION").get("log_folder"))
        log_file_name = "log.txt"
        log_level = {
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        if not os.path.exists(os.path.join(BASE_DIR, log_folder)):
            os.makedirs(log_folder)
        logging.basicConfig(
            format=u'%(filename)s\t[LINE:%(lineno)d]# %(levelname)-8s\t [%(asctime)s]  %(message)s',
            level=log_level[Next.get_instance().get("APPLICATION")["log_level"]])
            # filename=os.path.join(log_folder, log_file_name))

    @staticmethod
    def _check_boolean_value(config, name):
        mapping = {"true": True, "false": False}
        if isinstance(config.get(name), str) and config.get(name).lower() in mapping:
            config[name] = mapping.get(config.get(name).lower())

    @staticmethod
    def _check_int(config, name):
        if isinstance(config.get(name), str):
            try:
                    config[name] = int(config.get(name))
            except Exception:
                pass

    def _do_external_checks(self):
        registry = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(os.path.join(current_dir, self._external_check_folder)):
            self._logger.error("There is no external check folder %s" % self._external_check_folder)
            return
        checkers = os.listdir(os.path.join(current_dir, self._external_check_folder))
        checkers = [_ for _ in checkers if not _.startswith("__") and _.endswith(".py")]
        for checker in checkers:
            spec = spec_from_file_location(checker[:-3],
                                           os.path.join(current_dir, self._external_check_folder, checker))
            check_module = module_from_spec(spec)
            spec.loader.exec_module(check_module)
            notify_classes = [_ for _ in dir(check_module) if not _.startswith("__") and _.endswith("Check")]
            for cls in notify_classes:
                obj = getattr(check_module, cls)()
                if not getattr(obj, "skip", False):
                    registry.append(obj)
        # sorting checkers by its order
        len_registry = len(registry)
        registry.sort(key=lambda check_obj: getattr(check_obj, "order", len_registry), reverse=False)
        self._logger.info("Start external check...")
        for checker in registry:
            if hasattr(checker, "do_check"):
                self._logger.info("Do %s check" % checker.__class__.__name__)
                checker.do_check(self._config)


def set_option(name, value):
    setattr(_global_object, name, value)


def get_option(name):
    return getattr(_global_object, name, "")
