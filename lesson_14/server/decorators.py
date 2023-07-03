import inspect
import logging
import sys
import traceback
import socket

import logs.config_server_log


LOGGER = logging.getLogger('server')


# Реализация в виде класса
class Log:
    """Класс-декоратор"""
    def __call__(self, func_log):
        def wrap(*args, **kwargs):
            """Обертка"""
            ret = func_log(*args, **kwargs)
            LOGGER.debug(f'Была вызвана функция {func_log.__name__} c параметрами {args}, {kwargs}. '
                         f'Вызов из модуля {func_log.__module__}. Вызов из'
                         f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                         f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
            return ret
        return wrap

def login_required(func):
    '''
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    '''

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр Server
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server import Server
        from config import ACTION, PRESENCE
        if isinstance(args[0], Server):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presense, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
