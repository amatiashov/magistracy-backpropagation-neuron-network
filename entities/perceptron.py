import sys
from entities.base_neuron import BaseNeuron
from store.service.store_service import StoreService


class Perceptron(BaseNeuron):
    """
    Персептронный нейрон
    Умножает каждый вход на соответствующий вес и суммирует взвешенные входы.
    Если эта сумма больше заданного порогового значения, выход равен единице,
    в противном случае – нулю.
    Использует фиктивный входной сигнал с начальным весом -0.5
    """
    _start_weight_x0 = -0.5         # начальный вес фиктивного водного сигнала x0
    _dummy_signal_x0 = 1            # фиктивный сигнал x0
    _learning_temp = 0.1            # темп обучения
    _auto_save = False              # при каждом обучении сохранять ли состояние нейрона?

    def __init__(self, name, number_of_input=2, auto_save=True, store_service=None):
        store = store_service if store_service else StoreService()
        super().__init__(name, number_of_input, store_service=store)
        self._auto_save = auto_save
        # так как используется фиктивный входной сигнал, то необходимо для
        # него установить соответствующий вес
        if len(self._weight) != (number_of_input + 1):
            self._weight.insert(0, self._start_weight_x0)

    def calculate(self, signals):
        """
        Метод для вычисления взвешенной суммы
        :param signals: список входных сигналов
        :return: взвешенная сумма после преобразования активационной функцией
        """
        if len(signals) != self._number_of_input_signal:
            raise ValueError("Число входных сигналов не соответствует числу входов нейрона")

        result = self._dummy_signal_x0 * self._weight[0]
        for i in range(self._number_of_input_signal):
            # так как x0 не содержится в сигнатуре данного метода, а все веса
            # хранятся в едином массиве, к индексу очередного веса необходимо
            # прибавить единицу для правильного соответствия весов сигналам
            result += signals[i] * self._weight[i+1]
        return self.activate(result)

    @staticmethod
    def activate(result):
        """
        Функция активации нейрона - функция, вычисляющая выходной сигнал
        искусственного нейрона. 
        В данном случае используется пороговая функция активации
        :param result: взвешенная сумма (метод calculate).
        :return: 0 или 1
        """
        return 0 if result <= 0 else 1

    def learning(self, signals, expect, display=False):
        """
        Данный метод проводит обучение нейрона.
        В случае, если ожидаемый результат совпадает с вычисленным, обучение прекращается.
        Если же результат не равняется ожидаемому, происходит корректировка весов по
        следующему принципу:
                w[i] = w[i] + (expect - result) * signals[i] * learning_temp.
        Таким образом, в случае, если результат меньше ожидаемого, все веса увеличаться
        на некоторое значение и наоборот.
        Если был указан параметр auto_save происходит автоматическая сохранение состояния
        :param signals: список входных сигналов
        :param expect: ожидаемый отклик нейрона
        :param display: будет ли выводится процесс обучения в консоль
        :return: В случае удачного обучения (результат равен ожидаемому), True, иначе False
        """
        result = self.calculate(signals)
        if display:
            sys.stdout.write("Обучение нейрона. Входные данные: ")
            for i in range(len(signals)):
                sys.stdout.write("x{} = {} ".format(i+1, signals[i]))
            sys.stdout.write("Результат: {} ".format(result))
        if result != expect:
            self._weight[0] += (expect - result) * self._learning_temp * self._dummy_signal_x0
            for i in range(1, len(self._weight)):
                self._weight[i] += (expect - result) * signals[i - 1] * self._learning_temp
            if self._auto_save:
                self.save_state()
            if display:
                print(False)
            return False
        if display:
            print(True)
        return True
