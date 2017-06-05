"""Написать функцию, которая возвращает количество дней, оставшихся
до нового года. Функция должна корректно работать при запуске в любом году,
т. е. грядущий год должен вычисляться программно. Для решения задачи
понадобится стандартный модуль datetime"""
import datetime

def whenny():
    """функция возвращает количество дней до нового года"""
    today = datetime.datetime.now()
    nday = today.timetuple().tm_yday - 1
    nyear = today.timetuple().tm_year
    if (nyear % 4 ==0 and nyear % 100 != 0) or nyear % 400 == 0:
        return 366 - nday
    else:
        return 365 - nday
