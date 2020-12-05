"""
Prim's minimum spanning tree algorithm
"""
from __future__ import annotations

from heapq import heappop, heappush
import heapq

from typing import TypeVar, List, Dict, Generic, NamedTuple, Generator, Optional, Union, Set

import random

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
        else:
            raise RuntimeError("Empty heap")

    def __repr__(self) -> str:
        return repr(self._data)



class Vertex:
    def __init__(self, value: int, cost: int,
                 key: Optional[Union[int, float]] = None,
                 key_vertex: Optional[Vertex] = None) -> None:
        self.value = value
        self.cost = cost
        # self.in_frontier = in_frontier   # in X or not
        self.key = key                   # cheapest edge (cost)
        self.key_vertex = key_vertex     # the other vertex for the cheapest edge

    def __lt__(self, other: Vertex) -> bool:
        return self.key < other.key

    def __repr__(self) -> str:
        return repr(f"Vertex(value={self.value}, cost={self.cost}, "
                    f"key={self.key})")


Graph = List[List[Vertex]]
frontier: Set[int] = set()          # set of values of vertices
pushed_to_heap: Set[int] = set()    # set of values of vertices

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
        res_list[int(tup[0]) - 1].append(Vertex(int(tup[1]), int(tup[2])))      # undirected graph: each edge appears twice!
        res_list[int(tup[1]) - 1].append(Vertex(int(tup[0]), int(tup[2])))
    return res_list


g: Graph = build_graph('ex1_test_cases/ex1_3_test2')


def prim_overall_cost(g: Graph) -> int:
    """
    :param g: Adjacency list representing a graph which is List[List[Vertex]].
              Vertex is a NamedTuple
    :return: Overall cost of a minimum spanning tree found by the algorithm.
    """
    random.seed(902)
    x: List[Vertex] = []
    V: Set[int] = set(v for v in range(1, len(g) + 1))      # all vertices values
    # v_minus_x: List[Vertex] = []
    #t: List[Vertex] = []


    # choose first vertex randomly
    first_vertex: Vertex = random.choice(g[random.choice(range(len(g)))])
    x.append(first_vertex)
    frontier.add(first_vertex.value)
    v_minus_x = [v for sub_list in g for v in sub_list if v.value != first_vertex.value]

    def get_key_vertex(v: Vertex) -> Optional[Vertex]:
        """
        General function to compute the key of a vertex,
        where v is compared to other "many" vertices in 'other_vertices'
        """
        try:
            candidate: Vertex = min([vertex for vertex in g[v.value - 1] if vertex.value in frontier], key=lambda x: x.cost)
        except ValueError:
            return None
        return candidate

    # initial computation of keys
    h: Heap[Vertex] = Heap()
    vertices_in_heap: Dict[int, int] = {}   # {vertex.value: position_in_heap}

    for vertex in v_minus_x:
        cheapset_vertex = get_key_vertex(vertex)
        if cheapset_vertex:
            vertex.key = cheapset_vertex.cost
            vertex.key_vertex = cheapset_vertex
        else:
            vertex.key = float("inf")
        if vertex.value not in pushed_to_heap:
            h.heap_push(vertex)
            pushed_to_heap.add(vertex.value)

    def update_mapping() -> None:
        for i, vertx in enumerate(h._data):
            vertices_in_heap[vertx.value] = i
    update_mapping()

    while frontier != V:
        popped_vertex: Vertex = h.heap_pop()    # v
        update_mapping()
        x.append(popped_vertex)
        frontier.add(popped_vertex.value)
        v_minus_x = [v for sub_list in g for v in sub_list if v.value != popped_vertex.value]
        # maintain invariant 2
        popped_vertex_edges: List[Vertex] = g[popped_vertex.value - 1]
        for member_vertex in popped_vertex_edges:
            if member_vertex.value not in frontier:
                #if not h.is_empty:
                h.heap_delete(vertices_in_heap[member_vertex.value])
                update_mapping()
                # recompute key of w
                member_vertex.key = min(member_vertex.key, member_vertex.cost)
                member_vertex.key_vertex = popped_vertex
                h.heap_push(member_vertex)
                # update dictionary
                update_mapping()
                #else:
                #    break
    return sum(v.key for v in x if v.key)

prim_overall_cost(g)