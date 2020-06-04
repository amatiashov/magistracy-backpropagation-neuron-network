from entities.ART.comparison_layer import ComparisonLayer
from entities.ART.receiver1 import Receiver1
from entities.ART.receiver2 import Receiver2
from entities.ART.recognize_layer import RecognizeLayer
from entities.ART.reset_module import ResetModule


class Network(object):
    """
    Процесс классификации в APT состоит из трех основных фаз: распознавание, сравнение и поиск.
    """
    _receiver1 = None           # объект приемника 1
    _receiver2 = None           # объект приемника 2
    _comparison_layer = None    # объект слоя сравнения
    _recognize_layer = None     # объект слоя распознавания
    _winner_neuron = None       # нейрон, который является победителем в слое распознавания
    _auto_save = None

    def __init__(self, name, number_of_input, auto_save=True):
        """
        :param name: имя сети. На основании данного параметра генерируются
                    имя слоя распознавания и имена нейронов этого слоя   
        :param number_of_input: число входов сети - длина вектора данных
        :param auto_save: автоматическое сохранение состояния сети после обучения нейрона
        """
        self._auto_save = auto_save
        self._receiver1 = Receiver1.get_instance()
        self._receiver2 = Receiver2.get_instance()
        self._comparison_layer = ComparisonLayer(number_of_input=number_of_input)
        self._recognize_layer = RecognizeLayer(name, number_of_input=number_of_input)

    def recognize(self, input_signal):
        self._recognize_layer.activate_all_neuron()
        image_found = False

        while self._recognize_layer.get_number_of_active_neuron() > 0:
            r_vector = self.do_recognition_phase(x_vector=input_signal)
            c_vector = self.do_comparison_phase(x_vector=input_signal, r_vector=r_vector)
            response = self.do_search_phase(x_vector=input_signal, c_vector=c_vector)
            # Если образ из памяти не соответствует входному, возбужденный нейрон в слое распознавания тормозится.
            # Этот процесс повторяется до тех пор, пока не встретится одно из двух событий:
            if response:
                # 1. Найден запомненный образ, сходство которого с вектором input_signal выше уровня параметра сходства.
                # Проводится обучающий цикл, в процессе которого модифицируются веса векторов T и B,
                # связанных с возбужденным нейроном в слое распознавания.
                self.learn(neuron=self._winner_neuron, image=c_vector)
                image_found = True
                print("Найден похожий образ")
                break
        if image_found:
            return self._winner_neuron.get_t_vector().copy()
        print("Образ не найден. Создание нового нейрона...")
        # 2. Все запомненные образы проверены, определено, что они не соответствуют входному вектору,
        # и все нейроны слоя распознавания заторможены. В этом случае создается новый нейрон для этого
        # образа и его весовые векторы B и T устанавливаются соответствующими новому входному образу.
        new_neuron = self._recognize_layer.create_neuron()
        self.learn(neuron=new_neuron, image=input_signal)
        return new_neuron.get_t_vector().copy()

    def do_recognition_phase(self, x_vector):
        # В начальный момент времени входной вектор отсутствует на входе сети;
        # следовательно, все компоненты входного вектора X можно рассматривать как нулевые.
        # Тем самым сигнал G2 устанавливается в 0
        # следовательно, в нуль устанавливаются выходы всех нейронов слоя распознавания.
        self._receiver2.reset_resolution()
        # Затем на вход сети подается входной вектор X, который должен быть классифицирован.
        # Этот вектор должен иметь одну или более компонент, отличных от нуля,
        r_vector = self._recognize_layer.recognize(input_signal=x_vector)
        # в результате чего и G1, и G2 становятся равными единице.
        self._receiver1.gen_resolution(x_vector, r_vector)
        self._receiver2.gen_resolution(x_vector)
        c_vector = self._comparison_layer.compare(x_vector, r_vector)
        # Для каждого нейрона в слое распознавания вычисляется свертка вектора его весов и вектора C.
        # Нейрон с максимальным значением свертки имеет веса, наилучшим образом соответствующие входному вектору.
        # Он выигрывает конкуренцию и возбуждается, одновременно затормаживая все остальные нейроны этого слоя.
        # Таким образом, единственная компонента Rj вектора R становится равной единице,
        # а все остальные компоненты становятся равными нулю.
        r_vector = self._recognize_layer.recognize(input_signal=c_vector)
        return r_vector

    def do_comparison_phase(self, x_vector, r_vector):
        # Единственный возбужденный в слое распознавания нейрон возвращает единицу обратно в слой сравнения
        # в виде своего выходного сигнала Rj
        # Так как вектор r_vector не является больше нулевым, сигнал receiver1 устанавливается в нуль.
        # Таким образом, в соответствии с правилом двух третей, возбудиться могут только нейроны,
        # получающие на входе одновременно единицы от входного вектора X и вектора t_vector.
        self._receiver1.gen_resolution(x_vector, r_vector)
        index_winner_neuron = r_vector.index(1)
        self._winner_neuron = self._recognize_layer.get_neuron_by_index(index_winner_neuron)
        t_vector = self._winner_neuron.get_t_vector()
        c_vector = self._comparison_layer.compare(x_vector, t_vector)
        return c_vector

    def do_search_phase(self, x_vector, c_vector):
        if ResetModule.decide(x_vector, c_vector):
            # Если не выработан сигнал сброса, сходство является адекватным,
            # и процесс классификации завершается.
            return True
        # В противном случае другие запомненные образы должны быть исследованы
        # с целью поиска лучшего соответствия.
        self._winner_neuron.turn_off()
        return False

    def learn(self, neuron, image):
        """
        Обучение представляет собой процесс, в котором набор входных векторов подается последовательно на
        вход сети и веса сети изменяются при этом таким образом, чтобы сходные векторы активизировали
        соответствующие нейроны. Это – неуправляемое обучение, нет учителя и нет целевого вектора,
        определяющего требуемый ответ.
        :param neuron: 
        :return: 
        """
        s = sum(image)
        weights = [2*i / (2 - 1 + s) for i in image]
        neuron.set_weights(weights)
        neuron.set_t_vector(image.copy())
        if self._auto_save:
            neuron.save_state()
            self.save_state(layer_only=True)

    def save_state(self, layer_only=False):
        """
        Сохранение состояния сети
        :param layer_only: сохранить только список нейронов в слое без сохранения состояния нейронов
        :return: 
        """
        self._recognize_layer.save_state(layer_only)
