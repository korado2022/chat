"""Unit-тесты сервера"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from config import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import process_client_message

class TestServer(unittest.TestCase):
    '''
    В сервере только 1 функция для тестирования
    '''
    dict_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    dict_ok = {RESPONSE: 200}

    def test_action_no(self):
        """Ошибка если нет действия"""
        self.assertEqual(process_client_message(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Sergey'}}), self.dict_err)

    def test_action_wrong(self):
        """Ошибка если неизвестное действие"""
        self.assertEqual(process_client_message(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Sergey'}}), self.dict_err)

    def test_time_no(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Sergey'}}), self.dict_err)

    def test_user_no(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1.1'}), self.dict_err)

    def test_user_unknown(self):
        """Ошибка - не Guest"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Sergey1'}}), self.dict_err)

    def test_check_ok(self):
        """Корректный запрос"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Sergey'}}), self.dict_ok)


if __name__ == '__main__':
    unittest.main()
