import inspect
import logging
import sys
import traceback
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

