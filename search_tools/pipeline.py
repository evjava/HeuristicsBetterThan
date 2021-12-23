from typing import List, Callable, Tuple
from dataclasses import dataclass

from areas.area import Area
from algorithms.search_algorithm import SearchAlgorithm, RunOutput
from run_result import RunResult, AreaRunResult
from node import Node
from task import Task
from reader import Reader
from processors.processor import Processor, LProcessor, AreaProcessor
from time_limit import time_limit
from joblib import Parallel, delayed

from loguru import logger as log
log.remove()
log.add('runs.log', format='{time}  {level} {name} {message}', level='INFO')

import traceback


class Pipeline(object):
    def __init__(self,
                 reader:      Reader,
                 algorithms:  List[SearchAlgorithm],
                 processor:   Processor=lambda x:x,
                 timelimit:   int=10,
                 jobs:        int=1,
                 ):
        self.reader = reader
        self.algorithms = algorithms
        self.res_builder = AreaRunResult.create if processor.is_area() else RunResult.create
        self.timelimit = timelimit
        self.jobs = jobs
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
            self._ar_m, self._ar_tasks = m, tasks
            a_results = []
            # todo eliminate, move to some context? Maybe area?
            Node.TIME = 0
            for ai, a in enumerate(self.algorithms):
                self._ar_a = a
                log.info('Started algorithm {}, {}/{}', a, ai+1, len(self.algorithms))
                ts_ids = range(len(tasks))

                if self.jobs == 1:
                    a_out = [self._run_task(ti) for ti in ts_ids]
                else:
                    a_out = Parallel(n_jobs=self.jobs, require='sharedmem')(delayed(self._run_task)(ti) for ti in ts_ids)
                a_results.append((a.name, a_out))
                self._ar_a = None
            self._a_results = a_results
            self._ar_m, self._ar_tasks = None, None
        return self._a_results

    def _run_task(self, ti):
        area, tasks, algo = self._ar_m, self._ar_tasks, self._ar_a
        log.info('Started task idx={} ({})', ti, len(tasks))
        task = tasks[ti]
        try:
            with time_limit(self.timelimit, msg='{}: limit exceed for task_i={}'.format(algo, ti)):
                algo_res = algo.run(area, task.start_c, task.goal_c)
                res = self.res_builder(task, algo_res)
            log.success('Done task idx={} ({})', ti, len(tasks))
        except KeyboardInterrupt as ex:
            raise ex
        except Exception as ex:
            # traceback.print_exc()
            log.error("Task idx={} failed, not enough time", ti)
            res = None
        return res
            

    def run(self):
        m, tasks = self.m_tasks
        a_results = self.a_results(m, tasks)
        if isinstance(self.processor, AreaProcessor):
            self.processor.area = m
        result = self.processor.process(a_results)
        return result

    def with_algorithms(self, algorithms):
        pipeline_upd = Pipeline(
            reader = self.reader,
            algorithms = algorithms,
            processor = self.processor,
            timelimit = self.timelimit
        )
        pipeline_upd._m_tasks = self._m_tasks
        return pipeline_upd

    def with_processor(self, processor):
        if callable(processor):
            processor = LProcessor(processor)
        pipeline_upd = Pipeline(
            reader = self.reader,
            algorithms = self.algorithms,
            processor = processor,
            timelimit = self.timelimit,
            jobs = self.jobs
        )
        pipeline_upd._m_tasks = self._m_tasks
        pipeline_upd._a_results = self._a_results
        return pipeline_upd

    def clear_cache(self):
        self._m_tasks = None
        self._a_results = None

