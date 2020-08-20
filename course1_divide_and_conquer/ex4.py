from typing import List, Union, Tuple, Optional, Dict

import re

#import copy

#from math import log

from tqdm import tqdm

import random


class TupleDict(dict):
    def __contains__(self, key):
        if super(TupleDict, self).__contains__(key):
            return True
        return any(key in k for k in self)

    def get_keys_from_tup(self, key):
        for k in self.keys():
            if all(k1 == k2 or k2 is None for k1, k2 in zip(k, key)):
                yield k


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
    def __init__(self) -> None:
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []
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
        #new_edge_hash = hash(new_edge)
        self.add_filter_identical_edges(list(node1_found.edge_dict.values()), node1_found.edge_dict, new_edge, node1_found.value)
        self.add_filter_identical_edges(list(node2_found.edge_dict.values()), node2_found.edge_dict, new_edge, node2_found.value)
        #node1_found.edge_dict[(new_edge_hash, (new_edge.node1.value, new_edge.node2.value))] = new_edge
        #node2_found.edge_dict[(new_edge_hash, (new_edge.node2.value, new_edge.node1.value))] = new_edge
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
                               edge_dict: TupleDict,
                               new_edge: Edge,
                               current_node_num: Optional[int] = None) -> None:
        if not edge_list:
            new_edge_hash = hash(new_edge)
            edge_list.append(new_edge)
            edge_dict[(new_edge_hash, (new_edge.node1.value, new_edge.node2.value))] = new_edge
        else:
            if (new_edge.node2.value, new_edge.node1.value) in edge_dict:
                if current_node_num is None:    # Graph version
                    pass
                else:   # Node version (first node should be the current node)
                    if new_edge.node2.value == current_node_num:
                        try:
                            selected_hash = [key[0] for key in list(edge_dict.keys()) if
                                             (key[1][0] == new_edge.node1.value) and (key[1][1] == new_edge.node2.value)][0]
                        except IndexError:
                            return None
                        del edge_dict[(selected_hash, (new_edge.node1.value, new_edge.node2.value))]
                        new_edge_hash = hash(new_edge)
                        edge_dict[(new_edge_hash, (new_edge.node2.value, new_edge.node1.value))] = new_edge
                    elif new_edge.node1.value == current_node_num:
                        try:
                            selected_hash = [key[0] for key in list(edge_dict.keys()) if
                                             (key[1][0] == new_edge.node2.value) and (key[1][1] == new_edge.node1.value)][0]
                        except IndexError:
                            return None
                        del edge_dict[(selected_hash, (new_edge.node2.value, new_edge.node1.value))]
                        new_edge_hash = hash(new_edge)
                        edge_dict[(new_edge_hash, (new_edge.node1.value, new_edge.node2.value))] = new_edge
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
        node2_edges = list(this_edge.node2.edge_dict.values())
        node2_keys = list(this_edge.node2.edge_dict.keys())
        node2_indices_to_remove: List[int] = []
        for edge in node2_edges:
            if edge not in list(this_edge.node2.edge_dict.values()):
                continue
            if (edge.node1.value == this_edge.node2.value) and (edge.node2.value == this_edge.node1.value):
                # del edge from edge.node1
                selected_hash = random.choice([key[0] for key in
                                               list(edge.node1.edge_dict.keys())
                                               if key[1] == (edge.node1.value,
                                                             edge.node2.value)])
                del edge.node1.edge_dict[(selected_hash,
                                          (edge.node1.value, edge.node2.value))]
                # del edge from edge.node2
                if not [key[0] for key in list(edge.node2.edge_dict.keys())
                                               if key[1] == (edge.node2.value,
                                                             edge.node1.value)]:
                    continue
                selected_hash = random.choice([key[0] for key in
                                               list(edge.node2.edge_dict.keys())
                                               if key[1] == (edge.node2.value,
                                                             edge.node1.value)])
                del edge.node2.edge_dict[(selected_hash,
                                          (edge.node2.value, edge.node1.value))]
                continue
            if edge.node1.value == this_edge.node2.value:
                # reroute connected edges
                edge.node1 = this_edge.node1
                # add "new" edges to involved nodes
                #this_edge.node1.edges.append(edge)
                # to this_edge node1 (and delete the old edge from this_edge.node1)
                if (this_edge.node1.value, this_edge.node2.value) in this_edge.node1.edge_dict:
                    # delete one of existing (if multiple exist)
                    selected_hash = random.choice([key[0] for key in
                                                   list(this_edge.node1.edge_dict.keys())
                                                   if key[1] == (this_edge.node1.value,
                                                                 this_edge.node2.value)])
                    del this_edge.node1.edge_dict[(selected_hash,
                                                   (this_edge.node1.value, this_edge.node2.value))]

                if (this_edge.node1.value, edge.node2.value) not in this_edge.node1.edge_dict:
                    edge_hash = hash(edge)
                    this_edge.node1.edge_dict[(edge_hash, (this_edge.node1.value, edge.node2.value))] = edge

                # to edge node2 (and delete the old edge from edge.node2)
                if (edge.node2.value, this_edge.node2.value) in edge.node2.edge_dict:
                    selected_hash = random.choice([key[0] for key in
                                                   list(edge.node2.edge_dict.keys())
                                                   if key[1] == (edge.node2.value,
                                                                 this_edge.node2.value)])
                    del edge.node2.edge_dict[(selected_hash,
                                              (edge.node2.value, this_edge.node2.value))]
                edge.node2.edge_dict[(hash(edge), (edge.node2.value, this_edge.node1.value))] = edge

                # remove edges from the fused node
                # from this_edge (node2)
                if (this_edge.node2.value, this_edge.node1.value) in this_edge.node2.edge_dict:
                    selected_hash = random.choice([key[0] for key in
                                                   node2_keys
                                                   if key[1] == (this_edge.node2.value,
                                                                 this_edge.node1.value)])

                    # idx = node2_edges.index(this_edge.node2.edge_dict[(selected_hash,
                    #                                               (this_edge.node2.value, this_edge.node1.value))])
                    # node2_indices_to_remove.append(idx)
                    try:
                        del this_edge.node2.edge_dict[(selected_hash,
                                                       (this_edge.node2.value, this_edge.node1.value))]
                        node2_keys.remove((selected_hash,
                                                       (this_edge.node2.value, this_edge.node1.value)))
                    except KeyError:
                        pass

                # from edge (node1)
                if (this_edge.node2.value, edge.node2.value) in this_edge.node2.edge_dict:
                    selected_hash = random.choice([key[0] for key in
                                                   node2_keys
                                                   if key[1] == (this_edge.node2.value,
                                                                 edge.node2.value)])

                    # idx = node2_edges.index(this_edge.node2.edge_dict[(selected_hash,
                    #                                               (this_edge.node2.value, edge.node2.value))])
                    # node2_indices_to_remove.append(idx)
                    del this_edge.node2.edge_dict[(selected_hash,
                                                   (this_edge.node2.value, edge.node2.value))]
                    node2_keys.remove((selected_hash,
                                                   (this_edge.node2.value, edge.node2.value)))

        # remove the indices
        # for index in sorted(node2_indices_to_remove, reverse=True):
        #     del node2_edges[index]



                #except Exception as e:
                #    print(f'{e.__class__} occured')

            # if edge.node2.value == this_edge.node2.value:
            #     try:
            #         self.edges.remove(edge)
            #         edge.node2 = this_edge.node1
            #         self.edges.append(edge)
            #     except Exception as e:
            #         print(f'{e.__class__} occured')

                # remove from Graph nodes and edges list
        # try:
        #     for key, val in self.edge_dict:
        #         if val == this_edge:
        #             del self.edge_dict[key]
        #     self.edges.remove(this_edge)
        # except Exception as e:
        #     print(f'{e.__class__} occured')
        try:
            self.nodes.remove(this_edge.node2)
        except Exception as e:
            pass
            #print(f'{e.__class__} occured')

        self.rebuild_graph_edges()

    @staticmethod
    def _compute_search_dict(dict: TupleDict) -> Dict:
        '''
        Structure of search dict is
        d[node1_value][node2_value][hash]
        '''
        d: Dict = {}

        for (hsh, (nd1, nd2)), edge in dict.items():
            if nd1 not in d:
                d[nd1]: Dict = {}
            if nd2 not in d[nd1]:
                d[nd1][nd2]: Dict = {}
            d[nd1][nd2][hsh] = edge
        return d

    def rebuild_graph_edges(self) -> None:
        '''
        Clears self loops automatically
        '''
        graph_dict: TupleDict = TupleDict()
        for node in self.nodes:
            graph_dict.update(node.edge_dict)

        keys = list(graph_dict.keys())
        for key in keys:
            nd1_val = key[1][0]
            nd2_val = key[1][1]
            # clear self loops
            if nd1_val == nd2_val:  # this is a self loop
                del graph_dict[key]
                keys.remove(key)
                continue
            try:
                #d: Dict = self._compute_search_dict(graph_dict)
                try:
                    opposite_keys: List = []
                    current_keys: List = []
                    for k in graph_dict:
                        if re.match(rf'\([0-9]+, \({nd2_val}, {nd1_val}\)\)', str(k)):
                            opposite_keys.append(k[0])
                        elif re.match(rf'\([0-9]+, \({nd1_val}, {nd2_val}\)\)', str(k)):
                            current_keys.append(k[0])
                    #opposite_keys: List[int] = [hsh for hsh in d[nd2_val][nd1_val].keys()]
                    #current_keys: List[int] = [hsh for hsh in d[nd1_val][nd2_val].keys()]
                except KeyError:
                    continue
                #opposite_keys = list(graph_dict.get_keys_from_tup((None, (nd2_val, nd1_val))))
                #current_keys = list(graph_dict.get_keys_from_tup((None, (nd1_val, nd2_val))))
                if (len(opposite_keys) > 1) and (key in graph_dict) and (len(current_keys) == 1):
                    del graph_dict[key]
                    keys.remove(key)
                else:
                    del graph_dict[(opposite_keys[0], (nd2_val, nd1_val))]
                    keys.remove((opposite_keys[0], (nd2_val, nd1_val)))
            except IndexError:
                continue
        self.edge_dict = graph_dict

    def clear_self_loops(self) -> None:
        self_loops: List[Edge] = []
        for edge in list(self.edge_dict.values()):
            if (edge.node1 == edge.node2) or (edge.node1.value == edge.node2.value):
                self_loops.append(edge)
        for key, edge in self.edge_dict:
            if edge in self_loops:
                del self.edge_dict[key]
                self_loops.remove(edge)


