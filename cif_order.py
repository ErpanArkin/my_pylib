#!/usr/bin/python3

from pymatgen import Structure
from pymatgen.transformations.standard_transformations import OrderDisorderedStructureTransformation
from pymatgen.transformations.advanced_transformations import EnumerateStructureTransformation
from pymatgen.io.cif import CifWriter
import sys

try:
    cif_filename = sys.argv[1]
except ValueError:
    print("please give the cif file name as the 1st argument!")

s = Structure.from_file(cif_filename)
prim = s.get_primitive_structure()
# Merge sites that are less than 1A apart.
prim.merge_sites(1)

prim = prim.get_sorted_structure()
t = EnumerateStructureTransformation()
ordered = t.apply_transformation(prim, 5)
print(len(ordered))

for i in range(len(ordered)):
    c = CifWriter(ordered[i]['structure'], symprec=0.01)
    c.write_file("LLZO_ordered-" + str(i) + ".cif")
