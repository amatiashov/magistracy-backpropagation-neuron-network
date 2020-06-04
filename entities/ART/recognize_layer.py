from entities.ART.receiver2 import Receiver2
from entities.ART.recognize_neuron import RecognizeNeuron
from store.service.store_service import StoreService
from util.id_generator import generate_id


class RecognizeLayer(object):
    """
    Слой распознавания осуществляет классификацию входных векторов.
    Каждый нейрон в слое распознавания имеет соответствующий вектор весов.
    Только один нейрон с весовым вектором, наиболее соответствующим входному вектору, возбуждается;
    все остальные нейроны заторможены.
    """
    _recognize_neurons = None
    _receiver2 = None
    _number_of_input = None
    _store_service = None
    _r_vector = None
    _name = None
    _id = None

    def __init__(self, name, number_of_input):
        self._name = name + "#RecognizeLayer#"
        self._id = generate_id(name + "#RecognizeLayer#")
        self._number_of_input = number_of_input
        self._store_service = StoreService()
        self._receiver2 = Receiver2.get_instance()
        self._r_vector = [0 for _ in range(number_of_input)]
        neuron_list = self._store_service.get_recognize_neuron_list(self._id)
        self._recognize_neurons = []
        if neuron_list:
            print("Найдены сохраненные образы...")
        for neuron_name in neuron_list:
            self.create_neuron(neuron_name)

    def create_neuron(self, name=None):
        if name:
            neuron_name = name
        else:
            neuron_name = self._name + str(len(self._recognize_neurons)+1)
        neuron = RecognizeNeuron(name=neuron_name, number_of_input=self._number_of_input)
        self._recognize_neurons.append(neuron)
        return neuron

    def recognize(self, input_signal):
        if len(input_signal) != self._number_of_input:
            raise ValueError("Число входных сигналов должно равняться {}".format(self._number_of_input))

        if not self._receiver2.get_resolution():
            self._r_vector = [0 for i in range(self._number_of_input)]
            return self._r_vector

        self._r_vector = []
        for neuron in self._recognize_neurons:
            if neuron.is_ready():
                self._r_vector.append(neuron.wrap(input_signal))
            else:
                self._r_vector.append(0)
        index_winner_neuron = self._r_vector.index(max(self._r_vector))
        self._r_vector = [1 if i == index_winner_neuron else 0 for i in range(self._number_of_input)]
        return self._r_vector

    def activate_all_neuron(self):
        for neuron in self._recognize_neurons:
            neuron.turn_on()

    def get_neuron_by_index(self, index):
        return self._recognize_neurons[index]

    def get_r_vector(self):
        return self._r_vector

    def get_neuron_list(self):
        return self._recognize_neurons

    def save_state(self, layer_only=False):
        """
        Сохранение состояния слоя
        :param layer_only: если True - сохраняется только список нейронов в слое
        """
        self._store_service.save_state(obj=self, mode="ART.layer")
        if not layer_only:
            for neuron in self._recognize_neurons:
                neuron.save_state()

    def get_number_of_active_neuron(self):
        count = 0
        for neuron in self._recognize_neurons:
            if neuron.is_ready():
                count += 1
        return count

    def get_id(self):
        return self._id
