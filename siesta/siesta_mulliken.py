#!/usr/bin/env python3

import sys
import numpy as np
from ase.io import read

file = 'output.out'  # output from siesta, or as the 1st argument
if len(sys.argv) > 1:
    file = sys.argv[1]

elm = {}
charge = []
index = []
Qtot = []
in_mulliken = False

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


# structure file, can be any file at ase.io.read understands
str_file = 'siesta.xyz'
if len(sys.argv) > 2:
    str_file = sys.argv[2]

a = read(str_file)

# reset the values to do sum for each element
elm = dict.fromkeys(elm, 0)

charge_np = np.array(charge, dtype='float')
# put the net charge and calculate the sum
for i, j in zip(a, charge_np):
    i.charge = j[-1] - j[1]
    elm[i.symbol] += i.charge

if len(charge) / 2 == len(a):
    print('spin-polarized caculation...')
    for i, j in zip(a, charge_np[int(len(charge_np) / 2):]):
        i.charge -= j[1]
        elm[i.symbol] -= j[1]

        # output
a.write('charge.xyz',format='extxyz')

# fix some labels in xyz files
with open('charge.xyz') as f:
   newText=f.read().replace('initial_charges', 'Charge').replace(' =T ', ' ')

with open('charge.xyz', "w") as f:
   f.write(newText)


#a=read('charge.xyz')




print('net charge:{},total:{}'.format(elm, sum(Qtot)))
