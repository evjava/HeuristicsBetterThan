from dataclasses import dataclass

def prepare_result(task: Task, res):
    win, path_, n_exp, n_op = res
    if win:
        path, act_len = make_path(path_)
    else:
        path, act_len = None, None
    inst_args = (len(n_op) + len(n_exp), len(n_exp), act_len, task.opt_len, path)
    return inst_args


def run_task(mai_map: MapMAI, task: Task, search_f, heuristic, res_builder=RunResult.create):
    try:
        res = search_f(mai_map, *task.start, *task.goal, heuristic)
        rr = res_builder(task, res)
        return rr
    except Exception as e:
        traceback.print_exc()
        print('Execution error')
        print(e)
        return None        

LOG_FILE = 'run.log'
def now(): return dt.strftime(dt.now(), '%H:%M:%S.%f')
def log(*args): print(now(), ':', *args, file=open(LOG_FILE, 'a'))    

def take_shuffled(items, count):
    items2 = items[::]
    random.shuffle(items2)
    if len(items2) > count:
        log(f'\tdropped {len(items2) - count} items')
    return items2[:count]

REPORT_BAD = True
BAD_CNT = 5

def run_tasks(mai_map, tasks, search_f, h, res_builder):
    log(f'\tStarting running; h={h.__name__}')
    runner = lambda t: run_task(mai_map, t, search_f, h, res_builder)
    res = Parallel(n_jobs=7)(delayed(runner)(t) for t in tasks)
    good_res = [*filter(RunResult.path_found, res)]
    
    if REPORT_BAD:
        bad = 0
        for t, r in zip(tasks, res):
            if bad >= BAD_CNT:
                break
            if r.path_not_found():
                bad += 1
                print(f'Path not found for task {t}')
            elif r.act_div_opt() < 1:
                bad += 1
                print(f'Path can\'t be superoptimal: {t}, act: {r.act_len}, opt: {r.opt_len}')
    log(f'\t\tDone running; h={h.__name__}, map.size={mai_map.size}')
    return good_res

MAX_TASKS = 900

def run_tasks_hs(mai_map: MapMAI, tasks: List[Task], search_f, res_builder):
    tasks = take_shuffled(tasks, MAX_TASKS)
    log(f'Starting processing map, size={mai_map.size}, tasks.size={len(tasks)}')
    return [(h.__name__, run_tasks(mai_map, tasks, search_f, h, res_builder)) for h in HEURISTICS]

def bad_results(results): 
    return [r for r in results if r.act_len is None]
