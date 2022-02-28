# PPDS 2022 - Juraj Lapčák

[![Python 3.10.2](https://img.shields.io/badge/python-3.10.2-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[PPDS](https://uim.fei.stuba.sk/predmet/i-ppds/)

## About Assignment

Assignment is split into three tasks. The first task is focused on creating ADT simple barrier using Event synchronization object. The second task is focused on reusing previously implemented simple barrier on multiple barrier_example functions. In thirds task we implement computation of fibonacci sequence using synchronization objects Semaphore and Event.

## First Task

In first task we created actually reusable `SimpleBarrier` using Event synchronization object using following pseudoalgorithm:

```python
M.lock()
    C += 1
    if C == N:
        C = 0
        T.signal(N)
M.unlock()
T.wait()
```

Where M is mutex object, T is reprezentation of signalization sychronous object. This works fine when using `Semaphore` object. In our case we wanted to implement it with `Event` so we needed to first use `clear()` method so that `wait()` method of `SimpleBarrier` might become reusable.

We tested this implementation in `problem1.py` file using 100 threads. Where we can see that thread `id`s are grouped beautifuly into before and after thread groups:

```
...
Thread 12 before barrier
Thread 11 before barrier
Thread 10 before barrier
Thread 26 before barrier
Thread 20 before barrier
Thread 85 before barrier
Thread 89 before barrier
Thread 76 before barrier
Thread 52 before barrier
Thread 40 before barrier
Thread 35 before barrier
Thread 35 after barrier
Thread 21 after barrier
Thread 22 after barrier
Thread 27 after barrier
Thread 31 after barrier
Thread 42 after barrier
Thread 48 after barrier
Thread 49 after barrier
Thread 56 after barrier
Thread 73 after barrier
Thread 14 after barrier
...
```

## Second Task

We implemented reusable `SimpleBarrier` using `Event` object in the first task. So we had less work with second task. All that remained was to test it on `rendezvous` (before_barrier function) and `critical area` (after_barrier function) in infinite loop. Where we noticed that using one barrier threads fight for execution unpredictably. Using two barriers we secure that threads do not overtake unwantedly. Using following loop:

```python
while True:
    before_barrier(thread_id)
    B1.wait()
    after_barrier(thread_id)
    B2.wait()
```

Where B1 is first and B2 is second barrier.

## Third Task

In third task we created two modules: fibonacci1.py, fibonacci2.py. In first module (fibonacci1.py) we used N + 1 Semaphore synchronization object, where N is number of threads used to compute N numbers of fibonacci sequence after first `1`.

In second module (fibonacci2.py) we used Event synchronization object with the same number of objects and used threads.

Both implementations use the same logic but different objects. Firstly we initialize SimpleBarrier object reused from first problem. This object comes in handy when waiting for all threads to finish initialization and begin computation. Secondly we initialize N + 1 `Semaphores/Event`s, using (+1) because all threads signalize to following thread that it is ready to go. So the N+1-th `Semaphores/Event` is in reserve. We signalized to the first Semaphores/Event object that it is ready to go, so that after initialization of all threads first object can begin computation. In the final initialization we initialize N threads with `compute_fibonacci` function.

In `compute_fibonacci` function program is slept for random ammount of millisecond so that we force threads to finish initialization in random order. Using `SimpleBarrier`'s turnstile we wait for all threads to end initialization and force wait with signalization synchronous object. But of course we firsly signalized the first object to begin computation, that means it begins after all threads are initialized. After i-th thread is done it signalizes to (i+1)-th thread it is ready to go.

The lowest ammount of synchronization objects needed to implement this version of implementation is N where N is number of threads used. Actually N+2 if we count `Event` and `Mutex` object used in `SimpleBarrier`.

## Conclusion

Barrier object provides solution for situation where threads need to grouped and or wair for initialization so that they can execute parallel code predictably. We also learned that basic computational problem of Fibonacci numbers is possible to be solved using parallel programming differently than using recursion.
