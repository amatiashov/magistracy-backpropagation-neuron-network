import pymongo
# url_connection = "mongodb://user:password@host:port/?authSource=admin"
from next.next import Next


class MongoStore(object):
    _instance = None
    _connection = None
    _db = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def save_state(self, obj, mode):
        if mode == "baseNeuron":
            self.save_base_neuron(obj)

    def load_state(self, obj, mode):
        if mode == "baseNeuron":
            return self.load_base_neuron(obj)

    def __init__(self):
        config = Next.get_instance().get("MONGODB")
        url_connection = "mongodb://{}:{}@{}:{}/?authSource={}".format(
            config["user"],
            config["password"],
            config["host"],
            config["port"],
            config["authsource"]
        )
        self.connection = pymongo.MongoClient(url_connection)
        self._db = self.connection[config["db_name"]]

    def save_base_neuron(self, neuron):
        current_state = {"name": neuron.get_name(),
                         "id": neuron.get_id(),
                         "number_of_input_signal": neuron.get_number_of_input_signal(),
                         "weight": neuron.get_weight()}

        data = self._db.neurons.find_one({"id": neuron.get_id()})
        if data is not None:
            self._db.neurons.update({"id": neuron.get_id()}, current_state)
        else:
            self._db.neurons.save(current_state)

    def load_base_neuron(self, neuron):
        resource = self._db.neurons.find_one({"id": neuron.get_id()})
        if not resource:
            return False
        neuron.set_weight(resource["weight"])
        return True

