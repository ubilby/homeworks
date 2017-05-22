def location(x,y):
    
    if x == 0:
        if y == 0:
            return "точка является центром оси координат и не принадлежит ни одной четверти"
        elif y > 0:
            return "точка лежит между первой и второй четвертью"
        else:
            return "точка лежит между третьй и четвертой четвертью"

    elif y == 0:
        if x > 0:
            return "точка лежит между первой и четвертой четвертью"
        else:
            return "точка лежит между второй и третьей четвертью"

    else:
        if x > 0 and y > 0:
            return 1
        elif x > 0 and y < 0:
            return 4
        elif x < 0 and y > 0:
            return 2
        elif x < 0 and y < 0:
            return 3
