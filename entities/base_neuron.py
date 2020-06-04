import logging
from hashlib import md5
from random import random
from store.service.store_service import StoreService
from next.next import get_option


class BaseNeuron(object):
    _id = None                      # уникальный идентификатор нейрона в рамках конкретного слоя
    _name = None                    # последовательность символов для удобства идентификации нейрона
    _number_of_input_signal = None  # число входных сигналов нейрона
    _weight = None                  # массив весов входных сигналов

    _store_service = None           # объект сервиса, занимающегося хранением и получением состояния нейрона
    _logger = None

    def __init__(self, name, number_of_input=2, auto_load=True, gen_random_weight=True, store_service=None):
        """
        Для идентификации нейрона внутри слоя и внутри сети, для последующего сохранения и
        загрузки его состояния необходимо некое поле для хранения уникальной
        последовательности, которая будет являться идентификатором.
        Для этого используется поле _id, которое хранит md5 хеш.
        Правило генерации имени нейрона:
            {имя слоя, которому принадлежит нейрон} + {#} + {порядковый номер нейрона в слое}:

                new_layer#0 - нулевой нейрон в слое с именем "new_layer"

        :param name:                имя нейрона
        :param number_of_input:     число дендритов нейрона
        :param auto_load:           автоматическая загрузка состояния при инициализации
        :param gen_random_weight:   автоматическая генерация весовых коэффициентов по числу входов
        """
        self._logger = logging.getLogger(__name__)
        if name is None:
            raise ValueError("name must be not None")
        self._store_service = store_service or get_option("base_neuron_store") or StoreService()
        self.set_number_of_input_signal(number_of_input)
        self._name = name

        self._logger.debug("Neuron <{}> is initializing".format(self._name))
        # генерация уникального идентификатора
        self._id = self._generate_id()

        if auto_load:
            load_success = self.load_state()
            self._logger.debug("Downloading state from storage .... {}".format(load_success))
            if not load_success and gen_random_weight:
                self._logger.debug("Generating random weights....")
                # генерация начальных случайных весов
                self._weight = self.generate_random_weight(self._number_of_input_signal)
        self._logger.debug("Initialization success!\n\n")

    def _generate_id(self):
        if self._name is None:
            raise ValueError("Name must be not null")
        # пример генерации взят отсюда
        # http://stackoverflow.com/questions/5297448/how-to-get-md5-sum-of-a-string
        return md5(self._name.encode('utf-8')).hexdigest()

    def calculate(self, signals):
        """
        Метод для вычисления взвешенной суммы
        :param signals: список входных сигналов
        :return: взвешенная сумма
        """
        if len(signals) != self._number_of_input_signal:
            raise ValueError("Число входных сигналов не соответствует числу входов нейрона")
        result = 0
        for i in range(self._number_of_input_signal):
            result += signals[i] * self._weight[i]
        return result

    @staticmethod
    def generate_random_weight(number_of_weight):
        """
        Метод генерации случайных весов входных сигналов.
        :param number_of_weight: количество необходимых весов 
        :return: список случайных весов в пределах от -0.5 до 0.5
        """
        weight = []
        for i in range(number_of_weight):
            weight.append(random() - 0.5)
        return weight

    def print_state(self, short_output=True, print_step=10):
        """
        Данный метод выводит в консоли текущее состояние нейрона:
        его уникальный идентификатор, число дендритов и веса.
        :param short_output: вывод всех весов в консоли
        :param print_step:  шаг вывода весов
        :return: 
        """
        print("Текущие состояние нейрона <{}>:".format(self._name))
        print("ID: {}".format(self._id))
        print("Число дендритов: {}".format(self._number_of_input_signal))

        step = print_step if short_output else 1
        for i in range(0, len(self._weight), step):
            print("weight[{}] = {}".format(i, self._weight[i]))

    def set_number_of_input_signal(self, number_of_input_signal):
        if number_of_input_signal < 2:
            raise ValueError("Число входов не может быть меньше 2")
        self._number_of_input_signal = number_of_input_signal

    def set_weight(self, weight):
        self._weight = weight

    def save_state(self):
        self._store_service.save_state(self)

    def load_state(self):
        return self._store_service.load_state(self)

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_number_of_input_signal(self):
        return self._number_of_input_signal

    def get_weight(self):
        return self._weight
