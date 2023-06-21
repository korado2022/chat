import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import List
from typing import Optional
from sqlalchemy import create_engine

from config import SERVER_DATABASE


class Base(DeclarativeBase):
    pass

# Класс - серверная база данных:
class ServerStorage:
    # Класс - отображение таблицы всех пользователей
    # Экземпляр этого класса = запись в таблице AllUsers
    class Users(Base):
        __tablename__ = "users"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(30), unique=True)
        last_login: Mapped[str] = mapped_column(DateTime)


        def __init__(self, username):
            self.name = username
            self.last_login = datetime.datetime.now()
            self.id = None

        def __repr__(self) -> str:
            return f"User(id={self.id!r}, name={self.name!r})"



    # Класс - отображение таблицы активных пользователей:
    # Экземпляр этого класса = запись в таблице ActiveUsers
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
            return f"User_Active(id={self.id!r}, user_id={self.user_id!r})"

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
            return f"Login_History(id={self.id!r}, user_id={self.user_id!r})"

    def __init__(self):
        # Создаём движок базы данных
        # SERVER_DATABASE - sqlite:///server_base.db3
        # echo=False - отключаем ведение лога (вывод sql-запросов)
        # pool_recycle - По умолчанию соединение с БД через 8 часов простоя обрывается.
        # Чтобы это не случилось нужно добавить опцию pool_recycle = 7200 (переуст-ка соед-я через 2 часа)

        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)

        Base.metadata.create_all(self.database_engine)
        # Создаём сессию
        self.session = Session(bind=self.database_engine)

        # Если в таблице активных пользователей есть записи, то их необходимо удалить
        # Когда устанавливаем соединение, очищаем таблицу активных пользователей
        self.session.query(self.UsersActive).delete()
        self.session.commit()

    # Функция выполняющаяся при входе пользователя, записывает в базу факт входа
    def user_login(self, username, ip_address, port):
        print(username, ip_address, port)
        # Запрос в таблицу пользователей на наличие там пользователя с таким именем
        rez = self.session.query(self.Users).filter_by(name=username)
        # print(type(rez))
        print(rez.count())
        # Если имя пользователя уже присутствует в таблице, обновляем время последнего входа
        if rez.count():
            user = rez.first()
            user.last_login = datetime.datetime.now()
        # Если нет, то создаём нового пользователя
        else:
            # Создаем экземпляр класса self.Users, через который передаем данные в таблицу
            user = self.Users(username)
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
    def user_logout(self, username):
        # Запрашиваем пользователя, что покидает нас
        # получаем запись из таблицы Users
        user = self.session.query(self.Users).filter_by(name=username).first()
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
            self.Users.last_login,
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
    def history_login(self, username=None):
        # Запрашиваем историю входа
        query = self.session.query(self.Users.name,
                                   self.LoginHistory.hist_date_time,
                                   self.LoginHistory.hist_ip_addr,
                                   self.LoginHistory.hist_port
                                   ).join(self.Users)
        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.Users.name == username)
        return query.all()


# Отладка
if __name__ == '__main__':
    test_db = ServerStorage()
    # выполняем 'подключение' пользователя
    test_db.user_login('client_1', '192.168.1.4', 8888)
    test_db.user_login('client_2', '192.168.1.5', 7777)
    # выводим список кортежей - активных пользователей
    print(test_db.list_users_active())
    # выполняем 'отключение' пользователя
    test_db.user_logout('client_1')
    # выводим список активных пользователей
    print(test_db.list_users_active())
    # запрашиваем историю входов по пользователю
    test_db.history_login('client_1')
    # выводим список известных пользователей
    print(test_db.list_users())
