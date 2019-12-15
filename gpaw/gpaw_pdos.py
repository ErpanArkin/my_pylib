#!/usr/bin/env python3

import numpy as np
import pylab as plt
from gpaw import GPAW
from glob import glob
import sys

'''
pdos from .gpw, 1st argument is the index of the atom used for projection.
'''

file = glob('*.gpw')

calc = GPAW(file[-1], txt=None)
ef = calc.get_fermi_level()
structure = calc.get_atoms()
y = {i:0.0 for i in set(structure.get_chemical_symbols())}

for i in structure:
    energy, pdos = calc.get_orbital_ldos(a=i.index)
    y[i.symbol] += pdos

[plt.plot(energy - ef, y[i], label=i) for i in y]
plt.xlabel('E-E-Fermi (eV)')
plt.ylabel('PDOS')
plt.legend()
plt.savefig('pdos.png', dpi=300)
plt.show()


# for i in sys.argv[1:]:
#     energy, pdos = calc.get_orbital_ldos(a=int(i))
#     In = np.trapz(pdos, energy)
#     center = np.trapz(pdos * energy, energy) / In
#     width = np.sqrt(np.trapz(pdos * (energy - center)**2, energy) / In)
#     plt.plot(energy - ef, pdos, label=str(i))
# plt.xlabel('Energy (eV)')
# plt.ylabel('PDOS')
# plt.legend()
# plt.title('band center = %s eV, band width = %s eV' % (center, width))
# plt.show()
