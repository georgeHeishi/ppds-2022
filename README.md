# Assignment 01

[![Python 3.8.10](https://img.shields.io/badge/python-3.8.10-blue.svg)](https://www.python.org/downloads/release/python-3810/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

## About Assignment

The goal of this assignment is to implement two threads that use shared index of shared array of certain size. Each thread increments the element of array which is pointed at by shared index. The index is also incemented. If the index is pointing outside the range of array thread is terminated. After termination occurance of elements in array is counted and displayed.

We have split the assigment into two experiments. The first use of Mutex lock in [lock1.py file](lock1.py.md) and second use of Mutex lock in [lock2.py file](lock2.py.md). Both files use the `shared` object and `count` function, files differ in place where locks are placed therefore in paralel execution logic.

## Shared Object `shared`

Datafields:

    1. mutex   — shared lock that sleeps the program and makes sure concurtent programs  runs paralel
    2. counter — shared counter
    3. end     — size of elms array
    4. elms    — shared array with initialized values of 0

## Function `count`

One parameter:

    1. shared  — already initialized Shared object

No return value.

Function increments all elements in `shared.elm` array of `Shared` object in `shared.end` range.

## Experiments

### 0. Experiments without lock

While exeperimenting with `count` function without use of locks in following form:

```python
def count(shared):
        while True:
        if(shared.counter >= shared.end):
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
```

We experimented on `shared` object with `elms` of length of: 1_000, 10_000, 100_000 and 1_000_000.

1. 1_000 elements:
   when incementing 1000 elements using two thread we can see that the result is 1000 elements of value 1. `[(1, 1000)]`
2. 10_000 elements:
   when incementing 10000 elements using two thread we can see that the result is 10000 elements of value 1. `[(1, 10000)]`
3. 100_000 elements:
   we noticed similar result when incrementing 100000 elements `[(1, 100000)]`
4. 1_000_000 elements:
   problem start to occur when size of array is bigger that a million `[(1, 926582), (2, 73416), (0, 2)]`. 926582 elements of 1 value, 73416 elements of 2 value, which means threads joined shared index on 73416 elements.

### 1. First Use of Mutex Lock

The core of `count` function is based on two operations: incementing the actual element of array, and incrementing index of array. By first use of lock we combined these two operations into one atomic operation so that threads do not interfere in execution. It is important to note that Mutex needs to be unlocked after the two operations as well as in the case of counter being out of index range of elms array. Oterwise execution of program is going fall into deadlock.

### 2. Second Use of Mutex Lock

The other place where we could place the lock is on the while as a whole. Which leads to thread getting control over the whole cycle. Lock unlocks after the thread increments all elements of `shared.elm` array. Thereafter first method of locking part of a function allows threads to alternate between executing threads and truer paralel execution.

## Conclusion

Both uses of locks proved to have helped the flow of execution between threads and all elements of array were incremented to the same value of 1 in case of size of array being 1_000, 10_000, 100_000 and or 1_000_000.
