from fei.ppds import Thread, Semaphore, print
from random import randint
from time import sleep
from simplebarrier import SimpleBarrier

"""
This program implements computation of fibonacci sequence using N-threads with N+1 Semaphore 
synchronization objects. Before computing the fibonacci sequence, program waits for all threads
to finish initialization using SimpleBarrier from simplebarrier.py.
"""


def compute_fibonacci(sb, i):
    """
    Compute i-th fibonacci sequence number with i-th thread.

    Keyword arguments:
    sb -- initialized SimpleBarrier object
    i -- id of thread computing i-th fibonacci sequence number

    Returns:
    None
    """
    sleep(randint(1, 10)/10)
    print(i)

    # wait for all threads to get to this point
    sb.wait()

    # wait for (i-1)-th thread to finish calculation of its fibonacci number
    sem[i].wait()
    print(f"After wait {i}")
    fib_seq[i+2] = fib_seq[i] + fib_seq[i+1]
    print(fib_seq)
    # signal to i-th thread to start calculation
    sem[i+1].signal()


THREADS_COUNT = 10
sb = SimpleBarrier(THREADS_COUNT)

# initialize THREADS_COUNT + 1 signalization Semaphores, beloging to appropriate thread
sem = [Semaphore(0) for _ in range(THREADS_COUNT + 1)]
# signal that 0th thread is ready to go after barrier is down
sem[0].signal()

threads = [Thread(compute_fibonacci, sb, i) for i in range(THREADS_COUNT)]

# initialize fibonacci sequence with 0 on appropriate index
fib_seq = [0] * (THREADS_COUNT + 2)
fib_seq[1] = 1

[t.join() for t in threads]

print("Final fibonacci sequence")
print(fib_seq)
