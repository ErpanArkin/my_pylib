#!/usr/bin/env python3

'''
This is a script to plot temperature, energies, pressure, lattice constants
as a function of vasp md steps. This requires XDATCAR, total+kin.dat, OSZICAR
files. This is specially for multiple runs, where above files are just obtained
by appending the result from each run to a total file. For example:
for i in `seq 0 10`;do 
cat "$i"/OUTCAR >> OUTCAR;
cat "$i"/OSZICAR >> OSZICAR;
cat "$i"/XDATCAR >> XDATCAR;
grep  "Total+kin" "$i"/OUTCAR >> total+kin.dat;done
'''

import numpy as np
import matplotlib.pyplot as plt
import os.path


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
counter = 0
for line in open("OSZICAR"):
    if "T= " in line:
        tt = [float(line.split()[i]) for i in [2, 4, 10]]
        tt.insert(0, counter)
        t_e_ek.append(tt)
        counter += 1

# seperate prepare lattice constants since
# NBLOCK control how often these are printed.
with open('XDATCAR', 'r') as f:
    lines = f.readlines()
vol = []
latc = []
counter = 0
for i, j in enumerate(lines):
    if "configuration=" in j:
        counter = int(j.split()[-1])
        x = []
        for t in lines[i - 5:i - 2]:
            tt = [float(y) for y in t.split()]
            x.append(tt)
        ttt = np.linalg.norm(np.array(x), axis=1).tolist()
        ttt.insert(0, counter)
        latc.append(ttt)
        vol.append([counter, np.linalg.det(np.array(x))])
        counter += 1


temp_en = np.array(t_e_ek)
pres_np = np.array(pres)
latc_np = np.array(latc)
vol_np = np.array(vol)

fig, ax = plt.subplots(2, sharex='col')
fig.set_size_inches(
    (20, 15), forward=True)

plt.xlabel('steps')

# plot energy fluctuation w.r.t. mean
ax[0].plot(temp_en[:, 0], temp_en[:, 2] - temp_en[:, 2].mean())
ax[0].plot(temp_en[:, 0], temp_en[:, 3] - temp_en[:, 3].mean())
ax[0].legend(['free energy', 'Kinetic energy'], loc=2)

# plot temperature on secondary y-axis
ax2 = ax[0].twinx()
ax2.plot(temp_en[:, 0], temp_en[:, 1], 'k')
ax2.legend(['temperature'], loc=1)

# plot diagonal components of pressure
ax[1].plot(temp_en[:, 0], pres_np[:, 1:4])
ax[1].legend(['px', 'py', 'pz'], loc=2)

# scale volume values to lattice constants
# to be able to shown on the same scale


ax2 = ax[1].twinx()
for i in range(1, 4):
    latc_np[:, i] -= latc_np[:, i].mean()
vol_np[:, 1] -= vol_np[:, 1].mean()

sca = (vol_np[:, 1].max()) / (latc_np[:, 1:4].max())

ax2.plot(latc_np[:, 0], latc_np[:, 1:4], '--')
ax2.plot(vol_np[:, 0], vol_np[:, 1] / sca, 'k', linewidth=2)
ax2.legend(['lat_a', 'lat_b', 'lat_c',
            'volume\n(scaled 1/' + str(round(sca, 2)) + ')'], loc=1)

plt.savefig('vasp_md_total.png', dpi=300)
plt.show()
