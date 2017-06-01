"""Меню ежедневника"""
import sys

from diary import funckofmenu as actions


get_connection = lambda: actions.connect("diary.sqlite") #тоже самое, что и предыдущее создание функции (закоментированное) 


def goallist():
    """Вывести список задач"""
    pick = input("введите дату в формате ГГГГ ММ ДД, по которой хотите получить записи пустой ввод - даст список по сегодняшней дате, 0 - предыдущее меню")
    #if not pick:
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL_BY_DATE_TODAY)
        for record in cursor.fetchall():
            for i in record:
                print(i, end = " ")
            print()
    return print("\nСписок задач выведен\n")


def action_view():
    """Вывести список задач"""
    data_filter = input("введите дату в формате ГГГГ ММ ДД, по которой хотите получить записи пустой ввод - даст список по сегодняшней дате, 0 - предыдущее меню").split()
    data_filter = "-".join(data_filter)
    if data_filter:
        with get_connection() as conn:
            tasks = actions.find_goals_by_date(conn, data_filter)
            for lines in tasks:
                for columns in lines:
                    print(columns, end = " ")
                print()
        return

    else:
        return


def action_add():
    """Добавить задачу"""

    goal = input("Введите текст задачи: ")
    comment = input("Напишите комментарий: ")
    deadline = [i for i in input("Введите дату для записи формате 'ГГГГ ММ ДД' через пробел: ").split()]
    deadline = "-".join(deadline)
    
    #тут будуь проверки на корректность ввода goal, comment и deadline
    with get_connection() as conn:
        actions.add_goal(conn, goal, comment, deadline)
    #а тут вариант действий ну случай если аргументы - не подходят для предстоящего sql запроса

    return print("\nЗадача добавлена\n")



def editgoal():
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
        if pk not in range(a+1):
            print("В базе нет задачи под таким номером")
        
    while choice_of_editing not in (1, 2, 0):
        choice_of_editing = input("Введите 1 - чтобы изменить задачу, 2 - чтобы изменить дату дэдлайна, 0 - чтобы вернуться в основное меню: ")
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
                deadline = [i for i in input("Введите крайнюю дату выполнения в формате ГГГГ ММ ДД ЧЧ ММ через пробел: ").split()]
                deadline = "-".join(deadline[:3]) + " " + ":".join(deadline[3:]) + "00"                
                SQL_EDIT_DEADLINE_OK = SQL_EDIT_DEADLINE.format(deadline, pk)
                cursor = conn.execute(SQL_EDIT_DEADLINE_OK)
            return print("\nЗадача отредактирована\n")
        
        else: # если не была указана нужная команда, запусти цикл еще раз
            continue


def donegoal(): # тут я еще не понял: будет меняться статус на выполнена, или вообще столбец статус - не нужен, а задача будет удаляться? пока реализую первый вариант
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
        if pk not in range(a+1):
            print("В базе нет задачи под таким номером")
    with conn:
        SQL_EDIT_STATUS_OK = SQL_EDIT_STATUS.format(pk)
        cursor = conn.execute(SQL_EDIT_STATUS_OK)
    
    return print("\nЗадача завершена\n")


def restartg():# пока выполненные задачи не будут удаляться, эта функция будет менять статус обратно на не выполнена и обновлять дату старта
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
        if pk not in range(a+1):
            print("В базе нет задачи под таким номером")
            
    with conn:
        deadline = [i for i in input("Введите крайнюю дату выполнения в формате ГГГГ ММ ДД ЧЧ ММ через пробел: ").split()]
        deadline = "-".join(deadline[:3]) + " " + ":".join(deadline[3:]) + "00"          
        SQL_EDIT_RESTART_GOAL_OK = SQL_RESTART_GOAL.format(pk, pk, deadline)
        cursor = conn.executescript(SQL_EDIT_RESTART_GOAL_OK)


    return print("\nЗадача завершена\n")
    return print("\nЗадача перезапущена\n")


def exitmenu():
    """Выход"""
    sys.exit(0)


def show_menu():
    """Показать Меню"""
    print("""
1. Вывести список задач
2. Добавить задачу
3. Отредактировать задачу
4. Завершить задачу
5. Начать задачу сначала
m. Показать Меню
q. Выход
""")

          
def menu(): #для такой функции обычно используется имя main, 
    """функция навигации по ежедневнику"""

    with get_connection() as conn:
        actions.initialize(conn)    
    
    options = {
        "1" : action_view,
        "2" : action_add,
        "3" : editgoal,
        "4" : donegoal,
        "5" : restartg,
        "q" : exitmenu,
        }
    
    while 1:

        show_menu()
        
        pick = input("\nДля продолжения работы выберете действие: \n")
        action = options.get(pick)
        
        if action:
            print("\n" + action.__doc__+"\n")
            action()

        else:
            print("{}? Нет такой команды!\n".format(pick))