def get_cut(g_copy: Graph) -> Tuple[List[Edge], int]:
    #g_copy = copy.copy(g)
    #g_copy = copy.deepcopy(g)
    while len(g_copy.nodes) > 2:
        chosen_edge = random.choice(list(g_copy.edge_dict.values()))
        g_copy.fuze_nodes_of_edge(chosen_edge)
        #g_copy.clear_self_loops()
        #g_copy.rebuild_graph_edges()

    num_crossings: int = len(g_copy.edge_dict)
    return list(g_copy.edge_dict.values()), num_crossings

def get_min_cut(g_path: str, num_iter: Optional[float] = None) -> Tuple[List[Edge], int]:
    min_cut: Tuple[Optional[List[Edge]], float] = (None, float('inf'))
    # if num_iter is None:
    #     n = len(g.nodes)
    #     num_iter: int = int(round(n**2)*log(n))

    for _ in tqdm(range(num_iter), desc='searching for min_cuts'):
        g = read_input(g_path)
        cut = get_cut(g)
        if cut[1] < min_cut[1]:
            min_cut = cut
        del g
    return min_cut


# TODO: When there are 2 nodes left you DO need to keep opposite edges in the Graph!

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
#graph_test1 = read_input('ex4_test_case1.txt')
#graph_test1 = read_input('kargerMinCut.txt')
#cut_res = get_cut(graph_test1)

