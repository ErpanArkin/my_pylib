#!/usr/bin/env python3

'''
This script attach charges calculated with bader charge program to xyz 
for visualizing it with ovito.
This requires CONTCAR OUTACR ACF.dat files.
'''

from ase.io import read
from ase.io.bader import attach_charges
import numpy as np


a = read('CONTCAR')
attach_charges(a)
elm = []

# get the elements (elm) and their initial # of electron (chg)
with open('OUTCAR') as f:
    for line in f:
        if len(line.split()) > 2 and line.split()[0] == 'ZVAL':
            chg = line.split()[2:]
        if len(line.split()) > 1 and line.split()[0] == 'VRHFIN':
            elm.append(line.split()[1].strip('=').strip(':'))

elm.append('total')
ech = [0] * len(elm)
all_chg = dict(zip(elm, ech))


# calculate the rest charge
for i in a:
    for j, k in enumerate(elm):
        if i.symbol == k:
            i.charge = float(chg[j]) - i.charge
            all_chg[k] += i.charge
            break

# output xyz file with charge information
a.write('charge.xyz')

# fix some labels in xyz files
with open('charge.xyz') as f:
    newText = f.read().replace('initial_charges', 'Charge').replace(' =T ', ' ')

with open('charge.xyz', "w") as f:
    f.write(newText)


all_chg['total'] = sum(all_chg.values())
for i in all_chg:
    print(i, all_chg[i], ' ', end="")
print('')
