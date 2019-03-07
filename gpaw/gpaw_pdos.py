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
energy, pdos = calc.get_orbital_ldos(a=int(sys.argv[1]))
In = np.trapz(pdos, energy)
center = np.trapz(pdos * energy, energy) / In
width = np.sqrt(np.trapz(pdos * (energy - center)**2, energy) / In)
plt.plot(energy, pdos)
plt.xlabel('Energy (eV)')
plt.ylabel('PDOS on atom' + sys.argv[1])
plt.title('band center = %s eV, band width = %s eV' % (center, width))
plt.show()
