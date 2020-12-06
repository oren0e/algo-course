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


class Edge(NamedTuple):
    value: int
    with_vertex: int


class Vertex:
    def __init__(self, value: int, key: Optional[Union[int, float]] = None) -> None:
        self.value = value
        self.key = key                   # cheapest edge (cost)
        self.edges: List[Edge] = []

    def __lt__(self, other: Vertex) -> bool:
        return self.key < other.key

    def __repr__(self) -> str:
        return repr(f"Vertex(value={self.value}, key={self.key}\n Edges: {self.edges})")


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
    vertex_dict: Dict[int, Vertex] = {}
    for tup in read_data_gen(file):
        if int(tup[0]) not in vertex_dict:
            vertex_dict[int(tup[0])] = Vertex(value=int(tup[0]))
        if int(tup[1]) not in vertex_dict:
            vertex_dict[int(tup[1])] = Vertex(value=int(tup[1]))

        vertex_dict[int(tup[0])].edges.append(Edge(value=int(tup[2]), with_vertex=vertex_dict[int(tup[1])].value))
        vertex_dict[int(tup[1])].edges.append(Edge(value=int(tup[2]), with_vertex=vertex_dict[int(tup[0])].value))
        res_list[int(tup[0]) - 1].append(vertex_dict[int(tup[1])])      # undirected graph: each edge appears twice!
        res_list[int(tup[1]) - 1].append(vertex_dict[int(tup[0])])
    return res_list


g: Graph = build_graph('ex1_test_cases/ex1_3_test0')


def prim_overall_cost(g: Graph) -> int:
    """
    :param g: Adjacency list representing a graph which is List[List[Vertex]].
    :return: Overall cost of a minimum spanning tree found by the algorithm.
    """
    random.seed(902)
    x: List[Vertex] = []
    V: Set[int] = set(v for v in range(1, len(g) + 1))      # all vertices values

    # choose first vertex randomly
    first_vertex: Vertex = random.choice(g[random.choice(range(len(g)))])
    x.append(first_vertex)
    frontier.add(first_vertex.value)
    v_minus_x: Set[Vertex] = set([v for sub_list in g for v in sub_list if v.value != first_vertex.value])

    def compute_key(v: Vertex) -> int:
        min_cost = float("inf")
        for vertex in g[v.value - 1]:
            if vertex.value in frontier:
                for edge in vertex.edges:
                    if edge.with_vertex == v.value:
                        min_cost = min(min_cost, edge.value)
        return min_cost

    # initial computation of keys
    h: Heap[Vertex] = Heap()
    vertices_in_heap: Dict[int, int] = {}   # {vertex.value: position_in_heap}

    for vertex in v_minus_x:
        vertex.key = compute_key(vertex)
        # if not vertex.key:
        #     vertex.key = float("inf")
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
        v_minus_x = {v for v in v_minus_x if v.value != popped_vertex.value}
        #v_minus_x = [v for sub_list in g for v in sub_list if v.value != popped_vertex.value]
        # maintain invariant 2
        popped_vertex_vertices: List[Vertex] = g[popped_vertex.value - 1]
        for member_vertex in popped_vertex_vertices:
            if member_vertex.value not in frontier:
                #if not h.is_empty:
                h.heap_delete(vertices_in_heap[member_vertex.value])
                update_mapping()
                # recompute key of w
                member_vertex.key = min(member_vertex.key, compute_key(member_vertex))
                h.heap_push(member_vertex)
                # update dictionary
                update_mapping()
                #else:
                #    break
    return sum(v.key for v in x if v.key)

prim_overall_cost(g)