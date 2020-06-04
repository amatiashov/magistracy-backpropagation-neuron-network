from entities.backpropagation.neuron import Neuron


class Layer(object):
    _name = None                    # используется для генерации имен нейронов, принадлежащих слою
    _neurons = None                 # список всех нейронов данного слоя
    _result_set = None              # список, содержащий результат работы каждого нейрона в слое
    _number_of_input_signal = None  # число входных сигналов слоя
    _sigmas = None                  # список поправок сигма
    _auto_save = False              # при каждом обучении сохранять ли состояние слоя

    def __init__(self, name, number_neurons_in_layer=2, number_of_input_signal=2,
                 auto_save=False):
        """
        Имена нейронов генерируются автоматически на основании имени слоя.
        Правило формирования имени нейрона описано в комментарии к конструктору нейрона.
        Правило формирования имени слоя следующее:
            {имя сети} + {#} + {порядковый номер слоя, начиная с 0}:
                number_search#5 - пятый слой в сети number_search

        :param name: необходимо для формирования имени нейрона
        :param number_neurons_in_layer: число нейронов в слое - число выходов слоя
        :param number_of_input_signal: число входов слоя (так же число входов каждого нейрона в слое)
        :param auto_save: автоматическое сохранение состояния каждого нейрона
        """
        if name is None or name == "":
            raise ValueError("name must be not None")
        self._name = name
        self._number_of_input_signal = number_of_input_signal
        self._sigmas = [0 for i in range(number_neurons_in_layer)]
        self._auto_save = auto_save
        # инициализация нейронов в слое
        # так как список передается по ссылке, то для того, чтобы у каждого объекта
        # класса Layer был свой список _neurons, нужно присвоить этой ссылке новый пустой список
        self._neurons = []
        for i in range(number_neurons_in_layer):
            neuron_name = name + "#" + str(i)
            neuron = Neuron(name=neuron_name, number_of_input=number_of_input_signal)
            self._neurons.append(neuron)

    def calculate(self, input_data):
        """
        Метод подает на вход каждому нейрону в сети массив входных данных.
        @:return список, содержащий результат работы каждого нейрона в self._neurons
        :param input_data: список входных данных
        :return: список, содержащий результат работы каждого нейрона в self._neurons
        """
        self._result_set = []
        for neuron in self._neurons:
            result = neuron.calculate(input_data)
            self._result_set.append(result)
        return self._result_set

    def get_weighted_synaptic_sum(self, index):
        """
        Метод возвращает взвешенную синаптическую сумму. Это необходимо для
        алгоритма обратного распространения ошибки на этапе подстройки весов
        скрытого слоя. В цикле проходим по всем нейронам в слоя, получаем у
        каждого нейрона i-ый вес и умножаем на соответствующую сигму, вычисленную
        на этапе обучения
        :param index: индекс необходимого веса 
        :return: 
        """
        synaptic_sum = 0
        for i in range(len(self._neurons)):
            neuron_weight = self._neurons[i].get_weight()[index]
            synaptic_sum += neuron_weight * self._sigmas[i]
        return synaptic_sum

    def save_state(self):
        for neuron in self._neurons:
            neuron.save_state()

    def get_neuron_list(self):
        return self._neurons

    def get_sigmas(self):
        return self._sigmas

    def get_result_set(self):
        return self._result_set

    def get_input_size(self):
        return self._number_of_input_signal
