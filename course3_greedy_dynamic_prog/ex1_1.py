from typing import NamedTuple, List, Callable


class Pair(NamedTuple):
    weight: int
    length: int
    index: int
    value: int

    def __lt__(self, other) -> bool:
        return self.value < other.value


data: List[Pair] = []
with open('jobs.txt', 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            num_jobs = int(line.strip())
            continue
        data.append(Pair(int(line.strip().split()[0]),
                         int(line.strip().split()[1]),
                         i - 1, 0))


def diff_value(pair: Pair) -> int:
    return pair.weight - pair.length


def ratio_value(pair: Pair) -> float:
    return pair.weight / pair.length


def get_scheduled_pairs(inputs: List[Pair], metric: Callable) -> List[Pair]:
    sorted_pairs: List[Pair] = []
    # calculate difference for each input
    for pair in inputs:
        item = Pair(pair.weight, pair.length, pair.index, value=metric(pair))
        sorted_pairs.append(item)
    sorted_pairs = sorted(sorted_pairs, key=lambda x: (x.value, x.weight), reverse=True)
    current_length = 0
    res: List[Pair] = []
    for pair in sorted_pairs:
        current_length += pair.length
        new_item = Pair(pair.weight, current_length, pair.index, pair.value)
        res.append(new_item)
    return res


def get_total(metric: Callable) -> int:
    ordered_pairs: List[Pair] = get_scheduled_pairs(data, metric)
    total = 0

    for pair in ordered_pairs:
        total += (pair.weight * pair.length)
    return total


# test 1
#assert get_total(diff_value) == 74649
#assert get_total(ratio_value) == 72468
# test 0
#assert get_total(diff_value) == 1175612
#assert get_total(ratio_value) == 1142691
# test 17_160
#assert get_total(diff_value) == 17443162
#assert get_total(ratio_value) == 16931310

print("Question 1: ", get_total(diff_value))
print("Question 2: ", get_total(ratio_value))