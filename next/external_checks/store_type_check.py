import logging
from store.service.store_service import store_type_mapping


class StoreTypeCheck(object):
    _logger = None
    order = 1

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def do_check(self, configuration):
        conf = configuration.get("STORE")
        if conf.get("store_type") not in store_type_mapping:
            msg = "Store type <%s> is not supported!" % conf.get("store_type")
            self._logger.error(msg)
            raise ValueError(msg)
