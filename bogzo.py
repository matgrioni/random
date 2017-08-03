#!/usr/bin/env python

import argparse
import math
import random
import time

import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    # Mandatory arguments.
    parser.add_argument('down',     type=int, help='The lower limit for n for the comparisons')
    parser.add_argument('up',       type=int, help='The upper limit for n for the comparisons')
    parser.add_argument('attempts', type=int, help='The number of times to run sorts for a given n')

    # Optional arguments to choose which type of analysis you want.
    parser.add_argument('--hist', help='Provide a histogram analysis for each n from down to up', action='store_true')
    parser.add_argument('--avg',  help='Provide an analysis of the average for each n from down to up', action='store_true')
    parser.add_argument('--time', help='Provide an analysis of the time for each approach.', action='store_true')
    args = parser.parse_args()

    bogo_results = {}
    bozo_results = {}

    for n in xrange(args.down, args.up + 1):
        items = range(n)
        for attempt in xrange(args.attempts):
            random.shuffle(items)

            copy1 = items[:]
            copy2 = items[:]

            iters, time = bogo(copy1)
            try:
                bogo_results[n].append(iters)
            except KeyError:
                bogo_results[n] = [iters]

            iters, time = bozo(copy2)
            try:
                bozo_results[n].append(iters)
            except KeyError:
                bozo_results[n] = [iters]


    if args.hist:
        for n in range(args.down, args.up + 1):
            plt.hist(bogo_results[n], bins=25, alpha=0.5, label='bogo')
            plt.hist(bozo_results[n], bins=25, alpha=0.5, label='bozo')
            plt.legend(loc='upper right')
            plt.title('Bogo vs Bozo for n={}'.format(n))
            plt.show()

    if args.avg:
        diff = args.up - args.down + 1

        ns = range(args.down, args.up + 1)
        bogo_avgs = [0] * diff
        bozo_avgs = [0] * diff
        for n, results in bogo_results.items():
            bogo_avgs[n - args.down] = sum(results) / float(len(results))

        for n, results in bozo_results.items():
            bozo_avgs[n - args.down] = sum(results) / float(len(results))

        plt.plot(ns, bogo_avgs, label='bogo')
        plt.plot(ns, bozo_avgs, label='bozo')
        plt.yscale('log')
        plt.legend(loc='upper right')
        plt.title('Bogo vs Bozo for all n')
        plt.show()


def timeit(method):
    """
    Decorator to time a provided method. The result of the method and the time
    will be provided as a tuple, where the first element is the method result
    and the second result is the time it took to run the method in seconds.

    Returns:
        type((object, float)): The result of the method and the time to run it.
    """
    def timed(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()

        return (result, start - end)

    return timed


@timeit
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


@timeit
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
