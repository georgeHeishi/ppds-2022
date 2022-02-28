from random import randint
from time import sleep
from fei.ppds import Thread, print
from simplebarrier import SimpleBarrier

"""
This program uses implementation of ADT SimpleBarrier from problem1.py file and tests it as reusable Barrier on
infinite cycle with 10 threads.
"""


def before_barrier(thread_id):
    """
    Simulate code execution before barrier's turstile (sleep execution for a few millisecond).

    Keyword arguments:
    thread_id -- id of thread executing code

    Returns:
    None
    """
    sleep(randint(1, 10)/10)
    print(f"Thread  {thread_id} before barrier")


def after_barrier(thread_id):
    """
    Simulate code execution after barrier's turstile (sleep execution for a few millisecond).

    Keyword arguments:
    thread_id -- id of thread executing code

    Returns:
    None
    """
    print(f"Thread {thread_id} after barrier")
    sleep(randint(1, 10)/10)


def barrier_cycle(b1, b2, thread_id):
    """
    Simulate code before and after barrier, with it's representative barrier.

    Keyword arguments:
    b1 -- initialized first barrier
    b2 -- initialized second barrier
    thread_id -- id of thread executing code

    Returns:
    None
    """

    while True:
        before_barrier(thread_id)
        b1.wait()
        after_barrier(thread_id)
        b2.wait()


THREADS_COUNT = 10
sb1 = SimpleBarrier(THREADS_COUNT)
sb2 = SimpleBarrier(THREADS_COUNT)

threads = [Thread(barrier_cycle, sb1, sb2, i) for i in range(THREADS_COUNT)]
[t.join() for t in threads]
