from typing import List, Callable, Tuple
from dataclasses import dataclass

from areas.area import Area
from algorithms.search_algorithm import SearchAlgorithm, RunOutput
from run_result import RunResult, AreaRunResult
from node import Node
from task import Task
from reader import Reader
from processors.processor import Processor, LProcessor, AreaProcessor

class Pipeline(object):
    def __init__(self,
                 reader:      Reader,
                 algorithms:  List[SearchAlgorithm],
                 processor:   Processor = lambda x:x,
                 ):
        self.reader = reader
        self.algorithms = algorithms
        self.res_builder = AreaRunResult.create if processor.is_area() else RunResult.create
        if callable(processor):
            processor = LProcessor(processor)
        self.processor = processor
        self._m_tasks = None
        self._a_results = None

    @property
    def m_tasks(self):
        if self._m_tasks is None:
            self._m_tasks = self.reader.read_map_tasks()
        return self._m_tasks

    def a_results(self, m, tasks: List[Task]):
        tasks = (t for t in tasks if t.opt_len > 0)
        tasks = sorted(tasks, key=lambda t:t.opt_len)
        if self._a_results is None:
            a_results = []
            # todo eliminate, move to some context? Maybe area?
            Node.TIME = 0
            for a in self.algorithms:
                # todo wrap try/except
                # todo joblibs?
                a_out = [
                    self.res_builder(t, a.run(m, t.start_c, t.goal_c))
                    for t in tasks
                ]
                a_results.append((a.name, a_out))
            self._a_results = a_results
        return self._a_results

    def run(self):
        m, tasks = self.m_tasks
        a_results = self.a_results(m, tasks)
        if isinstance(self.processor, AreaProcessor):
            self.processor.area = m
        result = self.processor.process(a_results)
        return result

    def with_processor(self, processor):
        if callable(processor):
            processor = LProcessor(processor)
        pipeline_upd = Pipeline(
            reader = self.reader,
            algorithms = self.algorithms,
            processor = processor,
        )
        pipeline_upd._m_tasks = self._m_tasks
        pipeline_upd._a_results = self._a_results
        return pipeline_upd
