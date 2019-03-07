#!/usr/bin/env python3

'''
This script attach charges calculated with bader charge program to xyz
for visualizing it with ovito.
This requires *.STRUCT_OUT *.psf ACF.dat files.

Use the g2c_ng from Util/Grid directory of siesta code to get cube file and use bader on that:
    SystemLabel=`ls *.RHO | cut -d. -f1` ;g2c_ng -s "$SystemLabel".STRUCT_OUT -g "$SystemLabel".RHO ;for i in *.cube;do mv $i "$SystemLabel".RHO."$i"; done; bader "$SystemLabel".RHO.Up+Down.cube

'''
import os
from ase.io import read
from ase.io.bader import attach_charges
from glob import glob


try:
    a = read(glob('*.STRUCT_OUT')[0])
except IndexError:
    try:
        a = read(glob('siesta.XSF')[0])
    except IndexError:
        print('need either STRUCT_OUT or siesta.XSF from xv2xsf script!')   
        exit()

attach_charges(a, displacement=0.1)

elms = [x for x in os.listdir() if x.endswith('psf')]
elm = []
chg = []
for i in elms:
    with open(i) as f:
        t = 0
        for line in f:
            if t == 0:
                elm.append(line.split()[0])
            elif t == 3:
                chg.append(line.split()[-1])
            elif t > 3:
                break
            t += 1

elm.append('total')
ech = [0] * len(elm)
all_chg = dict(zip(elm, ech))
# calculate the rest charge
for i in a:
    for j, k in enumerate(elm):
        if i.symbol == k:
            i.charge = -i.charge + float(chg[j])
            all_chg[k] += i.charge
# output xyz file with charge information
a.write('charge.xyz')

# fix some labels in xyz files
with open('charge.xyz') as f:
   newText=f.read().replace('initial_charges', 'Charge').replace(' =T ', ' ')

with open('charge.xyz', "w") as f:
   f.write(newText)


all_chg['total'] = sum(all_chg.values())
for i in all_chg:
    print(i, all_chg[i], ' ', end=" ")
print('')
