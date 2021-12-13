from areas.area import Area
from containers.base_container import Container
from containers.path import Path
from typing import Tuple

RunOutput = Tuple[Path, Container, Container]

class SearchAlgorithm(object):
    def __init__(self, name, map_wrapper=None):
        # todo replace with algorithm-descriptor
        # (dataclass: .name, .parameters, #__repr__)
        self.name = name
        self.map_wrapper = map_wrapper

    def run(self, area: Area, start_c, goal_c) -> RunOutput:
        ''' returns 3-elements tuple:
            - Path (or None if not found), 
            - Closed
            - Open
        '''
        raise AttributeError('Not implemented yet...')
