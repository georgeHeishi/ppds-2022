# Assignment 04

[![Python 3.10.2](https://img.shields.io/badge/python-3.10.2-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[PPDS](https://uim.fei.stuba.sk/predmet/i-ppds/)

## Analysis and Mapping

Task is split into two categories of processess. First category are sensors that simulate writing of data. Second category are monitors that monitor written data from sensors.

Three sensors that write data independent on each other:

1. Sensor P (id = 0) -- writes data in 10-20 ms
2. Sensor T (id = 1) -- writes data in 10-20 ms
3. Sensor H (id = 2) -- writes data in 20-25 ms

Eight monitors that read data in updates every 40-50 ms independent on each other.

Monitors cannot start their work until all sensors have written data into Access Data. This is different from previous task.. and we need to use different synchronization pattern object. For this reason we used SimpleBarrier ADC, which wait is called only when sensors are initializing. After all 3 sensors have written it's data `bar_needed` is set to false and paralel execution may resume.

We discussed problem of initial writing sensor data. This problem is connected with signaling monitors that they can start reading data. For that we used an Event for letting know that data is valid. Of course we needed to ensure that when reading a value no sensor writes at that moment and current value is not incorrect. For that reason we used Turnstile. And last synchronization problem is ensuring integrity with lightswitch of `accessData` in which is 'data' stored.

## Pseudocode

```python

def init():
    accessData = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    validData = Event()
    barrier = SimpleBarrier(3)

    for monitor_id in <0, 7>:
        create_and_run_thread(monitor, monitor_id)
    for sensor_id in <0, 2>:
        create_and_run_thread(cidlo, sensor_id)

def monitor(monitor_id):
    validData.wait()

    while True:
        # Watch for update every 40-50 ms
        update_from_last = random(<40ms, 50ms>)
        sleep(update_from_last)

        # disable turnstile
        turnstile.wait()
            # lock Acess Data
            read_sensors_count = ls_monitor(accessData).lock()
        turnstile.signal()

        print('monitor: {monitor_id}: read monitors count: {read_sensors_count}')
        # lock access to accessData
        ls_monitor.unlock(accessData)


def sensor(sensor_id):
    while True:
        # Sensors make and update every 50-60 ms.
        update_from_last = random(<50ms, 60ms>)
        sleep(update_from_last)

        # sensor moves through turnstile
        turnstile.wait()
        turnstile.signal()

        # lock access to accessData
        write_sensors_count = ls_sensor(accessData).lock()

            # Write update is done for sensor P and T (sensor_id = 0, 1) in 10-20 ms
            # for sensor H (sensor_id = 2) in 20-25 ms.
            if sensor_id is equal to 2:
                write_time = random(<20ms, 25ms>)
            else:
                write_time = random(<10ms, 20ms>)

            print('sensor: {sensor_id}: write sensors count: {write_sensors_count}, write time: {write_time} ms')
            sleep(write_time)

            if Initialization first writing not done:
                barrier.wait()

            # signalize that initialization for sensor is done and monitor can read
            validData.signal()
            # lock access to accessData
        ls_sensor(accessData).unlock()
```
