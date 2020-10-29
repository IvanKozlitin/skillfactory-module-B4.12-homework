# испортируем модуль стандартнй библиотеки и datetime
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.Float)

class Athelete(Base):
    """
    Описывает структуру таблицы athelete для хранения данных атлетов
    """
    # задаем название таблицы
    __tablename__ = 'athelete'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст
    age = sa.Column(sa.Integer)
    # дата рождения (пример: 1990-05-21)
    birthdate = sa.Column(sa.Text)
    # пол
    gender = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.Float)
    # имя
    name = sa.Column(sa.Text)
    # вес
    weight = sa.Column(sa.Integer)
    # золотый медали
    gold_medals = sa.Column(sa.Integer)
    # серебрянные медали
    silver_medals = sa.Column(sa.Integer)
    # бронзовые медали
    bronze_medals = sa.Column(sa.Integer)
    # всего медалей
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Свой пол (Male / Female): ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("А также дата твоего рождения (В таком формате 1990-05-21): ")
    height = input("И в заключение, твой рост (В таком формате 1.82): ")
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user

def find(id_user, session): #!!!!! Переделать + вывести в отдельный модуль + users.py тоже вывести в отдельный модуль
    """
    Производит поиск пользователя в таблице user по заданному id и находит ближайших атлетов по воросту и росту
    """
    # нахдим пользователя по id в таблице user
    query = session.query(User).filter(User.id == id_user)
    # Проверяем нашли ли пользователя по id, если нет то возвращаем значения None
    if query.count() == 0:
        return (None, None, None)
    # записываем данные пользователя
    data_user = query[0]
    # создаём переменную для хранения данных атлета наиболее близкого к пользователю по дню рождению
    result_athelete_birthdate = {"birthdate": "1000-01-01"}
    # создаём переменную для хранения данных атлета наиболее близкого к пользователю по росту
    result_athelete_athelete_height = {"height": 0.0}
    # запрашиваем данные всех атлелтов
    query_athelete = session.query(Athelete)

    for one_athelete in query_athelete:
        # Сверяем данные итерируемого ателета с лучшим результатом на данный момент, если его результат лучше, то записываем его
        if one_athelete.height is not None:
            if abs((one_athelete.height) - data_user.height) < abs(result_athelete_athelete_height.get("height") - data_user.height):
                result_athelete_athelete_height["height"] = one_athelete.height
                athelete_height = one_athelete

        # разбиваем данные года, месяца и числа для дальнейшей вставки
        time_one_athelete = one_athelete.birthdate.split('-')
        time_result_athelete_birthdate = result_athelete_birthdate.get("birthdate").split('-')
        time_data_user = data_user.birthdate.split('-')
        time_1 = datetime.datetime(int(time_one_athelete[0]), int(time_one_athelete[1]), int(time_one_athelete[2]))
        time_2 = datetime.datetime(int(time_result_athelete_birthdate[0]), int(time_result_athelete_birthdate[1]), int(time_result_athelete_birthdate[2]))
        time_3 = datetime.datetime(int(time_data_user[0]), int(time_data_user[1]), int(time_data_user[2]))

        if abs((time_1 - time_3).days) < abs((time_2 - time_3).days):
            result_athelete_birthdate["birthdate"] = one_athelete.birthdate
            athelete_birthdate = one_athelete

    return (athelete_birthdate, athelete_height, data_user)

def print_users_list(athelete_birthdate, athelete_height, data_user):
    """
    Выводит на экран о запрошенном пользователе и атлетах, что ближе к нему по росту и восрасту
    Если не найден такой пользователь, то даём соответствующее сообщение
    """
    # проверяем на наличие пользователя
    if athelete_birthdate is not None and athelete_height is not None and data_user is not None:
        # выводим нужные данные
        print("ID запрошенного пользователя: {id}, его имя: {name}, дата рождения {date}, и рост {height}\n".format(id=data_user.id, name=(data_user.first_name + " " + data_user.last_name), date=data_user.birthdate, height=data_user.height))
        # выводим данные ателта ближайшего по росту
        print("ID атлета ближайшего по росту: {id}, его имя: {name}, и рост {height}\n".format(id=athelete_height.id, name=athelete_height.name, height=athelete_height.height))
        # выводим данные ателта ближайшего по дате рождения
        print("ID атлета ближайшего по дате рождения: {id}, его имя: {name}, и дата рождения {date}\n".format(id=athelete_birthdate.id, name=athelete_birthdate.name, date=athelete_birthdate.birthdate))
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Пользователя с таким id нет.")


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти пользователя по id и ближайших к нему спортсменов по дате рождения и росту\n2 - ввести данные нового пользователя\n")
    # проверяем режим
    if mode == "1":
        # выбран режим поиска, запускаем его
        id_user = input("Введи id пользователя для поиска: ")
        # вызываем функцию поиска по id
        athelete_birthdate, athelete_height, data_user = find(id_user, session)
        # вызываем функцию печати на экран результатов поиска
        print_users_list(athelete_birthdate, athelete_height, data_user)
    elif mode == "2":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        print("Некорректный режим:(")


if __name__ == "__main__":
    main()