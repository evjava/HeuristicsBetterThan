from node import Node
from queue import PriorityQueue
from sortedcontainers import SortedSet

class Open:
    def __init__(self):
        self.elements = SortedSet()
        self.seen_elements = {}

    def push(self, coord, key):
        if coord in self.seen_elements:
            old_key = self.seen_elements[coord]
            if (old_key, coord) in self.elements:
                self.elements.remove((old_key, coord))
        self.elements.add((key, coord))
        self.seen_elements[coord] = key

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
        if self.seen_elements.get(coord, False):
            if (self.seen_elements[coord], coord) in self.elements:
                return self.seen_elements[coord], coord
        return None

    def peek_best(self):
        return self.elements[0]

    def pop_best(self):
        while not self.is_empty:
            coord = self.elements.pop(0)[1]
            return coord
            #if coord in self.elements:
            #    del self.elements[coord]
                # todo eliminate, move to some context? Maybe area?
                #node.time = Node.TIME
                #Node.TIME += 1

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