#min_cut_res = get_min_cut(graph_test1, 100)
#min_cut_res = get_min_cut('ex4_test_case0.txt', 16)
min_cut_res = get_min_cut('kargerMinCut.txt', 2)
#print(min_cut_res)
#print(min_cut_res[1])
#print(f'First cut: ({min_cut_res[0][0].node1.value},{min_cut_res[0][0].node2.value})')
#print(f'Second cut: ({min_cut_res[0][1].node1.value},{min_cut_res[0][1].node2.value})')
#print(f'Third cut: ({min_cut_res[0][2].node1.value},{min_cut_res[0][2].node2.value})')



# simple test for dict
# import pickle
# with open('example_dict.pickle', 'rb') as f:
#     dict: Dict = pickle.load(f)
#
# d: Dict = {}
#
# for (hsh, (nd1, nd2)), edge in dict.items():
#     if nd1 not in d:
#         d[nd1]: Dict = {}
#     if nd2 not in d[nd1]:
#         d[nd1][nd2]: Dict = {}
#     d[nd1][nd2][hsh] = edge
#
# a: int = 63
# b: int = 183
# lst: List = []
# for c in d[a][b].keys():
#     lst.append(c)
# lst

# d = {(123, (12, 14)): 'a', (149, (12, 16)): 'b', (654, (80, 90)): 'c', (443, (16, 12)): 'd', (109, (12, 14)): 'e'}
#
# a = 12
# b = 16
# lst = []
# for key in d:
#     if re.match(rf'\([0-9]+, \({a}, {b}\)\)', str(key)):
#         lst.append(key[0])
#
# for key in d:
#     print(str(key))
#
# re.match(r'\([0-9]+, \(12, 16\)\)', str((149, (12, 16))))
# re.match(r'\([0-9]+, \(12, 16\)\)', str((149, (12, 16))))