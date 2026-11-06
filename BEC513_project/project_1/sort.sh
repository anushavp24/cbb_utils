#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C                          # fastest, consistent sort rules

SAMPLE="X"
SELECTION="standard"
SEL_FILE="selection.tsv"
RUN_A="shuf.a.bed.gz"
RUN_B="shuf.b.bed.gz"
TMPDIR="tmp_chrom"
OUTDIR="sorted_bed_file_per_sample"

JOBS=12                            # sorts running at the same time
MEM="200M"                                 # RAM per sort job (JOBS x MEM must fit in your RAM)

mkdir -p "$TMPDIR" "$OUTDIR"
OUT="${OUTDIR}/${SAMPLE}.${SELECTION}.sorted.bed.gz"

# 1. unzip A and B together -> python: one file per selected chromosome
zcat "$RUN_A" "$RUN_B" \
  | python3 split.py "$SEL_FILE" "$SAMPLE" "$SELECTION" "$TMPDIR"

# 2. sort every chromosome file by column 2, then 3, all at once, biggest files first
ls -S "${TMPDIR}/${SAMPLE}.${SELECTION}."*.bed \
  | xargs -P "$JOBS" -I{} sort -t $'\t' -s -k2,2n -k3,3n -S "$MEM" -T "$TMPDIR" -o {} {}

# 3. list the files in selection-file order, join once, compress
while read -r chrom; do
  if [ -n "$chrom" ]; then
    cat "${TMPDIR}/${SAMPLE}.${SELECTION}.${chrom}.bed"
  fi
done < "$SEL_FILE" | gzip -1 > "$OUT"

echo "Written: $OUT"
