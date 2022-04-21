# PPDS 2022 - Juraj Lapčák

[![Python](https://img.shields.io/badge/python-blue.svg)](https://www.python.org/downloads/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)
[PPDS](https://uim.fei.stuba.sk/predmet/i-ppds/)

## About

We implemented two versions of application: synchornous and asynchronous. The application compares words, from text file, with dictionary, from text file, with correct words that can be later used for correction of theoretically incorrect text.

First implemetation [substringanalysis.py](substringanalysis.py) is programmed synchronousely. Since dictionary contains lots of word and text can be of any lengt, the time needed to compare each word form text_input with every word from dictionary is `m * n` where `m` is length of text_input and `n`.

Second implementation [substringanalysisasync.py](substringanalysisasync.py) is meant to speed up splitting the tasks of comparing words from text_input and dictionary into multiple asynchronous tasks.

## Synchronous implementation

The synchronous program on average takes around 20 seconds to complete comparisons.

```
Starting!

Exectution time: 20.595824699965306
[('the', 3), ('quick', 5), ('brown', 5), ('fox', 3), ('jumps', 5), ('over', 4), ('the', 3), ('lazy', 4), ('dog', 3)]
```

## Asynchronouse implementation

By splitting the text of `m` words into `m` tasks we managed to speed up the analysis by 3 seconds, where every task is in control of analysing his own word from text.

```
Starting!
Task 1 analysing the
Task 2 analysing quick
Task 3 analysing brown
Task 4 analysing fox
Task 5 analysing jumps
Task 6 analysing over
Task 7 analysing the
Task 8 analysing lazy
Task 9 analysing dog
Task 1 finished
Task 3 finished
Task 6 finished
Task 2 finished
Task 5 finished
Task 4 finished
Task 7 finished
Task 9 finished
Task 8 finished

Exectution time: 17.280191799975
[('the', 3), ('brown', 5), ('over', 4), ('quick', 5), ('jumps', 5), ('fox', 3), ('the', 3), ('dog', 3), ('lazy', 4)]
```
