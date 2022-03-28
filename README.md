# Assignment 06

[![Python 3.10.2](https://img.shields.io/badge/python-3.10.2-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[PPDS](https://uim.fei.stuba.sk/predmet/i-ppds/)

## Barbershop

- Barbershop contains two rooms:

  1. _Waiting room_ with N `customer`s
  2. One `barber` stool

- If there are no `customer`s -- `barber` remains idle

- If `customer` walks in:

  1. If there is no room in _Waiting room_ (customer counter s of N size), customer `balk`s out
  2. If `barber` is busy, and there's room in _Waiting room_ `customer` joins others in waiting room
  3. If `barber` is idle, customer signalizes to barber to customer arrived

## What synchronization do we need?

1. First of all, we need to keep track of how many customers there are wainting.. for that we need a shared counter, that is kept under a integrity safe lock by a `customer Mutex`

2. Secondly we need to wait for customer to arrive so that a barber can start working. In parallel programming we can achieve this by waiting in `barber` thread for `customer` thread to send a signal and wake up. Vice versa in `customer` thread we need to wait for `barber` to get to barber shop and signalize that he is ready to cut hair. For this we need firt `rendezvous` -- arrive rendezvous consisted of two Semaphores.

3. Thirdly we need to ensure that cutting hair and receiving a hair cut executes 1:1 (one to one), and finishes in the same time. For that we need second `rendezvous` -- done rendezvous consisted of two Semaphores.

## Problem of overrunning customers

With first implementation of `customer` function in [barbershopoverrun](barbershopoverrun.py):

```python
customer():
    mutex.lock()
        if count_customer == N:
            balk()
        customers += 1
    mutex.unlock()

    customer_arrived.signal()
    barber_arrived.wait()

    getHairCut()

    customer_done.signal()
    barber_done.wait()

    mutex.lock()
        customers -= 1
    mutex.unlock()
```

```python
barber():
    barber_arrived.signal()
    customer_arrived.wait()

    cutHair()

    barber_done.signal()
    customer_done.wait()
```

In this pseudocode we introduced problem -- overruning customers. Where when the fastest customer thread gets to `barber.wait()` call wins and gets a haircut notwithstanding its order in the waiting room. We can fix this by introducing FIFO queue stack of barber semaphores, where customer who comes into waiting room puts a ticket to barber and gets into queue. When barber finishes cutting hair, we gets a ticket form the queue and calls the next customer.

Pseudocode looks like this:

```python
customer():
    customer_mutex.lock()
        if count_customer == N:
            balk()
        customers += 1
    customer_mutex.unlock()

    barber_arrived = Semaphore(0)
    barber_queue.put(barber_arrived)
    customer_arrived.signal()
    barber_arrived.wait()

    getHairCut()

    customer_done.signal()
    barber_done.wait()

    customer_mutex.lock()
        customers -= 1
    customer_mutex.unlock()
```

```python
barber():
    customer_arrived.wait()
    barber_mutex.lock()
        barber_arrived = barber_queue.get()
    barber_mutex.unlock()
    barber_arrived.signal()

    cutHair()

    barber_done.signal()
    customer_done.wait()
```
