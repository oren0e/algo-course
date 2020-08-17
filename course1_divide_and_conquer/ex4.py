from typing import List, Union, Tuple, Optional, Dict

import re

import copy

from math import log

from tqdm import tqdm

import random


class TupleDict(dict):
    def __contains__(self, key):
        if super(TupleDict, self).__contains__(key):
            return True
        return any(key in k for k in self)


class Node:
    def __init__(self, value) -> None:
        '''
        edge_dict is dict[(edge_hash,(edge.node1.value, edge.node2.value)), edge]
        '''
        self.value = value
        #self.edges: List[Edge] = []
        self.edge_dict: TupleDict[Tuple[int, Tuple[int, int]], Edge] = TupleDict({})


class Edge:
    def __init__(self, node1: Node, node2: Node) -> None:
        self.node1 = node1
        self.node2 = node2


class Graph:
    def __init__(self, nodes: List[Node] = [], edges: List[Edge] = []) -> None:
        self.nodes = nodes
        self.edges = edges
        self.edge_dict: TupleDict[Tuple[int, Tuple[int, int]], Edge] = TupleDict({})

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
        new_edge_hash = hash(new_edge)
        # self.add_filter_identical_edges(node1_found.edges, node1_found.edge_dict, new_edge)
        # self.add_filter_identical_edges(node2_found.edges, node2_found.edge_dict, new_edge)
        node1_found.edge_dict[(new_edge_hash, (new_edge.node1.value, new_edge.node2.value))] = new_edge
        node2_found.edge_dict[(new_edge_hash, (new_edge.node2.value, new_edge.node1.value))] = new_edge
        #node2_found.edges.append(new_edge)

        # avoid appending the same edge twice (only in the Graph case)
        self.add_filter_identical_edges(self.edges, self.edge_dict, new_edge)
        # if not self.edges:
        #     self.edges.append(new_edge)
        #     self.edge_dict[(new_edge.node1.value, new_edge.node2.value)] = new_edge
        # else:
        #     if (new_edge.node2.value, new_edge.node1.value) in self.edge_dict:
        #         pass
        #     else:
        #         self.edges.append(new_edge)
        #         self.edge_dict[(new_edge.node1.value, new_edge.node2.value)] = new_edge

    @staticmethod
    def add_filter_identical_edges(edge_list: List[Edge],
                               edge_dict: TupleDict[Tuple[int, Tuple[int, int]], Edge],
                               new_edge: Edge) -> None:
        if not edge_list:
            new_edge_hash = hash(new_edge)
            edge_list.append(new_edge)
            edge_dict[(new_edge_hash, (new_edge.node1.value, new_edge.node2.value))] = new_edge
        else:
            if (new_edge.node2.value, new_edge.node1.value) in edge_dict:
                pass
            else:
                new_edge_hash = hash(new_edge)
                edge_list.append(new_edge)
                edge_dict[(new_edge_hash, (new_edge.node1.value, new_edge.node2.value))] = new_edge

    def get_adjacency_list(self) -> List:
        '''
        Return list of lists. Outer list index is the Node value.
        Inner list has the adjacent nodes values.
        '''
        lst = [None for _ in range(len(self.nodes) + 1)]
        for node in self.nodes:
            if (len(node.edge_dict) == 1) and (list(node.edge_dict.keys())[0][1][1] == node.value):
                continue
            inner_list = []
            for edge in node.edge_dict.values():
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
        for edge in this_edge.node2.edge_dict.values():
            if edge == this_edge:
                continue
                #edge.node1.edges.remove()
            if edge.node1.value == this_edge.node2.value:
                try:
                    # reroute connected edges
                    edge.node1 = this_edge.node1
                    # add "new" edges to involved nodes
                    #this_edge.node1.edges.append(edge)
                    # to this_edge node1 (and delete the old edge from this_edge.node1)
                    if (this_edge.node1.value, this_edge.node2.value) in this_edge.node1.edge_dict:
                        del this_edge.node1.edge_dict[(this_edge.node1.value, this_edge.node2.value)]
                    if (this_edge.node1.value, edge.node2.value) not in this_edge.node1.edge_dict:
                        this_edge.node1.edge_dict[(this_edge.node1.value, edge.node2.value)] = edge

                    # to edge node2 (and delete the old edge from edge.node2)
                    if (edge.node2.value, this_edge.node2.value) in edge.node2.edge_dict:
                        del edge.node2.edge_dict[(edge.node2.value, this_edge.node2.value)]
                    edge.node2.edge_dict[(edge.node2.value, this_edge.node1.value)] = edge

                    # remove edges from the fused node
                    # from this_edge (node2)
                    if (this_edge.node2.value, this_edge.node1.value) in this_edge.node2.edge_dict:
                        del this_edge.node2.edge_dict[(this_edge.node2.value, this_edge.node1.value)]

                    # from edge (node1)
                    if (this_edge.node2.value, edge.node2.value) in this_edge.node2.edge_dict:
                        del this_edge.node2.edge_dict[(this_edge.node2.value, edge.node2.value)]

                    # remove from Graph nodes and edges list



                    self.edges.remove(edge)
                    edge.node1 = this_edge.node1
                    self.edges.append(edge)
                except ValueError:
                    #print('edge not in list')
                    break
            if edge.node2.value == this_edge.node2.value:
                try:
                    self.edges.remove(edge)
                    edge.node2 = this_edge.node1
                    self.edges.append(edge)
                except ValueError:
                    #print('edge not in list')
                    break


        try:
            self.nodes.remove(this_edge.node2)
        except ValueError:
            pass
            #print('node is not in list')
        try:
            self.edges.remove(this_edge)
        except ValueError:
            pass
            #print('selected edge not in list')

    def clear_self_loops(self) -> None:
        edge_list = self.edges
        for edge in edge_list:
            if (edge.node1 == edge.node2) or (edge.node1.value == edge.node2.value):
                edge_list.remove(edge)     # this is a self loop


def get_cut(g: Graph) -> Tuple[List[Edge], int]:
    g_copy = copy.deepcopy(g)
    while len(g_copy.nodes) > 2:
        chosen_edge = random.choice(g_copy.edges)
        g_copy.fuze_nodes_of_edge(chosen_edge)
        g_copy.clear_self_loops()

    num_crossings: int = len(g_copy.edges)
    return g_copy.edges, num_crossings


def get_min_cut(g: Graph, num_iter: Optional[float] = None) -> Tuple[List[Edge], int]:
    min_cut: Tuple[Optional[List[Edge]], float] = (None, float('inf'))
    if num_iter is None:
        n = len(g.nodes)
        num_iter: int = int(round(n**2)*log(n))

    for _ in tqdm(range(num_iter), desc='searching for min_cuts'):
        cut = get_cut(g)
        if cut[1] < min_cut[1]:
            min_cut = cut
    return min_cut




# read the input
def read_input(file: str) -> Graph:
    input_list: List[List[Union[str, int]]] = []
    with open(file, 'r') as f:
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
    return grph

#res = grph.get_adjacency_list()     # res[0] is None. res[1] to res[200] contain the data.

# test cases
graph_test1 = read_input('ex4_test_case0.txt')
#graph_test1 = read_input('kargerMinCut.txt')
cut_res = get_cut(graph_test1)

# min_cut_res = get_min_cut(graph_test1, 16)
# print(min_cut_res[1])
# print(f'First cut: ({min_cut_res[0][0].node1.value},{min_cut_res[0][0].node2.value})')
# print(f'Second cut: ({min_cut_res[0][1].node1.value},{min_cut_res[0][1].node2.value})')
