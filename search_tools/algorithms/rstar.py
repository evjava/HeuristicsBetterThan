from algorithms.search_algorithm import SearchAlgorithm
from node import Node
from containers.containers_coord_nodes import Open, Closed
from containers.containers_coord_times import DictContainer

from containers.containers_coord_times import Open as OpenTime
from containers.containers_coord_times import Closed as ClosedTime

from containers.containers3 import Open as Open1
from containers.containers3 import Closed as Closed1
from areas.area import Area
from areas.rstar_wrapper import RstarWrapperMap
from algorithms.astar import Astar
from collections import defaultdict
from containers.path import Path

INF = 1e12

def merge_containers(containers):
    es = {}
    # todo reuse containers[0]
    for c in containers:
        for e, t in c.elements.items():
            t_old = es.get(e, INF)
            if t < t_old:
                es[e] = t
    return DictContainer(es)

class Rstar(SearchAlgorithm):
    def __init__(self, heuristic, D, K, w):
        super().__init__(f'A*(h={heuristic.__name__})')
        self.h = heuristic
        self.D, self.K, self.w = D, K, w
        self.astar = Bounded_Astar(heuristic)

    def run(self, area: Area, start_coord, goal_coord):
        area = RstarWrapperMap(area)

        g, k, bp, avoid = {}, {}, {}, defaultdict(lambda: False)
        path = defaultdict(lambda: defaultdict(lambda: (None, INF)))

        start, goal = start_coord, goal_coord
        open, closed = Open1(), Closed1()

        open_time, closed_time = OpenTime(), ClosedTime()
        astar_time_open_containers, astar_time_closed_containers = [], []

        g[goal_coord] = INF
        bp[goal_coord] = bp[start_coord] = None

        k[goal_coord] = (1, INF)
        k[start_coord] = (0, self.w*self.h(*start_coord, *goal_coord))

        open.push(start, key=k[start_coord])
        g[start_coord] = 0

        open_time.push(start, 0)

        def update(s):
            if g[s] > self.w * self.h(*s, *start) or (
                    path[s][bp[s]][0] is None and avoid[s]):
                k[s] = (1, g[s] + self.w * self.h(*s, *start))
            else:
                k[s] = (0, g[s] + self.w * self.h(*s, *start))
            open.push(s, key=k[s])
            open_time.push(s, 0)

        def reevaluate(s):
            path[s][bp[s]] = self.astar.run(area, bp[s], s, open_time, closed_time, 200)

            if path[s][bp[s]][0] is None or (g[s] > self.w * self.h(*start, *s)):
                avoid[s] = True
                bp[s] = min(path[s].keys(), key=lambda bp_new: g[bp_new] + path[s][bp_new][1])

            g[s] = path[s][bp[s]][1] + g[bp[s]]

            update(s)

        while not open.is_empty:
            S_double = open.peek_best()
            if S_double[0][0] == 1:
                return [], merge_containers([open_time]), merge_containers([closed_time])
            s = open.pop_best()
            if s == goal:
                print(1)
            if k[goal] < k[s]:
                break

            if s != start and path[s][bp[s]][0] is None:
                reevaluate(s)
            else:
                closed.push(s)
                closed_time.push(s, open_time.time)
                succs = area.generate_random_neighbors(s, self.K, self.D)
                if area.compute_cost(s, goal) <= self.D:
                    succs.append(goal)
                succs = [coord for coord in succs if not closed.is_visited(coord)]
                for s_new in succs:

                    if open.find(s_new) is None:
                        g[s_new], bp[s_new] = INF, None
                        #path[s] = None

                    path[s][s_new] = None, self.h(*s, *s_new)
                    clow = path[s][s_new][1]

                    if bp[s_new] is None or g[s]+clow < g[s_new]:
                        g[s_new], bp[s_new] = g[s]+clow, s
                        update(s_new)

        global_path = []
        s = goal
        while bp[s] is not None:
            global_path.extend(path[bp[s]][s][0])
            s = bp[s]
        global_path = Path(global_path)

        return global_path, open_time, closed_time


class Bounded_Astar(SearchAlgorithm):
    def __init__(self, heuristic):
        super().__init__(f'A*(h={heuristic.__name__})')
        self.heuristic = heuristic

    def reconstruct_path(self, s):
        path = [s]
        s_ = s
        while s_.parent is not None:
            s_ = s_.parent
            path.append(s_)

        return path

    def run(self, area: Area, start_coord, goal_coord, open_time, closed_time, max_closed=200):
        start = Node(coord=start_coord)
        goal = Node(coord=goal_coord)

        calc_h = lambda c: self.heuristic(*c, *goal_coord)

        time_open, time_closed = defaultdict(lambda : INF), defaultdict(lambda : INF)
        op_nodes, cl_nodes = Open(), Closed()

        op_nodes.push(start)
        open_time.push(start.coord, 0)

        while not op_nodes.is_empty:
            if len(cl_nodes) > max_closed:
                break
            s = op_nodes.pop_best()
            if s == goal:
                path = self.reconstruct_path(s)
                lenght = s.g
                return path, lenght

            if s is None or not cl_nodes.push(s):
                continue
            closed_time.push(s.coord, open_time.time)

            for n_coord in area.get_neighbors(s.coord):
                if cl_nodes.is_visited(n_coord):
                    continue
                n_op = op_nodes.find_by_coord(n_coord)
                new_cost = s.g + area.compute_cost(s.coord, n_coord)
                if n_op is None or new_cost < n_op.g:
                    h = calc_h(n_coord)
                    n_node = Node(n_coord, g=new_cost, h=h, parent=s)
                    op_nodes.push(n_node)
                    open_time.push(n_coord, 0)
        return None, op_nodes.pop_best().F
