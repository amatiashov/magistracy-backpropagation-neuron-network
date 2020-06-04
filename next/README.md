# Next config


Модуль **next** предназначен для предоставления конфигурации другим модулям и пакетам. **Next** - центральный компонент модуля, через который происходит все взаимодействие с ним. Для получения объект данного класса необходимо вызвать метотод _get_instance_:

```python
config = Mext.get_instance(config_path=None, external_check=None)

    # config_path - путь до дискриптора конфигурации [string, not required]
    # external_check - нужно ли выполнять внешние проверки [boolean, not required]
```

## Дескрипторы

Для определения конфигурации используются ini, yaml, json файлы и переменные окружения.

### INI файлы
ini файлы используются исключительно для описания секций и параметров в секции:

```
[SECTION_NAME]
PARAM_NAME = param_value (имя параметра будет lowercase)
```

По умолчанию ищется **config.ini** файл внутри модуля. Вы можете изменить это поведение, задав в качестве значения переменной окружения _CONFIG_PATH_ путь к config.ini файлу.

### YAML and JSON 
С помощью yaml и json файлов можно описывать правила для конфигурации. По умолчанию используется сначала **config.yml**. Если файл не найден, то используется **config.json** внутри модуля
Пример yaml файла:
```yaml
REST_API:
- name: image_folder
  value: images
  sys_environment: REST_API_IMAGE_FOLDER
  required: True    
```

Тот же пример в json формате:
```json
{
    "REST_API": [
        {
           "name": "image_folder",                     // имя параметры в секции (обязательное поле)
           "value": "images",                          // значние По умолчанию  необязательное поле если есть sys_environment)
           "sys_environment": "REST_API_IMAGE_FOLDER", // имя переменной окужения для данного параметра (необязательное поле если есть value)
           "required": true                            // обязателен ли параметр для заполнения   (необязательное поле)
         }
    ]
}
```
 Для получения _image_folder_ параметра нужно прописать следующее:

```python
conf_space = Next.get_instance().get("REST_API")
image_folder = conf_space.get("image_folder")
```

По умолчанию для всех параметров значение поля **required** уставлено в _true_. Если не задано значение поля **value** и не определена соответствующая переменная окужения, будет выброшено исключение.

## Приоритет значений параметра
1.  sys environment
2.  config.yaml
3.  config.json
4.  config.ini

Для работы самого модуля конфигурации необходима секции **APPLICATION** со следующими параметрами:
```yaml
APPLICATION:
- name: log_level
  value: DEBUG
  sys_environment: APP_LOG_LEVEl
  required: True
- name: log_folder
  value: logs
  sys_environment: APP_LOG_FOLDER
```

## External check

Также в модуле предусмотрена возможность реализовать свои собсвенные проверки. Это может быть полезно, когда необходимо проверить, например, вхождение значения какого-либо параметра в орпделенный интервал значений **(10 < x < 20)**, либо на соответвие допустимым значениям **(value in ["a", "b", "c"])**.

Для этого необходимо класс с логикой проверки положить в каталог _external_checks_ (переопределить директорию можно
переменной _external_check_folder_ в **next.py**). Пример проверки можно посмотреть в **example.py**.

Отключить
внешние проверки можно заданием параметра 

    external_check=False

при создании объекта класса **Next**. Имя класса
должно оканчиваться на "Check" - ExampleCheck. Вся проверки выполняется в методе do_check, который в качестве параметра
принимает dic конфигурации.

```python
class ExampleCheck(object):
    order = 2           # задает порядок выполнения проверок. Необязательное поле
    skip = True         # Задается в случае, если необходимо пропустить выполнение данной проверки
```

## Global constants
В модуле доступны следующие константы:
* **BASE_DIR** - абсолютный путь к каталогу приложения, при условии, что config находится в корне приложения
* **RESOURCES_DIR** - resource каталог в приложении.
* **TESTS_RESOURCES_DIR** - resource каталог в каталоге tests

## Global parameters

Для установки глобальных параметров (достпуны в люом месте) во время работы приложения можно использовать метод **set_option**
```python
set_option("global_param", "param_value")
```
Для получения параметра global_param можно использовать метод **get_option**:
```python
glob_param = get_option("global_param")
```
