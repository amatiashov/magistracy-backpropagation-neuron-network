

class Receiver1(object):
    """
    Выходной сигнал Приемника 1 (G1) равен 1, если хотя бы одна компонента двоичного входного вектора X равна единице;
    однако если хотя бы одна компонента вектора R равна единице, G1 устанавливается в нуль.
    Таблица, определяющая эти соотношения:"""
    _instance = None
    _resolution = None

    def __init__(self):
        self._resolution = True

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def gen_resolution(self, x_vector, r_vector):
        if 1 in r_vector:
            self._resolution = False
            return False

        if 1 in x_vector:
            self._resolution = True
            return True

    def get_resolution(self):
        return self._resolution

    def reset_resolution(self):
        self._resolution = True
