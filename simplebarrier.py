'''
This script requires module `fei.ppds` installed withing Python environment.

This file can also be imported as module and contains following class:
    SimpleBarrier - implemented ADC SimpleBarrier
'''

from fei.ppds import Semaphore, Mutex

__author__ = "Juraj Lapcak, Matus Jokay"


class SimpleBarrier:
    '''
    Barrier class.

    Attributes:
        n -- number of threads to block with barrier
        counter -- number of threads currently blocked
        mutex -- shared lock that sleeps the program and makes sure concurtent programs runs paralel
        event --
    Methods:
        wait() -- representation of barrier's turnstile
    '''

    def __init__(self, n):
        '''
        Constructs attributes for SimpleBarrier object.

        Parameters:
            n -- number of threads the barrier blocks
        '''

        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        '''
        Lock's program until all threads completed turnstile.

        Parameters:
            print_str -- string to print
            savage_id -- id of savage to print
            print_last_thread -- (default False) whether to print last thread of not
            print_each_thread -- (default False) whether to print each thread of not
        Returns:
            None
        '''

        self.mutex.lock()
        self.counter += 1
        if print_each_thread:
            print(print_str % (savage_id, self.counter))
        if self.counter == self.n:
            self.counter = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.sem.signal(self.n)
        self.mutex.unlock()
        self.sem.wait()
