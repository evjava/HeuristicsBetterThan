import pathlib

from moving_ai.mai_map import MapMAI
from reader import Reader
from task import Task

def mai_task_from_line(line):
    b, m, mw, mh, sx, sy, gx, gy, d = line.split('\t')
    return Task((int(sx), int(sy)), (int(gx), int(gy)), float(d))

def read_tasks_from_movingai_file(path):
    all_lines_0 = (i.strip() for i in open(path, 'r').read().split('\n'))
    all_lines = [j for j in all_lines_0 if j != '']
    v, *lines = all_lines
    assert v == 'version 1'
    return list(map(mai_task_from_line, lines))

MAP_TASKS_CACHE = {}

def _build_mai_path():
    project_root = pathlib.Path(__file__).parent.parent.parent
    mai_path = project_root / 'resources' / 'moving_ai_maps'
    return mai_path.resolve()

MAI_PATH = _build_mai_path()

class MaiReader(Reader):
    def _map_path(self):
        name = self.payload
        return f'{MAI_PATH}/{name}.map'
    
    def read_map(self):
        map_path = self._map_path()
        map_ = MAP_TASKS_CACHE.get(map_path)
        if map_ is None:
            map_ = MapMAI.read_map_from_file(map_path)
            MAP_TASKS_CACHE[map_path] = map_
        return map_

    def read_tasks(self):
        if self._selected_tasks is not None:
            return self._selected_tasks
        tasks_path = self._map_path() + '.scen'
        ts = read_tasks_from_movingai_file(tasks_path)
        return ts

class MaiMaps:
    ARENA = 'arena'
    STARCRAFT = 'starcraft1_Aurora'
    MOSCOW = 'street_Moscow_2_512'
