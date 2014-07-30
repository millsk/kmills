#!/bin/bash

grep pressure OUTCAR | awk '{print $4}' > pressure
grep temperature OUTCAR | awk '$7 ~ "^[0-9,\.][0-9,\.]*$" {print $7}' > temperature

if [ "x$1" == "xpdf" ]; then
   output1="set term pdf"
   output2="set output \"pressure.pdf\""
   output3="set output \"temperature.pdf\""
fi


gnuplot -persist << GNUPLOTINPUT
$output1
$output2
set title "Pressure vs. Time"
set xlabel "Time, picoseconds"
set ylabel "Pressure, mbar"
unset key
plot 'pressure' using (\$0*`grep POTIM INCAR | sed 's|[^0-9|.]||g'`*0.001):1 with lines
GNUPLOTINPUT

gnuplot -persist << GNUPLOTINPUT
$output1
$output3
set title "Temperature vs. Time"
set xlabel "Time, picoseconds"
set ylabel "Temperature, K"
unset key
plot 'temperature' using (\$0*`grep POTIM INCAR | sed 's|[^0-9|.]||g'`*0.001):1 with lines
GNUPLOTINPUT
