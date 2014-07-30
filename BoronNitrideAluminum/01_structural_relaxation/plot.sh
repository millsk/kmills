#!/bin/bash

grep pressure OUTCAR | awk '{print $4}' > pressure
gnuplot -persist plot_pressure.gnuplot
