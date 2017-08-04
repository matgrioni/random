#!/usr/bin/env python

import argparse
import collections
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

    bogo_results = new_results_store()
    bozo_results = new_results_store()

    for n in xrange(args.down, args.up + 1):
        items = range(n)
        for attempt in xrange(args.attempts):
            random.shuffle(items)

            copy1 = items[:]
            copy2 = items[:]

            iters, time = bogo(copy1)
            bogo_results[n]['iters'].append(iters)
            bogo_results[n]['times'].append(time)

            iters, time = bozo(copy2)
            bozo_results[n]['iters'].append(iters)
            bozo_results[n]['times'].append(time)


    if args.hist:
        for n in range(args.down, args.up + 1):
            plt.hist(bogo_results[n], bins=25, alpha=0.5, label='bogo')
            plt.hist(bozo_results[n], bins=25, alpha=0.5, label='bozo')
            plt.legend(loc='upper right')
            plt.title('Bogo vs Bozo for n={}'.format(n))
            plt.show()

    if args.avg:
        ns = range(args.down, args.up + 1)
        bogo_avgs = average_metric(bogo_results, 'iters')
        bogo_ys = continuous_keys_to_list(bogo_avgs, args.down, args.up)

        bozo_avgs = average_metric(bozo_results, 'iters')
        bozo_ys = continuous_keys_to_list(bozo_avgs, args.down, args.up)

        plt.plot(ns, bogo_ys, label='bogo')
        plt.plot(ns, bozo_ys, label='bozo')
        plt.yscale('log')
        plt.legend(loc='upper right')
        plt.title('Bogo vs Bozo iters for all n')
        plt.show()

    if args.time:
        ns = range(args.down, args.up + 1)
        bogo_avgs = average_metric(bogo_results, 'times')
        bogo_ys = continuous_keys_to_list(bogo_avgs, args.down, args.up)

        bozo_avgs = average_metric(bozo_results, 'times')
        bozo_ys = continuous_keys_to_list(bozo_avgs, args.down, args.up)

        plt.plot(ns, bogo_ys, label='bogo')
        plt.plot(ns, bozo_ys, label='bozo')
        plt.yscale('log')
        plt.legend(loc='upper right')
        plt.title('Bogo vs Bozo time for all n')
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

        return (result, end - start)

    return timed


def new_results_store():
    """
    Create a new dictionary to store the results of the two sort. The structure
    of the store is designed so that on the first level, the key is the n for
    which the simulations were run. The value is then a dict whose key is the
    type of metric and the value is a list of the values of this metric for each
    run of the sort.

    Returns:
        type(dict): A mutlilayered defaultdict so no annoying nested exceptions.
    """
    return collections.defaultdict(lambda: collections.defaultdict(list))


def average_metric(results, metric):
    """
    Given a results dictionary as created in new_results_store, return the
    average for a given metric name.

    Args:
        results, type(dict): The results store.
        metric, type(string): The name of the metric.

    Returns:
        type(dict): An average for the desired metric from the results for each
                    available n.
    """
    avgs = {}
    for n, simulations in results.items():
        metrics = simulations[metric]
        avgs[n] = sum(metrics) / float(len(metrics))

    return avgs


def continuous_keys_to_list(d, down, up):
    """
    Converts a dictionary with integer keys that are continuously increasing, eg
    1, 2, 3, 4..., into a list in increasing order. The list is 0 based no matter
    the dictionary keys but it keeps the order and starts from down and ends at
    up.

    Args:
        d, type(dict): The dictionary to convert into a list.
        down, type(int): The starting key value.
        up, type(int): The ending key value.

    Returns:
        type(list): A list corresponding to the values for the keys from
                    [down, up] in ascending key order.
    """
    diff = up - down + 1
    ys = [0] * diff
    for i in xrange(down, up + 1):
        ys[i - down] = d[i]

    return ys


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
