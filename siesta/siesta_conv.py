#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import argparse

# 1st optional argument as output of siesta
# 2nd optional argument as the string to grep

parser = argparse.ArgumentParser(description='Plot convergence')
parser.add_argument('-f', type=str, default='output.out',
                    help='file to be queried: output of siesta, \
                    default: "output.out"')
parser.add_argument('-s', type=str, default='   scf:   ',
                    help='string to be queried in file, \
                    default:"   scf:   "')
parser.add_argument('-c', type=int, default=2,
                    help='column to plot, default: 2')
args = parser.parse_args()

block = []
data = []
s_pass = True

with open(args.f) as f:
    for line in f:
        if args.s in line:
            if len(line.split()) > 7:
                data.append(line.split()[1:])
        elif "Eharris(eV)" in line and s_pass:
            columns = line.split()[1:]
            s_pass = False

data_np = np.array(data, dtype='float')

print("columns:", columns, "use -c to change the column to plot.")

plt.plot(data_np[:, 0], data_np[:, args.c], '-*')
plt.xlabel(columns[0])
plt.ylabel(columns[args.c])
plt.tight_layout()
plt.show()
