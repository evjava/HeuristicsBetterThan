from algorithms.search_algorithm import SearchAlgorithm
from node import Node
from containers import Open, Closed
from area import Area
from algorithms.astar import Astar

INF = 1e12


class Rstar(SearchAlgorithm):
    def __init__(self, heuristic, D, K, w):
        super().__init__(f'A*(h={heuristic.__name__})')
        self.heuristic = heuristic
        self.D = D
        self.K = K
        self.w
        self.possible_bp = {}


    def run(self, area: Area, start_coord, goal_coord):

        start = Node(coord=start_coord)
        goal = Node(coord=goal_coord)

        calc_h = lambda c: self.heuristic(*c, *goal_coord)

        op_nodes = Open()
        op_nodes.push(start)
        cl_nodes = Closed()

        astar = Bounded_Astar(h=self.heuristic.__name__)

        def update(s):
            if s.g > self.w * self.heuristic(s.coord, self.start) or (s.path_to_bp is None and s.avoid):
                op_nodes.push(s, priority=(1, s.g+self.w*self.h(s.coord, start.coord)))
            else:
                op_nodes.push(s, priority=(0, s.g + self.w * self.h(s.coord, start.coord)))

        def reevaluate(s):
            s.path_to_bp, clow = astar(area, s.bp, s, 150)
            s.g = clow + s.bp.g

            if s.path_to_bp is None or (s.g > self.w*self.heuristic(start.coord, s.coord)):
                s.avoid = True
                for s_new, clow_new in self.possible_bp[s]:
                    if s_new.g + clow_new < s.g:
                        s.g = s_new.g + clow_new
                        s.bp = s_new

            update(s)

        while not op_nodes.is_empty:
            s = op_nodes.pop_best()
            if op_nodes.priorities[goal] < op_nodes.priorities[s]:
                break
            if s != start and s.path_to_bp is None:
                reevaluate(s)
            else:
                cl_nodes.push(s)
                succs = area.random_neighbors(s.coord, self.K, self.D)
                if area.dist(s.coord, goal.coord) < self.D:
                    succs.append(goal.coord)
                succs = [coord for coord in succs if not cl_nodes.is_visited(coord)]
                for s_new_coord in succs:
                    path, clow = None, self.heuristic(s.coord, s_new_coord)

                    if op_nodes.find_by_coord(s_new_coord) is None:
                        s_new = Node(s_new_coord)
                        s_new.g = INF
                        s_new.bp = None
                    else:
                        s_new = op_nodes.find_by_coord(s_new_coord)
                    if s_new.bp is None or s.g+clow < s_new.g:
                        s_new.g = s.g+clow
                        s_new.bp = s
                        update(s_new)

        return op_nodes.find_by_coord(goal_coord), op_nodes, cl_nodes


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

        op_nodes = Open()
        op_nodes.push(start)
        cl_nodes = Closed()

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
