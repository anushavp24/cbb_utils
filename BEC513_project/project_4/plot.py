# Usage : python graph.py < output.tsv

import matplotlib.pyplot as plt
from sys import stdin
import math
from scipy import stats

# ---------- Settings ----------
normal_label = "Solid Tissue Normal"

# ---------- Part 1: read the data ----------
normal_values, tumor_values = [], []

for line in stdin:
  words = line.strip().split("\t")

  # log2(TPM + 1) is the y value
  log_tpm = math.log(float(words[1]) + 1, 2)

  # Normal samples go to one list, everything else is tumor
  if words[2] == normal_label:
    normal_values.append(log_tpm)
  else:
    tumor_values.append(log_tpm)

# ---------- Part 2: p-value ----------
t_stat, p_value = stats.ttest_ind(tumor_values, normal_values)

# ---------- Part 3: boxplot ----------
labels = [f"Solid Tissue Normal (n = {len(normal_values)})",
          f"Primary Tumor (n = {len(tumor_values)})"]

plt.boxplot([normal_values, tumor_values], tick_labels=labels, notch=True)
plt.ylabel("log2(TPM + 1)")
plt.title(f"Lung Adenocarcinoma (p = {p_value:.1e})")
plt.tight_layout()
plt.savefig("output.png")
