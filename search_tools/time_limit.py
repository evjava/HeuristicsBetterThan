from contextlib import contextmanager
import threading
import _thread
import time

from loguru import logger as log
log.remove()
log.add('runs.log', format='{time}  {level} {name} {message}', level='INFO')

class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

import traceback

@contextmanager
def time_limit(seconds, msg='Failed'):
    if seconds is None:
        yield
    else:
        timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
        timer.start()
        try:
            time_start = time.time()
            yield
        except KeyboardInterrupt as ex:
            time_total = time.time() - time_start
            traceback.print_exc()
            log.info(time_total, seconds)
            if time_total < seconds:
                raise KeyboardInterrupt('Interrupted')
            else:
                raise TimeoutException("Timed out for operation {}".format(msg))
        finally:
            # if the action ends in specified time, timer is canceled
            timer.cancel()

@contextmanager
def time_limit_2(seconds, msg='Failed'):
    time_start = time.time()
    yield
    time_total = time.time() - time_start
    if seconds > time_total:
        raise TimeoutException("Timed out for operation {}".format(msg))
