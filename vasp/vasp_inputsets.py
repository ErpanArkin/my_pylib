#!/usr/bin/env python3

from pymatgen import Structure
import sys, importlib

'''
This script use the pymatgen.io.vasp.sets to generate vasp inputs.
1st argument is the name of the structure file
2nd argument is one of the set clsss in the above library
'''

pmg_sets=importlib.import_module('pymatgen.io.vasp.sets')
set=getattr(pmg_sets,sys.argv[2])
structure = Structure.from_file(sys.argv[1])
x= set(structure)
x.write_input(output_dir=''.join(sys.argv[1].split('.')[:-1])+'-'+sys.argv[2])
