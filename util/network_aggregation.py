import json
import logging
from entities.backpropagation.layer import Layer
from entities.backpropagation.network import Network

logger = logging.getLogger(__name__)


def create_net_from_json(fp):
    """
    Выполняет парсинг json файла и подготавливает все необходимы данные для
    дальнейшей работы
    :param fp: путь к файлу json
    :return: dict, содержащий объект Network и пути к служебным каталогам
    """

    logger.debug("Opening network topology %s" % fp)
    with open(fp) as f:
        data = json.loads(f.read())

    logger.debug(json.dumps(data, indent=4, ensure_ascii=False))

    network_name = data["network"]["name"]
    logger.debug("network name: %s", network_name)
    layers_description = network_name[network_name.index("[") + 1: network_name.index("]")]
    layers_description = layers_description.split("-")
    layers_description = list(map(lambda x: int(x), layers_description))

    layers = [Layer(name=network_name + "#0",
                    number_of_input_signal=data["network"]["input_size"],
                    number_neurons_in_layer=layers_description[0])]
    for i in range(1, len(layers_description)):
        layer = Layer(name=network_name + "#" + str(i),
                      number_of_input_signal=layers_description[i - 1],
                      number_neurons_in_layer=layers_description[i])
        layers.append(layer)

    rate = None
    if not data["network"].get("auto_rate"):
        rate = data["network"]["rate"]

    network = Network(auto_correct_learn_rate=data["network"].get("auto rate", False),
                      learn_rate=rate)
    for layer in layers:
        network.add_layer(layer)
    return {"name": network_name, "object": network, "payload": data.get("payload")}
