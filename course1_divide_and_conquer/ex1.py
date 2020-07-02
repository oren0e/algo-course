import math

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

def karatsuba(x: int, y: int) -> int:
    # base case
    if ((x // 10) == 0) or ((y // 10) == 0):
        small: int = x * y
    else:
        small: int = 1

    a, b = split_num(x)
    c, d = split_num(y)
    ac = karatsuba(a, c)*small
    bd = karatsuba(b, d)
    abcd = karatsuba(a+b, c+d)

    gaus_trick = abcd - ac - bd 


    # we are assuming that the two numbers have equal number of digits
    num_digits = int(math.log10(x) + 1)
    return 10**num_digits*ac + 10**(num_digits // 2)*(gaus_trick) + bd

karatsuba(2345679, 234)

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