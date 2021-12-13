from dataclasses import dataclass
from task import Task
from typing import List
from containers.base_container import Container

EPS = 0.000001

def prepare_result(task: Task, path, n_exp, n_op):
    act_len = path.cost if path else None
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
            opt = 'True' if self.correct() else f'False (opt: {self.opt_len:.3f})'
            msg = f'Path found! Length: {self.act_len:.3f}\n' \
                  f'Nodes created: {self.nodes_created}.\n' \
                  f'Number of steps: {self.steps}.\n' \
                  f'Correct: {opt}.'
        else:
            msg = 'Path not found!'
        return msg
    
    @staticmethod
    def create(task: Task, res):
        inst_args = prepare_result(task, *res)
        return RunResult(task, *inst_args[:-1])

@dataclass
class AreaRunResult(RunResult):
    path:       Container
    n_expanded: Container
    n_opened:   Container
        
    @staticmethod
    def create(task: Task, res):
        path_, n_exp, n_op = res
        win = path_ is not None
        inst_args = prepare_result(task, *res)
        return AreaRunResult(task, *inst_args, n_exp, n_op)
    
    def drop_expanded(s, max_time):
        args_0 = s.task, s.nodes_created, s.steps, s.act_len, s.opt_len
        new_expanded = [i for i in s.n_expanded if i.time <= max_time]
        args_1 = s.path, new_expanded, s.n_opened
        return AreaRunResult(*args_0, *args_1)
    
    def iter_coords(self):
        yield from (self.task.start_c, self.task.goal_c)
        # todo fix after API refinement
        yield from self.path
        # todo remove!
        # if isinstance(self.path[0], Node):
        #     yield from (p.coord for p in self.path)
        # else:
        #     yield from self.path
        yield from self.n_expanded.elements.keys()
        yield from self.n_opened.elements.keys()
