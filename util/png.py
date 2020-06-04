import logging
from PIL import Image
from math import sqrt

logger = logging.getLogger(__name__)

images_cache = dict()


def png_to_binary(src, cache=True):
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
            pixel = pixels[i, j]
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            image_bin.append((r + g + b) // 3 / 255)
    images_cache[src] = image_bin
    return image_bin
