def palindromli(x):
    """Преобразует полученный аргумент в строку и взвращает True  в случае,
    если строка - палиндром"""
    x = str(x)
    return x == x[::-1]

