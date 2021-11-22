from typing import Tuple
from dataclasses import dataclass
from moving_ai.mai_map import MapMAI

@dataclass
class Zoom:
    a:      Tuple[int, int]
    b:      Tuple[int, int]
    w:      int
    h:      int
    rotate: bool
        
    @staticmethod
    def no_zoom(m: MapMAI):
        return Zoom((0, 0), (m.width, m.height), m.width, m.width, False)
    
    @property
    def rotator(self): return -1 if self.rotate else 1
    
    def _size(self, scale): return (scale * self.w, scale * self.h)
    def size(self, scale): return self._size(scale)[::self.rotator]    
    
    def convert(self, c):
        x, y = c
        if self.a[0] <= x <= self.b[0] and self.a[1] <= y <= self.b[1]:
            new_c = (x - self.a[0], y - self.a[1])
            return new_c[::self.rotator]
        return None
        
    @staticmethod
    def calc_zoom(m, results):
        def flat_and_take(pos):
            for r in results: yield from map(lambda x:x[pos], r.iter_coords())

        a = min(flat_and_take(0)), min(flat_and_take(1))
        b = max(flat_and_take(0)), max(flat_and_take(1))
        c, d = m.size, 2
        aa = (max(0, a[0] - d), max(0, a[1] - d))
        bb = (min(c[0], b[0] + d), min(c[1], b[1] + d))
        w, h = bb[0] - aa[0], bb[1] - aa[1]
        return Zoom(aa, bb, w, h, h > w)
