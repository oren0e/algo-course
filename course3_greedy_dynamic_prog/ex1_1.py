from typing import NamedTuple, List, Dict

from heapq import heappush, heappop


class Pair(NamedTuple):
    weight: int
    length: int
    index: int


class PairDiff(NamedTuple):
    value: int
    index: int

    def __lt__(self, other) -> bool:
        return self.value < other.value


data: List[Pair] = []
num_jobs: int

with open('./ex1_test_cases/ex1_1_test0', 'r') as f:
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

def get_schedule_indices(inputs: List[Pair]) -> List[int]:
    h: List[PairDiff] = []
    for pair in inputs:
        item = PairDiff((-1) * (pair.weight - pair.length), pair.index)
        pairs_dict[pair.index] = pair
        heappush(h, item)

    res: List[int] = []
    while h:
        poped_item: PairDiff = heappop(h)
        # TODO: check here if h[0] and poped equal and if so take the one with the bigger weight
        if h:
            if poped_item.value == h[0].value:
                bigger_weight: Pair = pair_with_bigger_weight(pairs_dict[poped_item.index], pairs_dict[h[0].index])
                if bigger_weight.index == h[0].index:
                    second_pop = heappop(h)
                    res.append(second_pop.index)
        res.append(poped_item.index)
    return res


ordered_indices: List[int] = get_schedule_indices(data)
total: int = 0
for ind in ordered_indices:
    total += pairs_dict[ind].weight * pairs_dict[ind].length
# for i, ind in enumerate(ordered_indices):
#     try:
#         next_index: int = ordered_indices[i + 1]
#         if pairs_dict[ind].weight - pairs_dict[ind].length == pairs_dict[next_index].weight - pairs_dict[next_index].length:
#             chosen_pair: Pair = pair_with_bigger_weight(pairs_dict[ind], pairs_dict[next_index])
#             total += chosen_pair.weight * chosen_pair.length
#         else:
#             total += pairs_dict[ind].weight * pairs_dict[ind].length
#     except IndexError:
#         continue

# for test0
assert total == 1175612
print(total)
