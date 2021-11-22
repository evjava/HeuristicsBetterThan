from typing import Tuple, List

class Area(object):
    def get_neighbors(self, c: Tuple) -> List[Tuple]:
        ''' :return coordinates of neighbors of `c` '''
        raise AttributeError('Not implemented yet...')

    def compute_cost(self, c1: Tuple, c2: Tuple) -> float:
        ''' Computes cost of a move between the adjacent cells '''
        raise AttributeError('Not implemented yet...')
