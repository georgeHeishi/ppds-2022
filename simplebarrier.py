"""
This script requires module `fei.ppds` installed withing Python environment.

This file can also be imported as module and contains following class:
    SimpleBarrier - implemented ADC SimpleBarrier
"""

from fei.ppds import Event, Mutex

__author__ = "Juraj Lapcak, Matus Jokay"


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
        """
        Constructs attributes for SimpleBarrier object.

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
            self.counter = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()
