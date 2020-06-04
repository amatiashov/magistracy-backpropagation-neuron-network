import math

import logging


class Network(object):
    _layers = None              # список слоев в сети
    _auto_save = False          # автоматическое сохранение состояния слоев после обучения

    _tolerance = 0.1            # допустимая ошибка при обучении сети
    _learning_rate = 0.1        # темп обучения
    _correct_lear_rate = None   # автоматическая постройка скорости обучения
    _logger = None

    def __init__(self, auto_save=False, auto_correct_learn_rate=True, learn_rate=None):
        self._logger = logging.getLogger(__name__)
        self._layers = []
        self._auto_save = auto_save
        self._correct_lear_rate = auto_correct_learn_rate
        if learn_rate:
            self._learning_rate = learn_rate

    def add_layer(self, layer, index=None):
        """
        Добавление слоев в сеть
        :param layer: объект слоя
        :param index: место в списке _layers. Если не указан, то добавиться в конец
        :return: 
        """
        if index:
            self._layers.insert(index, layer)
        else:
            self._layers.append(layer)

    def calculate(self, input_signals):
        """
        Метод для вычисления результата работы сети
        На вход первому слою подается набор input_signals,
        далее результат работы каждого слоя подается на вход следующему слою
        :param input_signals: входной сигнал для сети
        :return: список выходов последнего слоя в сети
        """
        intermediate = self._layers[0].calculate(input_signals)
        for i in range(1, len(self._layers)):
            intermediate = self._layers[i].calculate(intermediate)
        return intermediate

    def learn(self, input_signal, expect):
        """
        Метод для обучения сети.
        http://www.aiportal.ru/articles/neural-networks/back-propagation.html
        Алгоритм обучения отличается для последнего и скрытых слоев, поэтому они
        разделены на два отдельных метода.
        :param input_signal: набор входных данных для обучения
        :param expect: ожидаемый отклик сети на input_signal
        :return: True, если ошибка не превышает _tolerance, иначе False
        """

        # алгоритм для постройки весов использует результат работы
        # предыдущего слоя, поэтому необходимо сначала получить результат
        # работы для каждого слоя
        self.calculate(input_signal)

        if self._correct_lear_rate:
            self._correct_learn_rate(expect)

        # формируем список входных сигналов для последнего слоя сети.
        # Если в сети более одного слоя, то для последнего слоя входные
        # данные - результат работы предыдущего слоя.
        data = input_signal
        if len(self._layers) > 1:
            data = self._layers[-2].get_result_set()
        out = self._learn_last_layer(data, expect)
        # если ошибка превысила порог, выполняем подстроку весов всех
        # скрытых слоев
        if not out:
            # обратный цикл начиная с предпоследнего слоя в сети
            for i in range(len(self._layers)-2, -1, -1):
                # Алгоритм обратного распространения ошибки использует для подстройки
                # весов текущего слоя в качестве входных сигналов результат работы
                # предыдущего слоя для последнего слоя входным сигналом является
                # список input_signal для каждого следующего - результат работы предыдущего слоя
                if i == 0:
                    input_data = input_signal
                else:
                    input_data = self._layers[i-1].get_result_set()
                self._learn_hidden_layer(layer_index=i, input_data=input_data)

        return out

    def _learn_last_layer(self, source_signal, expect):
        """
        Подстройка весов выходного слоя.
        Так как для каждого нейрона выходного слоя задано целевое значение,
        то подстройка весов легко осуществляется с использованием модифицированного дельта-правила
        :param source_signal: список входных сигналов для последнего слоя
        :param expect: список ожидаемого отклика сети
        :return: результат обучения сети. True, если ошибка меньше _tolerance, иначе False
        """
        learn_complete = True
        # получаем объект последнего слоя в сети
        layer = self._layers[-1]
        # получаем ссылку на список
        sigmas = layer.get_sigmas()
        # получаем список нейронов в слое
        neurons = layer.get_neuron_list()
        # получаем результат работы последнего слоя
        result_set = layer.get_result_set()
        for i in range(len(neurons)):
            # Если модуль разности полученного значения больше допустимого порога
            # ошибки _tolerance, корректируем веса текущего нейрона
            if math.fabs(result_set[i] - expect[i]) > self._tolerance:
                learn_complete = False
                neuron_weight = neurons[i].get_weight()
                # введем переменную сигма, равную разности между требуемым expect[i] и реальным result
                # выходами, умноженной на производную функции активации
                sigma = result_set[i] * (1 - result_set[i]) * (expect[i] - result_set[i])
                sigmas[i] = sigma
                for j in range(len(neuron_weight)):
                    neuron_weight[j] += sigma * source_signal[j] * self._learning_rate
        if not learn_complete and self._auto_save:
            layer.save_state()
        return learn_complete

    def _learn_hidden_layer(self, layer_index, input_data):
        """
        Подстройка весов скрытых слоев      
        :param layer_index: номер слоя в сети
        :param input_data: список входных сигналов для слоя
        :return: 
        """
        # получаем список нейронов слоя
        neurons = self._layers[layer_index].get_neuron_list()
        # получаем список ошибок sigma текущего слоя
        sigmas = self._layers[layer_index].get_sigmas()
        # получаем результат работы слоя
        result_set = self._layers[layer_index].get_result_set()
        for i in range(len(neurons)):
            neuron = neurons[i]
            result = result_set[i]
            # введем переменную сигма, равную производной функции активации, умноженной
            # на взвешенную сумму сигм следующего слоя
            sigma = result * (1 - result) * self._layers[layer_index+1].get_weighted_synaptic_sum(i)
            sigmas[i] = sigma
            neuron_weight = neuron.get_weight()
            for j in range(len(neuron_weight)):
                neuron_weight[j] += self._learning_rate * sigma * input_data[j]
        if self._auto_save:
            self._layers[layer_index].save_state()

    def _correct_learn_rate(self, expect):
        """
        Метод динамически изменяет темп обучения нейрона в зависимости от величины
        Вычисляем сумму квадратов разности между ожидаемым откликом сети (expect)
        и реально полученными значениями. Затем нормируем полученную сумму на количество
        нейронов в слое и извлекаем корень - то есть получаем среднее значение ошибки.
        Это значение плюс некоторое число, ужно для задания некоторого нижнего порога
        скорости и является темпом обучения     
        :param expect: 
        :return: 
        """
        squared_sum_errors = 0
        result = self._layers[-1].get_result_set()
        for i in range(len(expect)):
            squared_sum_errors += (expect[i] - result[i]) ** 2
        avg_error = math.sqrt(squared_sum_errors / len(result))
        self._learning_rate = avg_error + 0.05

    def save_state(self):
        for layer in self._layers:
            layer.save_state()

    def get_all_neurons(self):
        neurons = []
        for layer in self._layers:
            for neuron in layer.get_neuron_list():
                neurons.append(neuron)
        return neurons

    def get_input_size(self):
        if not self._layers:
            return None
        return self._layers[0].get_input_size()

    def get_learn_rate(self):
        return self._learning_rate

