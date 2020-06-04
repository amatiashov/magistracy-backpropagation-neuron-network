import os
from next.next import RESOURCES_DIR
from util.parser import NumberParser
from util.easyTables import EasyTables
from entities.perceptron import Perceptron
from util.folder_scaner import folder_scan
from store.impl.perceptron_mock_store import PerseptronMockStoreService

template_folder = os.path.join(RESOURCES_DIR, "digit_templates")
# инициализируем персептрон для проверки четности числа
perceptron = Perceptron(name="even", number_of_input=66, store_service=PerseptronMockStoreService())

# получаем список всех файлов в папке шаблонов
list_of_numbers = folder_scan(template_folder)

# словарь соответствия буквенных названий цифр и числовых
numbers = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
           "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

# генерируем словарь с именами шаблонов и массивом данных
templates = {}
for template_name in list_of_numbers:
    resources = NumberParser.parse("{}/{}".format(template_folder, template_name))
    templates[numbers[template_name]] = resources[0]

# для сортировки результата работы в таблице (чтобы числа шли от меньшего к большему)
# отсортируем ключи в словаре шаблонов
keys = []
for key in templates:
    keys.append(key)
keys.sort()

# обучение нейрона. Если число четное, ожидаем единицу, иначе 0
learn_complete = False
while not learn_complete:
    learn_complete = True
    for number in keys:
        expect_result = 1 if number % 2 == 0 else 0
        learn_result = perceptron.learning(templates[number], expect_result)
        if not learn_result:
            learn_complete = False

table = EasyTables(["Число", "Четное? (да/нет)", "Результат"])
for number in keys:
    result = perceptron.calculate(templates[number])
    answer = "да" if result > 0.9 else "нет"
    table.add_row([number, answer, result])
table.display()
