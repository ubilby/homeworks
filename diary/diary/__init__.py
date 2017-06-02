"""Меню ежедневника"""
import sys

from diary import funckofmenu as func


get_connection = lambda: func.connect("diary.sqlite") #тоже самое, что и предыдущее создание функции (закоментированное) 

def action_add():
    """Добавить задачу"""

    goal = input("Введите текст задачи: ")
    comment = input("Напишите комментарий: ")
    deadline = [i for i in input("Введите дату для записи формате 'ГГГГ ММ ДД' через пробел: ").split()]
    print()
    deadline = "-".join(deadline)
    with get_connection() as conn:
        func.add_goal(conn, goal, comment, deadline)
   
    print("Задача добавлена")
    

def action_view_all():
    """Вывести список всех задач"""
    with get_connection() as conn:
        urls = func.find_all_goals(conn)

        for url in urls:
            print("{url[id]} : {url[task]} : {url[text]} : {url[deadline]} : {url[OTHER]}".format(url=url))
        
    print("\nСписок задач выведен")


def action_view_for_day():
    """Вывести список невыполненных задач на указанную дату"""
    
    data_filter = input("введите дату в формате ГГГГ ММ ДД через пробел, по которой хотите получить записи (пустой ввод = сегодня)\n").split()
    data_filter = "-".join(data_filter)
    with get_connection() as conn:
        tasks = func.find_goals_by_date(conn, data_filter)
        if not tasks:
            print("Нет таких записей")
        for lines in tasks:
            print("{lines[id]} : {lines[task]} : {lines[text]} : {lines[deadline]} : {lines[OTHER]}".format(lines=lines))


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
    
    while True:
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
    with get_connection() as conn:
        edit_well_done = func.find_task_by_pk(conn, pk)


def action_finish(): 
    """Завершить задачу"""
    pk = input("Введите уникальный номер завершенной задачи:\n")
    with get_connection() as conn:
        are_in_base = func.find_task_by_pk(conn, pk)
        
        if not are_in_base:
            print("Нет записи под таким номером")
            return

        func.finish(conn, pk)
 

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

    
def exitmenu():
    """Выход"""
    sys.exit(0)


def show_menu():
    """Показать Меню"""
    print("""
1. Вывести список задач на указанную дату
2. Вывести список всех задач
3. Отредактировать задачу
4. Завершить задачу
5. Начать задачу сначала
6. Добавить задачу
q. Выход
""")

          
def menu(): #для такой функции обычно используется имя main, 
    """функция навигации по ежедневнику"""

    with get_connection() as conn:
        func.initialize(conn)    
    
    options = {
        "1" : action_view_for_day,
        "2" : action_view_all,
        "3" : action_edit,
        "4" : action_finish,
        "5" : action_restart,
        "6" : action_add,
        "q" : exitmenu,
        }
    
    while 1:
        show_menu()
        pick = input("Для продолжения работы выберете действие: \n")
        action = options.get(pick)
        
        if action:
            print("\n" + action.__doc__+"\n")
            action()

        else:
            print("{}? Нет такой команды!\n".format(pick))
