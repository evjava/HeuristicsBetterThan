from copy import deepcopy
from task import Task
import random

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

    def with_task(self, task: Task):
        reader_upd = deepcopy(self)
        reader_upd._selected_tasks = [task]
        return reader_upd

    def with_sampled_count_tasks(self, count: int):
        reader_upd = deepcopy(self)
        ts = self.read_tasks()
        reader_upd._selected_tasks = random.sample(ts, count)
        return reader_upd

    def with_idx_task(self, idx: int):
        reader_upd = deepcopy(self)
        reader_upd._selected_tasks = [self.read_tasks()[idx]]
        return reader_upd

    def __repr__(self):
        st = self._selected_tasks
        str_tasks = f': {st}' if st else ''
        return f'MapReader[{self.payload}{str_tasks}]'
