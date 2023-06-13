"""Кофнфиг клиентского логгера"""

import sys
import os
import logging
from config import LOGGING_LEVEL
sys.path.append('../')

# создаём формировщик логов (formatter):
CLIENT_FORMATTER = logging.Formatter('%(asctime)-30s %(levelname)-12s %(filename)-25s %(message)s')

# Подготовка имени файла для логирования
dir_name = os.path.dirname(os.path.abspath(__file__))
# dir_name = os.getcwd()
# Создаем вложенный каталог
subdir2 = os.path.join(dir_name, "client_logs")
# Проверяем наличие каталога (если нет то создаем)
if not os.path.exists(subdir2):
    os.makedirs(subdir2)
PATH = os.path.join(subdir2, 'client.log')

# создаём потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(CLIENT_FORMATTER)

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
