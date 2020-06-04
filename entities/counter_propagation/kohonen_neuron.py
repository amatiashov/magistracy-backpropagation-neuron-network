from math import sqrt
from random import random
from entities.base_neuron import BaseNeuron


class KohonenNeuron(BaseNeuron):

    def __init__(self, name, number_of_input=2):
        neuron_name = name + "{kohonen_neuron}"
        # для нейрона Кохонена первоначальная инициализация весов
        # выполняется не генерацией случайных чисел, поэтому выключим автоматическую
        super().__init__(neuron_name, number_of_input, gen_random_weight=False)
        # присваиваем всем весам нейрона Кохонена значение по
        # методу выпуклой комбинации (convex combination method)
        # Информация взята из книги Ф.Уоссермена "Нейрокомпьютерная техника: Теория и практика"
        # Глава 4. "Сети встречного распространения"
        # присваивать веса нужно только в том случае, если они не были взяты из
        # хранилища
        if not self._weight:
            norma = 1 / sqrt(number_of_input)
            # К каждому весу прибавляем небольшое отклонение
            normal_weight = [norma + 0.1 * random() for i in range(number_of_input)]
            self.set_weight(normal_weight)

    def calculate(self, source_signals):
        """
        Режим функционирования нейрона Кохонена заключается в вычислении скалярного
        произведения вектора весов на вектор входных сигналов. Фактически это можно
        интерпретировать как поиск наилучшего соответствия вектора входного сигнала
        к вектору весов одного из нейронов. Выигрывает тот нейрон, у которого скалярное
        произведение самое большое - максимальное соответствие вектору входных сигналов
        :param source_signals: список входных сигналов
        :return: 
        """
        return super().calculate(source_signals)
