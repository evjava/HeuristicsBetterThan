from queue import PriorityQueue
from containers.base_container import Container

class Open:
    def __init__(self):
        self.time = 0
        self.elements = {}
        self.queue = PriorityQueue()
        
    def push(self, e, priority): 
        self.elements[e] = self.time
        self.time += 1
        self.queue.put((priority, e))
        
    def pop_best(self):
        ''' returns (element, time) '''
        while not self.is_empty:
            e = self.queue.get()[1]
            t = self.elements.pop(e, None)
            if t is not None:
                return e, t

    @property
    def coords(self):          return self.__iter__()
    def time(self, e):         return self.elements[e]
    def __iter__(self):        return iter(self.elements)
    def __len__(self):         return len(self.elements)
    def __contains__(self, e): return e in self.elements
    @property
    def is_empty(self):        return len(self) == 0
    @property
    def is_not_empty(self):    return not(self.is_empty)

    def _peek(self):     return None if self.is_empty else self.queue.queue[0]
    def peek_best(self): return _get_or_none(self._peek(), 1)
    @property
    def min_key(self):   return _get_or_none(self._peek(), 0)

class Closed:
    def __init__(self):
        self.elements = {}

    @property
    def coords(self):          return self.__iter__()
    def time(self, e):         return self.elements[e]
    def __iter__(self):        return iter(self.elements)
    def __len__(self):         return len(self.elements)
    @property
    def is_empty(self):        return len(self) == 0
    def __contains__(self, e): return e in self.elements

    def push(self, e, time): 
        if e in self:
            return False
        else:
            self.elements[e] = time
            return True
    

def _get_or_none(elem, idx):
    return elem[idx] if elem else None

class DictContainer(Container):
    def __init__(self, elements, total_len=None):
        self.elements = elements
        self.total_len = total_len or len(self.elements)
        
    def time(self, e): return self.elements[e]
    def coords(self):  return iter(self.elements)
    def __len__(self): return self.total_len
