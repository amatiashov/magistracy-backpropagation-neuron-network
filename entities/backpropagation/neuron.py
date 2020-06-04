from math import exp
from entities.base_neuron import BaseNeuron
import decimal
import numpy as np


class Neuron(BaseNeuron):

    def __init__(self, name, number_of_input=2):
        super().__init__(name, number_of_input)

    def calculate(self, signals):
        """
        Метод для вычисления результаты работы нейрона
        :param signals: список входных сигналов, 0 или 1
        :return: 
        """
        result = super().calculate(signals)
        return self.activate(result)

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
        # return 1.0 / (1 + np.exp(-alpha * result, dtype=np.float128))

