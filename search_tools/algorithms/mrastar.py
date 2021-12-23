from algorithms.search_algorithm import SearchAlgorithm
from loguru import logger as log
from containers.containers_coord_times import Open, Closed, DictContainer
from containers.path import Path
from areas.area import Area
from areas.mrastar_wrapper import IRAstarWrapperMap

from loguru import logger as log
log.remove()
log.add('runs.log', format='{time}  {level} {name} {message}', level='INFO')

INF = 2e9

class MRAstar(SearchAlgorithm):
    def __init__(self, heuristic, resolutions, w_1, w_2):
        h_name = heuristic.__name__
        name = f'MRA*(h={h_name}, rs={resolutions}, w_1={w_1}, w_2={w_2})'
        super().__init__(name)
        self.heuristic = heuristic
        self.resolutions, self.w_1, self.w_2 = resolutions, w_1, w_2
        
    def run(self, area: Area, start_c, goal_c):
        area = IRAstarWrapperMap(area)
        # furniture
        g, bp, space_indices = {}, {}, SpaceIndices(self.resolutions) 
        h = lambda c: self.heuristic(*c, *goal_c)
        def key(s, i): return g[s] + (1 if i == 0 else self.w_1) * h(s)
        time = [0]

        # init start/goal
        g[start_c], g[goal_c] = 0, INF
        bp[start_c] = bp[goal_c] = None

        # init containers
        OPEN   = [Open()   for _ in space_indices]
        CLOSED = [Closed() for _ in space_indices]
        for i in space_indices(start_c):
            OPEN[i].push(start_c, key(start_c, i))
        q_s = QueueSelector(OPEN[1:])

        def expand_q_state(i):
            s, t = OPEN[i].pop_best()
            time[0] += 1
            CLOSED[i].push(s, time[0])
            # log.info('expanding: s={}, i={}', s, i)
            for sn in area.get_hop_neighbours(s, space_indices.hops[i]):
                if sn not in g: 
                    g[sn], bp[sn] = INF, None
                cost = area.compute_cost(s, sn)
                # log.info('cost: {}', cost)
                g_upd = g[s] + cost
                if g[sn] > g_upd:
                    g[sn], bp[sn] = g_upd, s
                    for i in (i for i in space_indices(sn) if sn not in CLOSED[i]):
                        OPEN[i].push(sn, key(sn, i))
        
        while True:
            i = q_s.select_q() + 1
            if i is None: break

            mk_i, mk_0 = OPEN[i].min_key or INF, OPEN[0].min_key or INF
            # log.info('chosen q={}, mk[i]={:.3f}, w_2*mk[0]={:.3f}', i, mk_i, self.w_2 * mk_0)
            # log.info('q sizes: {}', [len(i) for i in OPEN])
            if mk_i <= self.w_2 * mk_0:
                if g[goal_c] <= mk_i: break
                expand_q_state(i)
            else:
                if g[goal_c] <= self.w_2 * mk_0: break
                expand_q_state(0)
        
        # log.success('done! {:.3f}', g[goal_c])
        path = make_path(area, bp, g, goal_c)
        return path, merge_containers(OPEN), merge_containers(CLOSED)


def make_path(area, bp, g, node):
    if g[node] == INF: return None

    path = []
    cur = node
    while bp[cur] is not None:
        path.append(cur)
        cur = bp[cur]
    # todo refine path merge hops
    return Path(path[::-1], g[node])

def merge_containers(containers):
    es = {}
    # todo reuse containers[0]
    for c in containers:
        for e, t in c.elements.items():
            t_old = es.get(e, INF)
            if t < t_old:
                es[e] = t
    return DictContainer(es, sum(map(len, containers)))

class QueueSelector(object):
    def __init__(self, qs):
        self.qs = qs
        self.qi = -1
        
    def next_qi(self):
        self.qi = (self.qi + 1) % len(self.qs)
        return self.qi
        
    def select_q(self):
        qi = self.next_qi()
        start_qi = qi
        while True:
            if self.qs[qi].is_not_empty:
                return qi
            qi = self.next_qi()
            if qi == start_qi:
                return None

class SpaceGrid(object):
    def __init__(self, step):
        assert step % 2 == 1
        self.step = step
        self.mid = self.step // 2
        
    def __contains__(self, coord):
        assert len(coord) == 2
        res = all(c % self.step == self.mid for c in coord)
        return res
    
class SpaceIndices(object):
    def __init__(self, resolutions):
        # todo check consistency of resolutions?
        self.hops = (1,) + resolutions
        self.grids = [SpaceGrid(s) for s in self.hops]
        
    def __iter__(self):
        return iter(range(len(self.grids)))
    
    def __call__(self, c):
        return [i for i, g in enumerate(self.grids) if c in g]
