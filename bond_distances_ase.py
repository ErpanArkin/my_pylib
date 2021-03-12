from ase.io import read
from sys import argv

'''
The 1st argument is the filename of the structure.
Get distances between an atom, whose index is the 2nd argument, 
and a list of atoms whose indices are the rest of the arguments.
'''

a = read(argv[1])
neighbors = [int(i) for i in argv[3:]]

pt_o_lengths = a.get_distances(int(argv[2]),neighbors)
pt_o_lengths.sort()

print(pt_o_lengths)