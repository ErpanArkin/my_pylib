#!/usr/bin/env python3

from ase.io import iread,write
import sys

if len(sys.argv) > 1:
    intv =  int(sys.argv[1]) # output every intv steps
    fname = sys.argv[2]
else:
    intv = 1
    fname = 'vasprun1.xml'

a = iread(fname)

for i,j in enumerate(a):
    if i % intv == 0:
        write('XDATCAR.xyz',j,append=True)
