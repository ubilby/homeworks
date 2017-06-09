import random
from string import digits, ascii_letters


def password_generator(n):
    """так элегантно выглядит, мне аж самому понравилось)"""
    valid_values = list(digits + ascii_letters)
    radix = len(valid_values)

    yield "".join([str(valid_values[random.randrange(radix)]) for i in range(n)])

