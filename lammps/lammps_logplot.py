#!/usr/bin/env python

# Script:  logplot.py
# Purpose: use GnuPlot to plot two columns from a LAMMPS log file
# Syntax:  logplot.py log.lammps X Y1 Y2 ...
#          log.lammps = LAMMPS log file
#          X,Y = plot Y versus X where X,Y are thermo keywords
#          once plot appears, you are in Python interpreter, type C-D to exit
# Author:  Steve Plimpton (Sandia), sjplimp at sandia.gov

import sys
import matplotlib.pyplot as plt

from log import log

if len(sys.argv) < 6:
    raise StandardError("Syntax: \
logplot.py log.lammps 1st_step last_step X Y1 Y2 ...")

logfile = sys.argv[1]
init_step = int(sys.argv[2])
last_step = int(sys.argv[3])
xlabel = sys.argv[4]
ylabel = sys.argv[5:]

fig, ax = plt.subplots(len(ylabel), sharex='col')
for i, j in enumerate(ylabel):
    lg = log(logfile)
    x, y = lg.get(xlabel, j)
    ax[i].plot(x[init_step:last_step], y[init_step:last_step])
    plt.xlabel(xlabel)
    ax[i].set_ylabel(j)
plt.legend()
plt.show()
