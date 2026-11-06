#!/usr/bin/env python3
# Count how many fragments there are for each fragment length.
# Fragment length = end - start = column 3 - column 2 of the BED file.
#
# Usage:
#   zcat query.bed.gz | python3 count_lengths.py > query_counts.tsv
#
# Output: one line per length -> length <tab> count

import sys

counts = {}                      # key = fragment length, value = how many times we saw it

for line in sys.stdin:
    cols = line.split("\t")
    length = int(cols[2]) - int(cols[1])        # column 3 - column 2
    if length in counts:
        counts[length] = counts[length] + 1     # seen before: add 1
    else:
        counts[length] = 1                      # new length: start at 1

for length in counts:
    print(str(length) + "\t" + str(counts[length]))
