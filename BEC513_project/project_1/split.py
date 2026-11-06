#!/usr/bin/env python3
import os
import sys

selection_file, sample, selection, outdir = sys.argv[1:5]
os.makedirs(outdir, exist_ok=True)

# STEP 1: one output file per chromosome (bytes keys, 1 MB write buffer)
chrom_files = {}
with open(selection_file) as sel:
    for line in sel:
        chrom = line.strip()
        if chrom and chrom.encode() not in chrom_files:
            path = os.path.join(outdir, f"{sample}.{selection}.{chrom}.bed")
            chrom_files[chrom.encode()] = open(path, "wb", buffering=1 << 20)

# STEP 2 + 3: read raw bytes, take column 1, write the line if it is selected
get = chrom_files.get
for line in sys.stdin.buffer:
    fh = get(line[:line.find(b"\t")])   # column 1 = text before the first tab
    if fh is not None:
        fh.write(line)

# STEP 4: close all files
for fh in chrom_files.values():
    fh.close()
