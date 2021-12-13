from typing import List, Tuple

from run_result import RunResult

class Processor(object):
    def process(self, all_results: Tuple[Tuple[str, List[RunResult]]]):
        ''' List[RunResult]'s sorted and consistent '''
        # todo fix signature? 
        raise AttributeError('Not implemented yet...')

    def then(self, other):
        def process_self_then_p(all_results):
            self.process(all_results)
            other.process(all_results)
        return LProcessor(process_self_then_p)

    def is_area(self) -> bool:
        return False

class LProcessor(Processor):
    def __init__(self, callback):
        self.callback = callback

    def process(self, all_results):
        return self.callback(all_results)

class ComposeProcessor(Processor):
    def __init__(self, a: Processor, b: Processor):
        self.a, self.b = a, b

    def process(self, all_results):
        self.a.process(all_results)
        self.b.process(all_results)

    def is_area(self):
        return self.a.is_area() or self.b.is_area()

def check(nulls, not_nulls):
    check_nulls = all(map(lambda x: x is None, nulls))
    check_not_nulls = all(map(lambda x: x is not None, not_nulls))
    return check_nulls and check_not_nulls

class AreaProcessor(Processor):
    def __init__(self):
        self.area = None

    def process_with_area(self, area, all_results):
        raise AttributeError('Not implemented yet...')

    def process(self, all_results):
        if self.area is None:
            raise AttributeError('Map is not installed!')
        if not all(len(ar[1]) == 1 for ar in all_results):
            raise AttributeError('Only one task for visualization expected!')
        return self.process_with_area(self.area, all_results)

    def is_area(self):
        return True
