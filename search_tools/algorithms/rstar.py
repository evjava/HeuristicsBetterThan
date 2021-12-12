from algorithms.search_algorithm import SearchAlgorithm
from node import Node
from containers3 import Open, Closed
from containers import Open as Open1
from containers import Closed as Closed1
from area import Area
from algorithms.astar import Astar

INF = 1e12


class Rstar(SearchAlgorithm):
    def __init__(self, heuristic, D, K, w):
        super().__init__(f'A*(h={heuristic.__name__})')
        self.h = heuristic
        self.D, self.K, self.w = D, K, w
        self.astar = Bounded_Astar(h=heuristic.__name__)

    def run(self, area: Area, start_coord, goal_coord):
        path, g, k, bp, avoid = {}, {}, {}, {}, {}

        start, goal = start_coord, goal_coord
        open, closed = Open(), Closed()

        open.push(start)

        def update(s):
            if g[s] > self.w * self.heuristic(s, start) or (
                    path[s][bp[s]][0] is None and avoid[s]):
                k[s] = (1, g[s] + self.w * self.h(s, start))
            else:
                k[s] = (0, g[s] + self.w * self.h(s, start))
            open.push(s, key=k[s])

        def reevaluate(s):
            path[s][bp[s]] = self.astar(area, bp[s], s, 150)

            if path[s][bp[s]] is None or (g[s] > self.w * self.h(start, s)):
                avoid[s] = True
                bp[s] = min(path[s].keys(), key=lambda bp_new: g[bp_new] + path[s][bp_new][1])

            g[s] = path[s][bp[s]][1] + g[bp[s]]

            update(s)

        while not open.is_empty:
            s = open.pop_best()
            if k[goal] < k[s]:
                break

            if s != start and path[s][bp[s]] is None:
                reevaluate(s)
            else:
                closed.push(s)
                succs = area.random_neighbors(s, self.K, self.D)
                if area.dist(s, goal) <= self.D:
                    succs.append(goal)
                succs = [coord for coord in succs if not closed.is_visited(coord)]
                for s_new in succs:

                    if open.find(s_new) is None:
                        g[s_new], bp[s_new] = INF, None
                        path[s] = None

                    path[s][s_new] = None, self.h(s, s_new)
                    clow = path[s][s_new][1]

                    if bp[s_new] is None or g[s]+clow < s_new.g:
                        g[s_new], bp[s_new] = g[s]+clow, s
                        update(s_new)

        return goal, open, closed


class Bounded_Astar(SearchAlgorithm):
    def __init__(self, heuristic):
        super().__init__(f'A*(h={heuristic.__name__})')
        self.heuristic = heuristic
    def reconstruct_path(self, s):
        path = [s]
        s_ = s
        while s_.bp is not None:
            s_ = s_.bp
            path.append(s_)

        return path

    def run(self, area: Area, start_coord, goal_coord, max_closed=1e18):
        start = Node(coord=start_coord)
        goal = Node(coord=goal_coord)

        calc_h = lambda c: self.heuristic(*c, *goal_coord)

        op_nodes = Open1()
        op_nodes.push(start)
        cl_nodes = Closed1()

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

            for n_coord in area.get_neighbors(s.coord):
                if cl_nodes.is_visited(n_coord):
                    continue
                n_op = op_nodes.find_by_coord(n_coord)
                new_cost = s.g + area.compute_cost(s.coord, n_coord)
                if n_op is None or new_cost < n_op.g:
                    h = calc_h(n_coord)
                    n_node = Node(n_coord, g=new_cost, h=h, parent=s)
                    op_nodes.push(n_node)

        return None, op_nodes.pop_best().f
