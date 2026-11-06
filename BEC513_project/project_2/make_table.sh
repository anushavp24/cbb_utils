#!/bin/bash
# Join query counts with the reference proportions.
#
# Usage:
#   bash make_table.sh query.bed.gz reference.hist > length_table.tsv
#
# Output columns: length <tab> query_count <tab> ref_proportion
#   length not in query     -> count = 0
#   length not in reference -> proportion = 0

# 1. count the query lengths
zcat "$1" | python3 count_length.py > query_counts.tsv

# 2. clean the reference: remove Windows line ends, drop header (keep lines starting with a digit),
#    keep only the first two columns
tr -d '\r' < "$2" | grep -E '^[0-9]' | awk '{print $1 "\t" $2}' > ref_clean.tsv

# 3. join needs both files sorted on column 1 (as text)
LC_ALL=C sort -k1,1 query_counts.tsv > q_sorted.tsv
LC_ALL=C sort -k1,1 ref_clean.tsv > r_sorted.tsv

# 4. join: -a1 -a2 keeps lengths found in only one file, -e 0 fills the gap with 0
#    -o chooses output columns: join key, file1 column 2 (count), file2 column 2 (proportion)
LC_ALL=C join -t $'\t' -a1 -a2 -e 0 -o 0,1.2,2.2 q_sorted.tsv r_sorted.tsv | sort -n -k1,1

# 5. remove temporary files
rm -f query_counts.tsv ref_clean.tsv q_sorted.tsv r_sorted.tsv
