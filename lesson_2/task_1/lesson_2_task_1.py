"""
Задание 1
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:
    a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
    данными, их открытие и считывание данных. В этой функции из считанных данных
    необходимо с помощью регулярных выражений извлечь значения параметров
    «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
    каждого параметра поместить в соответствующий список. Должно получиться четыре
    списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
    функции создать главный список для хранения данных отчета — например, main_data
    — и поместить в него названия столбцов отчета в виде списка: «Изготовитель
    системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
    столбцов также оформить в виде списка и поместить в файл main_data (также для
    каждого файла);
    b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
    функции реализовать получение данных через вызов функции get_data(), а также
    сохранение подготовленных данных в соответствующий CSV-файл;
    c. Проверить работу программы через вызов функции write_to_csv().

"""

import re
import csv


def get_data():
    """Извлечение данных из файлов txt"""
    list_file = ["info_1.txt", "info_2.txt", "info_3.txt"]

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for f_n in list_file:
        file_obj = open(f_n)
        data = file_obj.read()

        # Получаем изготовителя системы
        os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*').findall(data)[0].split()[2]
        os_prod_list.append(os_prod_reg)

        # Получаем название ОС
        os_name_reg = re.compile(r'Windows\s\S*').findall(data)[0]
        os_name_list.append(os_name_reg)

        # Получаем код продукта
        os_code_reg = re.compile(r'Код продукта:\s*\S*').findall(data)[0].split()[2]
        os_code_list.append(os_code_reg)

        # Получаем тип системы
        os_type_reg = re.compile(r'Тип системы:\s*\S*').findall(data)[0].split()[2]
        os_type_list.append(os_type_reg)

    # Создаем названия столбцов
    headers = ['Номер п.п', 'Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    j = 1
    for i in range(0, 3):
        row_data = []
        row_data.append(j)
        row_data.append(os_prod_list[i])
        row_data.append(os_name_list[i])
        row_data.append(os_code_list[i])
        row_data.append(os_type_list[i])
        main_data.append(row_data)
        j += 1
    return main_data

def write_to_csv(out_file):
    """Запись данных в файл csv"""

    main_data = get_data()
    with open(out_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in main_data:
            writer.writerow(row)


write_to_csv('data_report.csv')
