from entities.perceptron import Perceptron
from store.impl.perceptron_mock_store import PerseptronMockStoreService

# Обучение нейрона вычислению бинарной операции ИЛИ. Число входов = 2

neuron = Perceptron(name="OR_2INPUT", number_of_input=2, auto_save=True, store_service=PerseptronMockStoreService())

neuron.learning([0, 0], 0, display=True)
neuron.learning([0, 1], 1, display=True)
neuron.learning([1, 0], 1, display=True)
neuron.learning([1, 1], 1, display=True)

print("0 OR 0 = {}".format(neuron.calculate([0, 0])))
print("0 OR 1 = {}".format(neuron.calculate([0, 1])))
print("1 OR 0 = {}".format(neuron.calculate([1, 0])))
print("1 OR 1 = {}".format(neuron.calculate([1, 1])))

# Обучение нейрона вычислению бинарной операции И. Число входов = 3
neuron = Perceptron(name="AND_3INPUT", number_of_input=3, auto_save=True, store_service=PerseptronMockStoreService())

neuron.learning([0, 0, 0], 0, display=True)
neuron.learning([1, 1, 1], 1, display=True)
neuron.learning([1, 0, 1], 0, display=True)
neuron.learning([0, 1, 0], 0, display=True)
neuron.learning([0, 1, 1], 0, display=True)

print("1 AND 1 AND 1 = {}".format(neuron.calculate([1, 1, 1])))
print("0 AND 0 AND 0 = {}".format(neuron.calculate([0, 0, 0])))
print("0 AND 1 AND 0 = {}".format(neuron.calculate([0, 1, 0])))
print("1 AND 0 AND 1 = {}".format(neuron.calculate([1, 0, 1])))
print("0 AND 1 AND 1 = {}".format(neuron.calculate([0, 1, 1])))
print("0 AND 1 AND 0 = {}".format(neuron.calculate([0, 1, 0])))


# Обучение нейрона вычислению бинарной операции ИЛИ. Число входов = 4
neuron = Perceptron(name="OR_4INPUT", number_of_input=4, auto_save=True, store_service=PerseptronMockStoreService())
neuron.learning([0, 0, 0, 0], 0, display=True)
neuron.learning([1, 0, 1, 0], 1, display=True)
neuron.learning([0, 1, 0, 1], 1, display=True)
neuron.learning([1, 1, 1, 0], 1, display=True)
neuron.learning([0, 1, 0, 0], 1, display=True)
neuron.learning([0, 1, 1, 1], 1, display=True)

print("0 OR 0 OR 0 OR 0 = {}".format(neuron.calculate([0, 0, 0, 0])))
print("0 OR 1 OR 0 OR 1 = {}".format(neuron.calculate([0, 1, 0, 1])))
print("1 OR 0 OR 1 OR 0 = {}".format(neuron.calculate([1, 0, 1, 0])))
print("1 OR 1 OR 1 OR 0 = {}".format(neuron.calculate([1, 1, 1, 0])))
print("0 OR 1 OR 1 OR 1 = {}".format(neuron.calculate([0, 1, 1, 1])))
print("0 OR 1 OR 0 OR 0 = {}".format(neuron.calculate([0, 1, 0, 0])))


# # Обучение нейрона вычислению бинарной операции И. Число входов = 4
neuron = Perceptron(name="AND_4INPUT", number_of_input=4, auto_save=True, store_service=PerseptronMockStoreService())
neuron.learning([0, 0, 0, 0], 0, display=True)
neuron.learning([0, 1, 0, 1], 0, display=True)
neuron.learning([1, 0, 1, 0], 0, display=True)
neuron.learning([1, 1, 1, 0], 0, display=True)
neuron.learning([0, 1, 1, 1], 0, display=True)
neuron.learning([1, 1, 1, 1], 1, display=True)

print("1 AND 1 AND 1 AND 1 = {}".format(neuron.calculate([1, 1, 1, 1])))
print("0 AND 1 AND 1 AND 1 = {}".format(neuron.calculate([0, 1, 1, 1])))
print("0 AND 0 AND 0 AND 0 = {}".format(neuron.calculate([0, 0, 0, 0])))
print("0 AND 1 AND 0 AND 1 = {}".format(neuron.calculate([0, 1, 0, 1])))
print("1 AND 0 AND 1 AND 0 = {}".format(neuron.calculate([1, 0, 1, 0])))
print("1 AND 1 AND 1 AND 0 = {}".format(neuron.calculate([1, 1, 1, 0])))
print("0 AND 1 AND 0 AND 0 = {}".format(neuron.calculate([0, 1, 0, 0])))


# Обучение нейрона вычислению бинарной операции ИЛИ. Число входов = 5
neuron = Perceptron(name="OR_5_INPUT", number_of_input=5, auto_save=True, store_service=PerseptronMockStoreService())
neuron.learning([0, 0, 0, 0, 0], 0, display=True)
neuron.learning([0, 0, 1, 0, 0], 1, display=True)
neuron.learning([1, 0, 0, 0, 0], 1, display=True)
neuron.learning([0, 0, 0, 0, 1], 1, display=True)
neuron.learning([1, 0, 1, 0, 1], 1, display=True)
neuron.learning([1, 1, 1, 0, 1], 1, display=True)
neuron.learning([0, 1, 0, 0, 0], 1, display=True)
neuron.learning([0, 1, 1, 1, 0], 1, display=True)

print("0 OR 0 OR 0 OR 0 OR 0 = {}".format(neuron.calculate([0, 0, 0, 0, 0])))
print("1 OR 0 OR 0 OR 0 OR 0 = {}".format(neuron.calculate([1, 0, 0, 0, 0])))
print("0 OR 0 OR 1 OR 0 OR 0 = {}".format(neuron.calculate([0, 0, 1, 0, 0])))
print("0 OR 0 OR 0 OR 0 OR 1 = {}".format(neuron.calculate([0, 0, 0, 0, 1])))
print("0 OR 1 OR 0 OR 1 OR 0 = {}".format(neuron.calculate([0, 1, 0, 1, 0])))
print("1 OR 0 OR 1 OR 0 OR 1 = {}".format(neuron.calculate([1, 0, 1, 0, 1])))
print("1 OR 1 OR 1 OR 0 OR 0 = {}".format(neuron.calculate([1, 1, 1, 0, 0])))
print("0 OR 1 OR 1 OR 1 OR 1 = {}".format(neuron.calculate([0, 1, 1, 1, 1])))
print("0 OR 1 OR 0 OR 0 OR 1 = {}".format(neuron.calculate([0, 1, 0, 0, 1])))
print("1 OR 1 OR 1 OR 1 OR 1 = {}".format(neuron.calculate([1, 1, 1, 1, 1])))
