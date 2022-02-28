from random import randint
from time import sleep
from fei.ppds import Thread, print
from simplebarrier import SimpleBarrier

"""
This program uses class ADT SimpleBarrier from simplebarrier.py and tests it on 100 threads.
"""


def barrier_example(barrier, thread_id):
    """
    Randomly sleeps program and calls barrier's turnstile. Also prints thread's id
    before and after turnstile has been completed.

    Keyword arguments:
    barrier -- initialized SimpleBarrier object
    thread_id -- id of thread

    Returns:
    None
    """
    sleep(randint(1, 10)/10)
    print("Thread %d before barrier" % thread_id)
    barrier.wait()
    print("Thread %d after barrier" % thread_id)


THREADS_COUNT = 100
sb = SimpleBarrier(THREADS_COUNT)

threads = [Thread(barrier_example, sb, i) for i in range(THREADS_COUNT)]
[t.join() for t in threads]
