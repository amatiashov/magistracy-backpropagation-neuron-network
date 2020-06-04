import logging


class ExampleCheck(object):
    _logger = None
    order = 2
    skip = True  # This class is just for example

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def do_check(self, configuration):
        """
        INT_PARAM must be defined in SPACE_NAME section and
        be more than 1000.
        :param configuration:
        :return:
        """
        space = configuration.get("SPACE_NAME")
        if not space:
            raise AttributeError("<SPACE_NAME> must be defined!")
        param = space.get("INT_PARAM")
        if not param:
            raise AttributeError("<INT_PARAM> must be defined!")
        if param < 1000:
            msg = "INT_PARAM must be more than 1000"
            self._logger.error(msg)
            raise ValueError(msg)
