from node import Node
from queue import PriorityQueue
from containers.base_container import Container

class Open(Container):
    ''' keys: coordinates, values: nodes '''
    def __init__(self): 
        self.elements: Dict[Tuple, Node] = {}
        self.queue = PriorityQueue()
        
    def push(self, node: Node, priority=None): 
        self.elements[node.coord] = node
        key = priority if priority is not None else node.comp()
        self.queue.put((key, node))
        
    def __iter__(self): return iter(self.elements.values())
    def __len__(self):  return len(self.elements)
    def coords(self):   return iter(self.elements)
    def time(self, e):  return self.elements[e].time

    @property
    def is_empty(self):
        return len(self) == 0

    @property
    def is_not_empty(self):
        return not(self.is_empty)

    def find_by_coord(self, coord):
        return self.elements.get(coord)

    def find(self, node):
        return self.find_by_coord(node.coord)

    def peek_best(self):
        return self.queue.queue[0][1]

    def pop_best(self):
        while not self.is_empty:
            node = self.queue.get()[1]
            if node.coord in self.elements:
                del self.elements[node.coord]
                # todo eliminate, move to some context? Maybe area?
                node.time = Node.TIME
                Node.TIME += 1
                return node
        return None

class Closed(Container):
    ''' keys: coordinates, values: nodes '''
    def __init__(self):
        self.elements: Dict[Tuple, Node] = {}

    def __iter__(self): return iter(self.elements.values())
    def __len__(self):  return len(self.elements)
    def coords(self):   return iter(self.elements)
    def time(self, e):  return self.elements[e].time

    @property
    def is_empty(self):
        return len(self) == 0

    def find(self, node):
        return self.elements.get(node.coord)

    def is_visited(self, coord):
        return coord in self.elements
    
    def push(self, node): 
        if self.is_visited(node.coord):
            return False
        else:
            self.elements[node.coord] = node
            return True
    
