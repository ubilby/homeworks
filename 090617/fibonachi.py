def fibonachi(n):
    """Это функция генератор, но последовательность чисел фибоначи
начинается не с 0,1 или 1,1"""
    spisok = [0, 1]
    yield 0
    yield 1
    while len(spisok) < n + 1:
        
        a = len(spisok)
        spisok.append(spisok[len(spisok)-2] + (spisok[len(spisok)-1]))
        yield spisok[a]
