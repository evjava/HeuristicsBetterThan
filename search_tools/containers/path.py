from typing import List, Tuple
from containers.base_container import Container
from node import Node

class Path(Container):
    def __init__(self, path: List[Tuple], cost: float):
        self.path = path
        self.cost = cost

    def coords(self):
        return iter(self.path)

    def __len__(self):
        return len(self.path)

    def time(self, e) -> int:
        return 0

    def __iter__(self):
        return iter(self.path)

def path_from_node(goal: Node) -> Path:
    if goal is None:
        return None
    else:
        node_path = _make_path(goal)
        c_path = [n.coord for n in node_path]
        return Path(c_path, goal.g)

def _make_path(goal) -> List[Node]:
    '''
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    '''
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1]    
    
