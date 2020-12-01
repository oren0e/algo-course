"""
Prim's minimum spanning tree algorithm
"""
from heapq import heappop, heappush
import heapq

from typing import TypeVar, List, Dict, Generic, NamedTuple

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
    in_frontier: bool = False   # in X or not

