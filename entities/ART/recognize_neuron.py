import sys
from math import exp
from store.service.store_service import StoreService
from util.id_generator import generate_id


class RecognizeNeuron(object):
    """
    В процессе функционирования каждый нейрон слоя распознавания вычисляет свертку
    вектора собственных весов и входного вектора C.
    Нейрон, имеющий веса, наиболее близкие вектору C, будет иметь самый большой выход,
    тем самым выигрывая соревнование и одновременно затормаживая все остальные нейроны в слое.
    """
    _is_ready = None
    _t_vector = None
    _weight = None
    _number_of_input = None
    _store_service = None
    _name = None
    _id = None

    def __init__(self, name, number_of_input):
        self._store_service = StoreService()
        self._is_ready = True
        self._number_of_input = number_of_input
        self._name = name
        self._id = generate_id(name)
        sys.stdout.write("Создание нейрона < {} >. Загрузка состояния :".format(name))
        load_success = self._store_service.load_state(obj=self, mode="ART.neuron")
        print(load_success)
        if not load_success:
            # Веса вектора инициализируются в одинаковые малые значения.
            # Эти значения должны удовлетворять условию:
            # weight < L / (L - 1 + number_of_input), обычно L = 2
            weight = 2 / (1 + number_of_input) - 0.01
            self._weight = [weight for _ in range(number_of_input)]
            # Веса вектора T все инициализируются в единичные значения
            self._t_vector = [1 for _ in range(number_of_input)]

    def wrap(self, input_signal):
        """
        В процессе функционирования каждый нейрон слоя распознавания вычисляет свертку вектора
        собственных весов и входного вектора C.
        Нейрон, имеющий веса, наиболее близкие вектору C, будет иметь самый большой выход,
        тем самым выигрывая соревнование и одновременно затормаживая все остальные нейроны в слое.
        :param input_signal: входной вектор C
        :return: 
        """
        response = 0
        for i in range(self._number_of_input):
            response += input_signal[i] * self._weight[i]
        return response
        # conv = convolve(input_signal, self._weight, "same")
        # return sum(conv)

    @staticmethod
    def activate(result, alpha=1):
        """
        Функция активации нейрона - функция, вычисляющая выходной сигнал
        искусственного нейрона. На вход принимает значение,
        полученной от сумматора (метод calculate).
        В данном методе применяется сигмоидальная функция активации,
        значения которой лежат в интервале от 0 до 0.(9)
        Ссылка на статью, посвященную описанию функций активации:
        http://www.aiportal.ru/articles/neural-networks/activation-function.html
        :param result: 
        :param alpha:   параметр наклона сигмоидальной функции активации, изменяя
                        этот параметр, можно построить функции с различной крутизной.
        :return: 
        """
        return 1.0 / (1 + exp(-alpha * result))

    def get_t_vector(self):
        return self._t_vector

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_number_of_input(self):
        return self._number_of_input

    def get_weight(self):
        return self._weight

    def turn_off(self):
        self._is_ready = False

    def turn_on(self):
        self._is_ready = True

    def is_ready(self):
        return self._is_ready

    def set_weights(self, weights):
        if len(weights) != self._number_of_input:
            raise ValueError("Число весов должно равняться {}".format(self._number_of_input))
        self._weight = weights

    def set_t_vector(self, t_vector):
        self._t_vector = t_vector

    def save_state(self):
        self._store_service.save_state(obj=self, mode="ART.neuron")

