import os

from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker, DeclarativeBase, Mapped, mapped_column, Session
from config import *
import datetime

class Base(DeclarativeBase):
    pass


# Класс - база данных сервера.
class ClientDatabase:
    # Класс - отображение таблицы известных пользователей.
    class KnownUsers(Base):
        __tablename__ = "known_users"
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(String(30))

        def __init__(self, username):
            self.id = None
            self.username = username

        def __repr__(self) -> str:
            return f"KnownUsers(id={self.id!r}, username={self.username!r})"

    # Класс - отображение таблицы истории сообщений
    class HistoryMessage(Base):
        __tablename__ = "history_message"
        id: Mapped[int] = mapped_column(primary_key=True)
        from_user: Mapped[str] = mapped_column(String(30))
        to_user: Mapped[str] = mapped_column(String(30))
        message: Mapped[str] = mapped_column(Text)
        date_mess: Mapped[str] = mapped_column(DateTime)


        def __init__(self, from_user, to_user, message):
            self.id = None
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date_mess = datetime.datetime.now()

        def __repr__(self) -> str:
            return f"HistoryMessage(id={self.id!r}, from_user={self.from_user!r}, to_user={self.to_user!r}, " \
                   f"message={self.message!r}, date_mess={self.date_mess!r})"

    # Класс - отображение списка контактов
    class Contacts(Base):
        __tablename__ = "contacts"
        id: Mapped[int] = mapped_column(primary_key=True)
        contact_name: Mapped[str] = mapped_column(String(30), unique=True)

        def __init__(self, contact_name):
            self.id = None
            self.contact_name = contact_name

        def __repr__(self) -> str:
            return f"Contacts(id={self.id!r}, contact_name={self.contact_name!r})"

    # Конструктор класса:
    def __init__(self, username):
        # Создаём движок базы данных, поскольку разрешено несколько клиентов одновременно, каждый должен иметь свою БД
        # Поскольку клиент мультипоточный, необходимо отключить проверки на подключения с разных потоков,
        # иначе sqlite3.ProgrammingError
        path = os.path.dirname(os.path.realpath(__file__))
        filename = f'client_{username}.db3'
        self.database_engine = create_engine(f'sqlite:///client_{username}.db3', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        Base.metadata.create_all(self.database_engine)


        # Создаём сессию
        self.session = Session(bind=self.database_engine)

        # Необходимо очистить таблицу контактов, т.к. при запуске они подгружаются с сервера.
        self.session.query(self.Contacts).delete()
        self.session.commit()

    # Функция добавления контактов
    def add_contact(self, contact_name):
        if not self.session.query(self.Contacts).filter_by(contact_name=contact_name).count():
            contact_row = self.Contacts(contact_name)
            self.session.add(contact_row)
            self.session.commit()

    # Функция удаления контакта
    def del_contact(self, contact_name):
        self.session.query(self.Contacts).filter_by(contact_name=contact_name).delete()

    # Функция добавления известных пользователей.
    # Пользователи получаются только с сервера, поэтому таблица очищается.
    def add_users(self, users_list):
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    # Функция сохраняющая сообщения
    def save_message(self, from_user, to_user, message):
        message_row = self.HistoryMessage(from_user, to_user, message)
        self.session.add(message_row)
        self.session.commit()

    # Функция возвращающая контакты
    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.Contacts.contact_name).all()]

    # Функция возвращающая список известных пользователей
    def get_users(self):
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    # Функция проверяющая наличие пользователя в известных
    def check_user(self, username):
        if self.session.query(self.KnownUsers).filter_by(username=username).count():
            return True
        else:
            return False

    # Функция проверяющая наличие пользователя контактах
    def check_contact(self, contact_name):
        if self.session.query(self.Contacts).filter_by(contacy_name=contact_name).count():
            return True
        else:
            return False

    # Функция возвращающая историю переписки
    def get_history(self, from_who=None, to_who=None):
        query = self.session.query(self.HistoryMessage)
        if from_who:
            query = query.filter_by(from_user=from_who)
        if to_who:
            query = query.filter_by(to_user=to_who)
        return [(history_row.from_user, history_row.to_user, history_row.message, history_row.date_mess)
                for history_row in query.all()]


# отладка
if __name__ == '__main__':
    test_db = ClientDatabase('test1')
    for i in ['test3', 'test4', 'test5']:
        test_db.add_contact(i)
    test_db.add_contact('test4')
    test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    test_db.save_message('test1', 'test2', f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
    test_db.save_message('test2', 'test1', f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
    print(test_db.get_contacts())
    print(test_db.get_users())
    print(test_db.check_user('test1'))
    print(test_db.check_user('test10'))
    print(test_db.get_history('test2'))
    print(test_db.get_history(to_who='test2'))
    print(test_db.get_history('test3'))
    test_db.del_contact('test4')
    print(test_db.get_contacts())
