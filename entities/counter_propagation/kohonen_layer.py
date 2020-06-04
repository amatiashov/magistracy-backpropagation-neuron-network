from math import sqrt
from entities.counter_propagation.kohonen_neuron import KohonenNeuron


class KohonenLayer(object):
    """
        В своей простейшей форме слой Кохонена функционирует в духе «победитель забирает все»,
        т. е. для данного входного вектора один и только один нейрон Кохонена выдает на выходе
        логическую единицу, все остальные выдают ноль. Нейроны Кохонена можно воспринимать
        как набор электрических лампочек, так что для любого входного вектора загорается одна из них.
        Слой Кохонена классифицирует входные векторы в группы схожих.
        Это достигается с помощью такой подстройки весов слоя Кохонена,
        что близкие входные векторы активируют один и тот же нейрон данного слоя.
    """
    _name = None                    # используется для генерации имен нейронов, принадлежащих слою
    _neurons = None                 # список всех нейронов данного слоя
    _result_set = None              # список, содержащий результат работы каждого нейрона в слое
    _number_of_input_signal = None  # число входных сигналов слоя
    _auto_save = False              # автоматическое сохранение состояния слоя после обучения
    _learn_rate = 0.3               # скорость обучения
    _normalize = False              # нормализовывать ли входные данные

    def __init__(self, name, number_neurons_in_layer=2, number_of_input_signal=2,
                 auto_save=False, use_normalize_data=False):
        if name is None or name == "":
            raise ValueError("name must be not None")
        name += "{kohonen_layer}"
        self._number_of_input_signal = number_of_input_signal
        self._name = name
        self._auto_save = auto_save
        self._normalize = use_normalize_data
        # инициализация нейронов в слое
        # так как список передается по ссылке, то для того, чтобы у каждого объекта
        # класса Layer был свой список _neurons, нужно присвоить этой ссылке новый пустой список
        self._neurons = []
        for i in range(number_neurons_in_layer):
            neuron_name = name + "#" + str(i)
            neuron = KohonenNeuron(name=neuron_name, number_of_input=number_of_input_signal)
            self._neurons.append(neuron)

    def calculate(self, input_signal):
        """
        Метод подает на вход каждому нейрону в сети массив входных данных.
        Далее интерпретируем полученный результат с помощью метода _interpret_calc_result
        :param input_signal: список входных сигналов
        :return: список, содержащий одну единицу - номер "нейрона-победителя"
        """
        if self._normalize:
            input_signal = self.prepared_input_signal(input_signal)
        result_set = []
        for neuron in self._neurons:
            result = neuron.calculate(input_signal)
            result_set.append(result)
        return self._interpret_calc_result(result_set)

    @staticmethod
    def _interpret_calc_result(result_set):
        """
        Данный метод ищет "нейрон-победитель" - максимальный элемент в списке result_set,
        присваивает этому элементу значение 1, остальные приравнивает к нулю
        :param result_set: отклик слоя на сходные данные
        :return: 
        """
        min_element = min(result_set)
        index_min_element = result_set.index(min_element)
        result_set = [1 if i == index_min_element else 0 for i in range(len(result_set))]
        return result_set

    def learn(self, input_signal):
        """
        В сетях Кохонена используется обучение без учителя.
        При подаче на вход сети вектора x побеждает тот нейрон,
        вектор весов которого в наименьшей степени отличаются от входного вектора.
        Чаще всего в качестве меры расстояния используется евклидова мера
        Подстройка веса выполняется следующим образом:
            Wnew = Wold + α(X–Wold)
        Wnew - новое значение веса, после корректировки
        Wold - значение веса до корректировки
        X - соответствующая компонента входного сигнала
        α - скорость обучения
        :param input_signal: набор входных сигналов
        """
        if self._normalize:
            input_signal = self.prepared_input_signal(input_signal)
        result_set = []
        for neuron in self._neurons:
            weights = neuron.get_weight()
            deviation = 0
            for i in range(len(weights)):
                deviation += (input_signal[i] - weights[i]) ** 2
            result_set.append(deviation)
        min_deviation = min(result_set)
        index_of_winner_neuron = result_set.index(min_deviation)
        winner_neuron = self._neurons[index_of_winner_neuron]
        weights_neuron = winner_neuron.get_weight()
        for i in range(len(weights_neuron)):
            weights_neuron[i] += self._learn_rate * (input_signal[i] - weights_neuron[i])
        if self._auto_save:
            winner_neuron.save_state()

    @staticmethod
    def prepared_input_signal(source_signal):
        """
        Предварительная обработка входных векторов. Весьма желательно (хотя и не обязательно) 
        нормализовать входные векторы перед тем, как предъявлять их сети. 
        Это выполняется с помощью деления каждой компоненты входного вектора на длину вектора. 
        Эта длина находится извлечением квадратного корня из суммы квадратов компонент вектора.
        :param source_signal: 
        :return: 
        """
        norma = sqrt(sum([x ** 2 for x in source_signal]))
        signals = [x / norma for x in source_signal]
        return signals

    def save_state(self):
        for neuron in self._neurons:
            neuron.save_state()
