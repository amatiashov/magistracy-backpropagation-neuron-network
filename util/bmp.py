import logging
from PIL import Image
from math import sqrt

logger = logging.getLogger(__name__)

images_cache = dict()


def bmp_to_binary(src, cache=True):
    """
    Функция представления изображения в формате bmp в виде
    массива нулей и единиц (1 - черный цвет, 0 - белый)
    :param src: путь к файлу bmp
    :return: list
    """
    if cache:
        if src in images_cache:
            logger.info("Use cache for %s" % src)
            return images_cache.get(src)
    logger.debug("Opening image by path %s" % src)
    img = Image.open(src)
    pixels = img.load()
    image_bin = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            value = 0 if pixels[i, j] == 255 else 1
            image_bin.append(value)
    images_cache[src] = image_bin
    return image_bin


def show_bmp(array, reverse=False):
    """
    Функция для представления списка нулей и единиц в виде bmp изображения.
    :param array: список нулей и единиц
    :param reverse: инвертирование белых и черных пикселей
    :return: 
    """
    size = int(sqrt(len(array)))
    img = Image.new('1', (size, size))
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if reverse:
                pixels[i, j] = 0 if array.pop(0) else 1
            else:
                pixels[i, j] = array.pop(0)
    img.show()
