'''
Implementing the Heap version of Dijkstra's algorithm

1. Implement heap with delete operation - Done
2. Implement main algorithm with the 2 primitives
3. Implement the case after the frontier changes (after we add w to X)
'''
import heapq

from typing import List, TypeVar, Generic, Optional, Tuple, Dict

import re

T = TypeVar('T')


class Edge:
    def __init__(self, value: Tuple[int, int, int]) -> None:
        self.value = value

    def __lt__(self, other) -> bool:
        return self.value[2] < other.value[2]

    def __eq__(self, other) -> bool:
        return self.value[2] == other.value[2]

    def __repr__(self) -> str:
        return repr(self.value)

    @property
    def vertex(self) -> int:
        return self.value[1]

    @property
    def vertex_weight(self) -> int:
        return self.value[2]

    @property
    def from_vertex(self) -> int:
        return self.value[0]


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
            row: int = int([item for item in re.sub(r'\t', ' ', line.strip()).split(' ')][0])
            if row > max_val:
                max_val = row
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
            for i, col in enumerate(re.sub(r'\t', ' ', line.strip()).split(' ')):
                if i == 0:
                    cell_num = int(col)
                elif i > 0:
                    data[cell_num - 1].append(tuple(int(t) for t in col.split(',')))
    return data


#g: WeightedGraph = read_data('./dijkstraData.txt')
g: WeightedGraph = read_data('./ex2_test_cases/test2')

def greedy_score(edges: List[Tuple[int, int, int]], ans: List[int]) -> int:
    return min(x[2] + ans[x[0] - 1] for x in edges)

def dijkstra(g: WeightedGraph) -> Tuple[List[int], List[List[int]]]:
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
    key[0] = 0
    paths = [[] for _ in range(n)]
    vertex_h_pos_map: Dict[int, int] = {}   # map between vertex and its position in the heap
    v_minus_x = [v for v in v_set if v not in x_set]

    while set(x_set) != set(v_set):
        # for x_i in x_set.copy():
        #     x_from = None
        for v in v_minus_x.copy():
            #if g[x_i - 1]:
            #last_x = x_set[-1]
            # for item in g:
            #     for sub_item in item:
            #         if (sub_item[0] in v_minus_x) and (g.index(item) + 1) in x_set:
            #             h.push(Edge((g.index(item) + 1, sub_item[0], sub_item[1])))

            edges = [(g.index(item) + 1, sub_item[0], sub_item[1]) for item in g
                              for sub_item in item
                              if (sub_item[0] in v_minus_x)
                              and (g.index(item) + 1) in x_set]
            #if edges:
            heads_v_min = min(edges, key=lambda x: x[2] + ans[x[0] - 1])
            key[heads_v_min[1] - 1] = greedy_score(edges, ans)
            #heads_v_min = h.pop_heap()
            last_x = heads_v_min[0]
            #heads_v_min = (heads_v_min[1], heads_v_min[2])
            h.push(Edge(heads_v_min))
            #x_from = x_i
            poped_from_h: Edge = h.pop_heap()
            #print(f'Adding {poped_from_h.vertex} to X')
            x_set.append(poped_from_h.vertex)
            # maintain invariant 2
            ans[poped_from_h.vertex - 1] = ans[last_x - 1] + poped_from_h.vertex_weight
            v_minus_x = [v for v in v_set if v not in x_set]
            if paths[poped_from_h.from_vertex - 1]:
                if poped_from_h.from_vertex != 1:
                    paths[poped_from_h.vertex - 1].extend(paths[poped_from_h.from_vertex - 1])
            else:
                if poped_from_h.from_vertex != 1:
                    paths[poped_from_h.vertex - 1].append(poped_from_h.from_vertex)
            paths[poped_from_h.vertex - 1].append(poped_from_h.vertex)
            for item in g[poped_from_h.vertex - 1]:
                if item[0] in v_minus_x:
                    if key[item[0] - 1] is not None:
                        key[item[0] - 1] = min(key[item[0] - 1], (ans[poped_from_h.vertex - 1] + item[1]))
                    else:
                        key[item[0] - 1] = ans[poped_from_h.vertex - 1] + item[1]

            #ans[poped_from_h.vertex - 1] = key[poped_from_h.vertex - 1]

    return key, paths
    #return ans


ans, paths = dijkstra(g)
print(ans, paths)

indices = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
print(','.join([str(ans[i-1]) for i in indices]))
#print(dijkstra(g))

'''
[0, 1, 2, 3, 4, 5, 6, 7]
'''