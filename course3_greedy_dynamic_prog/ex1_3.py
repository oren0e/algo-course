"""
Prim's minimum spanning tree algorithm
"""
from heapq import heappop, heappush
import heapq

from typing import TypeVar, List, Dict, Generic, NamedTuple, Generator, Optional

T = TypeVar('T')

class Heap(Generic[T]):
    def __init__(self) -> None:
        self._data: List[T] = []

    @property
    def is_empty(self) -> bool:
        return not self._data

    def heap_push(self, v: T) -> None:
        heappush(self._data, v)

    def heap_pop(self) -> T:
        if not self.is_empty:
            return heappop(self._data)
        raise RuntimeError('Empty heap')

    def peek(self) -> T:
        if not self.is_empty:
            return self._data[0]
        raise RuntimeError('Empty heap')

    def heap_delete(self, position: int) -> None:
        if not self.is_empty:
            self._data[position] = self._data[-1]
            self._data.pop()
            if position < len(self._data):
                heapq._siftup(self._data, position)
                heapq._siftdown(self._data, 0, position)
        raise RuntimeError("Empty heap")


class Vertex(NamedTuple):
    value: int
    cost: int
    in_frontier: List[bool] = [False]   # in X or not, change by x.in_frontier[0] = True


Graph = List[List[Vertex]]

def get_num_verticies(file: str) -> int:
    with open(file, 'r') as f:
        line = f.readline()
        return int(line.strip().split()[0])


def read_data_gen(file: str) -> Generator:
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            yield tuple(line.strip().split())


def build_graph(file: str) -> Graph:
    res_list: Graph = [[] for _ in range(get_num_verticies(file))]
    for tup in read_data_gen(file):
        res_list[int(tup[0]) - 1].append(Vertex(int(tup[1]), int(tup[2])))      # undirected graph: each edge appears once!
    return res_list

g: Graph = build_graph('ex1_test_cases/ex1_3_test0')


