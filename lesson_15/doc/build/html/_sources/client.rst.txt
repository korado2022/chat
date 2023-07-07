Client module documentation
=================================================

Клиентское приложение для обмена сообщениями. Поддерживает
отправку сообщений пользователям которые находятся в сети, сообщения шифруются
с помощью алгоритма RSA с длинной ключа 2048 bit.

Поддерживает аргументы командной строки:

``python client.py {имя сервера} {порт} -n или --name {имя пользователя} -p или -password {пароль}``

1. {имя сервера} - адрес сервера сообщений.
2. {порт} - порт по которому принимаются подключения
3. -n или --name - имя пользователя с которым произойдёт вход в систему.
4. -p или --password - пароль пользователя.

Все опции командной строки являются необязательными, но имя пользователя и пароль необходимо использовать в паре.

Примеры использования:

* ``python client.py``

*Запуск приложения с параметрами по умолчанию.*

* ``python client.py ip_address some_port``

*Запуск приложения с указанием подключаться к серверу по адресу ip_address:port*

* ``python -n test1 -p 123``

*Запуск приложения с пользователем test1 и паролем 123*

* ``python client.py ip_address some_port -n test1 -p 123``

*Запуск приложения с пользователем test1 и паролем 123 и указанием подключаться к серверу по адресу ip_address:port*

client.py
~~~~~~~~~

.. autofunction:: client.client.arg_parser

client_database.py
~~~~~~~~~~~~~~~~~~

.. autoclass:: client.client_database.ClientDatabase
	:members:
	
transport.py
~~~~~~~~~~~~

.. autoclass:: client.transport.ClientTransport
	:members:

main_window.py
~~~~~~~~~~~~~~

.. autoclass:: client.main_window.ClientMainWindow
	:members:

start_dialog.py
~~~~~~~~~~~~~~~

.. autoclass:: client.start_dialog.UserNameDialog
	:members:


add_contact.py
~~~~~~~~~~~~~~

.. autoclass:: client.add_contact.AddContactDialog
	:members:
	
	
del_contact.py
~~~~~~~~~~~~~~

.. autoclass:: client.del_contact.DelContactDialog
	:members:

decorators.py
~~~~~~~~~~~~~

.. autoclass:: server.decorators.Log
	:members:

.. autofunction:: server.decorators.login_required

errors.py
~~~~~~~~~

.. automodule:: client.errors
	:members:

metaclasses.py
~~~~~~~~~~~~~~

.. autoclass:: client.metaclasses.ClientVerifier
	:members:

Скрипт Logs
---------------------

Содержит конфигурацию для логирования работы клиентского модуля.

* Скрипт config_client_log.py содержит конфигурацию клиентского логгера.

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