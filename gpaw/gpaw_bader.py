#!/usr/bin/env python3

from ase.units import Bohr
from ase.io import write,read
from ase.io.cube import read_cube_data

from ase.io.bader import attach_charges

import sys

import subprocess

import os

exists = os.path.isfile('./ACF.dat')

if not exists:

    # if the data has not been multipled by Bohr**3, uncomment the following.
    # data, atoms = read_cube_data(sys.argv[1])
    # density = data * Bohr**3
    # write('density-temp.cube', atoms, data=density)
    # sys.argv[1] = 'density-temp.cube'
    res = subprocess.check_output(["bader", sys.argv[1]])

atoms = read(sys.argv[1])

attach_charges(atoms)

elm_set = set(atoms.get_chemical_symbols())
elm = dict.fromkeys(elm_set, 0)

total_charge = elm.copy()

with open(sys.argv[2]) as f:
    for line in f:
        if "-setup:" in line:
            x = line.split('-')[0]
        elif "  Z: " in line:
            elm[x] = int(line.split()[-1])

for i in atoms:
    i.charge = elm[i.symbol] - i.charge
    total_charge[i.symbol] += i.charge

atoms.write('charge.xyz')
print(total_charge,'sum: {}'.format(sum(total_charge.values())))