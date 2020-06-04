from next.next import Next
from store.impl.file_store import FileStore
from store.impl.mongodb_store import MongoStore


store_type_mapping = {
    "MONGODB": MongoStore,
    "FILE_SYSTEM": FileStore
}


class StoreService(object):
    """
    объект класса StoreService - основной объект, с которым взаимодействует
    нейрон с целью сохранения и получения своего состояния.
    При инициализации на основании StoreType задается тип хранилища,
    с которым будет работать сам StoreService.
    """
    _instance = None
    _store = None

    def __init__(self, store_type=""):
        if not store_type:
            config = Next.get_instance().get("STORE")
            self._store = store_type_mapping.get(config.get("store_type")).get_instance()

    def save_state(self, obj, mode="baseNeuron"):
        self._store.save_state(obj, mode)

    def load_state(self, obj, mode="baseNeuron"):
        return self._store.load_state(obj, mode)

    def get_recognize_neuron_list(self, layer_id):
        return self._store.get_recognize_neuron_list(layer_id)

    def get_client(self, name, password):
        return self._store.get_client(name, password)

    def get_client_by_id(self, uuid):
        return self._store.get_client_by_id(uuid)

    def clean(self):
        """
        Удаляет состояния всех слоев и нейронов в хранилище
        :return: 
        """
        self._store.clean()
