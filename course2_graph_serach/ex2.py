'''
Implementing the Heap version of Dijkstra's algorithm

1. Implement heap with delete operation - Done
2. Implement main algorithm with the 2 primitives
3. Implement the case after the frontier changes (after we add w to X)
'''
import heapq

from typing import List, TypeVar, Generic, Optional

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

