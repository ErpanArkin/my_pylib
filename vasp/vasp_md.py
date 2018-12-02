#!/usr/bin/env python3

'''
This is a script to plot temperature, energies, pressure, lattice constants
as a function of vasp md steps. This requires XDATCAR, vasprun.xml, OSZICAR
files. This is for single md run, use vasp_md_total.py for multiple runs.
'''

import numpy as np
import matplotlib.pyplot as plt
import os.path
from ase.io import iread

# read vasprun.xml with ase.io.iread
a = iread('vasprun.xml')
latc = []
vol = []
pres = []  # this pressure is not correct for md
for i in a:
    latc.append(i.get_cell_lengths_and_angles())
    vol.append(i.get_volume())
    pres.append(i.get_stress())

# pressure includes kinetic contribution, obatained by following bash command
# LC_ALL=C fgrep  "Total+kin" OUTCAR > total+kin.dat
if os.path.exists('total+kin.dat'):
    pres = []
    with open('total+kin.dat', 'r') as f:
        lines = f.readlines()
    for i, j in enumerate(lines):
        x = [float(y) for y in j.split()[1:]]
        x.insert(0, i)
        pres.append(x)


t_e_ek = []  # temperature, energies
for line in open("OSZICAR"):
    if "T= " in line:
        t_e_ek.append([float(line.split()[i]) for i in [0, 2, 4, 10]])


# seperate prepare lattice constants since
# NBLOCK control how often these are printed.
# latc = []  # lattice constants
# with open('XDATCAR', 'r') as f:
#     lines = f.readlines()
# for i, j in enumerate(lines):
#     if "configuration=" in j:
#         x = []
#         x.append(int(j.split()[2]))
#         for t in lines[i - 5:i - 2]:
#             x.append(np.linalg.norm([float(y) for y in t.split()]))
#         latc.append(x)


data = np.array(t_e_ek)
pres_np = np.array(pres)
latc_np = np.array(latc)
vol_np = np.array(vol)

fig, ax = plt.subplots(2, sharex='col')

plt.xlabel('steps')

# plot energy fluctuation w.r.t. mean
ax[0].plot(data[:, 0], data[:, 2] - data[:, 2].mean())
ax[0].plot(data[:, 0], data[:, 3] - data[:, 3].mean())
ax[0].legend(['free energy', 'Kinetic energy'], loc=2)

# plot temperature on secondary y-axis
ax2 = ax[0].twinx()
ax2.plot(data[:, 0], data[:, 1], 'k')
ax2.legend(['temperature'], loc=1)

# plot diagonal components of pressure
ax[1].plot(data[:, 0], pres_np[:, 1:4])
ax[1].legend(['px', 'py', 'pz'], loc=2)

# lattice fluctuation w.r.t. mean
for i in range(0, len(latc_np.T)):
    latc_np[:, i] -= latc_np[:, i].mean()
    vol_np -= vol_np.mean()

# scale volume values to lattice constants
# to be able to shown on the same scale

sca = (vol_np.max()) / (latc_np[:, :3].max())

ax2 = ax[1].twinx()
ax2.plot(data[:, 0], latc_np[:, :3], '--')
ax2.plot(data[:, 0], vol_np / sca, 'k', linewidth=2)
ax2.legend(['lat_a', 'lat_b', 'lat_c',
            'volume\n(scaled 1/' + str(round(sca, 2)) + ')'], loc=1)

plt.savefig('vasp_md.png')
plt.show()
