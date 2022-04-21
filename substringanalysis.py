'''
This file implements functions that test longest common substring of words
from input.txt file by words from dictionary and writes them into vystup.txt
file.

Functions:
   get_lcsubstring 
   main

Done with help and instructions from our lovely teacher and supervisor Matus Jokay at STU FEI.
'''

import time
from filedatahandler import prepare_dictionary, prepare_text_data, print_list_to_file

__author__ = 'Juraj Lapčák, Matúš Jokay'


def get_lcsubstring(x, y, m, n):
    '''
    Dynamic programming implementation of longest common substring algoritm by Soumen Ghosh
        - https://www.geeksforgeeks.org/longest-common-substring-dp-29/

    Parameters:
        x - str (sequence of characters), word x
        y - str (sequence of characters), word y
        m - length of x
        n - length of y
        
    Returns:
        substring_length - length of substring between x and y
    '''

    LCS_table = [[0 for k in range(n+1)] for l in range(m+1)]

    substring_length = 0

    for i in range(m + 1):
        for j in range(n + 1):
            if (i == 0 or j == 0):
                LCS_table[i][j] = 0
            elif (x[i-1] == y[j-1]):
                LCS_table[i][j] = LCS_table[i-1][j-1] + 1
                substring_length = max(substring_length, LCS_table[i][j])
            else:
                LCS_table[i][j] = 0
    return substring_length


def main():
    '''
    Main prepares dictionary and text input data and runs substring analysis for
    every word. Also writes results into output.txt.
    '''
    dictionary = prepare_dictionary('dictionary.txt')
    text_input = prepare_text_data('input.txt')

    longest_substring_lens = []

    print(f'\nStarting!')
    start = time.perf_counter()

    for word in text_input:
        longest_substring = 0
        for dict_word in dictionary:
            current_substring = get_lcsubstring(
                word, dict_word, len(word), len(dict_word))
            current_substring = get_lcsubstring(
                word, dict_word, len(word), len(dict_word))
            if current_substring > longest_substring:
                longest_substring_lens.append((word, longest_substring))

    duration = time.perf_counter() - start

    print(f'\nExectution time: {duration}')
    print(longest_substring_lens)
    print_list_to_file('output.txt', longest_substring_lens)


if __name__ == "__main__":
    main()
