Server module
=================================================

Серверный модуль мессенджера. Обрабатывает словари - сообщения, хранит публичные ключи клиентов.

Использование

Модуль поддерживает аргументы командной строки:

1. -p - Порт на котором принимаются соединения
2. -a - Адрес с которого принимаются соединения.
3. --no_gui Запуск только основных функций, без графической оболочки.

* В данном режиме поддерживается только 1 команда: exit - завершение работы.

Примеры использования:

``python server.py -p 8080``

*Запуск сервера на порту 8080*

``python server.py -a localhost``

*Запуск сервера принимающего только соединения с localhost*

``python server.py --no-gui``

*Запуск без графической оболочки*

server.py
~~~~~~~~~

.. autofunction:: server.server.arg_parser

.. autofunction:: server.server.config_load

.. autoclass:: server.server.Server
	:members:

.. autofunction:: server.server.main

server_database.py
~~~~~~~~~~~~~~~~~~

.. autoclass:: server.server_database.ServerStorage
	:members:

add_user.py
~~~~~~~~~~~

.. autoclass:: server.add_user.RegisterUser
	:members:

config_window.py
~~~~~~~~~~~~~~~~

.. autoclass:: server.config_window.ConfigWindow
	:members:

decorators.py
~~~~~~~~~~~~~

.. autoclass:: server.decorators.Log
	:members:

.. autofunction:: server.decorators.login_required

descriptrs.py
~~~~~~~~~~~~~

.. autoclass:: server.descriptrs.Port
	:members:

.. autoclass:: server.descriptrs.Adress
	:members:

errors.py
~~~~~~~~~

.. automodule:: server.errors
	:members:

main_window.py
~~~~~~~~~~~~~~

.. autoclass:: server.main_window.MainWindow
	:members:

metaclasses.py
~~~~~~~~~~~~~~

.. autoclass:: server.metaclasses.ServerVerifier
	:members:

remove_user.py
~~~~~~~~~~~~~~

.. autoclass:: server.remove_user.DelUserDialog
	:members:

server_gui.py
~~~~~~~~~~~~~

.. automodule:: server.server_gui
	:members:

stat_window.py
~~~~~~~~~~~~~~

.. autoclass:: server.stat_window.StatWindow
	:members:

Скрипт Logs
---------------------

Содержит конфигурацию для логирования работы серверного модуля.

* Скрипт config_server_log.py содержит конфигурацию серверного логгера.


Скрипт utils.py
---------------------

common.utils. **get_message** (client)


	Функция приёма сообщений от удалённых компьютеров. Принимает сообщения JSON,
	декодирует полученное сообщение и проверяет что получен словарь.

common.utils. **send_message** (sock, message)


	Функция отправки словарей через сокет. Кодирует словарь в формат JSON и отправляет через сокет.


Скрипт config.py
---------------------

Содержит разные глобальные переменные проекта.