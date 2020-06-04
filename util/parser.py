
class NumberParser(object):
    """
        Данный метод возвращает массив, содержащий информацию о шаблоне.
        Формат файла шаблона:
        I строка - имя шаблона
        II строка - пустая строка
        последующие строки содержат матрицу символов - сам шаблон
        Если символ матрицы входит в template, то в результирующий массив data
        добавляется 1, иначе 0
    """
    @staticmethod
    def parse(path_to_template):
        data = []
        template = ["|", "/", "\\", "-"]
        file = open(path_to_template, encoding="utf-8")
        head = file.readline().rstrip()
        file.readline()
        for line in file:
            for char in line.rstrip():
                if char in template:
                    data.append(1)
                else:
                    data.append(0)
        return [data, head]
