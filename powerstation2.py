'''
Author: Juraj Lapcak

Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''
from random import randint
from time import sleep
from fei.ppds import Thread, Event, Semaphore, print
from lightswitch import Lightswitch
from simplebarrier import SimpleBarrier

__author__ = "Juraj Lapcak, Matus Jokay"


class InitBarrier:
    '''
    InitBarrier class.

    Attributes:
        n -- number of threads to block with barrier
        bar_needed -- boolean that tells if InitBarrier is needed
    Methods:
        wait() -- representation of barrier's turnstile
        signalize() -- set needed to not needed
    '''

    def __init__(self, n):
        '''
        Initializes attributes for InitBarrier object.

        Parameters:
            n -- number of threads the barrier blocks
        '''

        self.barrier = SimpleBarrier(n)
        self.bar_needed = True

    def wait(self):
        '''
        Lock's thread until all threads completed turnstile.

        Parameters:
            None
        Returns:
            None
        '''

        if(self.bar_needed == True):
            self.barrier.wait()

    def signalize(self):
        '''
        Signalize that barrier is not needed.

        Parameters:
            None
        Returns:
            None
        '''

        self.bar_needed = False


def monitor(monitor_id):
    '''
    Monitor loop where monitors first wait for signal from all sensors
    and then read accessData in infiniteloop.

    Parameters:
        monitor_id -- id of monitor that is reading data
    Returns:
        None
    '''

    validData.wait()

    while True:
        # Watch for update every 40-50 ms
        update_from_last = randint(0, 10) + 40
        sleep(update_from_last / 1000)

        # disable turnstile
        turnstile.wait()

        # lock Acess Data
        read_sensors_count = ls_monitor.lock(accessData)
        turnstile.signal()

        print(
            f'monitor: {monitor_id}: read monitors count: {read_sensors_count}')
        # lock access to accessData
        ls_monitor.unlock(accessData)


def sensor(sensor_id):
    '''
    Sensor loop where sensors write data and signal to monitors that data is available. 

    Parameters:
        monitor_id -- id of monitor that is reading data
    Returns:
        None
    '''

    while True:
        # Sensors make and update every 50-60 ms.
        update_from_last = randint(0, 10) + 50
        sleep(update_from_last / 1000)

        # sensor moves through turnstile
        turnstile.wait()
        turnstile.signal()

        # lock access to accessData
        write_sensors_count = ls_sensor.lock(accessData)

        # Write update is done for sensor P and T (sensor_id = 0, 1) in 10-20 ms
        # for sensor H (sensor_id = 2) in 20-25 ms.

        if(sensor_id == 2):
            write_time = randint(0, 5) + 20
        else:
            write_time = randint(0, 10) + 10

        print(
            f'sensor: {sensor_id}: write sensors count: {write_sensors_count}, write time: {write_time} ms')
        sleep(write_time / 1000)

        initBarrier.wait()
        initBarrier.signalize()
        # signalize that initialization for sensor is done and monitor can reawd
        validData.signal()
        # lock access to accessData
        ls_sensor.unlock(accessData)


N_SENSORS = 3

accessData = Semaphore(1)
turnstile = Semaphore(1)
ls_monitor = Lightswitch()
ls_sensor = Lightswitch()
validData = Event()
initBarrier = InitBarrier(N_SENSORS)

monitors = [Thread(monitor, monitor_id) for monitor_id in range(8)]
sensors = [Thread(sensor, sensor_id) for sensor_id in range(N_SENSORS)]

[m.join() for m in monitors]
[s.join() for s in sensors]
