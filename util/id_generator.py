from hashlib import md5


def generate_id(identifier):
    if identifier is None:
        raise ValueError("Identifier must be not null")
    # пример генерации взят отсюда
    # http://stackoverflow.com/questions/5297448/how-to-get-md5-sum-of-a-string
    return md5(identifier.encode('utf-8')).hexdigest()
