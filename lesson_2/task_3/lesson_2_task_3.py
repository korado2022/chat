"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:
    a. Подготовить данные для записи в виде словаря, в котором первому ключу
    соответствует список, второму — целое число, третьему — вложенный словарь, где
    значение каждого ключа — это целое число с юникод-символом, отсутствующим в
    кодировке ASCII (например, €);
    b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
    При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
    также установить возможность работы с юникодом: allow_unicode = True;
    c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
    с исходными.
"""

import yaml

DATA_IN = {'items': ['computer', 'printer', 'keyboard', 'mouse'],
           'items_quantity': 4,
           'items_ptice': {'notebook': '200¥-1000¥',
                           'printer': '100¥-300¥',
                           'keyboard': '5¥-50¥',
                           'mouse': '4¥-7¥'}
           }

with open('file.yaml', 'w', encoding='utf-8') as f_out:
    yaml.dump(DATA_IN, f_out, default_flow_style=False, allow_unicode=True, sort_keys=False)

with open("file.yaml", 'r', encoding='utf-8') as f_in:
    DATA_OUT = yaml.load(f_in, Loader=yaml.SafeLoader)

print(DATA_IN == DATA_OUT)
