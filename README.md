# Assignment 05

[![Python 3.10.2](https://img.shields.io/badge/python-3.10.2-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[PPDS](https://uim.fei.stuba.sk/predmet/i-ppds/)

## Second modification of Dinning Savages problem

Problem is based on producing and consuming of goods, now actually servings of unfortunate missionary who fell into a trap of savaga clan somewhere in undisclosed location.

Savages try to take from pot, where there should be served food. If savage cannot find a serving in pot he signalizes to cooks that he is hungry. Then he waits for cooks to finish their cooking and eats his serving. These operations repeat infinitely between N savages who share M servings of missionary.

C number Cooks serve and put M servings into a pot. Their individual work is facilitated by a fact that they help each other in cooking M servings. Meaning everyone cooks 1 portion and puts it in the pot. After all cooks finished cooking they signalize to savages that pot is full.

```python
def init():
    eatMutex := Mutex()

    cookMutex := Mutex()
    cooksDone := 0

    servingMutex := Mutex()
    servings := 0

    fullPot := Semaphore(0)
    # multiplex for C cooks
    emptyPot := Semaphore(C)

    # barrier of N savages
    barrier1 := SimpleBarrier(N)
    barrier2 := SimpleBarrier(N)

    for savage_id in [0, 1, 2, ..., N-1]:
        create_and_run_thread(savage, savage_id)
    for cook_id in [0, 1, ..., C-1]:
        create_and_run_thread(cook, cook_id)

def getServingFromPot(savage_id):
    print("savage %2d: retreiving portion" % savage_id)
    servings := servings - 1

def savage(savage_id):
    while True:
        barrier1.wait("savage %2d: I have arrived, we are %2d",
                      savage_id,
                      print_each_thread = True)
        barrier2.wait("savage %2d: we have arrived, beginning feast",
                      savage_id,
                      print_last_thread = True)

        eatMutex.lock()
        print("savage %2d: remaining portions: %2d" % (savage_id, servings))
        if servings == 0:
            print("savage %2d: waking up cooks" % savage_id)
            emptyPot.signal()
            fullPot.wait()
        getServingFromPot(savage_id)
        eatMutex.unlock()

        print("savage %2d: feasting" % savage_id)

def putServingsInPot(cook_id):
    while True:
        servingMutex.lock()

            # M is number of servings
            if servings == M:
                servingMutex.unlock()
                break

            servings := servings + 1
            print("cook %2d: cooking, %2d serving cooked" %
                (cook_id, servings))
        servingMutex.unlock()

def cook(cook_id):
    while True:
        emptyPot.wait()
        putServingsInPot(cook_id)

        cookMutex.lock()
            cooksDone := cooksDone + 1
            if shared.cooksDone == C:
                cooksDone = 0
                full_pot.signal()
            print("cook %2d: is unlocking %2d" % (cook_id, cooksDone))

        shared.cookMutex.unlock()
```

Modification of solution of Dinning Savages 1:
1. We shortened individual cooking time 10-times -- because cooking of one serving takes shorter than cooking M portions.

2. Into function `put_servings_in_pot` we added a cycle in which putting a cooked serving into pot is protected by Mutex lock.

3. We added another integrity Mutex lock into a `cook` function, after putting a serving into pot by a cook of `cook_id`, protecting counter of all cooks who finished cooking and putting a serving into pot. This way we can count who was cooking and who finished cooking.