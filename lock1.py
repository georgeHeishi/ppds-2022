from collections import Counter
from fei.ppds import Mutex, Thread


class Shared():
    """Shared class between threads.

    Attributes:
    mutex -- shared lock that sleeps the program and makes sure concurtent programs runs paralel
    counter -- index into elm array
    end -- size of elms array
    elm -- shared array with initialized values of 0
    """

    def __init__(self, size):
        """Constructs attributes for shared object.

        Parameters:
        size -- size of elms array
        """

        self.mutex = Mutex()
        self.counter = 0
        self.end = size
        self.elms = [0] * (size)


def count(shared):
    """Increment elements in elm array of Shared object in shared.end range.

    Keyword arguments:
    shared -- initialized Shared object

    Returns:
    None
    """

    while True:
        # Lock incrementation of element and counter so it is an atomic operation
        shared.mutex.lock()
        if(shared.counter >= shared.end):
            # Unluck Mutex after incrementation and in case counter is out of range
            shared.mutex.unlock()
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
        # Unluck Mutex after incrementation and in case counter is out of range
        shared.mutex.unlock()


shared = Shared(1_000_000)

thread1 = Thread(count, shared)
thread2 = Thread(count, shared)

thread1.join()
thread2.join()

counter = Counter(shared.elms)
print(counter.most_common())
