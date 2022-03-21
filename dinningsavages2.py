'''
This script implements solution to second modification of Dinning Savages problem with 
multiple C cooks who cook to N savages.
Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''

from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep
from simplebarrier import SimpleBarrier

__author__ = 'Juraj Lapcak, Matus Jokay'


'''
M - number of portions
N - number of savages without cooks
C - number of cooks
'''
M = 5
N = 3
C = 5


class Shared:
    '''
    Shared class which contains synchronization objects needed.

    Atributes:
        eat_mutex -- Mutex
        cook_mutex -- Mutex which protects number of cooks done
        cooks_done -- number of cooks who finished cooking
        servings_mutex -- 
        servings -- number of servings
        full_pot -- event that signalizes full pot
        empty_pot -- multiplex of C (number of cooks) muplexes
        barrier1 -- SimpleBarrier 
        barrier2 -- SimpleBarrier 
    '''

    def __init__(self):
        self.eat_mutex = Mutex()
        self.cook_mutex = Mutex()
        self.cooks_done = 0
        self.serving_mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(C)
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)


def get_serving_from_pot(savage_id, shared: Shared):
    '''
    Function simulates retreiving cooked missionary from pot.

    Parameters:
        savage_id -- id of savage who is retreiving the portion
        shared -- initialized Shared object
    Returns:
        None
    '''

    print("savage %2d: retreiving portion" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    '''
    Function simulates eating missionary by a savage.

    Parameters:
        savage_id -- id of savage who is eating
    Returns:
        None
    '''

    print("savage %2d: feasting" % savage_id)
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared: Shared):
    '''
    Funtion simulates feasting of a savage with threadId of savage_id. 
    Savage in infinite cycle waits for other savages to come to feast tries to
    retreive a portion and eat it.

    Parameters:
        savage_id -- id of savage
        shared -- initialized Shared object
    Returns:
        None
    '''

    while True:
        shared.barrier1.wait(
            "savage %2d: I have arrived, we are %2d",
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait("savage %2d: we have arrived, beginning feast",
                             savage_id,
                             print_last_thread=True)

        shared.eat_mutex.lock()
        print("savage %2d: remaining portions: %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("savage %2d: waking up cooks" % savage_id)
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.eat_mutex.unlock()

        eat(savage_id)


def put_servings_in_pot(M, shared: Shared, cook_id):
    '''
    Function simulates putiing M cooked missionaries to pot.

    Parameters:
        M -- number of portions to put into a pot
        shared -- initialized Shared object
        cook_id -- threadId of cook who putting portion in pot
    Returns:
        None
    '''

    while True:
        shared.serving_mutex.lock()

        if shared.servings >= M:
            shared.serving_mutex.unlock()
            return
        shared.servings += 1
        print("cook %2d: cooking, %2d serving cooked" %
              (cook_id, shared.servings))
        # cooking one portion takes less
        sleep(0.4 + randint(0, 2) / 100)
        shared.serving_mutex.unlock()


def cook(cook_id, shared: Shared):
    '''
    Function simulates cooking .

    Parameters:
        cook_id -- threadId of cook who is cooking
        shared -- initialized Shared object
    Returns:
        None
    '''

    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(M, shared, cook_id)

        shared.cook_mutex.lock()

        shared.cooks_done += 1
        if shared.cooks_done >= C:
            shared.cooks_done = 0
            shared.full_pot.signal()
        print("cook %2d: is unlocking %2d" % (cook_id, shared.cooks_done))

        shared.cook_mutex.unlock()


threads = list()
shared = Shared()
for savage_id in range(0, N):
    threads.append(Thread(savage, savage_id, shared))

for cook_id in range(0, C):
    threads.append(Thread(cook, cook_id, shared))

for t in threads:
    t.join()
