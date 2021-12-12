from node import Node
from queue import PriorityQueue


class Open:
    def __init__(self):
        self.elements = {}
        self.queue = PriorityQueue()

    def push(self, coord, key):
        self.elements[coord] = coord
        self.queue.put((key, coord))

    def __iter__(self):
        return iter(self.elements.values())

    def __len__(self):
        return len(self.elements)

    @property
    def is_empty(self):
        return len(self) == 0

    @property
    def is_not_empty(self):
        return not (self.is_empty)

    def find(self, coord):
        return self.elements.get(coord)

    def peek_best(self):
        return self.queue.queue[0][1]

    def pop_best(self):
        while not self.is_empty:
            coord = self.queue.get()[1]
            if coord in self.elements:
                del self.elements[coord]
                # todo eliminate, move to some context? Maybe area?
                #node.time = Node.TIME
                #Node.TIME += 1
                return coord
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

    def find(self, coord):
        return self.elements.get(coord)

    def is_visited(self, coord):
        return coord in self.elements

    def push(self, coord):
        if self.is_visited(coord):
            return False
        else:
            self.elements[coord] = coord
            return True

