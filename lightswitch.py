'''
This script requires module `fei.ppds` installed withing Python environment.

This file can also be imported as module and contains following class:
    Lightswitch - implemented ADC Lightswitch
'''

from fei.ppds import Mutex

__author__ = "Juraj Lapcak, Matus Jokay"


class Lightswitch:
    """
    Lightswitch class.

    Attributes:
    counter -- counter of how many items are being locked
    mutex -- lock

    Methods:
    lock() -- turns on the lightswitch
    unlock() -- turns off the lightswitch
    """

    def __init__(self):
        """
        Initializes attributes for SimpleBarrier object.

        Parameters:
        self
        """

        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        """
        Turns on the lightswitch.

        Parameters:
        self
        semaphore -- initialized semaphore to lock

        Returns:
        count
        """

        self.mutex.lock()
        if self.counter == 0:
            semaphore.wait()
        self.counter += 1
        self.mutex.unlock()
        return self.counter

    def unlock(self, semaphore):
        """
        Turns off the lightswitch.

        Parameters:
        self
        semaphore -- initialized semaphore to lock

        Returns:
        None
        """

        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()
