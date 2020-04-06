#!/usr/bin/env python3

from ase.io import write
from gpaw import restart
import sys


# the 1st argument is the .gpw file
# the rest is the band indice, can be multiple

gpw_file = sys.argv[1]
bands = sys.argv[2:]
atoms, calc = restart(gpw_file, txt=None)
for band in bands:
    wf = calc.get_pseudo_wave_function(band=int(band))
    fname = '{0}_{1}.cube'.format(gpw_file, band)
    print('writing wf', band, 'to file', fname)
    write(fname, atoms, data=wf)
