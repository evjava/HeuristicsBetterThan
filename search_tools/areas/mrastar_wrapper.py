import math

from areas.area import Area
from moving_ai.mai_map import DELTAS, STRIGHT_DELTAS, DIAG_DELTAS, with_move, MapMAI

class IRAstarWrapperMap(Area):
    def __init__(self, area: Area):
        assert isinstance(area, MapMAI)
        self.area = area
        
    def get_neighbors(self, c): return self.area.get_neighbors(c)
    
    def compute_cost(self, c1, c2):
        # todo assert possible move
        i1, j1 = c1
        i2, j2 = c2
        return math.sqrt((i1 - i2)**2 + (j1 - j2)**2)
    
    def try_move(self, c, d, h):
        if h == 0:
            return c
        elif self.area.can_move(c, d):
            return self.try_move(with_move(c, d), d, h-1)
        else:
            return None
            
    def get_hop_neighbours(self, c, hop):
        assert hop >= 1
        if hop == 1:
            return self.get_neighbors(c)
        else:
            hop_ns = (self.try_move(c, d, hop) for d in DELTAS)
            return [n for n in hop_ns if n is not None]
