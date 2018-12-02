#!/usr/bin/env python3

"""
plot band and dos with prejections to elements. 

The current directory must hold vasprun.xml for band sturcture.
The ../ mush hold vasprun.xml for dos.

"""

from pymatgen.io.vasp.outputs import *
from pymatgen.electronic_structure.plotter \
  import BSDOSPlotter
import matplotlib.pyplot as plt

# get density of states
dosrun = Vasprun("../vasprun.xml", parse_projected_eigen=True)
dos = dosrun.complete_dos

# get band structure
bsrun = Vasprun('vasprun.xml', parse_projected_eigen=True)
bs = bsrun.get_band_structure(
    'KPOINTS', efermi=dosrun.efermi, line_mode=True)

# plot bs and dos together
bsdosplot = BSDOSPlotter(vb_energy_range=6, cb_energy_range=6) #, 
#  axis_fontsize(24.0), tick_fontsize(24.0), legend_fontsize(24.0))

# bsdosplot.get_plot(bs)
bsdosplot.get_plot(bs, dos=dos)
plt.show()
