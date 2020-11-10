from typing import Dict, List, Callable, Tuple

from collections import defaultdict

from multiprocessing import Pool

from functools import wraps

from timeit import default_timer as timer

file = 'ex4_data.txt'
t_range = range(-10000, 10001)

data: Dict[int, List[int]] = defaultdict(list)

with open(file, 'r') as f:
    for line in f:
        val = int(line.strip())
        data[val].append(val)

def time_func(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = timer()
        res = f(*args, **kwargs)
        end = timer()
        print(f'{f.__name__} took {end - start} seconds, OR, {(end - start) / 60} minutes')
        return res
    return wrapper


def find_2_sum(target: int) -> bool:
    for key in data.keys():
        lookup_key = target - key
        if (data.get(lookup_key) is not None) and (lookup_key != key):
            return True


@time_func
def solve_ex4() -> Tuple[int, List[bool]]:
    pool = Pool()
    result = pool.map(find_2_sum, t_range)
    return sum(item for item in result if item is not None), result


sum_res, res = solve_ex4()
print(sum_res)
