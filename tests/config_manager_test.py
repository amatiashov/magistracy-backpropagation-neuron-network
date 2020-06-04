import os
import pytest
from tests.utils import create_conf, delete_conf
from next.next import TESTS_RESOURCES_DIR, set_option, get_option, Next


class TestConfigManager:
    _created_config_files = list()

    def setup(self):
        Next._instance = None
        print("ConfigManager has been reset ...")

    def teardown_class(self):
        for conf in self._created_config_files:
            delete_conf(conf)

    def test_setup_and_get_option(self):
        opt_name = "PARAMETER_NAME"
        opt_value = "AVOKADO"
        set_option(opt_name, opt_value)
        assert get_option(opt_name) == opt_value

    def test_get_nonexistent_option(self):
        assert get_option("XYbREXpNabQ") == ""

    def test_read_custom_yml_conf(self):
        conf_obj = dict(
            TEST_SECTION=[
                dict(name="test_parameter", value="test_value", sys_environment="TEST_ENV", required=True)
            ]
        )
        conf_name = create_conf(sections=conf_obj)
        self._created_config_files.append(conf_name)
        instance = Next.get_instance(config_path=os.path.join(TESTS_RESOURCES_DIR, conf_name),
                                     external_check=False)
        configs = instance.get()
        assert configs.get("TEST_SECTION").get("test_parameter") == "test_value"

    def test_sys_environment(self):
        conf_obj = dict(
            TEST_SECTION=[
                dict(name="test_parameter", value="test_value", sys_environment="TEST_ENV", required=True)
            ]
        )
        os.environ["TEST_ENV"] = "test_value_from_env"
        conf_name = create_conf(sections=conf_obj)
        self._created_config_files.append(conf_name)
        instance = Next.get_instance(config_path=os.path.join(TESTS_RESOURCES_DIR, conf_name),
                                     external_check=False)

        os.environ.pop("TEST_ENV")
        assert instance.get("TEST_SECTION").get("test_parameter") == "test_value_from_env"

    def test_empty_value(self):
        conf_obj = dict(
            TEST_SECTION=[
                dict(name="test_parameter", sys_environment="TEST_ENV", required=True)
            ]
        )
        conf_name = create_conf(sections=conf_obj)
        self._created_config_files.append(conf_name)
        with pytest.raises(ValueError) as e:
            Next.get_instance(config_path=os.path.join(TESTS_RESOURCES_DIR, conf_name),
                              external_check=False)
        error_msg = "You have to define the 'test_parameter' variable in the 'TEST_SECTION' " \
                    "section or define the 'TEST_ENV' system variable!"
        assert error_msg in str(e.value)

    def test_return_empty_config(self):
        conf_obj = dict(
            TEST_SECTION=[
                dict(name="test_parameter", value="test_value", sys_environment="TEST_ENV", required=True)
            ]
        )
        conf_name = create_conf(sections=conf_obj)
        self._created_config_files.append(conf_name)
        instance = Next.get_instance(config_path=os.path.join(TESTS_RESOURCES_DIR, conf_name),
                                     external_check=False)

        assert instance.get("nonexistent-conf") == dict()

    def test_boolean_from_file(self):
        for boolean in [True, False]:
            self.setup()
            conf_obj = dict(
                TEST_SECTION=[
                    dict(name="BOOLEAN_PARAM", value=boolean, sys_environment="BOOL", required=True)
                ]
            )
            conf_name = create_conf(sections=conf_obj)
            self._created_config_files.append(conf_name)
            instance = Next.get_instance(config_path=os.path.join(TESTS_RESOURCES_DIR, conf_name),
                                         external_check=False)
            assert instance.get("TEST_SECTION").get("BOOLEAN_PARAM") is boolean

    def test_boolean_from_sys_env(self):
        mapping = {"true": True, "false": False, "True": True, "False": False}
        for boolean in mapping:
            self.setup()
            os.environ["BOOL"] = boolean
            conf_obj = dict(
                TEST_SECTION=[
                    dict(name="BOOLEAN_PARAM", sys_environment="BOOL", required=True)
                ]
            )
            conf_name = create_conf(sections=conf_obj)
            self._created_config_files.append(conf_name)
            instance = Next.get_instance(config_path=os.path.join(TESTS_RESOURCES_DIR, conf_name),
                                         external_check=False)

            os.environ.pop("BOOL")
            assert instance.get("TEST_SECTION").get("BOOLEAN_PARAM") is mapping.get(boolean)
