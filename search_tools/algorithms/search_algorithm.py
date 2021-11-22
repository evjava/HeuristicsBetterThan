from area import Area

class SearchAlgorithm(object):
    def __init__(self, name):
        # todo replace with algorithm-descriptor(dataclass: .name, .parameters, #__repr__)
        self.name = name

    def run(self, area: Area, start_coord, goal_coord):
        ''' returns 3-elements tuple:
            - goal node (or None if not found), 
            - closed
            - open 
        '''
        raise AttributeError('Not implemented yet...')
