'''
Implementing the Heap version of Dijkstra's algorithm

1. Implement heap with delete operation - Done
2. Implement main algorithm with the 2 primitives
3. Implement the case after the frontier changes (after we add w to X)
'''
import heapq

from typing import List, TypeVar, Generic, Optional, Tuple, Dict

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

def dijkstra(g: WeightedGraph) -> List[int]:
    '''
    Returns the shortest-path for every vertex from
    vertex 1 so e.g., ans[0] = 0
    '''
    n = len(g)
    h: Heap = Heap()
    x_set: List[int] = [1]
    v_set: List[int] = [i for i in range(1, n+1)]
    ans: List[Optional[int]] = [None for _ in range(n)]
    ans[0] = 0
    key: List[Optional[int]] = [None for _ in range(n)]
    vertex_h_pos_map: Dict[int, int] = {}   # map between vertex and its position in the heap
    v_minus_x = [v for v in v_set if v not in x_set]

    while set(x_set) != set(v_set):
        for v in v_minus_x:
            for x_i in x_set:
                if g[x_i - 1]:
                    heads_v = min([item for item in g[x_i - 1] if item[0] == v], key=lambda x: x[1])


