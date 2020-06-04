
"""
            #####                   BACKPROPAGATION                 #####
            #####   АЛГОРИТМ ОБУЧЕНИЯ МНОГОСЛОЙНОЙ НЕЙРОННОЙ СЕТИ   #####
            #####   МЕТОДОМ ОБРАТНОГО РАСПРОСТРАНЕНИЯ ОШИБКИ        #####

Данный тест работает с изображениями в формате BMP. Тест состоит из четырех фаз:
        * инициализация сети
        * обучение сети
        * распознавание изображений
        * анализ эффективности работы
Сначала создается сеть с определенным количеством слоев и нейронов в каждом слое. Затем идет обучение сети.

В папке с шаблонами (TEMPLATE_FOLDER) необходимо создать подкаталоги, каждый каталог - отдельная группа образов,
имя каталога - имя группы. В эти подкаталогах может находится n образов. Число нейронов во внешнем слое
определяется числом каталогов (групп) в папке с шаблонами. Ожидаемый отклик сети формируется автоматически.
Полученный списко групп образов сортируется по алфавиту и в ожидаемом отклике сети для i-ой группы i-ый
элемент массива равен 1, остальные. Далее сканируются все подкаталоги и формируется список образов (images)
в формате [бинарное представление, имя_группы]. Затем в цикле в случайном порядке выбирается образ и выполняется
процесс обучения сети. Процесс повторяется пока все образы не будут выбраны и сеть не обучиться.

В фазе распознавания сканируется каталог folder_for_scan и преобразованные в списки изображения подаются на
вход сети для распознавания. По окончании выводится таблица содержащая названием группы, к которой сеть
сопоставила конкретное изображение.

На этапе анализа эффективности работы на каждый образ накладывается шум (случайно инвертируем n бит
в последовательности), процентное соотношение между шумом и полезными данными задается параметром percent_of_noise.
Далее на вход сети подается зашумленное изображение и сравнивается группа, к которой сети отнесла данный образс той,
что указана в начале файла. В начале имени файла должно содержаться одно из имен групп, которым ранее сеть была
обучена. Пример  seven_824_23v2.bmp (относится к группе seven), car_audiA8.bmp (относится к группе car)
"""
import os
import re
import time
import logging
from random import randint
from datetime import datetime
from util.bmp import bmp_to_binary
from util.easyTables import EasyTables
from util.folder_scaner import folder_scan
from store.service.store_service import StoreService
from next.next import RESOURCES_DIR, Next
from util.network_aggregation import create_net_from_json

# Init configuration
Next.get_instance(config_path=os.path.join(RESOURCES_DIR, "applications", "bp_images_demo_descriptor.yml"),
                  external_check=False)

logger = logging.getLogger(__name__)

# запрос на очищение хранилища перед обучением
delete = input("Clean Store? [N/y]: ").lower()
store = StoreService()
if delete == 'y':
    logger.info("Cleaning store...")
    store.clean()

# learn определяет, нужно ли проводить процесс обучения
confirm = input("Learn? [N/y]: ").lower()
learn = True if confirm == "y" else False

# словарь, хранящий объект сети и служебную информацию
net = create_net_from_json(os.path.join(RESOURCES_DIR, "topologies", "bp_test_topology.json"))
# объект сети
network = net.get("object")
# размер входной последовательности
len_image = network.get_input_size()
# имя нейронной сети. Участвует в формировании имен слоев.
# Формат: "символьное_имя[N1-N2-N3-...-Nm]", где Ni - число нейронов в i слое
NETWORK_NAME = net.get("name")
# папка с образами для обучения. Путь относительно текущей директории
TEMPLATE_FOLDER = net.get("payload").get("template_folder")
# папка с образами для фазы распознавания
RECOGNIZE_FOLDER = net.get("payload").get("recognize_folder")
# получаем список всех групп образов для обучения - список папок с группами
group_list = folder_scan(os.path.join(RESOURCES_DIR, TEMPLATE_FOLDER))
# сортируем для дальнейшего маппинга номера выходного нейрона с именем группы
group_list.sort()

# Для задания числа входных сигналов сети возьмем длину любого шаблона из списка
# Далее проверка наличия шаблонов в папке TEMPLATE_FOLDER
for folder in group_list:
    if not folder_scan(os.path.join(RESOURCES_DIR, TEMPLATE_FOLDER, folder)):
        msg = "Group %s is empty!" % folder
        logger.error(msg)
        raise RuntimeError(msg)


# словарь соответсвтвия. Ключ - имя группы, значение - номер нейрона на выходе сети
group_identify = {}
table = EasyTables(["Group name", "Index of out network"])
logger.debug("Generate mapping...")
for i in range(len(group_list)):
    group_identify[group_list[i]] = i
    table.add_row([group_list[i], i])
    logger.info("Mapping. group: %s index:\t%d" % (group_list[i], i))
table.display()

