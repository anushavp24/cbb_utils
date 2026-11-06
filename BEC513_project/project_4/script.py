# Usage : tar -xzf ../given/tcga_data.tar.gz
# Usage : python script.py unzip < given/gdc_sample_sheet.tsv

from sys import stdin, argv
import pandas as pd
import os

# ---------- Settings ----------
root = argv[1]                  # folder with one sub-folder per sample
gene = "NKX2-1"                 # gene whose TPM we want
tpm_column = 6                  # position of the TPM value in a line
conditions = ["Solid Tissue Normal", "Primary Tumor"]

# ---------- Part 1: TPM of the gene for each sample ----------
sample_ids, tpm_values = [], []

for sample_dir in os.listdir(root):
  sample_path = os.path.join(root, sample_dir)

  for file_name in os.listdir(sample_path):
    if file_name.endswith("tsv"):
      file_path = os.path.join(sample_path, file_name)

      with open(file_path) as f:
        for line in f:
          words = line.strip().split("\t")
          if gene in words:
            tpm_values.append(words[tpm_column])
            sample_ids.append(sample_dir)
            break               # gene found, move to the next file

id_tpm = pd.DataFrame({"id": sample_ids, "tpm": tpm_values})

# ---------- Part 2: condition of each sample (from sample sheet) ----------
cond_ids, cond_values = [], []

for line in stdin:
  words = line.strip().split("\t")
  for condition in conditions:
    if condition in line:
      cond_ids.append(words[0])
      cond_values.append(condition)

id_cond = pd.DataFrame({"id": cond_ids, "cond": cond_values})

# ---------- Part 3: merge and save ----------
merged = pd.merge(id_tpm, id_cond, on="id")
merged.to_csv("output.tsv", sep="\t", index=False, header=False)
