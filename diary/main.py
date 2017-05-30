"""Меню ежедневника"""
import os.path
import sqlite3
from funckofmenu import * 

def menu(conn):
    """функция навигации по ежедневнику"""
    options = [goallist, adddgoal, editgoal, donegoal, restartg, exitmenu]
    pick = ""
    while pick != 5:

        for i, j in enumerate(options):
            print(i+1, j.__doc__, sep = " - ")

        pick = input("\nДля продолжения работы выберете действие (1-6): ")
        if pick not in ("1", "2", "3", "4", "5", "6"):
            print(pick + "???")
            print("Ошибка!\n")
            continue
        else:
            pick=int(pick) -1
        print()
        
        options[pick](conn)

    return print("Check it up")


            


initialize(connect("diary"))
conn = connect("diary")
cursor = conn.cursor()


menu(conn)
#conn.commit()


