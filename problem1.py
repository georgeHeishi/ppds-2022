from random import randint
from time import sleep
from fei.ppds import Thread, Event, Mutex, print

"""
This program implements class ADT SimpleBarrier and tests it on 100 threads.
"""


class SimpleBarrier:
    """
    Barrier class.

    Attributes:
    n -- number of threads to block with barrier
    counter -- number of threads currently blocked
    mutex -- shared lock that sleeps the program and makes sure concurtent programs runs paralel
    event -- 

    Methods:
    wait() -- representation of barrier's turnstile
    """

    def __init__(self, n):
        """Constructs attributes for SimpleBarrier object.

        Parameters:
        n -- number of threads the barrier blocks
        """
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """
        Lock's program until all threads completed turnstile.

        Parameters:
        None

        Returns:
        None
        """
        self.event.clear()
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.c = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()


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
