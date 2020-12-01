from typing import NamedTuple, List, Dict, Tuple

from heapq import heappush, heappop


class Pair(NamedTuple):
    weight: int
    length: int
    index: int


class PairDiff(NamedTuple):
    value: int
    index: int
    weight: int
    length: int

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __gt__(self, other) -> bool:
        return not self.value < other.value


data: List[Pair] = []
num_jobs: int

with open('./ex1_test_cases/ex1_1_test1', 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            num_jobs = int(line.strip())
            continue
        data.append(Pair(int(line.strip().split()[0]),
                         int(line.strip().split()[1]),
                         i - 1))

pairs_dict: Dict[int, Pair] = {}

def pair_with_bigger_weight(pair1: Pair, pair2: Pair) -> Pair:
    if pair1.weight > pair2.weight:
        return pair1
    return pair2

def get_schedule_indices(inputs: List[Pair]) -> Tuple[List[int], List[PairDiff]]:
    h: List[PairDiff] = []
    for pair in inputs:
        item = PairDiff(value=(-1) * (pair.weight - pair.length), index=pair.index,
                        weight=pair.weight, length=pair.length)
        pairs_dict[pair.index] = pair
        heappush(h, item)

    current_length: int = 0
    res: List[PairDiff] = []
    indices: List[int] = []
    while h:
        poped_item: PairDiff = heappop(h)
        current_length += poped_item.length
        new_item = PairDiff(poped_item.value, poped_item.index,
                            poped_item.weight, length=current_length)
        res.append(new_item)
        indices.append(poped_item.index)
    return indices, res

ordered_indices, new_pairs = get_schedule_indices(data)
diffs: List[int] = [pairs_dict[idx].weight - pairs_dict[idx].length for idx in ordered_indices]
total: int = 0

assert len(diffs) == len(ordered_indices)

flag = False

for i, ind in enumerate(ordered_indices):
    if flag:
        flag = False
        continue
    try:
        next_index: int = ordered_indices[i + 1]
        if diffs[i] == diffs[i + 1]:
            chosen_pair: Pair = pair_with_bigger_weight(pairs_dict[ind], pairs_dict[next_index])
            total += chosen_pair.weight * chosen_pair.length
            flag = True
            if chosen_pair.index == pairs_dict[ind].index:
                total += pairs_dict[next_index].weight * pairs_dict[next_index].length
            else:
                total += pairs_dict[ind].weight * pairs_dict[ind].length
        else:
            total += pairs_dict[ind].weight * pairs_dict[ind].length
    except IndexError:
        continue

# for test0
#assert total == 1175612
# for test1
assert total == 74649
print(total)
