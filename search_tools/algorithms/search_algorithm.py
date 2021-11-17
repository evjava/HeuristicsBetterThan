class SearchAlgorithm(object):
    def __init__(self, name):
        self.name = name

    def run(self, area, start_coord, goal_coord):
        ''' returns 3-elements tuple:
            - goal node (or None if not found), 
            - closed
            - open 
        '''
        raise AttributeError('Not Implemented yet...')
