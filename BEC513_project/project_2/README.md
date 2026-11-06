# Project 2: Rescale to Reference

This pipeline subsamples a query BED file so that its fragment length distribution matches a reference distribution. Only whole lines of the query are kept or discarded; no fragment is changed.

## Required Files

The following files are required:

- `make_table.sh` – Shell script that builds the length table (counts the query lengths and joins them with the reference).
- `count_lengths.py` – Python script used by `make_table.sh` to count fragments per length.
- `resample.py` – Python script that selects the fragments and writes the rescaled BED file.
- `plot.R` – R script that draws the distributions (base R only).
- `reference.hist` – Reference fragment length distribution.
- `query.bed.gz` – Input BED file containing query fragments.


## Requirements

- Python 3 (standard libraries only, for `count_lengths.py`, `resample.py` and `make_targets.py`)
- R (base R only, no packages) for `plot.R`
- Standard Linux tools: `zcat`, `sort`, `join`, `awk`, `grep`, `tr`



## How to Run

Run the following three steps in order.

### Step 1: build the length table

```bash
bash make_table.sh query.bed.gz reference.hist > length_table.tsv
```

`length_table.tsv` has three columns:

1. Fragment length
2. Number of query fragments with this length
3. Reference proportion for this length

A length that is missing from the query gets count `0`. A length that is missing from the reference gets proportion `0`.

### Step 2: rescale the query

```bash
python3 resample.py query.bed.gz length_table.tsv rep0.bed.gz 2000000 0
```

The arguments are, in order:

1. `query.bed.gz` – the query BED file
2. `length_table.tsv` – the table from Step 1
3. `rep0.bed.gz` – name of the output BED file (must end in `.bed.gz`)
4. `2000000` – N, the total number of fragments wanted (explained below)
5. `0` – random seed (optional, default 0)

### Step 3: plot

```bash
Rscript plot.R rep0_table.tsv rep0.png "Rep 0"
```

The arguments are the table written by Step 2, the name of the picture, and the label shown in the legend.

### Replicates

Change the seed for each replicate:

```bash
for seed in 0 1 2; do
    python3 resample.py query.bed.gz length_table.tsv rep$seed.bed.gz 2000000 $seed
    Rscript plot.R rep${seed}_table.tsv rep$seed.png "Rep $seed"
done
```

### Choosing N (optional)
```bash
python3 make_targets.py length_table.tsv                  # prints the strict N
python3 make_targets.py length_table.tsv --n 2000000      # prints kept, TVD, capped lengths
```

### N value

N is the total number of fragments wanted. For each length L:

$$n_{keep}(L) = \min\big(count(L),\ \text{round}(N \cdot R_L)\big)$$
-**Strict N**: the largest N with an exact match, set by the scarcest length.
-**Larger N**: keeps more data, but lengths where the query runs out are capped, so the curve falls below the reference there.


## Output

### 1. `rep0.bed.gz`

The rescaled BED file. It contains only lines that exist in the query file, unchanged.

### 2. `rep0_table.tsv`

A table with four columns:

1. Fragment length
2. Number of query fragments
3. Reference proportion
4. Number of fragments kept (`n_keep`)

### 3. `rep0.png`

A plot comparing three fragment length distributions:

- Reference (green) – target distribution.
- Query (purple) – original query distribution.
- Rep 0 (pink) – distribution after sampling.

The X-axis represents fragment length in base pairs, and the Y-axis represents normalised frequency. Each curve is divided by its own total, so all three add up to 1.

`resample.py` also prints the planned number of fragments, the number of capped lengths, and the number of lines written. It prints a WARNING if the query file does not match the table or if a target was not reached.

## Method

The method is exact-count stratified sampling, where each fragment length is one stratum.

1. Count the query fragments for each length (`count_lengths.py`, a dictionary of length to count).
2. Join the counts with the reference proportions (`make_table.sh`, using `join`).
3. Choose N and compute how many fragments to keep for each length (`resample.py`).
4. Go through the query once. For a line of length L, with `k` lines still to pick and `n` lines of that length not yet seen, keep the line with probability `k / n`. Then reduce `n` by 1, and reduce `k` by 1 if the line was kept.

Step 4 is called selection sampling. It picks exactly `n_keep(L)` lines for every length, and every possible subset of that size is equally likely. The file is read once and memory use is small, so it works for tens of millions of lines.

Fragment length is treated as independent of chromosome, because the reference distribution has only length and frequency.

## Total Variation Distance

TVD measures the difference between the reference and rescaled distributions.

\[
TVD = \frac{1}{2}\sum_i |R_i-S_i|
\]

Where:

- \(R_i\) is the normalised reference frequency.
- \(S_i\) is the normalised rescaled frequency.

A lower TVD indicates a closer match to the reference distribution. A TVD of zero indicates an exact match. TVD is printed by `make_targets.py`, calculated from the planned counts.


