import math

from areas.area import Area
from moving_ai.mai_map import DELTAS, STRIGHT_DELTAS, DIAG_DELTAS, with_move, MapMAI

from random import uniform

class RstarWrapperMap(Area):
    def __init__(self, area: Area):
        assert isinstance(area, MapMAI)
        self.area = area
        
    def get_neighbors(self, c): return self.area.get_neighbors(c)
    
    def compute_cost(self, c1, c2):
        # todo assert possible move
        i1, j1 = c1
        i2, j2 = c2
        return math.sqrt((i1 - i2)**2 + (j1 - j2)**2)

    def generate_random_neighbors(self, s, K, D):
        neighbors = []
        while len(neighbors) < K:
            alpha = uniform(0, 2 * math.pi)
            x, y = int(D * math.sin(alpha)), int(D * math.cos(alpha))
            if self.area.in_bounds((x+s[0], y+s[1])) and self.area.traversable((x+s[0], y+s[1])):
                neighbors.append((x+s[0], y+s[1]))
        return neighbors
