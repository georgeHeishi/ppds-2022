'''
This script implements solution to philosophers dining problem. 

This script requires module `fei.ppds` installed withing Python environment.

This file contains following functions: 
    think
    eat
    get_forks
    put_fork
    philosophers_loop
    
Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''

from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, print

__author__ = "Juraj Lapcak, Matus Jokay"


def think(philosopher_id):
    '''
    Philosophers think.

    Parameters:
        philosopher_id -- id of philosopher that is dining
    Returns:
        None
    '''
    print(f"I'm {philosopher_id} and I'm thinking")
    sleep(randint(10/50)/1000)


def eat(philosopher_id):
    '''
    Philosopher eat.

    Parameters:
        philosopher_id -- id of philosopher that is dining
    Returns:
        None
    '''
    print(f"I'm {philosopher_id} and I'm eating")
    sleep(randint(10/50)/1000)


def get_forks(forks, waiter, philosopher_id):
    '''
    Philosopher get fork.

    Parameters:
        forks -- forks that are take down (semaphores put to wait)
        waiter -- 
        philosopher_id -- id of who is taking a fork
    Returns:
        None
    '''
    waiter.wait()
    print(f"I'm {philosopher_id} and I'm getting a fork")
    forks[philosopher_id].wait()
    forks[(philosopher_id + 1) % PHILOSOPERS_N].wait()
    print(f"I'm {philosopher_id} and I took a fork")


def put_fork(forks, waiter, philosopher_id):
    '''
    Philosopher put fork.

    Parameters:
        forks -- forks that are put down (semaphores signalized that they can be taken)
        waiter -- 
        philosopher_id -- id of who is putting a fork
    Returns:
        None
    '''
    forks[philosopher_id].signal()
    forks[(philosopher_id + 1) % PHILOSOPERS_N].signal()
    print(f"I'm {philosopher_id} and I'm putting fork")
    waiter.signal()


def philosophers_loop(forks, waiter, philosopher_id):
    '''
    Main loop of philosopers dining. Philosophers take think, take fork, eat with it and put in down in a cycle.

    Parameters:
        forks -- forks that are put down
        waiter -- waiter (semaphores)
        philosopher_id -- id of philosopher that is dining
    Returns:
        None
    '''

    sleep(randint(40/100)/1000)

    while True:
        think(philosopher_id)
        get_forks(forks, waiter, philosopher_id)
        eat(philosopher_id)
        put_fork(forks, waiter, philosopher_id)


PHILOSOPERS_N = 5

forks = [Semaphore(1) for _ in range(PHILOSOPERS_N)]
waiter = Semaphore(PHILOSOPERS_N - 1)

philosophers = [Thread(philosophers_loop, forks, waiter,
                       philosopher_id) for philosopher_id in range(PHILOSOPERS_N)]
[p.join() for p in philosophers]
