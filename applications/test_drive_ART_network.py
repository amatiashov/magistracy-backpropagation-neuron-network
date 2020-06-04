"""
Проверка работы сети адаптивно резонансной теории
"""
import os
from PIL import Image
from entities.ART.network import Network
from util import folder_scaner
from next.next import BASE_DIR

def parse_image(src):
    """
    Функция представления изображения в формате bmp в виде
    массива нулей и единиц (0 - черный цвет, 1 - белый)
    :param src: путь к файлу bmp
    :return: list 
    """
    img = Image.open(src)
    pixels = img.load()
    data = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            value = 1 if pixels[i, j] == 255 else 0
            data.append(value)
    img.close()
    return data


def list_to_image(array):
    """
    Функция для представления списка нулей и единиц в виде bmp изображения.
    :param array: список нулей и единиц
    :return: 
    """
    img = Image.new('1', (100, 100))
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = array.pop(0)
    img.show()

# папка с образами
image_folder = os.path.join(BASE_DIR, "number_images")
# список образов в папке
templates = folder_scaner.folder_scan(image_folder)

# объект сети АРТ. Каждое изображение имеет разрешение 100x100, поэтому число входов = 10000
network = Network(name="IMAGE_NUMBERS", number_of_input=10000, auto_save=False)


print("----------------- {} -----------------".format("Фаза обучения"))

for template in templates:
    # в цикле проходим по всем образам и подаем их на вход сети
    image = image_folder + template
    print("template: ", template)
    out = network.recognize(parse_image(image))
    print()

print("----------------- {} -----------------".format("Фаза тестирования"))

image_folder = os.path.join(BASE_DIR, "number_images")
templates = folder_scaner.folder_scan(image_folder)
for template in templates:
    image = image_folder + template
    print("test template: ", template)
    copy = parse_image(image)
    data = parse_image(image)
    response = network.recognize(data)
    print()
    list_to_image(response)
