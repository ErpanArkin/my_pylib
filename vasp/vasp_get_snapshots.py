#!/usr/bin/env python3

from ase.io import iread
import numpy as np
import sys

'''
get the snapshot structures for the indice given by the arguments

e.g. get_snapshots.py 100 150 300

if no argument, three most lowest pressure structures are given
'''
np.set_printoptions(suppress=True) # set four decimal numbers for readibility.
lattice = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])

if len(sys.argv) > 1:
    snps = [int(i) for i in sys.argv[1:]]
    print('user input mode...')
else:
    data = []
    # fgrep  "Total+kin" OUTCAR > total+kin.dat
    pres = np.loadtxt('total+kin.dat', usecols=[1, 2, 3, 4, 5, 6])
    new = []
    for i, j in enumerate(pres):
        new.append([sum(abs(j)), i])
    pres_hyp = np.append(pres, new, 1)
    # sort along new column: total absolute pressure
    pres_hyp_sort = pres_hyp[pres_hyp[:, -2].argsort()]
    snps = [int(i) for i in pres_hyp_sort[:3][:, -1]]
    print('lowest pressure mode...')

print('generating snapshots:', snps, 'with pressure: \n', pres_hyp_sort[:3])

a = iread('vasprun.xml')
for i, j in enumerate(a):
    if any([i == x for x in snps]):
        j.write("POSCAR_" + str(i))
        lattice = np.append(lattice, np.reshape(j.get_cell(), (1, 9)), axis=0)
        last = j

ave_lat = lattice[1:].mean(axis=0)
last.set_cell(np.reshape(ave_lat, (3, 3)))

last.write('POSCAR_ave')
