"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
этого:
    a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
    (item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция
    должна предусматривать запись данных в виде словаря в файл orders.json. При
    записи данных указать величину отступа в 4 пробельных символа;
    b. Проверить работу программы через вызов функции write_order_to_json() с передачей
    в нее значений каждого параметра.
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    """Запись в файл json"""

    with open('orders.json', 'r', encoding='utf-8') as f_in:
        data = json.load(f_in)

    with open('orders.json', 'w', encoding='utf-8') as f_out:
        orders_list = data['orders']
        order_info = {'item': item, 'quantity': quantity,
                      'price': price, 'buyer': buyer, 'date': date}
        orders_list.append(order_info)
        json.dump(data, f_out, indent=4, ensure_ascii=False)


write_order_to_json('принтер', '5', '8200', 'Николаев С.П.', '15.03.2014')
write_order_to_json('сканер', '10', '12000', 'Веселков П.Р.', '03.02.2015')
write_order_to_json('компьютер', '15', '23000', 'Шумилов С.Н.', '26.07.2016')
