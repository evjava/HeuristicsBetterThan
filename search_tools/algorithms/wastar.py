from algorithms.search_algorithm import SearchAlgorithm
from node import Node
from containers import Open, Closed
from area import Area
from algorithms.astar import Astar

class WAstar(Astar):
    def __init__(self, heuristic, weight):
        SearchAlgorithm.__init__(self, f'WA*(h={heuristic.__name__},w={weight:.1f})')
        self.heuristic_0 = heuristic
        self.weight = weight
        self.heuristic = lambda *args: weight * self.heuristic_0(*args)
