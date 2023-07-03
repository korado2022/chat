"""Конфиг серверного логгера"""

import sys
import os
import logging
import logging.handlers
from config import LOGGING_LEVEL
# sys.path.append('../')

# создаём формировщик логов (formatter):
SERVER_FORMATTER = logging.Formatter('%(asctime)-30s %(levelname)-12s %(filename)-25s %(message)s')

# Подготовка имени файла для логирования
# dir_name = os.getcwd()
dir_name = os.path.dirname(os.path.abspath(__file__))
# Создаем вложенный каталог
subdir1 = os.path.join(dir_name, "server_logs")
# Проверяем наличие каталога (если нет то создаем)
if not os.path.exists(subdir1):
    os.makedirs(subdir1)

PATH = os.path.join(subdir1, 'server.log')

# создаём потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
