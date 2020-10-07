'''
We will have to do the following:
1. Find the highest label number (optional)
2. Represent Node as a NamedTuple with seen, value, and finish_time
3. Represent a Graph (with adjacency list)
4. Write the dfs() function
5. Write the dfs_loop() function
6. Write the find_scc() mother-function
'''

from typing import List, Optional, Dict, Tuple

from collections import Counter


class Node:
    def __init__(self, value: int,
                 seen: bool = False) -> None:
        self.value = value
        self.finish_time: Optional[int] = None
        self.seen = seen
        self.leader: Optional[Node] = None
        self.to_nodes: List[Node] = []

    def __repr__(self) -> str:
        return repr([node.value for node in self.to_nodes])


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


def read_input_to_graph(file: str, reversed: bool = False) -> Graph:
    output_list: Graph = [None for _ in range(find_max_node_value(file))]
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
                output_list[dest - 1].to_nodes.append(nodes[origin])
            else:
                if output_list[origin - 1] is None:
                    output_list[origin - 1] = nodes[origin]
                output_list[origin - 1].to_nodes.append(nodes[dest])
    return output_list

temp = read_input_to_graph('./ex1_test_cases/test1')
temp_rev = read_input_to_graph('./ex1_test_cases/test1', reversed=True)


def switch_to_finish_times(g: Graph) -> Graph:
    for node in g:
        node.value = node.finish_time
    return g

def dfs_loop(g: Graph, finish_time_values: bool = False) -> None:
    global t
    global s
    t = 0
    s = None
    n = len(g)
    for i in range(n-1, -1, -1):
        if not g[i].seen:
            s = i
            dfs(g, g[i])

def dfs(g: Graph, i: Node) -> None:
    '''
    Depth-first-search
    '''
    i.seen = True
    i.leader = g[s]
    for to_node in i.to_nodes:
        if not to_node.seen:
            dfs(g, to_node)
    t += 1
    i.finish_time = t

def get_scc_sizes(g: Graph) -> List[Tuple[int, int]]:
    '''
    Returns the 5 largest SCCs (by number of nodes with the same leader)
    '''
    leaders: [node.leader.value for node in g]
    return Counter(leaders).most_common(5)

# trying