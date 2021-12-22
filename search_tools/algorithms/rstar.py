from algorithms.search_algorithm import SearchAlgorithm
from node import Node
from containers.containers_coord_times import DictContainer
from containers.containers_coord_nodes import Open, Closed
from containers.containers_coord_times import Open as OpenTime
from containers.containers_coord_times import Closed as ClosedTime

from containers.containers_rstar import Open as OpenRstar
from containers.containers_rstar import Closed as ClosedRstar
from areas.area import Area
from areas.rstar_wrapper import RstarWrapperMap
from algorithms.astar import Astar
from collections import defaultdict
from containers.path import Path

INF = 1e12
EPS = 1e-5
def merge_containers(containers):
    es = {}
    # todo reuse containers[0]
    for c in containers:
        if isinstance(c, OpenRstar):
            for e, t in c.elements.values():
                t_old = es.get(e, INF)
                if t < t_old:
                    es[e] = t
        else:
            for e, t in c.elements.items():
                t_old = es.get(e, INF)
                if t < t_old:
                    es[e] = t
    return DictContainer(es)

class Rstar(SearchAlgorithm):
    def __init__(self, heuristic, D, K, w, exp_coeff=4):
        h_name = heuristic.__name__
        name = f'R*(h={h_name}, D={D}, K={K}, w={w}, exp_coeff={exp_coeff})'
        super().__init__(name)
        self.exp_coeff = exp_coeff
        self.h = heuristic
        self.D, self.K, self.w = D, K, w
        self.astar = Bounded_WAstar(heuristic, w)

    def run(self, area: Area, start_coord, goal_coord):
        area = RstarWrapperMap(area)

        g, k, bp, avoid = {}, {}, {}, defaultdict(lambda: False)
        path = defaultdict(lambda: defaultdict(lambda: (None, INF)))

        start, goal = start_coord, goal_coord
        open, closed = OpenRstar(), ClosedRstar()

        #open, closed_time = OpenTime(), ClosedTime()
        bwastar_open, bwastar_closed = [], []
        g[goal_coord] = INF
        bp[goal_coord] = bp[start_coord] = None

        k[goal_coord] = (1, INF)
        k[start_coord] = (0, self.w*self.h(*start_coord, *goal_coord))

        open.push(start, key=k[start_coord])
        g[start_coord] = 0


        def update(s):
            if ((g[s] > self.w * self.h(*s, *start)) or (path[s][bp[s]][0] is None and avoid[s])):
                k[s] = (1, g[s] + self.w * self.h(*s, *goal))
                avoid[s] = True
            else:
                k[s] = (0, g[s] + self.w * self.h(*s, *goal))
                avoid[s] = False

            open.push(s, key=k[s])

        def reevaluate(s):
            path[s][bp[s]], times = self.astar.run(area, bp[s], s, self.exp_coeff*self.D, start_time=open.time)

            bwastar_open.append(times[0])
            bwastar_closed.append(times[1])
            open.time = times[0].time

            if path[s][bp[s]][0] is None or (g[s] > self.w * self.h(*start, *s)):
                avoid[s] = True
                bp[s] = min(path[s].keys(), key=lambda bp_new: g[bp_new] + path[s][bp_new][1])

            g[s] = path[s][bp[s]][1] + g[bp[s]]

            update(s)

        while not open.is_empty:
            s = open.pop_best()
            #open_time.pop_best()
            if (k[goal][0] < k[s][0]) or (k[goal][0] == k[s][0] and k[goal][1]+EPS < k[s][1]):
                break
            if bp.get(goal) is not None:
                if path[goal][bp[goal]][0] is not None:
                    break
            if s != start and path[s][bp[s]][0] is None:
                reevaluate(s)
            else:
                if s == goal:
                    break
                closed.push(s, open.time)
                #closed_time.push(s, open_time.time)
                succs = area.generate_random_neighbors(s, self.K, self.D)
                if area.compute_cost(s, goal) <= self.D:
                    succs.append(goal)
                succs = [coord for coord in succs if not closed.is_visited(coord)]
                for s_new in succs:

                    if open.find(s_new) is None:
                        g[s_new], bp[s_new] = INF, None
                        #path[s] = None

                    path[s_new][s] = None, self.h(*s, *s_new)
                    clow = path[s_new][s][1]

                    if bp[s_new] is None or g[s]+clow < g[s_new]:
                        g[s_new], bp[s_new] = g[s]+clow, s
                        update(s_new)

        global_path = []
        s = goal
        while bp[s] is not None:
            c_path = [node.coord for node in path[s][bp[s]][0]]
            global_path.extend(c_path)
            s = bp[s]
        global_path = Path(global_path, g[goal])

        return global_path, merge_containers([open, *bwastar_open]), merge_containers([closed, *bwastar_closed])


class Bounded_WAstar(SearchAlgorithm):
    def __init__(self, heuristic, w):
        super().__init__(f'A*(h={heuristic.__name__})')
        self.heuristic = heuristic
        self.w = w
    def reconstruct_path(self, s):
        path = [s]
        s_ = s
        while s_.parent is not None:
            s_ = s_.parent
            path.append(s_)

        return path

    def run(self, area: Area, start_coord, goal_coord, max_closed, start_time):
        start = Node(coord=start_coord)
        goal = Node(coord=goal_coord)

        calc_h = lambda c: self.heuristic(*c, *goal_coord)

        open_time, closed_time = OpenTime(), ClosedTime()
        open_time.time = start_time

        op_nodes, cl_nodes = Open(), Closed()

        op_nodes.push(start)
        open_time.push(start.coord, start.F)

        while not op_nodes.is_empty:
            if len(cl_nodes) > max_closed:
                break
            s = op_nodes.pop_best()
            open_time.pop_best()
            if s == goal:
                path = self.reconstruct_path(s)
                lenght = s.g
                return (path, lenght), (open_time, closed_time)

            if s is None or not cl_nodes.push(s):
                continue
            closed_time.push(s.coord, open_time.time)

            for n_coord in area.get_neighbors(s.coord):
                if cl_nodes.is_visited(n_coord):
                    continue
                n_op = op_nodes.find_by_coord(n_coord)
                new_cost = s.g + area.compute_cost(s.coord, n_coord)
                if n_op is None or new_cost < n_op.g:
                    h = self.w * calc_h(n_coord)
                    n_node = Node(n_coord, g=new_cost, h=h, parent=s)
                    op_nodes.push(n_node)
                    open_time.push(n_coord, n_node.F)
        return (None, op_nodes.pop_best().F), (open_time, closed_time)