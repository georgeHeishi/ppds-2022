'''
This script implements Producer-Consumer relation in paralel execution.

This file also tests parameters of Producer-Consumer problem for optimal settings.
'''

from multiprocessing import Semaphore
from time import sleep
from fei.ppds import Thread, Mutex, Semaphore

import matplotlib.pyplot as plt


class Shared:
    """
    Shared Mutex, shared N-mutex Semaphore, and Event

    Parameters:
    shared -- initialized shared object, shared between produceer and consumer

    Returns:
    None
    """

    def __init__(self, n):
        """
        Initializes attributes for Shared object.

        Parameters:
        self
        n -- size of storage
        """

        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(n)
        self.items = Semaphore(0)
        self.count_produced = 0
        self.count_consumed = 0


def produce(shared, process_time, production_time):
    """
    Simulate production of new item, which is moved into storage, where it can be retrieved by consumer.

    Parameters:
    shared -- initialized shared object, shared between produceer and consumer

    Returns:
    None
    """

    while True:
        # simulate production (longer than saving)
        sleep(production_time)

        # check free storage space
        shared.free.wait()

        if(shared.finished):
            break

        # lock storage access
        shared.mutex.lock()

        # simulate storing in storage
        shared.count_produced += 1

        # unlock storage access (leave storage)
        shared.mutex.unlock()

        # signal new item in storage
        shared.items.signal()


def consume(shared, process_time):
    """
    Simulate consuming of an item, which is being taken from storage and used.

    Parameters:
    shared -- initialized shared object, shared between produceer and consumer

    Returns:
    None
    """

    while True:
        # wait for items to be in storage
        shared.items.wait()

        if(shared.finished):
            break

        # lock storage access
        shared.mutex.lock()

        # simulate taking item from storage
        shared.count_consumed += 1

        # unlock storage access (leave storage)
        shared.mutex.unlock()

        # signalize new item to be produced
        shared.free.signal()

        # process item
        sleep(process_time)


def show_plot(results_produced, results_consumed):
    """
    Show two matplotlib subplots where left one is data produced and right one is data consumed.

    Parameters:
    results_produced -- triple of produced data
    results_consumed -- triple of consumed data

    Returns:
    None
    """

    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    x = [a[0] for a in results_produced]
    y = [a[1] for a in results_produced]
    z = [a[2] for a in results_produced]
    ax.set_xlabel('Production time (s)')
    ax.set_ylabel('Storage capacity')
    ax.set_zlabel('Number of products produced per second (s)')
    ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    x = [a[0] for a in results_consumed]
    y = [a[1] for a in results_consumed]
    z = [a[2] for a in results_consumed]
    ax.set_xlabel('Production time (s)')
    ax.set_ylabel('Storage capacity')
    ax.set_zlabel('Number of products consumed per second (s)')
    ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

    plt.show()


production_time_params = [0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.1]
process_time_params = [0.001, 0.002, 0.004, 0.006, 0.008]
consumers_params = [2, 4, 6, 8, 10]
producents_params = [2, 4, 6, 8, 10]
storage_capacity_params = [5, 10, 15, 20]

results_produced = []
results_consumed = []

inte = 0
interations = len(production_time_params) * len(consumers_params) * 10
print('0%')

for p_t in production_time_params:
    for s_c in storage_capacity_params:
        count_produced_sum = 0
        count_consumed_sum = 0
        for i in range(10):
            s = Shared(s_c)
            consumers = [Thread(consume, s, 0.004)
                         for _ in range(4)]
            producers = [Thread(produce, s, 0.004, p_t)
                         for _ in range(8)]

            sleep_time = 0.05
            sleep(sleep_time)
            s.finished = True

            s.items.signal(100)
            s.free.signal(100)
            [t.join() for t in consumers+producers]

            count_produced_sum += s.count_produced / sleep_time
            count_consumed_sum += s.count_consumed / sleep_time

            inte = inte+1
            print(str((inte / interations) * 100) + '%')
        average_produced = count_produced_sum / 10
        average_consumed = count_consumed_sum / 10

        results_produced.append((p_t, s_c, average_produced))
        results_consumed.append((p_t, s_c, average_consumed))


show_plot(results_produced, results_consumed)
