#!/usr/bin/python3

from ase.io import iread
import numpy as np
import matplotlib.pyplot as plt
import argparse

# TODO: minimum pressure case for lammps

parser = argparse.ArgumentParser(description='Construct a structure \
    with the average positions and cell dimensions, or minimum pressure.')
parser.add_argument('filename', type=str,
                    help='filename of the md trajectory output: \
                    vasprum.xml or .lammpstrj')
parser.add_argument('-r', '--range', type=int, nargs='+',
                    help='range of steps to be used, if only one is given, \
                    range will be from this step till the end. \
                    If nothing is give, use the whole range.')
parser.add_argument('-s', '--pos', dest='pos', action='store_true',
                    default=False, help='average atom"s positions. \
                    Default: False')
parser.add_argument('-m', '--min', dest='minp', action='store_true',
                    default=False, help='use the cell with minimum \
                    pressure. Default: False')
parser.add_argument('-f', '--format', type=str,
                    help='format can be vasprun.xml or lammpstrj from \
                    lammps dump.')
parser.add_argument('-p', '--plot', dest='plot', action='store_true',
                    default=False, help='plot the average cell vs all cells')
args = parser.parse_args()

d_range = [0, -1]

if args.range:
    for i, j in enumerate(args.range):
        if i > 1:
            break
        else:
            d_range[i] = int(j)

if 'lammpstrj' in args.filename:
    fmt = 'lammps-dump'
elif 'vasprun' in args.filename:
    fmt = 'vasp-xml'
elif args.format:
    fmt = args.format
else:
    fmt = None

a = iread(args.filename, format=fmt)

data = []
pos = []
cell = []

for i in a:
    data.append(i)
    pos.append(i.positions)
    cell.append(i.cell)

pos_ave = np.mean(np.array(pos[d_range[0]:d_range[1]]), axis=0)
cell_ave = np.mean(np.array(cell[d_range[0]:d_range[1]]), axis=0)


if args.minp:
    pres = []
    with open('total+kin.dat', 'r') as f:
        for line in f:
            pres.append([float(j) for j in line.split()[1:]])
    pres_np = np.array(pres)
    # get the index of minimum pressure
    i_minp = np.argmin(abs(pres_np[:, 0]) +
                       abs(pres_np[:, 1]) +
                       abs(pres_np[:, 2]))
    data[i_minp - 1].write('POSCAR_ave_minP' + '.vasp')
else:
    data[-1].set_cell(cell_ave)
    if args.pos:
        data[-1].set_positions(pos_ave)
        data[-1].write('POSCAR_ave_' + str(d_range[0]) +
                       '_' + str(d_range[1]) + '.vasp')


if args.plot:
    cellnp = np.array(cell[d_range[0]:d_range[1]])
    plt.plot(cellnp.reshape(len(cellnp), 9))
    for i in cell_ave:
        plt.hlines(i, 0, len(cell))
    plt.show()
