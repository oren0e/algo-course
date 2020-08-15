from typing import List, Tuple

import re

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

    def add_node(self, new_node_val: int) -> None:
        new_node = Node(new_node_val)
        self.nodes.append(new_node)

    def add_edge(self, node1: Node, node2: Node) -> None:
        new_edge = Edge(node1, node2)
        self.edges.append(new_edge)

    def get_adjacency_list(self) -> List[List[int]]:
        '''
        Return list of lists. Outer list index is the Node value.
        Inner list has the adjacent nodes values.
        '''
        lst = [None for _ in range(len(self.nodes))]
        for i, node in enumerate(self.nodes, 1):
            if node.value == i:
                inner_list = []
                for edge in node.edges:
                    inner_list.append(edge.node2.value)
            if inner_list:
                lst[i] = inner_list
        return lst

# read the input
input_list: List[List[int]] = []
with open('kargerMinCut.txt', 'r') as f:
    for line in f:
        row_list: List[int] = []
        row_string: str = re.sub(r'[\t]',' ',line.rstrip())
        row_list.extend(row_string.split(' '))
        input_list.append(row_list)

# make it int instead of str
for i, sub_list in enumerate(input_list):
    for j, num in enumerate(sub_list):
        input_list[i][j] = int(input_list[i][j])