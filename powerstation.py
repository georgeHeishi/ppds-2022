'''
This script implements solution to Nuclear power plant where monitors read information that is written.
Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''
from random import randint
from time import sleep
from fei.ppds import Thread, Event, Semaphore, print
from lightswitch import Lightswitch

__author__ = "Juraj Lapcak, Matus Jokay"


def monitor(monitor_id):
    '''
    Monitor loop where monitors first wait for signal from sensors that data is available.
    Then monitors update every 500ms and read data from Access Data.

    Parameters:
        monitor_id -- id of monitor that is reading data
    Returns:
        None
    '''

    validData.wait()

    while True:
        # monitor má prestávku 500 ms od zapnutia alebo poslednej aktualizácie
        sleep(500 / 1000)

        # disable turnstile
        turnstile.wait()

        # lock Acess Data
        read_sensors_count = ls_monitor.lock(accessData)
        turnstile.signal()

        print(
            f'monitor: {monitor_id}: read monitors count: {read_sensors_count}')
        # data accessed, unlock Access Data
        ls_monitor.unlock(accessData)


def sensor(sensor_id):
    '''
    Sensor loop where sensors write data and signal to monitors that data is available. 
    Writing data is simulated by waiting 10-15 ms.

    Parameters:
        monitor_id -- id of monitor that is reading data
    Returns:
        None
    '''

    while True:
        # sensor moves through turnstile
        turnstile.wait()
        turnstile.signal()

        # lock access to accessData
        write_sensors_count = ls_sensor.lock(accessData)

        # writing data simulated by waiting 10-15 ms
        # inform abou sensor doing writing and accessed data
        write_time = randint(0, 5) + 10

        print(
            f'sensor: {sensor_id}: write sensors count: {write_sensors_count}, write time: {write_time} ms')
        sleep(write_time / 1000)

        # signalize written data
        validData.signal()

        # data accessed, unlock Access Data
        ls_sensor.unlock(accessData)


accessData = Semaphore(1)
turnstile = Semaphore(1)
ls_monitor = Lightswitch()
ls_sensor = Lightswitch()
validData = Event()

monitors = [Thread(monitor, monitor_id) for monitor_id in range(2)]
sensors = [Thread(sensor, sensor_id) for sensor_id in range(11)]

[m.join() for m in monitors]
[s.join() for s in sensors]
