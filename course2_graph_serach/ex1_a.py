from __future__ import annotations

from typing import List, Optional, Dict, Tuple, TypeVar, Generic, Union

from collections import Counter, defaultdict, OrderedDict

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

    def __repr__(self) -> str:
        return repr(self.value)

Graph = List[Node]

def find_max_node_value(file: str) -> Tuple[int, int]:
    '''
    Returns max value for the current direction
    and the total max value (either direction)
    '''
    max_val: int = 0
    with open(file, 'r') as f:
        for i, line in enumerate(f, start=1):
            row: List[int] = [int(item) for item in line.strip().split(' ')]
            if row[0] > max_val:
                max_val = row[0]
            elif row[1] > max_val:
                max_val = row[1]
    offset: int = i - max_val
    return max_val, max_val + offset


from_to_nodes: Dict[Node, List[Node]] = defaultdict(list)
from_to_values: Dict[int, List[int]] = defaultdict(list)
nodes: Dict[int, Node] = {}

def read_input_to_graph(file: str, reversed: bool = False) -> Tuple[Graph, List[List[Node]], Graph]:
    to_nodes_length, output_length = find_max_node_value(file)
    offset = output_length - to_nodes_length
    output_list: Union[Graph, List[None]] = [None for _ in range(to_nodes_length)]
    output_general: Union[Graph, List[None]] = [None for _ in range(output_length - offset)]
    to_nodes: List[List[Node]] = [[] for _ in range(to_nodes_length)]

    with open(file, 'r') as f:
        for i, line in enumerate(f, start=1):
            row: List[int] = [int(item) for item in line.strip().split(' ')]
            origin, dest = row[0], row[1]
            # build nodes dict
            if origin not in nodes:
                nodes[origin] = Node(value=origin)
            if dest not in nodes:
                nodes[dest] = Node(value=dest)

            if dest not in from_to_values[origin]:
                from_to_values[origin].append(dest)
            if origin not in from_to_values[dest]:
                from_to_values[dest].append(origin)

            if nodes[dest] not in from_to_nodes[nodes[origin]]:
                from_to_nodes[nodes[origin]].append(nodes[dest])
            if nodes[origin] not in from_to_nodes[nodes[dest]]:
                from_to_nodes[nodes[dest]].append(nodes[origin])

            if i not in nodes:  # for omitted cases
                nodes[i] = Node(value=i)

            if reversed:
                if output_list[dest - 1] is None:
                    output_list[dest - 1] = nodes[dest]
                try:
                    if output_general[i - 1] is None:
                        output_general[i - 1] = nodes[i]
                except IndexError:
                    pass
                to_nodes[dest - 1].append(nodes[origin])
            else:
                if output_list[origin - 1] is None:
                    output_list[origin - 1] = nodes[origin]
                try:
                    if output_general[i - 1] is None:
                        output_general[i - 1] = nodes[i]
                except IndexError:
                    pass
                to_nodes[origin - 1].append(nodes[dest])
    return output_list, to_nodes, output_general

temp_rev, to_nodes_rev, g_graph = read_input_to_graph('./ex1_test_cases/test5', reversed=True)

def reverse_graph(g: Graph, to_nodes: List[List[Node]]) -> Tuple[Graph, List[List[Node]]]:
    '''
    Returns the reversed to_nodes list for the same Graph g
    '''
    reverse_list: List[List[Node]] = [[] for _ in range(len(g))]
    g_new: Union[Graph, List[None]] = [None for _ in range(len(g))]
    for node in g:
        if node is not None:
            for to_node in to_nodes[node.value - 1]:
                reverse_list[to_node.value - 1].append(node)
                if g_new[to_node.value - 1] is None:
                    g_new[to_node.value - 1] = to_node
    return g_new, reverse_list


global stack
stack = []

def dfs_loop(g: Graph, to_nodes: List[List[Node]], second_pass: bool = False) -> None:
    global t
    global s
    t = 0
    s = None
    n = len(g)
    if second_pass:
        while stack:
            i = stack.pop()
            if i is not None:
                if not i.seen2:
                    s = i
                    dfs(g, i, to_nodes, second_pass=True)
    else:
        for i in range(n-1, -1, -1):
            if g[i] is not None:
                if not g[i].seen:
                    s = g[i]
                    dfs(g, g[i], to_nodes)

def dfs(g: Graph, i: Node, to_nodes: List[List[Node]], second_pass: bool = False) -> None:
    global t
    global s
    if second_pass:
        i.seen2 = True
        i.leader = s
        for to_node in to_nodes[i.value - 1]:
            if not to_node.seen2:
                dfs(g, to_node, to_nodes, second_pass=True)
    else:
        i.seen = True
        for to_node in to_nodes[i.value - 1]:
            if not to_node.seen:
                dfs(g, to_node, to_nodes)
        t += 1
        i.finish_time = t
        stack.append(i)


def change_values(g: Graph, d: Dict) -> Graph:
    for k, v in d.items():
        g[k-1].value = v
    return g

def arrange_nodes_for_2nd_pass(to_nodes: List[List[Node]], d: Dict) -> List[List[Node]]:
    nodes_list: List[List[Node]] = [[] for _ in range(len(to_nodes))]
    for i, item in enumerate(to_nodes):
        if (i + 1) in d:
            new_i = d[(i + 1)]
            nodes_list[new_i - 1] = item
    return nodes_list


def get_scc_sizes(g: Graph) -> List[Tuple[int, int]]:
    '''
    Returns the 5 largest SCCs (by number of nodes with the same leader)
    '''
    leaders = [node.leader.value for node in g]
    return Counter(leaders).most_common(5)

dfs_loop(g_graph, to_nodes_rev)
_, to_nodes = reverse_graph(temp_rev, to_nodes_rev)

finish_times_dict = {i.value: i.finish_time for i in g_graph}
g_graph1 = change_values(g_graph, finish_times_dict)
to_nodes_switched = arrange_nodes_for_2nd_pass(to_nodes, finish_times_dict)
dfs_loop(g_graph1, to_nodes_switched, second_pass=True)

print(get_scc_sizes(g_graph1))