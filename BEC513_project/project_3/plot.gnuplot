set terminal pngcairo size 1400,900 enhanced font 'Sans,14'
set output 'plot.png'

set title 'Fragment length vs position around CTCF sites' font 'Sans,16'
set xlabel 'Position relative to region center (bp)'
set ylabel 'Fragment length (bp)'
set cblabel 'Fragment count'

# half-unit padding so edge cells are not cut in half
set xrange [-500.5:500.5]
set yrange [39.5:500.5]
set cbrange [0:50]

set xtics 100
set ytics 50
set tics out nomirror
set border 3
set lmargin 10
set rmargin 14

# magma-style palette, as in your picture
set palette defined (0 '#000004', 0.15 '#2c115f', 0.3 '#721f81', \
                     0.45 '#b73779', 0.6 '#f1605d', 0.8 '#fd9567', 1 '#fcfdbf')
unset key

plot 'matrix.tsv' using 1:2:3 with image
