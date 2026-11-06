import sys
from collections import Counter

XMIN, XMAX = -500, 500     # position window (relative to region center)
YMIN, YMAX = 40, 500       # fragment length window

counts = Counter()

for line in sys.stdin:
    f = line.split()
    if len(f) < 12:
        continue
    try:
        r_start, r_end = int(f[2]), int(f[3])      # region: columns 3, 4
        s, e = int(f[8]), int(f[9])                # fragment: columns 9, 10
        y = int(f[11])                             # length: column 12
    except ValueError:
        continue

    x = (s + e) // 2 - (r_start + r_end) // 2      # fragment midpoint - region center
    if XMIN <= x <= XMAX and YMIN <= y <= YMAX:
        counts[(x, y)] += 1

for x in range(XMIN, XMAX + 1):
    for y in range(YMIN, YMAX + 1):
        print(x, y, counts.get((x, y), 0))
    print()
