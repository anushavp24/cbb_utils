# Project 4: NKX2-1 Expression in Lung Adenocarcinoma (TCGA-LUAD)

Compares the expression of the gene **NKX2-1** between **Primary Tumor** and **Solid Tissue Normal** samples from TCGA Lung Adenocarcinoma, using RNA-seq data from the GDC. The result is a notched boxplot of log2(TPM + 1) with the sample count for each group and a t-test p-value.

## Folder structure

```
project_4/
├── given/
│   ├── tcga_data.tar.gz         # RNA-seq files, one folder per sample
│   └── gdc_sample_sheet.tsv     # sample sheet: file ID and sample type
├── script.py                    # step 1: build output.tsv
├── plot.py                      # step 2: draw output.png
├── output.tsv                   # created by script.py
├── output.png                   # created by plot.py
└── README.md
```

## Requirements

- Python 3
- pandas, matplotlib (3.9 or newer, because `plot.py` uses `tick_labels`), scipy

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas matplotlib scipy
```

## How to run

Run everything from the project folder (`project_4`).

**1. Extract the data into a folder called `unzip`**

```bash
mkdir unzip
tar -xzf given/tcga_data.tar.gz -C unzip
```

The archive has no wrapper folder, so each sample folder (named by a UUID) lands directly inside `unzip`.

**2. Build the table of TPM and condition per sample**

```bash
python script.py unzip < given/gdc_sample_sheet.tsv
```

This creates `output.tsv`.

**3. Draw the boxplot**

```bash
python plot.py < output.tsv
```

This creates `output.png`.

**4. (Optional) Remove the extracted data**

```bash
rm -r unzip
```

`plot.py` only needs `output.tsv`, so the extracted folder can be deleted once step 2 is done.

## How it works

### script.py

1. Goes through every sample folder inside the root folder given as the first argument.
2. Opens each file ending in `tsv` and reads it line by line until it finds the line containing `NKX2-1`.
3. Takes the value in the 7th column (index 6, the `tpm_unstranded` column of the STAR gene counts file) and stores it with the sample folder name as the ID.
4. Reads the sample sheet from standard input and keeps the rows that contain `Solid Tissue Normal` or `Primary Tumor`. The first column (the file ID) is the sample ID.
5. Merges the two tables on the ID and writes `output.tsv` (tab-separated, no header).

### plot.py

1. Reads `output.tsv` from standard input.
2. Converts each TPM to **log2(TPM + 1)**. The +1 avoids taking the log of zero.
3. Splits the values into normal and tumor groups.
4. Runs a two-sample t-test (`scipy.stats.ttest_ind`) between tumor and normal.
5. Draws a notched boxplot with the group sizes in the labels and the p-value in the title, and saves it as `output.png`.

## Output

`output.tsv` has three tab-separated columns and no header:

| Column | Meaning |
|--------|---------|
| 1 | Sample ID (folder name) |
| 2 | TPM of NKX2-1 (`tpm_unstranded`) |
| 3 | Condition (`Solid Tissue Normal` or `Primary Tumor`) |

`output.png` is the final figure:

![NKX2-1 boxplot](output.png)

## Notes

- Samples are matched only if their ID appears in both the extracted folders and the sample sheet.
- The p-value comes from `ttest_ind` with its default setting, which assumes equal variance in both groups (Student's t-test).
- Any condition other than `Solid Tissue Normal` in `output.tsv` is counted as tumor by `plot.py`. This is safe here because `script.py` only keeps the two conditions.
- The scripts read the TPM from a fixed column position. If the input file format changes, update `tpm_column` in `script.py`.

