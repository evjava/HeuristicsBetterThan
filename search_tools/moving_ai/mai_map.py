import math
import itertools as it
import matplotlib.pyplot as plt
import numpy as np

_cst = lambda i1, j1, i2, j2: abs(i1 - i2) + abs(j1 - j2)

DELTAS = {(i, j) for i, j in it.product((-1, 0, 1), (-1, 0, 1)) if i != 0 or j != 0}
STRIGHT_DELTAS = {d for d in DELTAS if abs(d[0]) + abs(d[1]) == 1}
DIAG_DELTAS = { d:{s for s in STRIGHT_DELTAS if _cst(*s, *d) == 1} for d in (DELTAS - STRIGHT_DELTAS) }

# . - passable terrain
# G - passable terrain
# @ - out of bounds
# O - out of bounds
# T - trees (unpassable)
# S - swamp (passable from regular terrain)
# W - water (traversable, but not passable from terrain)

# dict where values is a passable loc-types from key
TRAVERSABLE = {
    '.': '.GS',
    'G': '.GS',
    'S': '.GW',
    'W': 'S'
}

def parse_dim(key, line):
    prefix = key + ' '
    assert line.startswith(prefix)
    return int(line[len(prefix):])

def with_move(a, d): return a[0] + d[0], a[1] + d[1]
def with_d(a):       return lambda d: with_move(a, d)

def check(x, callback):
    assert callback, f'bad value: {x}'
    return x

class MapMAI:
    def __init__(self, width, height, cells):
        self._width = check(width, lambda: all(len(l) == width for l in cells))
        self._height = check(height, lambda: len(cells) == height)
        self._cells = cells
        
    @staticmethod            
    def read_map_from_file(file_name:str):
        data = open(file_name, 'r').read().strip()
        return MapMAI.read_map_from_str(data)
        
    @staticmethod
    def read_map_from_str(data:str):
        all_lines = [i.strip() for i in data.split('\n')]
        tp, h, w, m, *lines = all_lines
        assert tp == 'type octile' and m == 'map'
        height, width = parse_dim('height', h), parse_dim('width', w)
        return MapMAI(width, height, lines)
    
    def pos(self, c):         return self._cells[c[1]][c[0]]
    def loc_type(self, c):    return self._cells[c[1]][c[0]]
    def in_bounds(self, b):   return 0 <= b[0] < self._width and 0 <= b[1] < self._height
    def traversable(self, b): return self.loc_type(b) in TRAVERSABLE
    def passable(self, a, b): return self.loc_type(b) in TRAVERSABLE.get(self.loc_type(a), '')
    def is_ok(s, a, b):       return s.in_bounds(b) and s.traversable(b) and s.passable(a, b)
    def can_move(s, a, d):    return s.is_ok(a, with_move(a, d))
    
    def _get_neighbors(self, a):
        '''
        Get a list of neighbouring cells as (i,j) tuples.
        It's assumed that grid is 8-connected but cutting corners is prohibited
        '''
        straight = {d for d in STRIGHT_DELTAS if self.can_move(a, d)}
        yield from map(with_d(a), straight)
        
        diag_0 = {d for d in DIAG_DELTAS if self.can_move(a, d)}
        diag = {d for d in diag_0 if DIAG_DELTAS[d] <= straight}
        yield from map(with_d(a), diag)
        
    def get_neighbors(self, c): return list(self._get_neighbors(c))
        
    @property
    def size(self): return (self._width, self._height)
    @property
    def width(self): return self._width
    @property
    def height(self): return self._height
    
    def iter_coords_types(self):
        for i in range(self._width):
            for j in range(self._height):
                c = (i, j)
                yield (c, self.pos(c))

    def compute_cost(self, c1, c2):
        i1, j1 = c1
        i2, j2 = c2
        if abs(i1 - i2) + abs(j1 - j2) == 1: #cardinal move
            return 1
        elif abs(i1 - i2) + abs(j1 - j2) == 2: #diagonal move
            return math.sqrt(2)
        else:
            # todo maybe return +inf instead?
            msg = 'Trying to compute the cost of a non-supported move!' \
                  f'ONLY cardinal and diagonal moves are supported. (i1={i1}, j1={j1}, i2={i2}, j2={j2})'
            raise Exception(msg)

    def draw(self, name):
        trav_cells = np.zeros((self._width, self._height))
        for i in range(self._width):
            for j in range(self._height):
                trav_cells[i][j] = self.traversable((i,j))
        plt.imshow(trav_cells)
        plt.title(name)