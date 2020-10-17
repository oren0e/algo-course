'''
Implementing the Heap version of Dijkstra's algorithm

1. Implement heap with delete operation - Done
2. Implement main algorithm with the 2 primitives
3. Implement the case after the frontier changes (after we add w to X)
'''
import heapq

from typing import List, TypeVar, Generic, Optional, Tuple

T = TypeVar('T')


class Heap(Generic[T]):
    def __init__(self) -> None:
        self._data: List[T] = []

    @property
    def is_empty(self) -> bool:
        return not self._data

    def push(self, v: T) -> None:
        heapq.heappush(self._data, v)

    def pop_heap(self) -> Optional[T]:
        if not self.is_empty:
            return heapq.heappop(self._data)
        else:
            return None

    def delete(self, i: int) -> None:
        if not self.is_empty:
            self._data[i] = self._data[-1]
            self._data.pop()
            if i < len(self._data):
                heapq._siftup(self._data, i)
                heapq._siftdown(self._data, 0, i)
        else:
            print('Empty heap')

    def __repr__(self) -> str:
        return repr(self._data)

# import data into adjacency list
def find_max_node_value(file: str) -> int:
    '''
    Returns max value for the current direction
    and the total max value (either direction)
    '''
    max_val: int = 0
    with open(file, 'r') as f:
        for i, line in enumerate(f, start=1):
            row: List[int] = [int(item[0]) for item in line.strip().split(' ')]
            if row[0] > max_val:
                max_val = row[0]
            #elif row[1] > max_val:
             #   max_val = row[1]
    offset: int = i - max_val
    return max_val #, max_val + offset


WeightedGraph = List[List[Tuple[int]]]


def read_data(file: str) -> WeightedGraph:
    data: WeightedGraph = [[] for _ in range(find_max_node_value(file))]

    with open(file, 'r') as f:
        for line in f:
            cell_num = None
            for i, col in enumerate(line.strip().split(' ')):
                if i == 0:
                    cell_num = int(col)
                elif i > 0:
                    data[cell_num - 1].append(tuple(int(t) for t in col.split(',')))
    return data


g: WeightedGraph = read_data('./ex2_test_cases/test1')

