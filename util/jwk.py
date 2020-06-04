import random
import string


def gen_secret(length=100):
    """
    Generate random string including ascii and digits
    :param length: length result string
    :return: random string
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


print(gen_secret())

