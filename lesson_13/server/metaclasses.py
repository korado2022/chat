import dis

# Метакласс для проверки соответствия сервера:
class ServerVerifier(type):
    def __init__(self, cls_name, base_classes, cls_dict):
        # cls_name - экземпляр метакласса - Server
        # bases - кортеж базовых классов - ()
        # clsdict - словарь атрибутов и методов экземпляра метакласса
        # {'__module__': '__main__',
        # '__qualname__': 'Server',
        # 'port': <descrptrs.Port object at 0x000000DACC8F5748>,
        # '__init__': <function Server.__init__ at 0x000000DACCE3E378>,
        # 'init_socket': <function Server.init_socket at 0x000000DACCE3E400>,
        # 'main_loop': <function Server.main_loop at 0x000000DACCE3E488>,
        # 'process_message': <function Server.process_message at 0x000000DACCE3E510>,
        # 'process_client_message': <function Server.process_client_message at 0x000000DACCE3E598>}

        # Список методов, которые используются в функциях класса:
        methods = []
        # Атрибуты, используемые в функциях классов
        attrs = []
        # перебираем ключи
        for func in cls_dict:
            # Пробуем
            try:
                # Возвращает итератор по инструкциям в предоставленной функции
                # , методе, строке исходного кода или объекте кода.
                ret = dis.get_instructions(cls_dict[func])
                # ret - <generator object _get_instructions_bytes at 0x00000062EAEAD7C8>
                # ret - <generator object _get_instructions_bytes at 0x00000062EAEADF48>
                # ...
                # Если не функция то ловим исключение
                # (если порт)
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые методы и атрибуты.
                for fn in ret:
                    # print(fn)
                    # fn - Instruction(opname='LOAD_GLOBAL', opcode=116, arg=9, argval='send_message',
                    # argrepr='send_message', offset=308, starts_line=201, is_jump_target=False)
                    # opname - имя для операции
                    if fn.opname == 'LOAD_GLOBAL':
                        if fn.argval not in methods:
                            # заполняем список методами, использующимися в функциях класса
                            methods.append(fn.argval)
                    elif fn.opname == 'LOAD_ATTR':
                        if fn.argval not in attrs:
                            # заполняем список атрибутами, использующимися в функциях класса
                            attrs.append(fn.argval)
        print(methods)
        # Если обнаружено использование недопустимого метода connect, бросаем исключение:
        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        # Если сокет не инициализировался константами SOCK_STREAM(TCP) AF_INET(IPv4), тоже исключение.
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        # Обязательно вызываем конструктор предка:
        super().__init__(cls_name, base_classes, cls_dict)
