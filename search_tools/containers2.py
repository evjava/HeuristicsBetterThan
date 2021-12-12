from queue import PriorityQueue

class Open2:
    def __init__(self): 
        self.elements = set()
        self.queue = PriorityQueue()
        
    def push(self, e, priority): 
        self.elements.add(e)
        self.queue.put((priority, e))
        
    def pop_best(self):
        while not self.is_empty:
            e = self.queue.get()[1]
            if e in self:
                self.elements.remove(e)
                return e

    def __iter__(self):        return iter(self.elements)
    def __len__(self):         return len(self.elements)
    def __contains__(self, e): return e in self.elements
    @property
    def is_empty(self):        return len(self) == 0
    @property
    def is_not_empty(self):    return not(self.is_empty)

    def _peek(self):     return None if self.is_empty else self.queue.queue[0]
    def peek_best(self): return _get_or_none(self._peek(), 1)
    def min_key(self):   return _get_or_none(self._peek(), 0)

class Closed2:
    def __init__(self):
        self.elements = set()

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    @property
    def is_empty(self):
        return len(self) == 0

    def __contains__(self, e):
        return e in self.elements

    # todo remove
    def is_visited(self, coord):
        return coord in self
    
    def push(self, e): 
        if e in self:
            return False
        else:
            self.elements.add(e)
            return True
    

def _get_or_none(elem, idx):
    return elem[idx] if elem else None
