from collections import defaultdict
from pandas import Series, DataFrame
import itertools as it
import pandas as pd
import math
import csv
import sys
import argparse
import collections
import glob
import os
import re
import requests
import string
import sys

class Armin():

    def apriori(self, input_filename, output_filename, min_support_percentage, min_confidence):
        """
        Implement the Apriori algorithm, and write the result to an output file

        PARAMS
        ------
        input_filename: String, the name of the input file
        output_filename: String, the name of the output file
        min_support_percentage: float, minimum support percentage for an itemset
        min_confidence: float, minimum confidence for an association rule to be significant

        """

        items = set(())
        basket = []
        vfi = []
        support_index = []

        # Gather unique items and list transactions.
        # "Put the lotion in the basket" lol
        with open(input_filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
            for row in reader:
                r = ','.join(row).split(',')[1:]
                d = [i.strip() for i in r]
                r = {i.strip() for i in r}
                basket.append(d)
                items = items.union(r)
        items = list(items)
        items.sort()

        # Unique items
        for i in range(len(items) + 1):
            # Every combination of possible subsets
            combo = it.combinations(items, i + 1)

            # Unique items * length of subset
            for c in combo:
                c = set(c)
                count = 0
                # Number of transactions
                for a in basket:
                    a = set(a)
                    # Count+1 IF current combo/subset of uniques is in current transaction
                    if c.issubset(a):
                        count += 1

                # Sup!
                support = count / len(basket)

                if support >= min_support_percentage:
                    # Accepted subsets to list, sort, include in VFI
                    c = list(c)
                    c.sort()
                    vfi.append(c)
                    # Don't forget that support percentage!
                    support_index.append(support)

                # If single item and it's not in VFI get rid of it
                elif len(c) == 1:
                    c = list(c)
                    items.remove(c[0])

        # Write it all to a heckin new file
        with open(output_filename, "w", newline="") as f:
            for i in range(len(vfi)):
                row = csv.writer(f)
                line = vfi[i]
                line.insert(0, 'S')
                line.insert(1, '%.4f' % support_index[i])
                row.writerow(line)

            # Get the subsets that made it through min_support
            ss = vfi.copy()
            ss = [x[2:] for x in ss]
            unions = vfi.copy()
            unions = {(str(x[2:])): x[1] for x in unions}

            for pair in it.combinations(ss, 2):
                pair = list(pair)
                a = set(pair[0])
                b = set(pair[1])

                u = a.union(b)
                u = list(u)
                u.sort()

                if str(u) in unions:
                    union_support_percent = float(unions[str(u)])
                    first = list(a)
                    first.sort()

                    second = list(b)
                    second.sort()

                    if len(a.intersection(b)) == 0:
                        row = csv.writer(f, quoting=csv.QUOTE_NONE, quotechar=None, escapechar='\\')

                        first_support_percent = float(unions[str(first)])
                        flipped_support_percent = float(unions[str(second)])

                        conf = union_support_percent / first_support_percent
                        flipped_conf = union_support_percent / flipped_support_percent

                        if conf >= min_confidence:
                            row.writerow(['R'] + [str('%.4f' % union_support_percent)] +
                                         [str('%.4f' % conf)] + first + ['\'=>\''] + second)

                        if flipped_conf >= min_confidence:
                            row.writerow(['R'] + [str('%.4f' % union_support_percent)] +
                                         [str('%.4f' % flipped_conf)] + second + ['\'=>\''] + first)

if __name__ == "__main__":
    armin = Armin()
    armin.apriori('input.csv', 'output.sup=0.5,conf=0.7.csv', 0.5, 0.7)
    armin.apriori('input.csv', 'output.sup=0.5,conf=0.8.csv', 0.5, 0.8)
    armin.apriori('input.csv', 'output.sup=0.6,conf=0.8.csv', 0.6, 0.8)
    armin.apriori('example.csv', 'output_example.csv', 0.5, 0.6)