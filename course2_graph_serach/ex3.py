import heapq

from typing import List, Generic, TypeVar, Optional

T = TypeVar('T')

medians: List[int] = []
data: List[int] = []


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self.data: List[T] = []

    @property
    def is_empty(self) -> bool:
        return not self.data

    def push(self, v: T) -> None:
        heapq.heappush(self.data, v)

    def pop(self) -> Optional[T]:
        if not self.is_empty:
            return heapq.heappop(self.data)
        else:
            print('Empty queue')
            return None

    def peek(self) -> Optional[T]:
        if not self.is_empty:
           return self.data[0]
        else:
            print('Empty queue')
            return None

    def __repr__(self) -> str:
        return repr(self.data)

    def __len__(self) -> int:
        return len(self.data)

class MaxPriorityQueue(PriorityQueue):
    def push(self, v: T) -> None:
        heapq.heappush(self.data, (-1 * v))

    def pop(self) -> Optional[T]:
        if not self.is_empty:
            return heapq.heappop(self.data) * (-1)
        else:
            print('Empty queue')
            return None

    def peek(self) -> Optional[T]:
        if not self.is_empty:
            return self.data[0] * (-1)
        else:
            print('Empty queue')
            return None

# test the data structure
temp = MaxPriorityQueue()
temp.push(5)
temp.push(590)
temp.push(3445)
temp.push(100)

assert len(temp) == 4
assert temp.peek() == 3445
temp.pop()
temp.pop()
assert temp.peek() == 100


h_lo = MaxPriorityQueue()     # supports extract_max
h_hi = PriorityQueue()        # supports extract_min

'''
The idea is to maintain the invariant that the smallest half of the numbers
that we've seen so far are all in h_lo, and the largest half of numbers we've seen 
so far are all in h_hi.
'''

with open('Median.txt', 'r') as f:
    for line in f:
        data.append(int(line.strip()))

# handle first case
h_hi.push(data[0])
medians.append(data[0])

for num in data[1:]:
    if num < h_hi.peek():
        h_lo.push(num)
    else:
        h_hi.push(num)
    diff = abs(len(h_lo) - len(h_hi))
    if diff > 1:
        if len(h_lo) > len(h_hi):
            h_hi.push(h_lo.pop())
        elif len(h_hi) > len(h_lo):
            h_lo.push(h_hi.pop())
    # median append
    if len(h_lo) == len(h_hi):
        medians.append(h_lo.peek())
    else:
        if len(h_lo) > len(h_hi):   # odd (whichever has the bigger length (+1 element)
            medians.append(h_lo.peek())
        else:
            medians.append(h_hi.peek())

#assert sum(medians) % 10000 == 142    # for test0
#assert sum(medians) % 10000 == 9335
print(sum(medians) % 10000)
