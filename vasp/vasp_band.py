#!/usr/bin/python3  

from pymatgen.io.vasp.outputs import Vasprun                                                                                                                                      
from pymatgen.electronic_structure.plotter import BSPlotter   
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", action="store_true", dest="plot", default=True, help="whether to plot BS")
parser.add_option("-e", action="store_true", dest="edges", default=True, help="output band edges")
(options, args) = parser.parse_args()

v = Vasprun("vasprun.xml")                                                                                                                                                              
bs = v.get_band_structure(line_mode=True)                                                                                                                                               
print(bs.get_band_gap())
  
if options.edges:
  print(bs.get_cbm(),bs.get_vbm())
  
if options.plot:
  BSPlotter(bs).get_plot(vbm_cbm_marker=True,ylim=[-4,4]).show()
