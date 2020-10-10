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
        self.old_value = None
        self.been_switched = False

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


def read_input_to_graph(file: str, reversed: bool = False) -> Tuple[Graph, List[List[Node]]]:
    output_list: Union[Graph, List[None]] = [None for _ in range(find_max_node_value(file))]
    to_nodes: List[List[Node]] = [[] for _ in range(find_max_node_value(file))]
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

#temp = read_input_to_graph('./ex1_test_cases/test1')
temp_rev, to_nodes_rev = read_input_to_graph('./ex1_test_cases/test1', reversed=True)
#temp, to_nodes = reverse_graph(temp_rev, to_nodes_rev)

# TODO: the nodes that are in .to_nodes are not changed in this way and that is a problem!
#       maybe I need to switch from using the priority queue.
old_new_values: Dict[int, int] = {}  # old_value: new_value

def reverse_graph(g: Graph, to_nodes: List[List[Node]]) -> Tuple[Graph, List[List[Node]]]:
    '''
    Returns the reversed to_nodes list for the same Graph g
    '''
    reverse_list: List[List[Node]] = [[] for _ in range(len(g))]
    g_new: Union[Graph, List[None]] = [None for _ in range(len(g))]
    for node in g:
        for to_node in to_nodes[node.value - 1]:
            reverse_list[to_node.value - 1].append(node)
            if g_new[to_node.value - 1] is None:
                g_new[to_node.value - 1] = to_node
    return g_new, reverse_list

def max_heap_value(node: Node) -> Node:
    node_copy = copy.deepcopy(node)
    node_copy.old_value = node_copy.value
    node_copy.value = node_copy.finish_time
    node_copy.finish_time = node_copy.finish_time * (-1)
    if node_copy.old_value not in old_new_values:
        old_new_values[node_copy.old_value] = node_copy.value
    return node_copy

global pq
pq = PriorityQueue()

def switch_to_nodes_values(to_nodes: List[List[Node]]) -> List[List[Node]]:
    '''
    Switches the old values to the new finish_time values.
    Also switches the relevant indices in the adjacency list
    '''
    nodes_list: List[List[Node]] = [None for _ in range(len(to_nodes))]
    for i, item in enumerate(to_nodes):
        for to_node in item:
            if (to_node.value in old_new_values) and (not to_node.been_switched):
                # TODO: consider assigning entire node and not just its value
                #nodes_list[old_new_values[to_node.value].value - 1].append(to_node)
                to_node.value = old_new_values[to_node.value]
                to_node.been_switched = True
        # find the new value for i+1
        if (i+1) in old_new_values:
            new_i = old_new_values[(i+1)]
            nodes_list[new_i - 1] = item
    return nodes_list


def dfs_loop(g: Graph, to_nodes: List[List[Node]],
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
                dfs(g, g[i.value - 1], to_nodes, second_pass=True)
    else:
        for i in range(n-1, -1, -1):
            if not g[i].seen:
                s = i + 1
                dfs(g, g[i], to_nodes)

def dfs(g: Graph, i: Node, to_nodes: List[List[Node]], second_pass: bool = False) -> None:
    '''
    Depth-first-search
    '''
    global t
    global s
    if second_pass:
        i.seen2 = True
        i.leader = g[s.value - 1]
        for to_node in to_nodes[i.value - 1]:
            if not to_node.seen2:
                dfs(g, to_node, to_nodes, second_pass=True)
    else:
        i.seen = True
        i.leader = g[s - 1]
        for to_node in to_nodes[i.value - 1]:
            if not to_node.seen:
                dfs(g, to_node, to_nodes)
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
dfs_loop(temp_rev, to_nodes_rev)
temp, to_nodes = reverse_graph(temp_rev, to_nodes_rev)
to_nodes = switch_to_nodes_values(to_nodes)
dfs_loop(temp, to_nodes, finish_time_values=True)

get_scc_sizes(temp)