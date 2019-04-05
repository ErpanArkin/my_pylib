#!/usr/bin/env python3

import sys
import numpy as np
from ase.io import read,iread,write

file = 'output.out'  # output from siesta, or as the 1st argument
if len(sys.argv) > 1:
    file = sys.argv[1]

elm = {}
charge = []
index = []
Qtot = []
in_mulliken = False
total_sets = []

# parse the output and get valance and mulliken charge
with open(file, 'r') as f:
    for line in f:
        if len(line.split()) > 1:
            if 'atom: Called for' in line:
                lst_elm = line.split()[3]
            if 'Total valence charge' in line:
                elm[lst_elm] = float(line.split()[-1])
            if 'mulliken: Atomic and Orbital Populations' in line:
                in_mulliken = True

                charge = []
            lo = True
            if in_mulliken and 'Species:' in line:
                chg_0 = elm[line.split()[-1]]
            try:
                test = int(line.split()[0])
            except ValueError:
                lo = False
            if in_mulliken and lo:
                x = line.split()[:2]
                x.append(chg_0)
                charge.append(x)
            if 'mulliken: Qtot =' in line:
                Qtot.append(float(line.split()[-1]))
                next(f)
                if 'mulliken' not in next(f):
                    in_mulliken = False
                    # append for each md steps
                    total_sets.append(np.array(charge,dtype='float'))

total = np.array(total_sets)

a = iread('siesta.AXSF')
for i,j in zip(a,total[1:]):
    i.set_initial_charges(j[:,1]-j[:,2])
    write('total_charges.xyz',i,append=True)