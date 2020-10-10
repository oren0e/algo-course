'''
We will have to do the following:
1. Find the highest label number (optional)
2. Represent Node as a NamedTuple with seen, value, and finish_time
3. Represent a Graph (with adjacency list)
4. Write the dfs() function
5. Write the dfs_loop() function
6. Write the find_scc() mother-function
'''

from __future__ import annotations

from typing import List, Optional, Dict, Tuple, TypeVar, Generic, Union

from collections import Counter

import heapq

import copy

import random

random.seed(1273)
T = TypeVar('T')

class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.finish_time: Optional[int] = None
        self.seen = False
        self.seen2 = False
        self.leader: Optional[Node] = None
        #self.to_nodes: List[Node] = []

    def __lt__(self, other: Node) -> bool:
        return self.finish_time < other.finish_time

    def __repr__(self) -> str:
        return repr(self.value)

    # @property
    # def get_to_nodes(self) -> List[int]:
    #     return [to_node.value for to_node in self.to_nodes]


class PriorityQueue(Generic[T], list):
    def __init__(self) -> None:
        self._data: List[Optional[T]] = []
        super().__init__()

    @property
    def is_empty(self) -> bool:
        return not self._data

    def push(self, v: T) -> None:
        heapq.heappush(self._data, v)

    def popq(self) -> Optional[T]:
        if not self.is_empty:
            return heapq.heappop(self._data)
        else:
            return None

    def __repr__(self) -> str:
        return repr(self._data)


Graph = List[Node]


def find_max_node_value(file: str) -> int:
    max_val: int = 0
    with open(file, 'r') as f:
        for line in f:
            row: List[int] = [int(item) for item in line.strip().split(' ')]
            if row[0] > max_val:
                max_val = row[0]
            elif row[1] > max_val:
                max_val = row[1]
    return max_val

# TODO: if a value does not appear at all e.g. 1 to 10 except that 4
#   does not appear, it will be None. This None can interfere, check that out!


def read_input_to_graph(file: str, reversed: bool = False) -> Tuple[Graph, Graph]:
    output_list: Graph = [None for _ in range(find_max_node_value(file))]
    to_nodes: Union[Graph, List[List]] = [[] for _ in range(find_max_node_value(file))]
    nodes: Dict[int, Node] = {}
    with open(file, 'r') as f:
        for line in f:
            row: List[int] = [int(item) for item in line.strip().split(' ')]
            origin, dest = row[0], row[1]
            # build nodes dict
            if origin not in nodes:
                nodes[origin] = Node(value=origin)
            if dest not in nodes:
                nodes[dest] = Node(value=dest)

            if reversed:
                if output_list[dest - 1] is None:
                    output_list[dest - 1] = nodes[dest]
                to_nodes[dest - 1].append(nodes[origin])
            else:
                if output_list[origin - 1] is None:
                    output_list[origin - 1] = nodes[origin]
                to_nodes[origin - 1].append(nodes[dest])
    return output_list, to_nodes


def reverse_graph(g: Graph, finish_time_values: bool = False) -> Graph:
    reverse_list: List[Union[Node, List]] = [Node(value=-(len(g)+1)) for _ in range(len(g))]
    for node in g:
        for to_node in node.to_nodes:
            if finish_time_values:
                reverse_list[to_node.value - 1].value = to_node.finish_time * (-1)
            else:
                reverse_list[to_node.value - 1].value = to_node.value

            reverse_list[to_node.value - 1].to_nodes.append(node)
            reverse_list[to_node.value - 1].seen = to_node.seen
            reverse_list[to_node.value - 1].seen2 = to_node.seen2
            reverse_list[to_node.value - 1].finish_time = to_node.finish_time
            reverse_list[to_node.value - 1].leader = to_node.leader
    return reverse_list


#temp = read_input_to_graph('./ex1_test_cases/test1')
temp_rev, to_nodes_rev = read_input_to_graph('./ex1_test_cases/test1', reversed=True)

# TODO: the nodes that are in .to_nodes are not changed in this way and that is a problem!
#       maybe I need to switch from using the priority queue.
def max_heap_value(node: Node) -> Node:
    node.value = node.finish_time
    node.finish_time = node.finish_time * (-1)
    return node

global pq
pq = PriorityQueue()

def dfs_loop(g: Graph,
             finish_time_values: bool = False) -> None:
    global t
    global s
    t = 0
    s = None
    n = len(g)
    if finish_time_values:
        while not pq.is_empty:
            i = pq.popq()
            if not g[i.value - 1].seen2:
                s = i
                dfs(g, g[i.value - 1], second_pass=True)
    else:
        for i in range(n-1, -1, -1):
            if not g[i].seen:
                s = i
                dfs(g, g[i])

def dfs(g: Graph, i: Node, second_pass: bool = False) -> None:
    '''
    Depth-first-search
    '''
    global t
    global s
    if second_pass:
        i.seen2 = True
        i.leader = g[s.value - 1]
        for to_node in i.to_nodes:
            if not to_node.seen2:
                dfs(g, to_node, second_pass=True)
    else:
        i.seen = True
        #i.leader = g[s]
        for to_node in i.to_nodes:
            if not to_node.seen:
                dfs(g, to_node)
        t += 1
        i.finish_time = t
        pq.push(max_heap_value(i))

def get_scc_sizes(g: Graph) -> List[Tuple[int, int]]:
    '''
    Returns the 5 largest SCCs (by number of nodes with the same leader)
    '''
    leaders = [node.leader.value for node in g]
    return Counter(leaders).most_common(5)

# trying
dfs_loop(temp_rev)
temp = reverse_graph(temp_rev)
dfs_loop(temp, finish_time_values=True)
