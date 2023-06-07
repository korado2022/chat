import inspect
import logging
import sys
import traceback
import logs.config_server_log
import logs.config_client_log


if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    LOGGER = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('client')


# Реализация в виде функции
def log(func_log):
    """Функция-декоратор"""
    def wrap(*args, **kwargs):
        """Обертка"""
        ret = func_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_log.__module__}. Вызов из'
                     f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return ret
    return wrap

