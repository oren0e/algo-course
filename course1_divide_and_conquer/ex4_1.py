from typing import List, Union

import re

import random

from tqdm import tqdm

import copy

class Graph:
    def __init__(self, data: List[List[int]]) -> None:
        self.data = data
        
    def __repr__(self) -> str:
        return f'{self.__class__} with {self.num_nodes} nodes ' \
               f'and {self.num_edges} edges'

    @property
    def num_nodes(self) -> int:
        return sum(1 for sub_list in self.data if sub_list)

    @property
    def num_edges(self) -> int:
        return sum(len(sub_list) for sub_list in self.data) // 2

    def get_num_crossings(self) -> int:
        if self.num_nodes != 2:
            raise ValueError("graph has more than 2 nodes")
        else:
            return self.num_edges
    
    def fuze_nodes(self, node1_idx: int, node2_idx: int) -> None:
        '''
        The convention will be that the second node
        gets fuzed.
        '''
        # 1. Deal with the chosen edge first
        node2_val: int = self.data[node1_idx].pop(node2_idx)
        node1_val: int = node1_idx + 1
        node1_val_opp_idx = self.data[node2_val - 1].index(node1_val)
        self.data[node2_val-1].pop(node1_val_opp_idx)

        # 2. Deal with all what is connected to node2
        node2_edges: List[int] = copy.deepcopy(self.data[node2_val-1])
        def _clean_edges(this_node1_val: int, this_node2_val: int) -> None:
            this_node2_val_idx = self.data[node2_val-1].index(this_node2_val)
            poped_this_node2_val = self.data[node2_val-1].pop(this_node2_val_idx)

            this_node1_val_idx = self.data[poped_this_node2_val - 1].index(this_node1_val)
            self.data[poped_this_node2_val - 1].pop(this_node1_val_idx)
            self.data[poped_this_node2_val - 1].append(node1_val)
            self.data[node1_idx].append(poped_this_node2_val)

        for item in node2_edges:
            _clean_edges(node2_val, item)

        def _clear_self_loops() -> None:
            for i, sub_list in enumerate(self.data):
                self.data[i] = [num for num in sub_list if ((i+1) != num)]

        _clear_self_loops()
    
    def print_adjacency_list(self) -> None:
        print(self.data)


def read_input(file: str) -> List[List[int]]:
    output_list: List[List[Union[str, int]]] = []
    with open(file, 'r') as f:
        for line in f:
            row_list: List[str] = []
            row_string: str = re.sub(r'[\t]',' ',line.rstrip())
            row_list.extend(row_string.split(' '))
            output_list.append([int(i) for i in row_list[1:]])
    return output_list

def get_cut(g: Graph) -> int:
    while g.num_nodes > 2:
        # edge is an index i,j for the list of lists
        chosen_edge = random.choice([(i, j)
                                     for i, sub_list in enumerate(g.data)
                                     for j, _ in enumerate(sub_list)])
        g.fuze_nodes(*chosen_edge)
    num_crossings: int = g.get_num_crossings()
    return num_crossings

def get_min_cut(g_path: str, num_iter: int) -> int:
    min_cut: float = float('inf')
    for _ in tqdm(range(num_iter), desc='searching for min_cuts'):
        g = Graph(read_input(g_path))
        cut = get_cut(g)
        if cut < min_cut:
            min_cut = cut
        del g
    return min_cut


get_min_cut('kargerMinCut.txt', num_iter=100)
