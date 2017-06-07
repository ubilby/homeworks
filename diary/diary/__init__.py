"""Меню ежедневника"""
import sys
from collections import OrderedDict, namedtuple

from diary import funckofmenu as func


get_connection = lambda: func.connect("diary.sqlite") #тоже самое, что и предыдущее создание функции (закоментированное) 

Action = namedtuple("Action", ["func", "name"])
actions = OrderedDict()


def action(cmd, name):
    def decorator(func):
        actions[cmd] = Action(func = func, name = name)
        return func
    return decorator
    

@action("1", "Вывести список всех задач")
def action_view_all():
    """Вывести список всех задач"""
    with get_connection() as conn:
        urls = func.find_all_goals(conn)

        for url in urls:
            print("{url[id]} : {url[task]} : {url[text]} : {url[deadline]} : {url[OTHER]}\n".format(url=url))
        
    print("\nСписок задач выведен")


@action("2", "Вывести список невыполненных задач на указанную дату")
def action_view_for_day():
    """Вывести список невыполненных задач на указанную дату"""
    
    data_filter = func.of_date()

    if not data_filter:
        print("Ошибка. некорректно указана дата!")

    
    with get_connection() as conn:
        tasks = func.find_goals_by_date(conn, data_filter)
        if not tasks:
            print("Нет таких записей")
        for lines in tasks:
            print("{lines[id]} : {lines[task]} : {lines[text]} : {lines[deadline]} : {lines[OTHER]}".format(lines=lines))


@action("3", "Отредактировать задачу")
def action_edit():
    """Отредактировать задачу"""
    pk = input("Введите уникальный номер задачи, которую требуется отредактировать:\n")
    with get_connection() as conn:
        goal = func.find_task_by_pk(conn, pk)

        if not goal:
            print("Нет записи под таким номером")
            return

        print("{goal[id]} : {goal[task]} : {goal[text]} : {goal[deadline]} : {goal[OTHER]}".format(goal=goal))

    actions = {
        "1" : func.edit_goal,
        "2" : func.edit_comment,
        "3" : func.edit_date
        }
    
    while True: #Это нагромождение строк через принт - нужно заменить декораторами!
        action = input("""
1. Изменить формулировку цели
2. Переписать коментарий к задаче
3. Изменить дату выполнения задачи
m. Выйти в основное меню
""")
        if action == "m":
            return
    
        if action not in actions:
            continue

        else:
            break

    actions[action](conn, pk)


@action("4", "Завершить задачу")
def action_finish(): 
    """Завершить задачу"""
    pk = input("Введите уникальный номер завершенной задачи:\n")
    with get_connection() as conn:
        are_in_base = func.find_task_by_pk(conn, pk)
        
        if not are_in_base:
            print("Нет записи под таким номером")
            return

        func.finish(conn, pk)
 
@action("5", "Перезапустить задачу")
def action_restart():
    """Перезапустить задачу"""
    pk = input("Введите уникальный номер завершенной задачи:\n")
    with get_connection() as conn:
        are_in_base = func.find_task_by_pk(conn, pk)

        if not are_in_base:
            print("Нет записи под таким номером")
            return

        func.restart(conn, pk)
        func.edit_date(conn, pk)
    print("задача перезапущена")


@action("6", "Добавить задачу")
def action_add():
    """Добавить задачу"""
    goal = input("Введите текст задачи: ")
    comment = input("Напишите комментарий: ")
    deadline = func.of_date()
    
    if not deadline:
        print("Ошибка! Дата указана не корректно")
        return

    with get_connection() as conn:
        func.add_goal(conn, goal, comment, deadline)
   
    print("Задача добавлена")    


@action("q", "Выйти")    
def exitmenu():
    """Выход"""
    sys.exit(0)


@action("m", "Показать меню")
def show_menu():
    """Показать Меню"""
    print("Diary v0.9 - учебнйы ежедневник")
    for cmd, action in actions.items(): # интерпритатор пробегает по меню, считывает декораторы и создает словарь действий
        print("{}.{}".format(cmd, action[1])) #это список кортежей - пара (ключ, згначение) и выводит список

              
def menu(): #для такой функции обычно используется имя main, 
    """функция навигации по ежедневнику"""
    with get_connection() as conn:
        func.initialize(conn)    
    
    while 1:
        show_menu()
        pick = input("\nДля продолжения работы выберете действие: \n")
        action = actions.get(pick)
        
        if action:
            actions[pick][0]()

        else:
            print("{}? Нет такой команды!\n".format(pick))


