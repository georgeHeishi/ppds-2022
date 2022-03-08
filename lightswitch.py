'''
This script implements ADT Lightswitch class.

This file can also be imported as module and contains following class:
    Lightswitch - implemented ADT Lightswitch
'''

from fei.ppds import Mutex


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

    def __init_(self):
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
        None
        """

        self.mutex.lock()
        if self.counter == 0:
            semaphore.wait()
        self.cnt += 1
        self.mutex.unlock()

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
        self.cnt -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()
