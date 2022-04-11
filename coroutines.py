'''
This file implemets coroutines of simulated battle between monster and knight.

This file contains following classes: 
    colors
    Scheduler
This file contains following functions: 
    gen_turn
    attack
    knight_turn
    monster_turn
Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''

from random import randint

__author__ = 'Juraj Lapčák, Matúš Jokay'


# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal-in-python
class colors:
    DEFAULT = '\33[0m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'


class Scheduler():
    '''
    Scheduler class

    Atributes:
        tasks - list of task to run in order
    '''

    def __init__(self):
        '''
        Initialize Barbershop object:

        Parameters:
            None
        '''
        self.tasks = list()

    def append_task(self, task):
        '''
        Add a task into task list.

        Parameters:
            task - task to be added into the list

        Returns:
            None
        '''
        next(task)
        self.tasks.append(task)

    def run_tasks(self):
        '''
        Run all tasks in tasks list.

        Parameters:
            None

        Returns:
            None
        '''
        ret_value = 0
        while True:
            try:
                task = self.tasks.pop(0)
                ret_value = task.send(ret_value)
                self.tasks.append(task)
            except StopIteration:
                for t in self.tasks:
                    t.close()
                break


def gen_turn(scheduler: Scheduler):
    '''
    Generate order in which Coroutines will be run.

    Parameters:
        scheduler- initialized Scheduler object

    Returns:
        None        
    '''
    # generate radnom 0 or 1
    # 0 - knight starts
    # 1 - monster starts
    turn = randint(0, 1)

    if(turn):
        scheduler.append_task(knight_turn())
        scheduler.append_task(attack())
        scheduler.append_task(monster_turn())
        scheduler.append_task(attack())
    else:
        scheduler.append_task(monster_turn())
        scheduler.append_task(attack())
        scheduler.append_task(knight_turn())
        scheduler.append_task(attack())

    scheduler.run_tasks()


def attack():
    '''
    Attack Coroutine. 
    Generates number in range <1, 10> and passes it to next coroutine. 
    From which it waits for remaining health and name of unit that used its number for attacking.

    Parameters:
        None  

    Returns:
        None 

    Yields:
        dmg - number (damage)
    '''

    while True:
        try:
            dmg = randint(1, 10)
            remaining_hp, unit_name = (yield dmg)
            print(colors.DEFAULT +
                  f'\n{unit_name} Remaining health: {remaining_hp}')

        except GeneratorExit:
            break


def knight_turn():
    '''
    Knight Coroutine.
    Waits for Damage number uses it for attacking an enemy and checks if enemy's health
    is not <= 0. In whick cases it breaks iteration.

    Parameters:
        None  

    Returns:
        None 

    Yields:
        monster_hp - number (remaining healtg of monster)
        unit_name - 'Knight' string
    '''

    monster_hp = 100
    while True:
        try:
            dmg = (yield (monster_hp, 'Knight'))

            print(colors.RED + f'Knight attacking for {dmg} points')

            monster_hp -= dmg

            if(monster_hp <= 0):
                break

        except GeneratorExit:
            print(colors.YELLOW + f'\nKnight has been defeated')

            print(colors.GREEN + f'Remaining health of Monster: {monster_hp}')
            break


def monster_turn():
    '''
    Monster Coroutine.
    Waits for Damage number uses it for attacking an enemy and checks if enemy's health
    is not <= 0. In whick cases it breaks iteration.

    Parameters:
        None  

    Returns:
        None 

    Yields:
        knight_hp - number (remaining healtg of knight)
        unit_name - 'Monster' string
    '''

    knight_hp = 100
    while True:
        try:
            dmg = (yield (knight_hp, 'Monster'))

            print(colors.RED + f'Monster attacking for {dmg} points')

            knight_hp -= dmg

            if(knight_hp <= 0):
                break

        except GeneratorExit:
            print(colors.YELLOW + f'\nMonster has been slain')

            print(colors.GREEN + f'Remaining health of Knight: {knight_hp}')
            break


if __name__ == "__main__":
    scheduler = Scheduler()
    gen_turn(scheduler)
