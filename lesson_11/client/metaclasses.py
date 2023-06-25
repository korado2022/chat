import dis


class ClientVerifier(type):
    def __init__(self, cls_name, base_classes, cls_dict):
        # Список методов, которые используются в функциях класса:
        methods = []
        for func in cls_dict:
            # Пробуем
            try:
                ret = dis.get_instructions(cls_dict[func])
                # Если не функция, то ловим исключение
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые методы.
                for fn in ret:
                    if fn.opname == 'LOAD_GLOBAL':
                        if fn.argval not in methods:
                            methods.append(fn.argval)
        # Если обнаружено использование недопустимого метода accept, listen, socket бросаем исключение:
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе обнаружено использование запрещённого метода')
        # Вызов get_message или send_message из utils считаем корректным использованием сокетов
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(cls_name, base_classes, cls_dict)
