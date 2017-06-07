import sqlite3
import os.path as Path
import datetime

from collections import OrderedDict, namedtuple

SQL_INSERT_GOAL = """
            INSERT INTO diary (task, text, deadline) VALUES (?, ?, ?)
            """

SQL_SELECT_ALL = """
    SELECT
        id, task, text, deadline,
    CASE (status)
        WHEN 1
        THEN "Выполнено"
        ELSE "Не выполнено"
        END "OTHER"
    FROM
        diary
"""

SQL_EDIT_GOAL = """
            UPDATE diary SET task = (?) WHERE id = (?)
"""

SQL_EDIT_COMMENTS = """
            UPDATE diary SET text = (?) WHERE id = (?)
"""

SQL_EDIT_DATE = """
            UPDATE diary SET deadline = (?) WHERE id = (?)
"""

SQL_EDIT_STATUS_OFF = """
            UPDATE diary SET status = 1 WHERE id = (?)
"""

SQL_EDIT_STATUS_ON = """
            UPDATE diary SET status = 0 WHERE id = (?)
"""



EditAction = namedtuple("Action", ["func", "name"])
EditActions = OrderedDict()


def edit_action(cmd, name):
    def decorator(func):
        EditActions[cmd] = EditAction(func = func, name = name)
        return func
    return decorator


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect(db_name=None):
    """Немного измененная функций sqlite3.connect"""
    if db_name is None:
        db_name = ':memory:'
        
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    return conn


def initialize(conn):
    """Функция создания БД, если ее нет"""
    with conn:
        script_file_path = Path.join(Path.dirname(__file__), 'schema.sql')

    with open(script_file_path) as f:
        conn.executescript(f.read())



def add_goal(conn, goal, comment, deadline):
    """Принимает цель, комментарий и дату выполнения. Добавляет соответствующую запись в таблицу.""" 
    with conn:
        cursor = conn.execute(SQL_INSERT_GOAL, (goal, comment, deadline,))
    return 

@edit_action("1", "Изменить задачу")
def edit_goal(conn, pk):
    """Функция изменяет цель в записи по номеру"""
    goal = input("Введите новую формулировку задачи:\n")
    with conn:
        cursor = conn.execute(SQL_EDIT_GOAL, (goal, pk,))

        
@edit_action("2", "Изменить комментарий")
def edit_comment(conn, pk):
    """Функция изменяет комментарий указанной записи по ее номеру"""
    comment = input("Ппрокомментируйте задачу заново:\n")
    with conn:
        cursor = conn.execute(SQL_EDIT_COMMENTS, (comment, pk,))


@edit_action("3", "Изменить дату")        
def edit_date(conn, pk):
    """Функция изменяет дату по id"""
    new_date = input("Введите новую дату в формате ГГГГ ММ ДД (через пробел):\n").split()
    new_date = "-".join(new_date)
    with conn:
        cursor = conn.execute(SQL_EDIT_DATE, (new_date, pk,))


def find_task_by_pk(conn, pk):
    """Находит запись по id"""
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL + " WHERE id = ?", (pk,))
        return cursor.fetchone()


def find_all_goals(conn):
    """Находит все записи сотритует по дате исполнения"""
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL + " ORDER BY deadline ASC")
        return cursor.fetchall()


def find_goals_by_date(conn, deadline = None):
    """принимает подключание и дату. Выводит список невыполненных задач на указанную дату"""    
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL + " WHERE status = 0 AND deadline = DATE(?)", (deadline,))
        return cursor.fetchall()

    
def finish(conn, pk):
    """принимает подключение и номер записи, меняет статус на выполнено"""
    with conn:
        cursor = conn.execute(SQL_EDIT_STATUS_OFF, (pk,))
    print("Задача завершена")


def restart(conn, pk):
    """принимает подключение и номер записи, меняет статус на не выполнено"""
    with conn:
        cursor = conn.execute(SQL_EDIT_STATUS_ON, (pk,))
    

def of_date():
    
    try:
        date = [int(i) for i in input("Введите дату в формате ГГГГ ММ ДД (по-умолчанию - сегодня): ").split()]

        if not date:
            return datetime.date.isoformat(datetime.date.today())

        test = datetime.date(*date)

    except (ValueError, TypeError):
        return False

    return datetime.date.isoformat(test)
