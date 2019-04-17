#!/usr/bin/env python3

from ase.io import iread
import numpy as np
import sys

'''
compute average lattice constants form vasprun.xml
in the steps range specified by the first and the second arguments.
Generate a new poscar, see the write function, with average lattice
constants with the internal coordinates taken from the last step.
'''

a = iread('vasprun.xml')

# default range: all steps
begin = 1
end = -1

# user defined
if len(sys.argv) == 3:
    begin = sys.argv[1]
    end = sys.argv[2]


lattice = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])
for i in a:
    lattice = np.append(lattice, np.reshape(i.get_cell(), (1, 9)), axis=0)
    last = i

ave_lat = lattice[int(begin):int(end), :].mean(axis=0)
last.set_cell(np.reshape(ave_lat, (3, 3)))

last.write('POSCAR_ave_{}_{}'.format(begin,end))
