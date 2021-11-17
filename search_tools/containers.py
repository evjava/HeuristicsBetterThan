from node import Node
from queue import PriorityQueue

class Open:
    def __init__(self): 
        self.elements = {}
        self.queue = PriorityQueue()
        
    def push(self, node: Node): 
        self.elements[node.coord] = node
        self.queue.put((node.comp(), node))
        
    def __iter__(self):
        return iter(self.elements.values())

    def __len__(self):
        return len(self.elements)

    @property
    def is_empty(self):
        return len(self) == 0

    def find_by_coord(self, coord):
        return self.elements.get(coord)

    def find(self, node):
        return self.find_by_coord(node.coord)

    def pop_best(self):
        while not self.is_empty:
            node = self.queue.get()[1]
            if node.coord in self.elements:
                del self.elements[node.coord]
                node.time = Node.TIME
                Node.TIME += 1
                return node
        return None


class Closed:
    def __init__(self):
        self.elements = {}

    def __iter__(self):
        return iter(self.elements.values())

    def __len__(self):
        return len(self.elements)

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
    
