# Project 1: BED File Sorting

## Overview

This project sorts BED files for a sample according to a given chromosome order.

The pipeline combines all BED files belonging to the same sample, keeps only chromosomes present in the selection file, and sorts the records based on chromosome order and starting position.

The output is saved as a compressed BED file (`.bed.gz`) for the sample.

## Required Files

The following files are required:

- `make_sorted_bed.sh` – Bash script that runs the full pipeline.
- `split_by_chrom_v2.py` – Python script that filters the records and splits them by chromosome.
- `selection.tsv` – File containing the required chromosome order.
- Input BED files of the sample (for example `shuf.a.bed.gz` and `shuf.b.bed.gz`).

Example directory structure:

```text
PROJECT-1/
├── make_sorted_bed.sh
├── split_by_chrom_v2.py
├── selection.tsv
├── shuf.a.bed.gz
└── shuf.b.bed.gz
```

## Requirements

The following tools are required:

- Bash
- `zcat`
- `sort`
- `gzip`
- Python 3 (standard library only, nothing to install)

These tools are available by default on most Linux systems.

## Settings

Open `make_sorted_bed.sh` and edit the variables at the top of the file:

| Variable | Meaning | Example |
|---|---|---|
| `SAMPLE` | Sample name, used in the output file name | `X` |
| `SELECTION` | Selection name, used in the output file name | `standard` |
| `SEL_FILE` | Selection file with the chromosome order | `selection.tsv` |
| `RUN_A` | First BED file of the sample | `shuf.a.bed.gz` |
| `RUN_B` | Second BED file of the sample | `shuf.b.bed.gz` |
| `JOBS` | Number of files sorted at the same time (number of CPU cores) | `8` |
| `MEM` | Memory allowed for each sort | `300M` |

To process another sample, change `SAMPLE`, `RUN_A` and `RUN_B`, and run the script again.

## How to Run

Make the script executable:

```bash
chmod +x make_sorted_bed.sh
```

Run the script:

```bash
./make_sorted_bed.sh
```

The script reads the BED files named in `RUN_A` and `RUN_B` and uses `selection.tsv` to determine the chromosome order.

## Output

The script creates the following output directory:

```text
sorted_bed_file_per_sample/
```

The sample gets a compressed BED file containing the sorted and combined records.

The output file is named:

```text
{SAMPLE}.{SELECTION}.sorted.bed.gz
```

For example:

```text
sorted_bed_file_per_sample/X.standard.sorted.bed.gz
```

Temporary files are written to `tmp_chrom/`. They can be removed after checking the output:

```bash
rm -r tmp_chrom
```
