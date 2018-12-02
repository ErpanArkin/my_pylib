#!/usr/bin/env python3

'''
This script attach force calculated with vasp to xyz 
for visualizing it with ovito.
one argument can be the vasprun.xml file, default is "vasprun.xml"
'''

from ase.io import iread
import os
import argparse

parser = argparse.ArgumentParser(description='xyz file with forces from vasprun.xml')
parser.add_argument('vasprun',type=str, default='vasprun.xml', nargs='?',
                    help='name of the vasprun.xml')

args = parser.parse_args()

s = iread(args.vasprun)

try:
    os.remove('forces.xyz')
except OSError:
    pass

for i in s:
    i.write('forces.xyz',append=True)
