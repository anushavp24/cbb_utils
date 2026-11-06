# Draw query, reference and sampled fragment length distributions (base R only).
# No BED file is read: the 4th column (n_keep) of the table made by resample.py is the sampled result.
#
# Usage:
#   Rscript plot.R rep0_table.tsv rep0.png "Rep 0"
#
# Table columns: length, query_count, ref_proportion, n_keep

args <- commandArgs(trailingOnly = TRUE)
table_file <- args[1]
png_file   <- args[2]
label <- "Rep 0"
if (length(args) >= 3) {
  label <- args[3]
}

# ---------- read the table ----------
tab <- read.table(table_file, sep = "\t", header = FALSE)
frag_len <- tab[, 1]
qcount   <- tab[, 2]
ref      <- tab[, 3]
keep     <- tab[, 4]

# ---------- make every curve add up to 1 ----------
query <- qcount / sum(qcount)
samp  <- keep / sum(keep)

# ---------- draw ----------
png(png_file, width = 1600, height = 1000, res = 200)
plot(frag_len, query, type = "l", col = "purple", lwd = 2,
     xlim = c(0, 700), ylim = c(0, max(query, samp, ref)),
     xlab = "Fragment length (bp)", ylab = "Normalised frequency")
lines(frag_len, samp, col = "deeppink", lwd = 5)      # thick pink = sampled result
lines(frag_len, ref, col = "green", lwd = 1.5)        # thin green on top = reference
legend("topright",
       legend = c(paste0("Query (n = ", format(sum(qcount), big.mark = ","), ")"),
                  "Reference",
                  paste0(label, " (n = ", format(sum(keep), big.mark = ","), ")")),
       col = c("purple", "green", "deeppink"), lwd = c(2, 1.5, 5))
dev.off()
