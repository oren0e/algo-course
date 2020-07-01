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


# test cases
assert recursive_mult(1234, 5678) == 1234*5678
assert recursive_mult(10, 2) == 10*2
assert recursive_mult(1, 1) == 1*1
assert recursive_mult(2345679, 234) == 2345679*234, "We assumed that the numbers have the same digit length"

# answer to exercise
assert recursive_mult(3141592653589793238462643383279502884197169399375105820974944592, 2718281828459045235360287471352662497757247093699959574966967627) == \
3141592653589793238462643383279502884197169399375105820974944592 * 2718281828459045235360287471352662497757247093699959574966967627