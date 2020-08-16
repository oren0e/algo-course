from typing import List, Union, Tuple, Optional

import re

import copy

from math import log

import random

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.edges: List[Edge] = []


class Edge:
    def __init__(self, node1: Node, node2: Node) -> None:
        self.node1 = node1
        self.node2 = node2


class Graph:
    def __init__(self, nodes: List[Node] = [], edges: List[Edge] = []) -> None:
        self.nodes = nodes
        self.edges = edges
        # TODO: add containers for fused nodes

    def add_node(self, new_node_val: int) -> None:
        new_node = Node(new_node_val)
        self.nodes.append(new_node)

    def add_edge(self, node1_value: int, node2_value: int) -> None:
        node1_found = None
        node2_found = None
        # check if nodes already exist
        for node in self.nodes:
            if node1_value == node.value:
                node1_found = node
            if node2_value == node.value:
                node2_found = node
        if node1_found is None:
            node1_found = Node(node1_value)
            self.nodes.append(node1_found)
        if node2_found is None:
            node2_found = Node(node2_value)
            self.nodes.append(node2_found)

        new_edge = Edge(node1_found, node2_found)
        node1_found.edges.append(new_edge)
        node2_found.edges.append(new_edge)
        self.edges.append(new_edge)

    def get_adjacency_list(self) -> List:
        '''
        Return list of lists. Outer list index is the Node value.
        Inner list has the adjacent nodes values.
        '''
        lst = [None for _ in range(len(self.nodes) + 1)]
        for node in self.nodes:
            if (len(node.edges) == 1) and (node.edges[0].node2.value == node.value):
                continue
            inner_list = []
            for edge in node.edges:
                if edge.node2.value == node.value:
                    continue
                inner_list.append(edge.node2.value)
            if inner_list:
                lst[node.value] = inner_list
        return lst

    def fuze_nodes_of_edge(self, this_edge: Edge) -> None:
        '''
        Without loss of generality the node that vanishes
        will be always node2
        '''
        # treat all the edges of the fused node
        for edge in this_edge.node2.edges:
            if edge == this_edge:
                continue
            if edge.node1.value == this_edge.node2.value:
                self.edges.remove(edge)
                edge.node1 = this_edge.node1
            if edge.node2.value == this_edge.node2.value:
                self.edges.remove(edge)
                edge.node2 = this_edge.node1
            self.edges.append(edge)

        self.nodes.remove(this_edge.node2)
        self.edges.remove(this_edge)

    def clear_self_loops(self) -> None:
        for edge in self.edges:
            if (edge.node1 == edge.node2) or (edge.node1.value == edge.node2.value):
                self.edges.remove(edge)     # this is a self loop


def get_cut(g: Graph) -> Tuple[Node, Node, int]:
    g_copy = copy.deepcopy(g)
    while len(g_copy.nodes) > 2:
        chosen_edge = random.choice(g_copy.edges)
        g_copy.fuze_nodes_of_edge(chosen_edge)
        g_copy.clear_self_loops()

    num_crossings: int = len(g_copy.edges)
    return g_copy.edges[0].node1, g_copy.edges[0].node2, num_crossings

def get_min_cut(g: Graph, num_iter: Optional[float] = None) -> Tuple[Node, Node, int]:
    min_cut: Tuple[Optional[Node], Optional[Node], float] = (None, None, float('inf'))
    if num_iter is None:
        n = len(g.nodes)
        num_iter: int = int(round(n**2)*log(n))

    for iter in range(num_iter):
        cut = get_cut(g)
        if cut[2] < min_cut[2]:
            min_cut = cut
    return min_cut




# read the input
input_list: List[List[Union[str, int]]] = []
with open('kargerMinCut.txt', 'r') as f:
    for line in f:
        row_list: List[str] = []
        row_string: str = re.sub(r'[\t]',' ',line.rstrip())
        row_list.extend(row_string.split(' '))
        input_list.append(row_list)

# make it int instead of str
for i, sub_list in enumerate(input_list):
    for j, num in enumerate(sub_list):
        input_list[i][j] = int(input_list[i][j])

# read into Graph class
grph = Graph()
for sub_list in input_list:
    for num in sub_list[1:]:
        grph.add_edge(sub_list[0], num)

res = grph.get_adjacency_list()     # res[0] is None. res[1] to res[200] contain the data.

