'''
This script implements solution to Cigarette Smokers problem, where 3 smokers roll and smoke cigarettes 
and 3 agents provide smoking goods.
Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''
from random import randint
from time import sleep
from fei.ppds import Thread, Mutex, Semaphore, print

__author__ = "Juraj Lapcak, Matus Jokay"


class Shared(object):
    '''
    Shared class which contains synchronization objects needed.

    Attributes:
        agent_sem -- holds agents
        isPaper -- bool, if is paper available
        isMatch -- bool, if is match available
        isTobacco -- bool, if is tobacco available
        paper, pusher_paper -- event Semaphore
        match, pusher_match -- event Semaphore
        tobacco, pusher_tobacco -- event Semaphore
        mutex -- Mutex
    Methods:
    '''

    def __init__(self):
        '''
        Initializes shared object.

        Parameters:
            self
        '''
        self.agent_sem = Semaphore(1)

        self.match = Semaphore(0)
        self.paper = Semaphore(0)
        self.tobacco = Semaphore(0)

        self.isMatch = 0
        self.isPaper = 0
        self.isTobacco = 0

        self.pusher_match = Semaphore(0)
        self.pusher_paper = Semaphore(0)
        self.pusher_tobacco = Semaphore(0)

        self.mutex = Mutex()


def agent_a(shared):
    '''
    Simulates agent who waits for signal to give tobacco and paper.

    Parameters:
        None

    Return: 
        None
    '''
    while True:
        sleep(randint(0, 10) / 100)
        # shared.agent_sem.wait()
        print("agent: tobacoo, paper")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_b(shared):
    '''
    Simulates agent who waits for signal to give match and paper.

    Parameters:
        None
    Return: 
        None
    '''
    while True:
        sleep(randint(0, 10) / 100)
        # shared.agent_sem.wait()
        print("agent: paper, match")
        shared.paper.signal()
        shared.match.signal()


def agent_c(shared):
    '''
    Simulates agent who waits for signal to give tobacco and match.

    Parameters:
        None
    Return: 
        None
    '''
    while True:
        sleep(randint(0, 10) / 100)
        # shared.agent_sem.wait()
        print("agent: tobacco, match")
        shared.tobacco.signal()
        shared.match.signal()


def make_cigarette(who):
    '''
    make_cigarette() function simulates making cigarette, by pausing program for <0ms, 10ms>.

    Parameters:
        who -- who is making cigarette 

    Returns:
        None
    '''
    print(f'{who} making cigarette')
    sleep(randint(0, 10) / 100)


def smoke(who):
    '''
    smoke() function simulates smoking, by pausing program for <0ms, 10ms>.

    Parameters:
        who -- who is making cigarette 

    Returns:
        None
    '''
    print(f'{who} smoking')
    sleep(randint(0, 10) / 100)


def smoker_m(shared):
    '''
    Simulates smoker who waits for paper and tobacco and has match, makes cigarette and smokes it.

    Parameters:
        None
    Returns:
        None
    '''
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusher_tobacco.wait()
        shared.pusher_paper.wait()
        make_cigarette('match')
        shared.agent_sem.signal()
        smoke('match')


def smoker_t(shared):
    '''
    Simulates smoker who waits for paper and match and has tobacco, makes cigarette and smokes it.

    Parameters:
        None
    Returns:
        None
    '''
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusher_paper.wait()
        shared.pusher_match.wait()
        make_cigarette('tobacco')
        shared.agent_sem.signal()
        smoke('tobacco')


def smoker_p(shared):
    '''
    Simulates smoker who waits for tobacco and match and has papers, makes cigarette and smokes it.

    Parameters:
        shared -- initialized Shared object
    Returns:
        None
    '''
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusher_tobacco.wait()
        shared.pusher_match.wait()
        make_cigarette('paper')
        shared.agent_sem.signal()
        smoke('paper')


def pusher_match(shared):
    '''
    Simulates pusher who pushes matches to smokers.

    Parameters:
        shared -- initialized Shared object
    Returns:
        None
    '''
    while True:
        print('match.wait()')
        shared.match.wait()
        shared.mutex.lock()
        print('mmmmmmm1')
        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusher_paper.signal()
        elif shared.isPaper:
            shared.isPaper -= 1
            shared.pusher_tobacco.signal()
        else:
            shared.isMatch += 1
        print('mmmmmmm2')
        shared.mutex.unlock()


def pusher_paper(shared):
    '''
    Simulates pusher who pushes rolling paper to smokers.

    Parameters:
        shared -- initialized Shared object
    Returns:
        None
    '''
    while True:
        print('paper.wait()')
        shared.paper.wait()
        shared.mutex.lock()
        print('pppppppp1')
        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusher_match.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.pusher_tobacco.signal()
        else:
            shared.isPaper -= 1
        print('pppppppp2')
        shared.mutex.unlock()


def pusher_tobacco(shared):
    '''
    Simulates pusher who pushes tobacco to smokers.

    Parameters:
        shared -- initialized Shared object
    Returns:
        None
    '''
    while True:
        print('tobacco.wait()')
        shared.tobacco.wait()
        shared.mutex.lock()
        print('tttttt1')
        if shared.isPaper:
            shared.isPaper -= 1
            shared.pusher_match.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.pusher_paper.signal()
        else:
            shared.isTobacco += 1
        print('tttttt2')
        shared.mutex.unlock()


shared = Shared()

smokers = [Thread(smoker_m, shared), Thread(
    smoker_t, shared), Thread(smoker_p, shared)]
pushers = [Thread(pusher_match, shared), Thread(
    pusher_tobacco, shared), Thread(pusher_paper, shared)]
agents = [Thread(agent_a, shared), Thread(
    agent_b, shared), Thread(agent_c, shared)]
for t in smokers + agents + pushers:
    t.join()
