#!/usr/bin/env python

import numpy as np

fmap = {
        'a': 0, 'b': 1, # A1
        'u': 0, 'y': 1, 'l': 2, 't': 3, # A4
        'g': 0, 'p': 1, 'gg': 2, # A5
        'c': 0, 'd': 1, 'cc': 2, # A6
        'i': 3, 'j': 4, 'k': 5, # A6
        'm': 6, 'r': 7, 'q': 8, # A6
        'w': 9, 'x': 10, 'e': 11, # A6
        'aa': 12, 'ff': 13, # A6
        'v': 0, 'h': 1, 'bb': 2, # A7
        'j': 3, 'n': 4, 'z': 5, # A7
        'dd': 6, 'ff': 7, 'o': 8, # A7
        't': 0, 'f': 1, # A9, A10, A12
        'g': 0, 'p': 1, 's': 2, # A13
        '+': 0, '-': 1 # class
       }

def map_feature(fvalue):
    if fvalue in fmap:
        return fmap[fvalue] # categorical
    if fvalue == '?':
        return -1 # missing value
    return float(fvalue) # continuous

"""
    A1: 0, 1 categorical
    A2: continuous
    A3: continuous
    A4: 0, 1, 2, 3 categorical
    A5: 0, 1, 2 categorical
    A6: 0 - 13 categorical
    A7: 0 - 8 categorical
    A8: continuous
    A9: 0, 1 categorical
    A10: 0, 1 categorical
    A11: continuous
    A12: 0, 1 categorical
    A13: 0, 1, 2 categorical
    A14: continuous
    A15: continuous
    C: 0, 1 class
"""
def read_data(filename):
    D = np.zeros((600, 16))
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            D[i,:] = np.array([map_feature(x)
                               for x in line.strip().split(',')])
            i += 1
    return D

def main():
    X = read_data('crx.data.txt')
    print X

if __name__ == "__main__":
    main()
