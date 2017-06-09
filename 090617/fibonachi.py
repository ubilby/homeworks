def fibonachi(n):
    """функция-генератор чисел фибоначи"""
    f1 = 0
    f2 = 1
    m = 0

    yield 0

    while m < n:
        m += 1
        f1, f2 = f2 + f1, f1

        yield f1
