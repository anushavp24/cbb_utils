# Project 3 : Fragment Length vs Position Vplot

## Overview

This project builds a matrix of sequenced DNA fragments around CTCF binding sites and plots it as a V-plot using Gnuplot.

The Python script reads overlap data from standard input, calculates the position of each fragment relative to the region center, counts how many fragments share the same position and length, and writes the result as a plain text matrix file. A Gnuplot script then draws the matrix as a V-plot.

## Required Files

The following files are required:

- `make_matrix.py` – Python script that generates the matrix file.
- `plot.gnuplot` – Gnuplot script that plots the matrix.
- `input.bed.gz` – Input data, with one fragment overlapping a region per line (see Input Format).

Example directory structure:

```text
PROJECT/
├── make_matrix.py
├── plot.gnuplot
├── input.bed.gz
├── matrix.tsv           (created by make_matrix.py)
└── plot.png    (created by plot.gnuplot)
```

## Requirements

The following tools are required:

- Python 3 (standard library only, no extra packages)
- Gnuplot (with the `pngcairo` terminal)



## How to Run

Generate the matrix file (the script reads from standard input):

```bash
zcat input.bed.gz | python3 make_matrix.py > matrix.tsv
```

Plot the matrix:

```bash
gnuplot plot.gp
```

## Output

Two files are created:

```text
matrix.tsv
plot.png
```

`matrix.tsv` is a plain matrix in long form. Each line has three values:

```text
x y z
```

- `x` – position of the fragment midpoint relative to the region center (bp)
- `y` – fragment length (bp)
- `z` – number of fragments with that `x` and `y`


`plot.png` is the vplot, with position on the x-axis, fragment length on the y-axis and fragment count as color.

## Method

The script performs the following operations:

1. Reads the input line by line from standard input.
2. Calculates the region center from columns 3 and 4.
3. Calculates the fragment midpoint from columns 9 and 10.
4. Calculates `x = fragment midpoint - region center`.
5. Takes `y` from column 12 (fragment length).
6. Keeps only `-500 <= x <= 500` and `40 <= y <= 300`.
7. Counts each `(x, y)` pair using a dictionary.
8. Writes `x y z` for every pair in the window.Malformed lines (missing columns or non-numeric values) are skipped.

## Reference Point

Positions are measured from the **region center**, so 0 on the x-axis is the middle of the CTCF binding site.

```text
   region center = (region start + region end) // 2
   x             = (fragment start + fragment end) // 2 - region center
```

