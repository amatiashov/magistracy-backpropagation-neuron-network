import hashlib
import os
import shutil
from next.next import Next, RESOURCES_DIR
from werkzeug.security import safe_str_cmp


class FileStore(object):
    """
    Данный класс предназначен сохранения состояний нейрона в файловом хранилище.
    Для получения объект класса необходимо вызвать статический метод get_instance
    """
    _instance = None
    _base_neuron_folder = None
    _art_layers_folder = None
    _art_neurons_folder = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """
        Данный метод реализует паттерн проектирования Singleton
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            # методу __init__ первым аргументом должен передаваться инстанс объекта, но не класс
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self, store_folder=None):
        if not store_folder:
            store_folder = Next.get_instance().get("FILE_STORE").get("base_folder")
        self._store_folder = store_folder
        # каталог для хранения базовых нейронов
        self._base_neuron_folder = os.path.join(RESOURCES_DIR, store_folder, "baseNeurons")
        # каталог для хранения слоев ART
        self._art_layers_folder = os.path.join(RESOURCES_DIR, store_folder, "ART", "layers")
        # каталог для хранения нейронов ART
        self._art_neurons_folder = os.path.join(RESOURCES_DIR, store_folder, "ART", "neurons")

        self.create_service_folder()

    def clean(self):
        """
        Удаляет состояния всех слоев и нейронов в хранилище
        http://stackoverflow.com/a/303225
        :return: 
        """
        shutil.rmtree(os.path.join(RESOURCES_DIR, self._store_folder))
        self.create_service_folder()

    def create_service_folder(self):
        """
        Создает все необходимые каталоги
        :return: 
        """
        if not os.path.exists(self._base_neuron_folder):
            os.makedirs(self._base_neuron_folder)
        if not os.path.exists(self._art_layers_folder):
            os.makedirs(self._art_layers_folder)
        if not os.path.exists(self._art_neurons_folder):
            os.makedirs(self._art_neurons_folder)

    def save_state(self, obj, mode):
        """
        Точка входа для сохранения объектов
        :param obj: сохраняемый объект
        :param mode: режим сохранения:
                        baseNeuron  - сохранение объекта родительского класса BaseNeuron
                        ART.neuron  - сохранение объекта класса RecognizeNeuron
                        ART.layer   - сохранение объекта класса RecognizeLayer
        """
        if mode == "baseNeuron":
            self.save_base_neuron(obj)
        if mode == "ART.layer":
            self.save_art_layer(obj)
        if mode == "ART.neuron":
            self.save_recognize_neuron(obj)

    def load_state(self, obj, mode):
        if mode == "baseNeuron":
            return self.load_base_neuron(obj)
        if mode == "ART.neuron":
            return self.load_recognize_neuron(obj)

    def save_base_neuron(self, neuron):
        """
        Метод для сохранения текущего состояния объекта.
        Формат файла:
        I строка    - name
        II строка   - id
        III число дендритов
        последующие строки являются значением весов по одному на строке
        :param neuron: 
        :return: 
        """
        network_name = neuron.get_name()[:neuron.get_name().index("]")+1]
        if not os.path.exists(os.path.join(self._base_neuron_folder, network_name)):
            os.makedirs(os.path.join(self._base_neuron_folder, network_name))

        try:
            with open(os.path.join(self._base_neuron_folder, network_name, neuron.get_id()), "w") as f:
                f.write("{}\n".format(neuron.get_name()))
                f.write("{}\n".format(neuron.get_id()))
                f.write("{}\n".format(neuron.get_number_of_input_signal()))
                for weight in neuron.get_weight():
                    f.write(str(weight) + '\n')
            return True
        except:
            print("Не удалось сохранить текущее состояние")
            return False

    def load_base_neuron(self, neuron):
        load_success = False

        network_name = neuron.get_name()[:neuron.get_name().index("]")+1]

        try:
            with open(os.path.join(self._base_neuron_folder, network_name, neuron.get_id())) as f:
                # читаем имя нейрона (для пропуска)
                f.readline().strip()
                # читаем id нейрона (для пропуска)
                f.readline().strip()
                number_of_input_signal = int(f.readline().strip())
                if number_of_input_signal != neuron.get_number_of_input_signal():
                    raise ValueError
                weight = []
                for line in f:
                    weight.append(float(line))
                neuron.set_weight(weight)
                load_success = True
        except Exception:
            pass
        return load_success

    def save_art_layer(self, layer):
        id = layer.get_id()
        neurons = layer.get_neuron_list()
        file = None
        try:
            file = open(self._art_layers_folder + id, "w")
            for neuron in neurons:
                file.write(neuron.get_name() + "\n")
        except:
            print("Не удалось сохранить текущее состояние слоя {}".format(layer.get_id()))
        finally:
            if file:
                file.close()

    def save_recognize_neuron(self, neuron):
        """
        Сохранение нейрона в файл.
        Формат файла:
        первые N строк - веса нейрона
        последующие N строк - вектор T, где N - число входов нейрона
        :return: 
        """
        file = None

        try:
            file = open(self._art_neurons_folder + neuron.get_id(), "w")
            for i in range(neuron.get_number_of_input()):
                file.write("{}\n".format(neuron.get_weight()[i]))
            for i in range(neuron.get_number_of_input()):
                file.write("{}\n".format(neuron.get_t_vector()[i]))
        except Exception:
            print("Не удалось сохранить текущее состояние нейрона")
        finally:
            if file:
                file.close()

    def load_recognize_neuron(self, neuron):
        load_success = False
        file = None

        try:
            file = open(self._art_neurons_folder + neuron.get_id(), "r")
            weights = []
            for i in range(neuron.get_number_of_input()):
                weights.append(float(file.readline().strip()))
            neuron._weight = weights
            t_vector = []
            for i in range(neuron.get_number_of_input()):
                t_vector.append(int(file.readline().strip()))
            neuron._t_vector = t_vector
            load_success = True
        except Exception:
            pass
        finally:
            if file:
                file.close()
        return load_success

    def get_recognize_neuron_list(self, layer_id):
        """
        На основании id слоя получаем список всех нейронов, которые принадлежат данному слою
        :param layer_id: идентификатор слоя
        :return: список имен нейронов
        """
        neurons = []
        file = None
        try:
            file = open(self._art_layers_folder + layer_id, "r")
            for line in file:
                neurons.append(line.rstrip())
        except Exception:
            pass
        finally:
            if file:
                file.close()
        return neurons

    def get_client(self, name, password):
        if safe_str_cmp(name, "sysadm"):
            if hashlib.sha256(password.encode()).hexdigest() == hashlib.sha256("sysadm".encode()).hexdigest():
                return dict(name="sysadm",
                            password=hashlib.sha256("sysadm".encode()).hexdigest(),
                            id="7f71c693ea8549478de9054abfaf7f6f")

    def get_client_by_id(self, uuid):
        if uuid == "7f71c693ea8549478de9054abfaf7f6f":
            return dict(name="sysadm",
                        password=hashlib.sha256("sysadm".encode()).hexdigest(),
                        id="7f71c693ea8549478de9054abfaf7f6f")
