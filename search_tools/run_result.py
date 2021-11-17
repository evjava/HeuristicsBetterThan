from dataclasses import dataclass
from task import Task
from typing import List
from node import Node
from containers import Open, Closed

EPS = 0.000001

def make_path(goal):
    '''
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    '''
    length = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length

def prepare_result(task: Task, res):
    path_, n_exp, n_op = res
    win = path_ is not None
    if win:
        path, act_len = make_path(path_)
    else:
        path, act_len = None, None
    inst_args = (len(n_op) + len(n_exp), len(n_exp), act_len, task.opt_len, path)
    return inst_args

@dataclass
class RunResult:
    task:          Task
    nodes_created: int
    steps:         int
    act_len:       float
    opt_len:       float
        
    def correct(self): return abs(self.act_len - self.opt_len) < EPS
    def path_found(self): return self.act_len is not None
    def path_not_found(self): return not self.path_found()
    def act_div_opt(self): 
        return 1 if abs(self.act_len - self.opt_len) < EPS else self.act_len / self.opt_len
    
    @property
    def report(self):
        if self.path_found():
            msg = f'Path found! Length: {self.act_len:.3f}. ' \
                  f'Nodes created: {self.nodes_created}. ' \
                  f'Number of steps: {self.steps}. ' \
                  f'Correct: {self.correct()}.'
        else:
            msg = 'Path not found!'
        return msg
    
    @staticmethod
    def create(task: Task, res):
        inst_args = prepare_result(task, res)
        return RunResult(task, *inst_args[:-1])
    

@dataclass
class EnrichedRunResult(RunResult):
    path:       List[Node]
    n_expanded: Closed
    n_opened:   Open
        
    @staticmethod
    def create(task: Task, res):
        win, path_, n_exp, n_op = res
        inst_args = prepare_result(task, res)
        return EnrichedRunResult(task, *inst_args, n_exp, n_op)
    
    def drop_expanded(s, max_time):
        args_0 = s.task, s.nodes_created, s.steps, s.act_len, s.opt_len
        new_expanded = [i for i in s.n_expanded if i.time <= max_time]
        args_1 = s.path, new_expanded, s.n_opened
        return EnrichedRunResult(*args_0, *args_1)
    
    def iter_coords(self):
        yield from (self.task.start, self.task.goal)
        yield from (p.coord for p in self.path)
        yield from self.n_expanded.elements.keys()
        yield from self.n_opened.elements.keys()
