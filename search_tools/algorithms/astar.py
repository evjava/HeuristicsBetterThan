from algorithms.search_algorithm import SearchAlgorithm
from node import Node
from containers import Open, Closed

class Astar(SearchAlgorithm):
    def __init__(self, heuristic):
        super().__init__(f'A*(h={heuristic.__name__})')
        self.heuristic = heuristic

    def run(self, area, start_coord, goal_coord):
        start = Node(coord=start_coord)
        goal = Node(coord=goal_coord)

        calc_h = lambda c: self.heuristic(*c, *goal_coord)

        op_nodes = Open()
        op_nodes.push(start)
        cl_nodes = Closed()
        
        while not op_nodes.is_empty:
            s = op_nodes.pop_best()
            if s == goal:
                return s, cl_nodes, op_nodes
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
        
        return None, cl_nodes, op_nodes
