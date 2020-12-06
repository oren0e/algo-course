from typing import NamedTuple, List

from heapq import heappush, heappop


class Pair(NamedTuple):
    weight: int
    length: int
    index: int
    value: int

    def __lt__(self, other) -> bool:
        return self.value < other.value


data: List[Pair] = []
with open('ex1_test_cases/ex1_1_test17_160', 'r') as f:
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
        item = Pair(pair.weight, pair.length, pair.index, value=(-1) * (pair.weight - pair.length))     # max heap
        heappush(h, item)

    current_length = 0
    res: List[Pair] = []
    # TODO: this solution works only for ties in 2 elements in a row. Write a solution for n in a row
    while h:
        popped_item1: Pair = heappop(h)
        try:
            popped_item2: Pair = heappop(h)
            if popped_item1.value == popped_item2.value:
                chosen_pair: Pair = pair_with_bigger_weight(popped_item1, popped_item2)
                current_length += chosen_pair.length
                new_item = Pair(chosen_pair.weight, current_length, chosen_pair.index, chosen_pair.value)
                res.append(new_item)
                if chosen_pair.weight > popped_item1.weight:     # poped2 was chosen
                    current_length += popped_item1.length
                    new_item1 = Pair(popped_item1.weight, current_length, popped_item1.index, popped_item1.value)
                    res.append(new_item1)
                else:       # poped1 was chosen
                    current_length += popped_item2.length
                    new_item2 = Pair(popped_item2.weight, current_length, popped_item2.index, popped_item2.value)
                    res.append(new_item2)
            else:
                current_length += popped_item1.length
                new_item1 = Pair(popped_item1.weight, current_length, popped_item1.index, popped_item1.value)
                current_length += popped_item2.length
                new_item2 = Pair(popped_item2.weight, current_length, popped_item2.index, popped_item2.value)
                res.append(new_item1)
                res.append(new_item2)
        except IndexError:      # heap is empty in the second pop
            current_length += popped_item1.length
            new_item1 = Pair(popped_item1.weight, current_length, popped_item1.index, popped_item1.value)
            res.append(new_item1)
    return res


ordered_pairs: List[Pair] = get_scheduled_pairs(data)
total = 0

for pair in ordered_pairs:
    total += (pair.weight * pair.length)

print(total)
# for i, pair in enumerate(ordered_pairs):
#     try:
#         next_pair: Pair = ordered_pairs[i + 1]
#         if pair.value == next_pair.value:
#             chosen_pair: Pair = pair_with_bigger_weight(pair, next_pair)
#             total += chosen_pair.weight * chosen_pair.length
#         else:
#             total += pair.weight * pair.length
#     except IndexError:
#         total += pair.weight * pair.length

# test 1
# assert total == 74649
# test 0
# assert total == 1175612
# test 17_160
#assert total == 17443162
#print(total)