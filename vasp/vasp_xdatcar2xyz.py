#!/usr/bin/env python3
'''
This script convert XDATCAR to xyz file for
visualization expecially in ovito.
'''

from ase.io import iread,write
import os.path

output = 'XDATCAR.xyz'

a=iread('XDATCAR')

# remove existing output, otherwise the script just append it.
try:
    os.remove(output)
except OSError:
    pass

#write iteratively
for i in a:
    write(output,i,format='extxyz',append=True)
