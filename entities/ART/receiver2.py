
class Receiver2(object):
    """
    Выход Приемника 2, равен единице, если входной вектор X имеет хотя бы одну единичную компоненту.
    Более точно, G2 является логическим ИЛИ от компонента вектора X.
    """
    _instance = None
    _resolution = None

    def __init__(self):
        self._resolution = False

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def gen_resolution(self, x_vector):
        self._resolution = 1 if 1 in x_vector else 0
        return self._resolution

    def get_resolution(self):
        return self._resolution

    def reset_resolution(self):
        self._resolution = False
