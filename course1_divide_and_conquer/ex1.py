import math
import random
from typing import Tuple

# recursive approach
def split_num(num: int) -> Tuple[int, int]:
    num_digits = int(math.log10(num) + 1)
    first_half = num_digits // 2
    a = (num // 10 ** (first_half)) #* 10 ** (first_half + 1)
    b = num % 10 ** (first_half)

    return a, b


def recursive_mult(x: int, y: int) -> int:
    # base case
    if ((x // 10) == 0) or ((y // 10) == 0):
        return x * y

    a, b = split_num(x)
    c, d = split_num(y)
    ac = recursive_mult(a, c)
    ad = recursive_mult(a, d)
    bc = recursive_mult(b, c)
    bd = recursive_mult(b, d)

    # we are assuming that the two numbers have equal number of digits
    num_digits = int(math.log10(x) + 1)
    return 10**num_digits*ac + 10**(num_digits // 2)*(ad+bc) + bd

def which_is_longer(x: int, y: int) -> int:
    num_digits_x = int(math.log10(x) + 1)
    num_digits_y = int(math.log10(y) + 1)

    if num_digits_x > num_digits_y:
        return x
    elif num_digits_y > num_digits_x:
        return y
    else:   # equally sized
        return random.choice([x, y])

def karatsuba(x: int, y: int) -> int:
    # base case
    if ((x // 10) == 0) or ((y // 10) == 0):
        return x * y

    num_digits = int(math.log10(which_is_longer(x, y)) + 1)

    a = x // 10 ** (num_digits // 2)
    b = x % 10 ** (num_digits // 2)
    c = y // 10 ** (num_digits // 2)
    d = y % 10 ** (num_digits // 2)

    # if num_digits_x > num_digits_y:
    #     b = x % 10 ** (num_digits_y)
    #     a = x // 10 ** (num_digits_y)
    #     c, d = split_num(y)
    # elif num_digits_y > num_digits_x:
    #     b = y % 10 ** (num_digits_x)
    #     a = y // 10 ** (num_digits_x)
    #     c, d = split_num(x)
    # else:
    #     a, b = split_num(x)
    #     c, d = split_num(y)
    #a, b = split_num(x)
    #c, d = split_num(y)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    abcd = karatsuba(a+b, c+d)

    gaus_trick = abcd - ac - bd 

    return (10**(2*(num_digits//2)))*ac + 10**(num_digits // 2)*(gaus_trick) + bd

karatsuba(123, 456)

# test cases
assert recursive_mult(1234, 5678) == 1234*5678
assert recursive_mult(10, 2) == 10*2
assert recursive_mult(1, 1) == 1*1
assert recursive_mult(2345679, 234) == 2345679*234, "We assumed that the numbers have the same digit length"
assert recursive_mult(1111111111111111,22222222222222) == 1111111111111111*22222222222222

assert karatsuba(1234, 5678) == 1234*5678
assert karatsuba(10, 2) == 10*2
assert karatsuba(1, 1) == 1*1
assert karatsuba(2345679, 234) == 2345679*234, "We assumed that the numbers have the same digit length"
assert karatsuba(1111111111111111,22222222222222) == 1111111111111111*22222222222222

