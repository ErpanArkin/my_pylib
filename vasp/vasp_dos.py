#!/usr/bin/env python3

"""
plot dos with prejections to elements. 

The current directory mush hold vasprun.xml for dos.

Optional -v lot w.r.t Vacuum level, this needs CONTACR and LOCPOT files.

http://home.ustc.edu.cn/~lipai/scripts/vasp_scripts/python_plot_dos_band.html
"""


from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-v", action="store_true", dest="verbose",
                  help="plot w.r.t Vacuum level, this needs \
                  CONTACR and LOCPOT files.")

(options, args) = parser.parse_args()


v = Vasprun('vasprun.xml')
cdos = v.complete_dos
element_dos = cdos.get_element_dos()
plotter = DosPlotter()
efermi = v.efermi

if options.verbose:
    from pymatgen.core import Element
    from pymatgen.io.vasp.outputs import Locpot, Poscar
    from pymatgen.analysis.surface_analysis import WorkFunctionAnalyzer

    l = Locpot.from_file('LOCPOT')
    s = Poscar.from_file('CONTCAR')

    wf = WorkFunctionAnalyzer(s.structure, l.get_average_along_axis(1),
                              efermi, shift=0)
    loc_vac = wf.vacuum_locpot

    for i in element_dos:
        element_dos[i].efermi = loc_vac

    plotter.add_dos_dict(element_dos)
    plt = plotter.get_plot(xlim=[-9, 1])
    plt.plot([efermi - loc_vac, efermi - loc_vac],
             plt.ylim(), 'b--', linewidth=2, label='EF')

    plt.xlabel('Energies - Vac(eV)')
    plt.legend()
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()  # all the text.Text instance in the legend
    plt.setp(ltext, fontsize=30)
    plt.tight_layout()
    plt.savefig('dos.png')
    plt.show()

else:
    plotter.add_dos_dict(element_dos)
    plotter.show()
    plotter.save_plot('vasp_dos.png', xlim=[-8, 7], img_format='png')
