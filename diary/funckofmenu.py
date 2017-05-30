import sqlite3
import os.path

#это блок sql запросов: по одному на каждую функцию
SQL_INSERT_GOAL ="""
            INSERT INTO diary ("Задача", "Комментарий") VALUES (?, ?)
            """

SQL_SELECT_ALL = """
    SELECT
        "Номер", "Задача", "Комментарий", "Статус", "ДатаСоздания"
    FROM
        diary
            """

SQL_EDIT_GOAL = """
            UPDATE diary SET "Задача" = "{}" WHERE "Номер" = {}
            """
SQL_EDIT_COMMENT = """
            UPDATE diary SET "Комментарий" = "{}" WHERE "Номер" = {}
            """
SQL_EDIT_STATUS = """
            UPDATE diary SET "Статус" = "Выполнено" WHERE "Номер" = {}
            """
SQL_RESTART_GOAL = """
            UPDATE diary SET "Статус" = "Не выполнено" WHERE "Номер" = {};
            UPDATE diary SET "ДатаСоздания" = CURRENT_TIMESTAMP WHERE "Номер" = {}
            """


def goallist(conn):
    """Вывести список задач"""
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL)
        for record in cursor.fetchall():
            for i in record:
                print(i, end = " ")
            print()
    return print("\nСписок задач выведен\n")

def adddgoal(conn):
    """Добавить задачу"""
    print("Добавить задачу")
    goal = input("Введите название задачи: ")
    comment = input("Прокоментируйте задачу (если требуется): ")
    
    with conn:
        cursor = conn.execute(SQL_INSERT_GOAL, (goal, comment,))
    return print("\nЗадача добавлена\n")


def editgoal(conn):
    """Отредактировать задачу"""
    pk = -1 
    choice_of_editing = None
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL)
        a = len(cursor.fetchall()) #опредялеям размер базы в строках
        
    while not pk in range(a+1): #убеждаемся, что введенный номер есть в базе
        pk = input("Введите номер номер задачи (0, чтобы вернуться в предыдущее меню): ")
        if not pk.isdigit():
            continue
        pk = int(pk)
        if pk == 0:
            return #пожалуй, эту часть нужно в отдельную функцию выделить
        
    while choice_of_editing not in (1, 2, 0):
        choice_of_editing = input("Введите 1 - чтобы изменить задачу, 2 - чтобы изменить комментарий, 0 - чтобы вернуться в основное меню: ")
        if not choice_of_editing.isdigit(): #здесь мы проверям введенно значение на число, чтобы не было ошибки с интом
            continue
        choice_of_editing = int(choice_of_editing)
        
        if choice_of_editing == 0:
            return
        
        if choice_of_editing == 1:     
            with conn:
                goal = input("Укажите измененную формулировку задачи: ")
                SQL_EDIT_GOAL_OK = SQL_EDIT_GOAL.format(goal, pk)#тут, может быть из-за русского языка, не получилось отформатить при передаче курсору
                cursor = conn.execute(SQL_EDIT_GOAL_OK)
            return print("\nЗадача отредактирована\n")
        
        elif choice_of_editing == 2:
            with conn:
                goal = input("Старый комментарий будет удален, напишите новый комментарий: ")
                SQL_EDIT_COMMENT_OK = SQL_EDIT_COMMENT.format(goal, pk)
                cursor = conn.execute(SQL_EDIT_COMMENT_OK)
            return print("\nЗадача отредактирована\n")
        
        else: # если не была указана нужная команда, запусти цикл еще раз
            continue

def donegoal(conn): # тут я еще не понял: будет меняться статус на выполнена, или вообще столбец статус - не нужен, а задача будет удаляться? пока реализую первый вариант
    """Завершить задачу"""
    print("Указанная задача вместо статуса 'не выполнено', получит статус 'выполнено'")
    pk = -1 
    choice_of_editing = None
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL)
        a = len(cursor.fetchall()) #опредялеям размер базы в строках
        
    while not pk in range(a+1): #убеждаемся, что введенный номер есть в базе
        pk = input("Введите номер номер задачи (0, чтобы вернуться в предыдущее меню): ")
        if not pk.isdigit():
            continue
        pk = int(pk)
        if pk == 0:
            return #пожалуй, эту часть нужно в отдельную функцию выделить, т.к. с нее все мои функции начинают работать)

    SQL_EDIT_STATUS_OK = SQL_EDIT_STATUS.format(pk)
    cursor = conn.execute(SQL_EDIT_STATUS_OK)
    
    return print("\nЗадача завершена\n")


def restartg(conn):# пока выполненные задачи не будут удаляться, эта функция будет менять статус обратно на не выполнена и обновлять дату старта
    """Начать задачу сначала"""
    print("Указанная задача вместо статуса 'выполнено', получит статус 'не выполнено' и обновится время")
    pk = -1 
    choice_of_editing = None
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL)
        a = len(cursor.fetchall()) #опредялеям размер базы в строках
        
    while not pk in range(a+1): #убеждаемся, что введенный номер есть в базе
        pk = input("Введите номер номер задачи (0, чтобы вернуться в предыдущее меню): ")
        if not pk.isdigit():
            continue
        pk = int(pk)
        if pk == 0:
            return #пожалуй, эту часть нужно в отдельную функцию выделить

    SQL_EDIT_STATUS_OK = SQL_RESTART_GOAL.format(pk, pk)
    cursor = conn.executescript(SQL_EDIT_STATUS_OK)
    
    return print("\nЗадача завершена\n")
    return print("\nЗадача перезапущена\n")


def exitmenu(conn):
    """Выход"""
    conn.close()
    return print("\nОстались невыполненные задачи!\n")


def connect(db_name=None):
    if db_name is None:
        db_name = ':memory:'

    conn = sqlite3.connect(db_name)
    return conn


def initialize(conn):

    with open('schema.sql') as f:
        conn.executescript(f.read())

__all__ = [
            "goallist",
            "adddgoal",
            "editgoal",
            "donegoal",
            "restartg",
            "exitmenu",
            "sqlite3",
            "SQL_INSERT_GOAL",
            "connect",
            "initialize"
            ]
#в __all__ переданы только названия функций, а имена sql-запросов - нет, но ошибок использования этих имен при запуске main.py - нет.
#нужно еще разобраться с датой (настроить часовой пояс +3)
