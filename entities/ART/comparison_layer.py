from entities.ART.comparison_neuron import ComparisonNeuron


class ComparisonLayer(object):
    """
     Слой сравнения получает двоичный входной вектор Х и первоначально пропускает его неизмененным
     для формирования выходного вектора "C". На более поздней фазе в распознающем слое вырабатывается
     двоичный вектор "R", модифицирующий вектор "C".
    """
    _comparison_neurons = None
    _number_of_input = None

    def __init__(self, number_of_input=5):
        self._number_of_input = number_of_input
        self._comparison_neurons = [ComparisonNeuron() for _ in range(number_of_input)]

    def compare(self, input_signal, R_vector):
        if len(input_signal) != self._number_of_input:
            raise ValueError("Число входных сигналов должно равняться {}".format(self._number_of_input))
        if len(R_vector) != self._number_of_input:
            raise ValueError("Длина вектора R должна равняться {}".format(self._number_of_input))

        out = []
        for i in range(len(input_signal)):
            out.append(self._comparison_neurons[i].compare(input_signal[i], R_vector[i]))
        return out
