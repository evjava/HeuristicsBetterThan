from algorithms.astar import Astar
from algorithms.astar_heuristics import diagonal_dist
from moving_ai.mai_map_reader import MaiReader, MaiMaps
from pipeline import *
from run_result import RunResult

EPS = 0.000001

def process(a_results):
    for a, rs in a_results.items():
        print(a)
        for r in rs:
            print('\t', r.act_len, r.opt_len, abs(r.act_len - r.opt_len) < EPS)

def build_dummy_pipeline():
    return Pipeline(
        reader=MaiReader(MaiMaps.ARENA),
        algorithms=[Astar(diagonal_dist)],
        res_builder=RunResult.create,
        processor=LProcessor(process)
    )

p = build_dummy_pipeline()
p.run()
