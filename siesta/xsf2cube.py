#!/usr/bin/env python3

from ase.io.xsf import read_xsf
from ase.io.cube import write_cube
from ase.io import read
import glob

'''
convert xsf with grid data to cube for Bader analysis
need xsf grid data from rho2xsf script, rename it *_data.XSF
and xsf structure  from xv2xsf script
then run "bader *_data.cube" for Bader analysis

'''

grid = glob.glob('*_data.XSF')

all_xsf = glob.glob('*.XSF')

stru = list(set(all_xsf) - set(grid))

xsf = read_xsf(open(grid[0], 'r'), read_data=True)

write_cube(open(str(grid[0])[:-4] + ".cube", 'w'),
           atoms=read(stru[0]), data=xsf[0])
