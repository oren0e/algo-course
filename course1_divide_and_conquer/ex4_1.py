from typing import List, Union

import re

class Graph:
    def __init__(self, data: List[List[int]]) -> None:
        self.data = data
        
    def __repr__(self) -> str:
        return f'{self.__class__} with {len(self.data)} nodes ' \
               f'and {sum(len(sub_list) for sub_list in self.data) // 2} edges'
    
    def get_num_crossings(self):
        pass
    
    def fuze_nodes(self, node1: int, node2: int) -> None:
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

input_data: List[List[int]] = read_input('ex4_test_case0.txt')
g = Graph(input_data)
g