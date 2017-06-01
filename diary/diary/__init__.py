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
        tasks = func.find_all_goals(conn)

        for lines in tasks:
            print(lines[0], " : ".join(lines[1:-1]), lines[-1], sep=" : ")
        
    print("\nСписок задач выведен")


def action_view_for_day():
    """Вывести список задач на указанную дату"""
    
    data_filter = input("введите дату в формате ГГГГ ММ ДД через пробел, по которой хотите получить записи (пустой ввод = сегодня)\n").split()
    data_filter = "-".join(data_filter)
    with get_connection() as conn:
        tasks = func.find_goals_by_date(conn, data_filter)
        if not tasks:
            print("Нет таких записей")
        for lines in tasks:
            print(lines[0]," : ".join(lines[1:-1]), lines[-1], sep = " : ")


def action_edit():
    """Отредактировать задачу"""
    pk = input("Введите уникальный номер задачи, которую требуется отредактировать:\n")
    print()
    if pk.isdigit():
        with get_connection() as conn:
            are_in_base = func.find_task_by_pk(conn, pk)

            if not are_in_base:
                print("Нет записи под таким номером")
                return

            print(are_in_base[0], " : ".join(are_in_base[1:-1]), are_in_base[-1], sep = " : ")

    else:
        print("Не корректно указан номер")
        return

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
            print("Запись обновлена")
            print(edit_well_done[0], " : ".join(edit_well_done[1:-1]),edit_well_done[-1], sep=" : ")
            print()


def action_finish(): #
    """Завершить задачу"""
    pk = input("Введите уникальный номер завершенной задачи:\n")
    print()
    if pk.isdigit():
        with get_connection() as conn:
            are_in_base = func.find_task_by_pk(conn, pk)

            if not are_in_base:
                print("Нет записи под таким номером")
                return
            
    
    else:
        print("Не корректно указан номер")
        return

    with get_connection() as conn:
        done = func.can_finish(conn, pk)
        if not done:
            return
        func.finish(conn, pk)
        
        

def action_restart():
    """Перезапустить задачу"""
    pk = input("Введите уникальный номер задачи, которую хотите перезапустить:\n")
    print()
    if pk.isdigit():
        with get_connection() as conn:
            are_in_base = func.find_task_by_pk(conn, pk)

            if not are_in_base:
                print("Нет записи под таким номером")
                return

    else:
        print("Не корректно указан номер")
        return

    with get_connection() as conn:
        done = func.can_restat(conn, pk)

        if not done:
            return

        func.restart(conn, pk)
        func.edit_date(conn, pk)

    print(find_task_by_pk)

    
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
