

class ResetModule(object):
    """
    Модуль сброса измеряет сходство между векторами X и C.
    Если они отличаются сильнее, чем требует параметр сходства, вырабатывается сигнал сброса
    возбужденного нейрона в слое распознавания.
    """

    @staticmethod
    def decide(x_vector, c_vector):
        """
        В процессе функционирования модуль сброса вычисляет сходство как отношение количества единиц
        в векторе C к их количеству в векторе C.
        Если это отношение ниже значения параметра сходства, вырабатывается сигнал сброса.
        :param x_vector: двоичный вектор входного сигнала
        :param c_vector: вектор "запомненного" образа
        :return: 
        """
        D = sum(x_vector)
        N = sum(c_vector)
        S = N / D
        if S >= 0.8:
            return True
        return False
