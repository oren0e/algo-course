from typing import NamedTuple, List, Dict, Tuple

from heapq import heappush, heappop


class Pair(NamedTuple):
    weight: int
    length: int
    index: int
    value: float

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __gt__(self, other) -> bool:
        return not self.value < other.value


data: List[Pair] = []
with open('./ex1_test_cases/ex1_1_test0', 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            num_jobs = int(line.strip())
            continue
        data.append(Pair(int(line.strip().split()[0]),
                         int(line.strip().split()[1]),
                         i - 1, 0))


def pair_with_bigger_weight(pair1: Pair, pair2: Pair) -> Pair:
    if pair1.weight > pair2.weight:
        return pair1
    return pair2

def get_scheduled_pairs(inputs: List[Pair]) -> List[Pair]:
    h: List[Pair] = []  # Heap
    # calculate difference for each input
    for pair in inputs:
        item = Pair(pair.weight, pair.length, pair.index, value=(-1) * (pair.weight / pair.length))     # max heap
        heappush(h, item)

    current_length = 0
    res: List[Pair] = []
    while h:
        popped_item: Pair = heappop(h)
        current_length += popped_item.length
        new_item = Pair(popped_item.weight, current_length, popped_item.index, popped_item.value)
        res.append(new_item)
    return res


ordered_pairs: List[Pair] = get_scheduled_pairs(data)
total = 0

for i, pair in enumerate(ordered_pairs):
    try:
        next_pair: Pair = ordered_pairs[i + 1]
        if pair.value == next_pair.value:
            chosen_pair: Pair = pair_with_bigger_weight(pair, next_pair)
            total += chosen_pair.weight * chosen_pair.length
        else:
            total += pair.weight * pair.length
    except IndexError:
        total += pair.weight * pair.length

# test 1
#assert total == 72468
# test 0
assert total == 1142691