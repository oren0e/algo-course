from typing import List, Union

import re

import random

from tqdm import tqdm

class Graph:
    def __init__(self, data: List[List[int]]) -> None:
        self.data = data
        
    def __repr__(self) -> str:
        return f'{self.__class__} with {self.get_num_nodes()} nodes ' \
               f'and {self.get_num_edges()} edges'

    def get_num_nodes(self) -> int:
        return len(self.data)

    def get_num_edges(self) -> int:
        return sum(len(sub_list) for sub_list in self.data) // 2

    def get_num_crossings(self) -> int:
        pass
    
    def fuze_nodes(self, node1_idx: int, node2_idx: int) -> None:
        '''
        The convention will be that the second node
        gets fuzed.
        '''
        # TODO:
        #       1. remove node2 from the relevant place
        #       2. remove the opposite
        #       3. remove other connceted nodes to the fuzed one
        #       4. eventually when the sublist is empty - remove it.
        pass
    
    def print_adjacency_list(self) -> None:
        pass


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
    while g.get_num_nodes() > 2:
        # edge is an index i,j for the list of lists
        chosen_edge = random.choice([(i, j)
                                     for i, sub_list in enumerate(g.data)
                                     for j, _ in enumerate(sub_list)])
        g.fuze_nodes(chosen_edge)
    num_crossings: int = g.get_num_crossings()
    return num_crossings

def get_min_cut(g_path: str, num_iter: int) -> int:
    min_cut: float = float('inf')
    for _ in tqdm(range(num_iter), desc='searching for min_cuts'):
        g = read_input(g_path)
        cut = get_cut(g)
        if cut < min_cut:
            min_cut = cut
        del g
    return min_cut


input_data: List[List[int]] = read_input('ex4_test_case0.txt')
g = Graph(input_data)
g