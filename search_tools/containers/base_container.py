from typing import Iterable, Tuple, List

class Container(object):
    def time(self, e: Tuple) -> int:
        ''' return time by coordinate '''
        raise AttributeError('Not implemented yet.')

    def coords(self) -> Iterable[Tuple]:
        ''' iterate coordinates '''
        raise AttributeError('Not implemented yet.')

    def __len__(self) -> int:
        raise AttributeError('Not implemented yet.')
