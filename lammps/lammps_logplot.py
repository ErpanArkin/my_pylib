#!/usr/bin/env python

# Script:  logplot.py
# Purpose: use GnuPlot to plot two columns from a LAMMPS log file
# Syntax:  logplot.py log.lammps X Y1 Y2 ...
#          log.lammps = LAMMPS log file
#          X,Y = plot Y versus X where X,Y are thermo keywords
#          once plot appears, you are in Python interpreter, type C-D to exit
# Author:  Steve Plimpton (Sandia), sjplimp at sandia.gov

import sys,os
import matplotlib.pyplot as plt

from log import log

if len(sys.argv) < 4:
  raise StandardError, "Syntax: logplot.py log.lammps X Y"

logfile = sys.argv[1]
xlabel = sys.argv[2]
ylabel = sys.argv[3:]

fig, ax = plt.subplots(len(ylabel),sharex='col')
for i,j in enumerate(ylabel):
    lg = log(logfile)
    x,y = lg.get(xlabel,j)
    ax[i].plot(x,y)
    plt.xlabel(xlabel)
    ax[i].set_ylabel(j)
plt.legend()
plt.show()



