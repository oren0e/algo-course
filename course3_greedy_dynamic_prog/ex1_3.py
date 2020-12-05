"""
Prim's minimum spanning tree algorithm
"""
from __future__ import annotations

from heapq import heappop, heappush
import heapq

from dataclasses import dataclass, field

from typing import TypeVar, List, Dict, Generic, NamedTuple, Generator, Optional, Union

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
        raise RuntimeError("Empty heap")

    def __repr__(self) -> str:
        return repr(self._data)



class Vertex:
    def __init__(self, value: int, cost: int,
                 in_frontier: bool = False,
                 key: Optional[Union[int, float]] = None,
                 key_vertex: Optional[Vertex] = None) -> None:
        self.value = value
        self.cost = cost
        self.in_frontier = in_frontier   # in X or not
        self.key = key                   # cheapest edge (cost)
        self.key_vertex = key_vertex     # the other vertex for the cheapest edge

    def __lt__(self, other: Vertex) -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        return repr(f"Vertex(value={self.value}, cost={self.cost}, "
                    f"in_frontier={self.in_frontier}, key={self.key}, key_vertex={self.key_vertex})")


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
        res_list[int(tup[0]) - 1].append(Vertex(int(tup[1]), int(tup[2])))      # undirected graph: each edge appears twice!
        res_list[int(tup[1]) - 1].append(Vertex(int(tup[0]), int(tup[2])))
    return res_list


g: Graph = build_graph('ex1_test_cases/ex1_3_test0')


def prim_overall_cost(g: Graph) -> int:
    """
    :param g: Adjacency list representing a graph which is List[List[Vertex]].
              Vertex is a NamedTuple
    :return: Overall cost of a minimum spanning tree found by the algorithm.
    """
    random.seed(902)
    x: List[Vertex] = []
    # v_minus_x: List[Vertex] = []
    t: List[Vertex] = []

    # choose first vertex randomly
    first_vertex: Vertex = random.choice(g[random.choice(range(len(g)))])
    x.append(first_vertex)
    first_vertex.in_frontier = True
    #g[first_vertex.value - 1] = True
    v_minus_x = [v for sub_list in g for v in sub_list if v.value != first_vertex.value]

    def get_key_vertex(v: Vertex) -> Optional[Vertex]:
        """
        General function to compute the key of a vertex,
        where v is compared to other "many" vertices in 'other_vertices'
        """
        try:
            candidate: Vertex = min([vertex for vertex in g[v.value - 1] if vertex.in_frontier], key=lambda x: x.cost)
            #candidates: List[Vertex] = [vertex for vertex in g[v.value - 1] if vertex.in_frontier]
        except ValueError:
            return None
        # assert all(candidate.cost == candidates[0].cost for candidate in candidates),\
        #             "Costs not equal in min candidates!"
        # return random.choice(candidates)
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
        h.heap_push(vertex)

    for i, vertx in enumerate(h._data):
        vertices_in_heap[vertx.value] = i

    while set(x) != set(v_minus_x):
        popped_vertex: Vertex = h.heap_pop()    # v
        x.append(popped_vertex)
        # TODO: popped_vertex.in_frontier = True
        v_minus_x = [v for sub_list in g for v in sub_list if v.value != popped_vertex.value]
        # maintain invariant 2
        popped_vertex_edges: List[Vertex] = g[popped_vertex.value - 1]
        for member_vertex in popped_vertex_edges:
            if member_vertex in v_minus_x:
                h.heap_delete(vertices_in_heap[member_vertex.value])
                # recompute key of w
                member_vertex.key = min(member_vertex.key, member_vertex.cost)
                member_vertex.key_vertex = popped_vertex
                h.heap_push(member_vertex)
                # update dictionary
                for i, vertx in enumerate(h._data):
                    vertices_in_heap[vertx.value] = i

    return sum(v.cost for v in x)

prim_overall_cost(g)