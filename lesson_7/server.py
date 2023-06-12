"""Программа-сервер"""
import logging
import time
from socket import *
import sys
import json

import select

import logs.config_server_log
from config import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from utils import get_message, send_message
from decorators import log



#Инициализация логирования сервера.
LOGGER = logging.getLogger('server')

@log
def process_client_message(message, messages_list, client):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :param messages_list:
    :param client:
    :return:
    '''
    LOGGER.debug(f'Получено сообщение от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Sergey':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
             TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    :return:
    '''

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        LOGGER.debug('Не указан номер порта, будет подставлено значение по умолчанию 8079')
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)


    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        LOGGER.debug('Не указан адрес, который будет слушать сервер, слушать будет все')
        print('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет
    print(listen_address)
    print(listen_port)
    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # список клиентов, очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        # client, client_address = transport.accept()
        # try:
        #     message_from_client = get_message(client)
        #     print(message_from_client)
        #     LOGGER.debug(f'Получено сообщение: {message_from_client}')
        #     # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
        #     response = process_client_message(message_from_client)
        #     LOGGER.info(f'Cформирован ответ клиенту: {response}')
        #     send_message(client, response)
        #     LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
        #     client.close()
        # except (ValueError, json.JSONDecodeError):
        #     LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
        #                         f'клиента {client_address}. Соединение закрывается.')
        #     client.close()
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            LOGGER.info(f'Установлено соединение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
