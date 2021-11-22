from copy import deepcopy
from task import Task

class Reader(object):
    def __init__(self, payload: str):
        self.payload = payload
        self._selected_tasks = None

    def read_map(self):
        ''' reads map '''
        raise AttributeError('Not implemented yet...')

    def read_tasks(self):
        ''' reads tasks '''
        raise AttributeError('Not implemented yet...')

    def read_map_tasks(self):
        return self.read_map(), self.read_tasks()

    def with_task(self, t: Task):
        reader_upd = deepcopy(self)
        reader_upd._selected_tasks = [t]
        return reader_upd
