# Assignment 01

## About Assignment

The goal of this assignment is to implement two threads that use shared index of shared array of certain size. Each thread increments the element of array which is pointed at by shared index. The index is also incemented. If the index is pointing outside the range of array thread is terminated. After termination occurance of elements in array is counted and displayed.

## Shared Object `shared`

Datafields:

    1. mutex   — shared lock that sleeps the program and makes sure concurtent programs  runs paralel
    2. counter — shared counter
    3. end     — size of elms array
    4. elms    — shared array with initialized values of 0

## Function `count`

One parameter:

    1. shared  — already initialized Shared object

Function increments elements in `shared.elm` array of `Shared` object in `shared.end` range.

### First Use of Mutex Lock

The core of `count` function is based on two operations: incementing the actual element of array, and incrementing index of array. By first use of we combined these two operations into one atomic operation so that threads do not interfere in execution. It is important to note that Mutex needs to be unlocked after the two operations as well as in the case of counter being out of index range of elms array. Oterwise execution of program is going fall into deadlock.

### Second Use of Mutex Lock

The other place where we could place the lock is on the while as the whole. Which leads to thread getting control over the whole cycle and lock unlocks after the thread increments all elements of `shared.elm` array. Thereafter first method of locking part of a function allows threads to alternate between executing threads.
