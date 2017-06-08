import random
from string import digits, ascii_letters

valid_values = list(digits + ascii_letters)
radix = len(valid_values)

def password_generator(n):
    """так элегантно выглядит, мне аж самому понравилось)"""
    yield "".join([str(valid_values[random.randrange(radix)]) for i in range(n)])

