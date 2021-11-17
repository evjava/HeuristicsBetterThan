from algorithms.search_algorithm import SearchAlgorithm
from containers import Open, Closed
from typing import List, Callable, Tuple
from dataclasses import dataclass
from run_result import RunResult
from node import Node

@dataclass
class Reader(object):
    payload: str

    def read(self):
        raise AttributeError('Not implemented yet...')

class Processor(object):
    def process(self, results):
        raise AttributeError('Not implemented yet...')

@dataclass
class LProcessor(Processor):
    callback: any

    def process(self, results):
        self.callback(results)

class Pipeline(object):
    def __init__(self,
                 reader:      Reader,
                 algorithms:  List[SearchAlgorithm],
                 res_builder: Callable[Tuple[Node, Closed, Open], RunResult] = RunResult.create,
                 processor:   Processor = lambda x:x,
                 ):
        self.reader = reader
        self.algorithms = algorithms
        self.res_builder = res_builder
        if callable(processor):
            processor = LProcessor(processor)
        self.processor = processor
        self._m_tasks = None
        self._a_results = None

    @property
    def m_tasks(self):
        if self._m_tasks is None:
            self._m_tasks = self.reader.read()
        return self._m_tasks

    def a_results(self, m, tasks):
        if self._a_results is None:
            a_results = []
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
        self.processor.process(a_results)

    def with_processor(self, processor):
        if callable(processor):
            processor = LProcessor(processor)
        return Pipeline(
            reader = self.reader,
            algorithms = self.algorithms,
            res_builder = self.res_builder,
            processor = processor,
        )
