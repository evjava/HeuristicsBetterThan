class Node:
    '''
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node
    - F: f-value of the node
    - parent: pointer to the parent-node 

    You might want to add other fields/methods for Node
    '''
    
    TIME = 0

    def __init__(self, coord, g = 0, h = 0, F = None, parent = None, k = 0):
        self.coord = coord
        self.g = g
        self.h = h
        self.F = F if F else self.g + h
        self.parent = parent
        self.time = 0
    
    def __eq__(self, other):
        return other is not None and self.coord == other.coord

    def __repr__(self):
        return 'Node(c={}, g={:.3f})'.format(self.coord, self.g)

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        return self.comp() < other.comp()
    
    def comp(s): return (s.F, s.h)
