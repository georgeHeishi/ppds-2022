from collections import Counter
from fei.ppds import Mutex, Thread


# class Shared contains fields:
# mutex     - shared lock that sleeps the program and makes sure concurtent programs runs paralel
# counter   - shared counter
# size      - size of elms array
# elm       - shared array with initialized values of 0
class Shared():
    def __init__(self, size):
        self.mutex = Mutex()
        self.counter = 0
        self.end = size
        self.elms = [0] * (size)


# functions which takes:
# shared    - already initialized Shared object
# function doesnt return anything
# function increments elements in elm array of Shared object in shared.end range
def count(shared):
    # lock the whole cycle
    shared.mutex.lock()
    while True:
        if(shared.counter >= shared.end):
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
    shared.mutex.unlock()


shared = Shared(1_000_000)

thread1 = Thread(count, shared)
thread2 = Thread(count, shared)

thread1.join()
thread2.join()

counter = Counter(shared.elms)
print(counter.most_common())
