from contextlib import contextmanager
import threading
import _thread
import time

class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

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
