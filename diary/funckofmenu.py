def goallist():
    """Вывести список задач"""
    return print("\nСписок задач выведен\n")


def adddgoal():
    """Добавить задачу"""
    return print("\nЗадача добавлена\n")


def editgoal():
    """Отредактировать задачу"""
    return print("\nЗадача отредактирована\n")

    
def donegoal():
    """Завершить задачу"""
    return print("\nЗадача завершена\n")


def restartg():
    """Начать задачу сначала"""
    return print("\nЗадача перезапущена\n")


def exitmenu():
    """Выход"""
    return print("\nОстались невыполненные задачи!\n")


__all__ = [
            "goallist",
            "adddgoal",
            "editgoal",
            "donegoal",
            "restartg",
            "exitmenu"
            ]
