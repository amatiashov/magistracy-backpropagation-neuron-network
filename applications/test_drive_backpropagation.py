import os
from util.parser import NumberParser
from util.folder_scaner import folder_scan
from entities.backpropagation.layer import Layer
from entities.backpropagation.network import Network
from next.next import RESOURCES_DIR, set_option
from store.impl.perceptron_mock_store import PerseptronMockStoreService

"""
            #####                   BACKPROPAGATION                 #####
            #####   АЛГОРИТМ ОБУЧЕНИЯ МНОГОСЛОЙНОЙ НЕЙРОННОЙ СЕТИ   #####
            #####   МЕТОДОМ ОБРАТНОГО РАСПРОСТРАНЕНИЯ ОШИБКИ        #####

    Суть данного теста в следующем. Необходимо создать несколько слое, затем связать их в сеть.
    Провести процедуру обучения на всех имеющихся образах (шаблоны чисел в папке TEMPLATE_FOLDER)
    и затем, изменяя входные данные (внося исправления в шаблоны из папки TEMPLATE_FOLDER),
    наблюдать за вычислением сети.
    Шаблоны сканируются автоматически. Список ожидаемого отклика формируется следующим образом:
    для i-ого шаблона i-ый элемент в списке выставляется равным единице, остальные нулю.
"""

set_option("base_neuron_store", PerseptronMockStoreService())

# имя нейронной сети. Участвует в формировании имен слоев
NETWORK_NAME = "template_number"
# папка с образами для обучения. Путь относительно текущей директории
TEMPLATE_FOLDER = "digit_templates"

# получаем список всех образов для обучения
templates = folder_scan(os.path.join(RESOURCES_DIR, TEMPLATE_FOLDER))
templates.sort()

# Для задания числа входных сигналов сети возьмем длину любого шаблона из списка
len_input_data = len(NumberParser.parse(os.path.join(RESOURCES_DIR, TEMPLATE_FOLDER, templates[0]))[0])

# Создаем нулевой слой сети.
# number_of_input_signal равен числу входных сигналов.
# number_neurons_in_layer определяет число нейронов в слое и
# так же число выходов самого слоя
layer0 = Layer(name="{}#0".format(NETWORK_NAME),  number_of_input_signal=len_input_data,
               number_neurons_in_layer=7)
# При создании второго слоя в сети необходимо выставить number_of_input_signal
# равным числу выходов предыдущего слоя.
# Экспериментальное наблюдение: если число нейронов в данном слое (layer1) равно 10,
# сеть учится наиболее быстро и более устойчива к помехам в образах
layer1 = Layer(name="{}#1".format(NETWORK_NAME),  number_of_input_signal=7,
               number_neurons_in_layer=10)
# Число нейронов в последнем слое в данном случае равно
# числу распознаваемых образов - длине списка templates
layer2 = Layer(name="{}#2".format(NETWORK_NAME),  number_of_input_signal=10,
               number_neurons_in_layer=len(templates))


network = Network()

network.add_layer(layer0)
network.add_layer(layer1)
network.add_layer(layer2)

# формируем список входных данных шаблонов
data = []
for i in range(len(templates)):
    data.append(NumberParser.parse(os.path.join(RESOURCES_DIR, TEMPLATE_FOLDER, templates[i])))

# learn определяет, нужно ли проводить процесс обучения
learn = True

if learn:
    # формируем списки ожидаемого отклика сети.
    expects = []
    for i in range(len(templates)):
        expect = [0 for x in range(len(templates))]
        expect[i] = 1
        expects.append(expect)
    count_epoch = 0
    result = False
    while not result:
        result = True
        for i in range(len(templates)):
            if not network.learn(data[i][0], expects[i]):
                result = False
        count_epoch += 1
        if count_epoch % 500 == 0:
            for i in range(len(templates)):
                result_set = network.calculate(data[i][0])
                print("{} -> ".format(data[i][1]), list(map(lambda x: round(x, 3), result_set)))
            print("----------")
            # FIXME!!!
            print("learn temp = ", network._learning_rate)
    print("COUNT EPOCH = ", count_epoch)
if learn:
    network.save_state()

for i in range(len(templates)):
    result = network.calculate(data[i][0])
    print("{}) {}  ->\t".format(i+1, data[i][1]), list(map(lambda x: round(x, 3), result)))
