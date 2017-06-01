import sqlite3
import datetime
import os.path as Path

SQL_INSERT_GOAL ="""
            INSERT INTO diary ("task","text","deadline") VALUES (?, ?, ?)
            """

SQL_SELECT_ALL = """
    SELECT
        "id", "task", "text", "deadline",
    CASE (status)
        WHEN 1
        THEN "Выполнено"
        ELSE "Не выполнено"
        END "OTHER"
    FROM
        diary"""

SQL_SELECT_ALL_BY_DATE_TODAY = """
    SELECT
        "id", "task", "text", "deadline",
    CASE (status)
        WHEN 1
        THEN "Выполнено"
        ELSE "Не выполнено"
        END "OTHER"
    FROM
        diary WHERE deadline = DATE('NOW')

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
def connect(db_name=None):
    if db_name is None:
        db_name = ':memory:'
        
    conn = sqlite3.connect(db_name)
    return conn


def initialize(conn):
    with conn:
        script_file_path = Path.join(Path.dirname(__file__), 'schema.sql')

    with open(script_file_path) as f:
        conn.executescript(f.read())


def add_goal(conn, goal, comment, deadline):
    """Принимает цель, комментарий и дату выполнения. Добавляет соответствующую запись в таблицу.""" 
    with conn:
        cursor = conn.execute(SQL_INSERT_GOAL, (goal, comment, deadline,))
    return 


def edit_comment(conn, pk):
    comment = input("Ппрокомментируйте задачу заново:\n")
    with conn:
        cursor = conn.execute(SQL_EDIT_COMMENTS, (comment, pk,))


def edit_goal(conn, pk):
    goal = input("Введите новую формулировку задачи:\n")
    with conn:
        cursor = conn.execute(SQL_EDIT_GOAL, (goal, pk,))

        
def edit_date(conn, pk):
    new_date = input("Введите новую дату в формате ГГГГ ММ ДД (через пробел):\n").split()
    new_date = "-".join(new_date)
    with conn:
        cursor = conn.execute(SQL_EDIT_DATE, (new_date, pk,))


def find_task_by_pk(conn, pk):
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL + " WHERE id = ?", (pk,))
        return cursor.fetchone()


def find_all_goals(conn):
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL + " ORDER BY deadline ASC")
        return cursor.fetchall()


def find_goals_by_date(conn, deadline = None):
    """Вывести список задач"""    
    if deadline:
        with conn:
            cursor = conn.execute(SQL_SELECT_ALL + " WHERE deadline = DATE(?)", (deadline,))
            return cursor.fetchall()

    else:
        with conn:
            cursor = conn.execute(SQL_SELECT_ALL + " WHERE deadline = DATE('NOW')")       
            return cursor.fetchall()

def can_finish(conn, pk):
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL + " WHERE id = (?) AND status = 0 ", (pk,))
        return cursor.fetchall()

    
def finish(conn, pk):
    with conn:
        cursor = conn.execute(SQL_EDIT_STATUS_OFF, (pk,))


def can_restat(conn, pk):
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL + " WHERE id = (?) AND status = 1", (pk,))
        return cursor.fetchall()


def restart(conn, pk):
    with conn:
        cursor = conn.execute(SQL_EDIT_STATUS_ON, (pk,))
    
    

def is_date_ok():
    pass
#в __all__ переданы только названия функций, а имена sql-запросов - нет, но ошибок использования этих имен при запуске main.py - нет.
#нужно еще разобраться с датой (настроить часовой пояс +3)
