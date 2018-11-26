#!/usr/bin/python3

'''
This script attach charges calculated with bader charge program to xyz 
for visualizing it with ovito.
This requires CONTCAR OUTACR ACF.dat files.
'''

from ase.io import read
from ase.io.bader import attach_charges
a = read('CONTCAR')
attach_charges(a)

# get the elements (elm) and their initial # of electron (chg)
with open('OUTCAR') as f:
    for line in f:
        if len(line.split()) > 2 and line.split()[0] == 'ZVAL':
            chg = line.split()[2:]
        if 'POSCAR:' in line:
        	elm = line.split()[1:]
        	
elm.append('total')        	
ech = [0] * len(elm)
all_chg = dict(zip(elm,ech))
#calculate the rest charge
for i in a:
    for j,k in enumerate(elm):
    	if i.symbol == k:
            i.charge = -i.charge +float(chg[j])
            all_chg[k] += i.charge
# output xyz file with charge information
a.write('charge.xyz')

all_chg['total'] = sum(all_chg.values())
for i in all_chg:
    print(i,all_chg[i],' ', end="")
print('')
