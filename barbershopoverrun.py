'''
This file implemets solution to barbershop problem with random overrun of customers.

This script requires module `fei.ppds` installed withing Python environment.

This file contains following class: 
    Barbershop

This file contains following functions: 
    cutHair
    getHairCut
    balk
    barber
    customer

Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''
from fei.ppds import Thread, Mutex, Semaphore, print
from random import randint
from time import sleep

__author__ = 'Juraj Lapčák, Matúš Jokay'

BARBERS = 1
CUSTOMERS = 3

__author__ = 'Juraj Lapčák, Matúš Jokay'


class Barbershop:
    '''
    Barbershop class 

    Atributes:
        b_arrived - Semaphore event needed for rendezvous when waiting for getting into barbershop
        c_arrived - Semaphore event needed for rendezvous when waiting for getting into barbershop
        b_done - Semaphore event needed for rendezvous when waiting for leaving
        c_done - Semaphore event needed for rendezvous when waiting for leaving
        mutex - Mutex lock needed for keeping integrity of customers counter
        customers - customers counter
    '''

    def __init__(self):
        '''
        Initialize Barbershop object:

        Parameters: 
            None
        '''
        self.b_arrived = Semaphore(0)
        self.c_arrived = Semaphore(0)

        self.b_done = Semaphore(0)
        self.c_done = Semaphore(0)

        self.mutex = Mutex()
        self.customers = 0


def cutHair(id: int):
    '''
    Parameters: 
        id - id of barber cutting hair
    '''
    print(f'barber: {id} cutting hair')
    sleep(randint(0, 10) / 100)


def getHairCut(id: int):
    '''
    Parameters: 
        id - id of customer getting haircut
    '''
    print(f'customer: {id} getting haircut')
    sleep(randint(0, 10) / 100)


def balk(id: int):
    '''
    Parameters: 
        id - id of customer walking out
    '''
    print(f'customer: {id} leaving')


def barber(barber_id: int, barbershop: Barbershop):
    '''
    Simulates cycle of barber waiting for customers to walk into barbeshop and 
    cutting their hair in parallel of customer getting a haircut.

    Parameters: 
        barber_id - id of barber cutting hair
        barbershop - Barbershop object
    '''
    while True:
        # rendezvous - wait for customer to enter barbershop
        barbershop.b_arrived.signal()
        barbershop.c_arrived.wait()

        cutHair(barber_id)

        # rendezvous - wait for customer to get up from getting a cut
        barbershop.b_done.signal()
        barbershop.c_done.wait()
        print(f'barber: {barber_id} haircut finished')


def customer(customer_id: int, barbershop: Barbershop):
    '''
    Simulates cycle of customer waiting in to get his haircut without queue.
    Meaning which customer is faster in getting up from rendezvous, that is getting a haircut.

    Parameters: 
        customer_id - id of customer cutting hair
        barbershop - Barbershop object
    '''
    while True:
        sleep(randint(0, 10) / 100)
        barbershop.mutex.lock()
        print(
            f'customer: {customer_id} entered there are {barbershop.customers}/{CUSTOMERS} customers')
        if barbershop.customers == CUSTOMERS:
            balk(customer_id)
            barbershop.mutex.unlock()
            continue

        barbershop.customers += 1
        barbershop.mutex.unlock()

        # rendezvous - wait for barber to get ready to cut next customer
        barbershop.c_arrived.signal()
        barbershop.b_arrived.wait()

        getHairCut(customer_id)

        # rendezvous - wait for barber to finish cutting
        barbershop.c_done.signal()
        barbershop.b_done.wait()
        print(f'customer: {customer_id} haircut finished')

        barbershop.mutex.lock()
        barbershop.customers -= 1
        barbershop.mutex.unlock()


if __name__ == "__main__":
    barbershop = Barbershop()
    b = [Thread(barber, barber_id, barbershop) for barber_id in range(BARBERS)]
    c = [Thread(customer, customer_id, barbershop)
         for customer_id in range(CUSTOMERS + 2)]

    for t in b+c:
        t.join()
