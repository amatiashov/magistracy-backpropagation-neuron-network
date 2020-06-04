
class PerseptronMockStoreService(object):
    """
    Mock персистентного хранилища для Персептрона.
    Не выполняет никаких реальных операций по сохранению и загрузке
    состояния нейрона.
    """

    def save_state(self, obj, mode="baseNeuron"):
        pass

    def load_state(self, obj, mode="baseNeuron"):
        pass

    def clean(self):
        pass
