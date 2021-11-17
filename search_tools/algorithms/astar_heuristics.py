import math

def make_metric(proto_metric):
    def metric(i1, j1, i2, j2):
        dx, dy = abs(int(i1) - int(i2)), abs(int(j1) - int(j2))
        return proto_metric(dx, dy)
    metric.__name__ = proto_metric.__name__.split('_')[1]
    return metric

def _manhattan_dist(dx, dy): return dx + dy
def _diagonal_dist(dx, dy): return min(dx, dy)*math.sqrt(2) + abs(dx - dy)
def _chebyshev_dist(dx, dy): return max(dx, dy)
def _euclidean_dist(dx, dy): return math.sqrt(dx**2 + dy**2)

manhattan_dist = make_metric(_manhattan_dist)
diagonal_dist = make_metric(_diagonal_dist)
chebyshev_dist = make_metric(_chebyshev_dist)
euclidean_dist = make_metric(_euclidean_dist)

HEURISTICS = [manhattan_dist, diagonal_dist, euclidean_dist, chebyshev_dist]    
