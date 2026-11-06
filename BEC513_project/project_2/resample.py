#!/usr/bin/env python3
# Resample the query so its fragment length distribution matches the reference.
# This one script replaces make_targets.py + sample.py.
# It also saves <output name>_table.tsv (length, count, proportion, n_keep) for plot.R.
#
# Usage:
#   python3 resample.py query.bed.gz length_table.tsv out.bed.gz N seed
# Example:
#   python3 resample.py query.bed.gz length_table.tsv rep0.bed.gz 2000000 0
#
# length_table.tsv columns: length, query_count, ref_proportion

import sys
import gzip
import random

query_file = sys.argv[1]
table_file = sys.argv[2]
out_file = sys.argv[3]
n = int(sys.argv[4])                     # total fragments we would like to keep
seed = 0
if len(sys.argv) >= 6:
    seed = int(sys.argv[5])

random.seed(seed)

# ---------- 1. read the table ----------
lengths = []
counts = []
props = []
fh = open(table_file)
for line in fh:
    parts = line.split("\t")
    lengths.append(int(parts[0]))
    counts.append(int(parts[1]))
    props.append(float(parts[2]))
fh.close()

# make the reference proportions add up to exactly 1
total_ref = 0.0
for p in props:
    total_ref = total_ref + p

# ---------- 2. how many to keep for each length ----------
keeps = []           # number kept for each length (same order as the table)
n_left = {}          # lines of this length we have not seen yet
k_left = {}          # lines of this length we still need to pick
total_kept = 0
capped = 0
for i in range(len(lengths)):
    want = round(n * props[i] / total_ref)
    if counts[i] < want:                 # query has too few: keep all of them
        keep = counts[i]
        capped = capped + 1
    else:
        keep = want
    keeps.append(keep)
    n_left[lengths[i]] = counts[i]
    k_left[lengths[i]] = keep
    total_kept = total_kept + keep

sys.stderr.write("N = " + str(n) + ", planned to keep = " + str(total_kept) + ", capped lengths = " + str(capped) + "\n")

# ---------- 3. go through the query and pick lines ----------
written = 0
fin = gzip.open(query_file, "rt")
fout = gzip.open(out_file, "wt")
for line in fin:
    cols = line.split("\t")
    L = int(cols[2]) - int(cols[1])      # column 3 - column 2
    if L not in n_left:
        sys.stderr.write("length " + str(L) + " is not in the table. Was the table made from this file?\n")
        sys.exit(1)
    if k_left[L] > 0:
        if random.random() < k_left[L] / n_left[L]:
            fout.write(line)
            k_left[L] = k_left[L] - 1
            written = written + 1
    n_left[L] = n_left[L] - 1
fin.close()
fout.close()

# ---------- 4. checks ----------
for L in n_left:
    if n_left[L] != 0:
        sys.stderr.write("WARNING: query file does not match the table\n")
        break
for L in k_left:
    if k_left[L] != 0:
        sys.stderr.write("WARNING: some targets were not reached\n")
        break
sys.stderr.write("wrote " + str(written) + " lines to " + out_file + "\n")

# ---------- 5. save the 4-column table for plotting: length, count, proportion, n_keep ----------
table_out = out_file.replace(".bed.gz", "") + "_table.tsv"
fo = open(table_out, "w")
for i in range(len(lengths)):
    fo.write(str(lengths[i]) + "\t" + str(counts[i]) + "\t" + str(props[i]) + "\t" + str(keeps[i]) + "\n")
fo.close()
sys.stderr.write("wrote plotting table to " + table_out + "\n")
