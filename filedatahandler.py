'''
This file implements writing and reading list and or set to file.
File also contains functions that can be imported:
    prepare_text_data
    prepare_dictionary
    print_list_to_file

Author: Juraj Lapčák    
'''


import unicodedata

__author__ = 'Juraj Lapčák'


def prepare_text_data(data_path: str):
    '''
    Read data from data_path file to list and return in.

    Parameters:
        data_path - string, path to data-file
    Returns:
        data_from_file - list of stripped words
    '''

    data_from_file = list()

    with open(data_path, 'r', encoding='cp1251') as f:
        for line in f:
            split_line = line.split()
            split_line = [unicodedata.normalize('NFD', (word.strip()).lower()).encode(
                'ascii', 'ignore').decode("utf-8") for word in split_line]
            data_from_file.extend(split_line)

    return data_from_file


def prepare_dictionary(data_path: str):
    '''
    Read data from data_path file to set and return in.

    Parameters:
        data_path - string, path to data-file
    Returns:
        data_from_file - set of stripped words
    '''

    data_from_file = set()

    with open(data_path, 'r', encoding='cp1251') as f:
        for line in f:
            split_line = line.split()
            split_line = [unicodedata.normalize('NFD', (word.strip()).lower()).encode(
                'ascii', 'ignore').decode("utf-8") for word in split_line]
            data_from_file.update(split_line)

    return data_from_file


def print_list_to_file(data_path: str, list_to_print: list):
    '''
    Write data from list file to data_path file.

    Parameters:
        data_path - string, path to data-file
    Returns:
        None
    '''

    with open(data_path, 'w') as f:
        f.writelines(' '.join(str(line) for line in list_to_print))
