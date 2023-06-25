import argparse
import datetime
import sys

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import List
from typing import Optional
from sqlalchemy import create_engine



class Base(DeclarativeBase):
    pass

# Класс - серверная база данных:
class ServerStorage:
    # Класс - отображение таблицы всех пользователей
    # Экземпляр этого класса = запись в таблице Users
    class Users(Base):
        __tablename__ = "users"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(30), unique=True)
        last_login: Mapped[str] = mapped_column(DateTime)


        def __init__(self, name):
            self.name = name
            self.last_login = datetime.datetime.now()
            self.id = None

        def __repr__(self) -> str:
            return f"User(id={self.id!r}, name={self.name!r})"



    # Класс - отображение таблицы активных пользователей:
    # Экземпляр этого класса = запись в таблице UsersActive
    class UsersActive(Base):
        __tablename__ = "users_active"
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
        ip_address: Mapped[str] = mapped_column(String(15))
        port: Mapped[int] = mapped_column(Integer)
        login_time: Mapped[str] = mapped_column(DateTime)


        def __init__(self, user_id, ip_address, port, login_time):
            self.user_id = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

        def __repr__(self) -> str:
            return f"UsersActive(id={self.id!r}, user_id={self.user_id!r}, ip_address={self.ip_address!r}, " \
                   f"port={self.port!r}, login_time={self.login_time!r})"

    # Класс - отображение таблицы истории входов
    # Экземпляр этого класса = запись в таблице LoginHistory
    class LoginHistory(Base):
        __tablename__ = "login_history"
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
        hist_date_time: Mapped[str] = mapped_column(DateTime)
        hist_ip_addr: Mapped[str] = mapped_column(String(15))
        hist_port: Mapped[int] = mapped_column(Integer)

        def __init__(self, user_id, date, ip, port):
            self.id = None
            self.user_id = user_id
            self.hist_date_time = date
            self.hist_ip_addr = ip
            self.hist_port = port

        def __repr__(self) -> str:
            return f"LoginHistory(id={self.id!r}, user_id={self.user_id!r})"

    # Класс - отображение таблицы контактов пользователей
    class UsersContacts(Base):
        __tablename__ = "contacts"
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
        contact_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

        def __init__(self, user_id, contact_id):
            self.id = None
            self.user = user_id
            self.contact_id = contact_id

        def __repr__(self) -> str:
            return f"UsersContacts(id={self.id!r}, user_id={self.user_id!r}, contact_id={self.contact_id!r})"

    # Класс отображение таблицы истории действий
    class UsersHistory(Base):
        __tablename__ = "users_history"
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
        sent: Mapped[int] = mapped_column(Integer)
        accepted: Mapped[int] = mapped_column(Integer)

        def __init__(self, user_id):
            self.id = None
            self.user_id = user_id
            self.sent = 0
            self.accepted = 0

        def __repr__(self) -> str:
            return f"UsersHistory(id={self.id!r}, user_id={self.user_id!r}, sent={self.sent!r}, accepted={self.accepted!r})"

    def __init__(self, path):
        # Создаём движок базы данных
        # SERVER_DATABASE - sqlite:///server_base.db3
        # echo=False - отключаем ведение лога (вывод sql-запросов)
        # pool_recycle - По умолчанию соединение с БД через 8 часов простоя обрывается.
        # Чтобы это не случилось нужно добавить опцию pool_recycle = 7200 (переуст-ка соед-я через 2 часа)

        # Создаём движок базы данных
        print(path)
        self.database_engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        Base.metadata.create_all(self.database_engine)
        # Создаём сессию
        self.session = Session(bind=self.database_engine)

        # Если в таблице активных пользователей есть записи, то их необходимо удалить
        # Когда устанавливаем соединение, очищаем таблицу активных пользователей
        self.session.query(self.UsersActive).delete()
        self.session.commit()

    # Функция выполняющаяся при входе пользователя, записывает в базу факт входа
    def user_login(self, name, ip_address, port):
        print(name, ip_address, port)
        # Запрос в таблицу пользователей на наличие там пользователя с таким именем
        rez = self.session.query(self.Users).filter_by(name=name)
        # print(type(rez))
        # print(rez.count())
        # Если имя пользователя уже присутствует в таблице, обновляем время последнего входа
        if rez.count():
            user = rez.first()
            user.last_login = datetime.datetime.now()
        # Если нет, то создаём нового пользователя
        else:
            # Создаем экземпляр класса self.Users, через который передаем данные в таблицу
            user = self.Users(name)
            self.session.add(user)
            # Комит здесь нужен, чтобы присвоился ID
            self.session.commit()

        # Теперь можно создать запись в таблицу активных пользователей о факте входа.
        # Создаем экземпляр класса self.UsersActive, через который передаем данные в таблицу
        new_active_user = self.UsersActive(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        # и сохранить в историю входов
        # Создаем экземпляр класса self.LoginHistory, через который передаем данные в таблицу
        history = self.LoginHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(history)

        # Сохраняем изменения
        self.session.commit()

    # Функция фиксирующая отключение пользователя
    def user_logout(self, name):
        # Запрашиваем пользователя, что покидает нас
        # получаем запись из таблицы Users
        user = self.session.query(self.Users).filter_by(name=name).first()
        # print(f"user_logout: {user}")
        # Удаляем его из таблицы активных пользователей.
        # Удаляем запись из таблицы ActiveUsers
        self.session.query(self.UsersActive).filter_by(user_id=user.id).delete()


        # Применяем изменения
        self.session.commit()

    # Функция возвращает список известных пользователей со временем последнего входа.
    def list_users(self):
        query = self.session.query(
            self.Users.name,
            self.Users.last_login
        )
        # Возвращаем список кортежей
        return query.all()

    # Функция возвращает список активных пользователей
    def list_users_active(self):
        # Запрашиваем соединение таблиц и собираем кортежи имя, адрес, порт, время.
        query = self.session.query(
            self.Users.name,
            self.UsersActive.ip_address,
            self.UsersActive.port,
            self.UsersActive.login_time
        ).join(self.Users)
        # Возвращаем список кортежей
        return query.all()

    # Функция возвращающая историю входов по пользователю или всем пользователям
    def history_login(self, name=None):
        # Запрашиваем историю входа
        query = self.session.query(self.Users.name,
                                   self.LoginHistory.hist_date_time,
                                   self.LoginHistory.hist_ip_addr,
                                   self.LoginHistory.hist_port
                                   ).join(self.Users)
        # Если было указано имя пользователя, то фильтруем по нему
        if name:
            query = query.filter(self.Users.name == name)
        return query.all()

    # Функция фиксирует передачу сообщения и делает соответствующие отметки в БД
    def process_message(self, sender, recipient):
        # Получаем ID отправителя и получателя
        sender_id = self.session.query(self.Users).filter_by(name=sender).first().id
        recipient_id = self.session.query(self.Users).filter_by(name=recipient).first().id
        # Запрашиваем строки из истории и увеличиваем счётчики
        sender_row = self.session.query(self.UsersHistory).filter_by(user_id=sender_id).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UsersHistory).filter_by(user_id=recipient_id).first()
        recipient_row.accepted += 1

        self.session.commit()

    # Функция добавляет контакт для пользователя.
    def add_contact(self, user, contact):
        # Получаем ID пользователей
        user = self.session.query(self.Users).filter_by(name=user).first().id
        contact = self.session.query(self.Users).filter_by(name=contact).first().id

        # Проверяем что не дубль и что контакт может существовать (полю пользователь мы доверяем)
        if not contact or self.session.query(self.UsersContacts).filter_by(user_id=user.id,
                                                                           contact_id=contact.id).count():
            return

        # Создаём объект и заносим его в базу
        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    # Функция удаляет контакт из базы данных
    def remove_contact(self, user, contact):
        # Получаем ID пользователей
        user = self.session.query(self.Users).filter_by(name=user).first().id
        contact = self.session.query(self.Users).filter_by(name=contact).first().id

        # Проверяем что контакт может существовать (полю пользователь мы доверяем)
        if not contact:
            return

        # Удаляем требуемое
        print(self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user_id == user.id,
            self.UsersContacts.contact_id == contact.id
        ).delete())
        self.session.commit()

    # Функция возвращает список контактов пользователя.
    def get_contacts(self, name):
        # Запрашиваем указанного пользователя
        user = self.session.query(self.Users).filter_by(name=name).one()

        # Запрашиваем его список контактов
        query = self.session.query(self.UsersContacts, self.Users.name). \
            filter_by(user_id=user.id). \
            join(self.Users, self.UsersContacts.contact_id == self.Users.id)

        # выбираем только имена пользователей и возвращаем их.
        return [contact[1] for contact in query.all()]

    # Функция возвращает количество переданных и полученных сообщений
    def history_message(self):
        query = self.session.query(
            self.Users.name,
            self.Users.last_login,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.Users)
        # Возвращаем список кортежей
        return query.all()




# Отладка
if __name__ == '__main__':
    test_db = ServerStorage()
    # выполняем 'подключение' пользователя
    test_db.user_login('client_1', '192.168.1.4', 8888)
    test_db.user_login('client_2', '192.168.1.5', 7777)
    test_db.user_login('client_3', '192.168.1.14', 8889)
    test_db.user_login('client_4', '192.168.1.15', 7778)
    print(test_db.list_users())
    # выводим список кортежей - активных пользователей
    # print(test_db.list_users_active())
    # выполняем 'отключение' пользователя
    # test_db.user_logout('client_1')
    # выводим список активных пользователей
    # print(test_db.list_users_active())
    # запрашиваем историю входов по пользователю
    # test_db.history_login('client_1')
    # выводим список известных пользователей
    # print(test_db.list_users())
    # test_db.process_message('client_3', 'client_4')
    # print(test_db.history_message())