if learn:
    logger.info("Start learning...")
    start_time = time.time()
    # список образов - [бинарное предстваление образа, имя группы]
    images = []
    # словарь соответствия группы образов и выхода сети
    expect = {}
    for i in range(len(group_list)):
        expect[group_list[i]] = [1 if i == _ else 0 for _ in range(len(group_list))]

        template_group = group_list[i]
        for template in folder_scan(os.path.join(RESOURCES_DIR, TEMPLATE_FOLDER, template_group)):
            binary_image = bmp_to_binary(os.path.join(RESOURCES_DIR, TEMPLATE_FOLDER, template_group, template))
            images.append([binary_image, template_group])

    count_epoch = 0
    complete_learn = False
    while not complete_learn:
        complete_learn = True
        # хранит рание выбранные образы
        memory = set()
        while len(memory) < len(images):
            # индекс следующего образа в images
            next_image = randint(0, len(images)-1)
            if next_image not in memory:
                memory.add(next_image)
                source = images[next_image]
                if not network.learn(source[0], expect[source[1]]):
                    complete_learn = False

        count_epoch += 1
        # каждые n чиклов выводим пргресс обучения
        if count_epoch % 1 == 0:
            table = EasyTables(["Group", "Correct response", "Index", "Full response"])
            for group in group_list:
                for image in images:
                    if image[1] == group:
                        response = list(map(lambda x: round(x, 3), network.calculate(image[0])))
                        correct_out = group_identify[image[1]]
                        table.add_row([group, response[correct_out], correct_out, response])
            table.display()
            print("Learn process. Network name: %s" % NETWORK_NAME)
            print("Count epoch: %d " % count_epoch)
            print("learn temp: %d" % network.get_learn_rate())
            print("Spent time: %s min" % round((time.time() - start_time)/60), 2)

        if count_epoch % 5 == 0:
            start = time.time()
            print("Save state of network {} ({})".format(NETWORK_NAME, datetime.now()))
            network.save_state()
            print("OK! {} sec".format(round(time.time()-start, 2)))

    print("COUNT EPOCH: {}".format(count_epoch))
    print("Spent time: {} sec ({} min)".format(time.time() - start_time, round((time.time() - start_time) / 60), 2))
    print("Save state of network {} ({})".format(NETWORK_NAME, datetime.now()))
    network.save_state()


# """*************************** ФАЗА РАСПОЗНАВАНИЯ ***************************"""
print("Recognize images...")
title = ["File name", "Prediction", "Full response"]
table = EasyTables(title)
for template in folder_scan(os.path.join(RESOURCES_DIR, RECOGNIZE_FOLDER)):
    bin_image = bmp_to_binary(os.path.join(RESOURCES_DIR, RECOGNIZE_FOLDER, template))
    # округление результов распознования
    response = list(map(lambda x: round(x, 3), network.calculate(bin_image)))
    winner_index = response.index(max(response))
    row = [template]
    # поиск группы по индексу максимального выхода сети
    for key in group_identify:
        if group_identify[key] == winner_index:
            row.append(key)
            break
    row.append(response)
    table.add_row(row)
table.display()

"""********************** АНАЛИЗ ЭФФЕКТИВНОСТИ РАБОТЫ **********************"""
# процент зашумления изображения
percent_of_noise = 15
# шаблон поиска имени группы в начале файла
pattern = r"^[a-zA-Z]+"
# список образов в каталоге
image_list = folder_scan(os.path.join(RESOURCES_DIR, RECOGNIZE_FOLDER))
image_list.sort()


# словарь образов. Ключ - имя файла, значение - список
# [бинарное представление, имя_группы]
images = {}
for image in image_list:
    file_name = re.match(pattern, image)
    if file_name:
        images[image] = [bmp_to_binary(os.path.join(RESOURCES_DIR, RECOGNIZE_FOLDER, image)), file_name.group(0)]
    else:
        print("File: <{}>. No matching group found.".format(image))


for noise_level in range(20, 103, 3):
    percent_of_noise = noise_level
    # общее число ошибок распознавания
    count_error = 0
    # число уже обработанных вариантов
    processed_images = 0
    start_time = time.time()
    while processed_images < 10000:
        for image in images:
            processed_images += 1
            cp = images[image][0].copy()

            noise = set()
            while len(noise) < int(len_image*percent_of_noise/100):
                noise.add(randint(0, len_image-1))

            for i in noise:
                cp[i] = 0 if cp[i] else 1
            prediction = network.calculate(cp)
            winner_index = prediction.index(max(prediction))
            group = None
            for key in group_identify:
                if group_identify[key] == winner_index:
                    group = key
                    break

            if group != images[image][1]:
                    count_error += 1
            if processed_images % 100 == 0:
                print("Network name: ", NETWORK_NAME)
                print("Noise level: {}%".format(percent_of_noise))
                print("Remaining {}% ({} images pass)".format(100-processed_images/10000*100, processed_images))
                print("Count of errors -  {}".format(count_error))
                print("Precision {}%".format(round((1-count_error/processed_images)*100, 2)))
                print("time: {} min".format(round((time.time() - start_time)/60, 2)))
                print()
# print("------------------------------")
# print("Network name: ", NETWORK_NAME)
# print("Noise level: {}%".format(percent_of_noise))
# print("Count of errors -  {}".format(count_error))
# print("Count of template", processed_images)
# print("Precision: {}%".format(round((1 - count_error/processed_images)*100, 3)))
