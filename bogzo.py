#!/usr/bin/env python

import argparse
import math
import random

import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('down',     type=int, help='The lower limit for n for the comparisons')
    parser.add_argument('up',       type=int, help='The upper limit for n for the comparisons')
    parser.add_argument('attempts', type=int, help='The number of times to run sorts for a given n')
    args = parser.parse_args()

    bogo_results = {}
    bozo_results = {}

    for n in xrange(args.down, args.up + 1):
        items = range(n)
        for attempt in xrange(args.attempts):
            random.shuffle(items)

            copy1 = items[:]
            copy2 = items[:]

            bogo_iters = bogo(copy1)
            try:
                bogo_results[n].append(bogo_iters)
            except KeyError:
                bogo_results[n] = [bogo_iters]

            bozo_iters = bozo(copy2)
            try:
                bozo_results[n].append(bozo_iters)
            except KeyError:
                bozo_results[n] = [bozo_iters]


    for n in xrange(args.down, args.up + 1):
        plt.hist(bogo_results[n], bins=25, alpha=0.5, label='bogo')
        plt.hist(bozo_results[n], bins=25, alpha=0.5, label='bozo')
        plt.legend(loc='upper right')
        plt.title('Bogo vs Bozo for n={}'.format(n))
        plt.show()

def bogo(items):
    """
    Performs a bogo sort (random permutation) on the given items and returns how
    many permutations it took to do so.

    Args:
        items, type(list(int)): The items to sort.

    Returns:
        The number of permutations needed until sorted.
    """
    iters = 0
    while not is_sorted(items):
        random.shuffle(items)
        iters += 1

    return iters


def bozo(items):
    """
    Performs a bozo sort on the given items and returns the number of swaps
    until sorted.

    Args:
        items, type(list(int)): The items to sort.

    Returns:
        The number of swaps needed until sorted.
    """
    iters = 0

    idxs = range(len(items))
    while not is_sorted(items):
        idx1, idx2 = random.sample(idxs, 2)

        tmp = items[idx1]
        items[idx1] = items[idx2]
        items[idx2] = tmp

        iters += 1

    return iters


def is_sorted(items):
    """
    Returns whether a list is sorted or not.

    Args:
        items, type(list(int)): The items to check for sortedness.

    Returns:
        True if the list is sorted in ascending order. False otherwise.
    """
    good = True
    last = -float('inf')
    for i in items:
        if i <= last:
            good = False
            break

        last = i

    return good


if __name__ == '__main__':
    main()
