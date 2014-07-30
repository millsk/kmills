#!/bin/bash

grep pressure OUTCAR | awk '{print $4}' > pressure
grep temperature OUTCAR | awk '$7 ~ "^[0-9,\.][0-9,\.]*$" {print $7}' > temperature
gnuplot -persist plot_pressure.gnuplot
gnuplot -persist plot_temperature.gnuplot
