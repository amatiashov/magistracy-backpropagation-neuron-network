from entities.ART.receiver1 import Receiver1


class ComparisonNeuron(object):
    """
    Каждый нейрон в слое сравнения получает три двоичных входа:
    1. компонента хi входного вектора X;
    2. cигнал обратной связи Ri – взвешенная сумма выходов распознающего слоя;
    3. вход от Приемника 1 (один и тот же сигнал подается на все нейроны этого слоя).
    """
    _receiver1 = None

    def __init__(self):
        self._receiver1 = Receiver1.get_instance()

    def compare(self, input_signal, Ri):
        """
        Чтобы получить на выходе нейрона единичное значение, как минимум два из
        трех его входов должны равняться единице; в противном случае его выход будет нулевым.
        Таким образом реализуется правило двух третей.
        :param input_signal: компонента вектора X
        :param Ri: компонента вектора R
        :return: 
        """
        resolution = self._receiver1.get_resolution()
        if sum([resolution, input_signal, Ri]) > 1:
            return 1
        else:
            return 0
