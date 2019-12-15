from gpaw import GPAW
from ase.io import write
import numpy as np
import matplotlib.pyplot as plt
import sys

try:
    file = sys.argv[1]
except IndexError:
    print('supply .gpw file as the 1st argument.')
    sys.exit()

calc = GPAW(file, txt=None)
efermi = calc.get_fermi_level()
v = calc.get_electrostatic_potential().mean(1).mean(0)
z = np.linspace(0, calc.atoms.cell[2, 2], len(v), endpoint=False)
plt.figure(figsize=(6.5, 4.5))
plt.plot(z, v, label='xy-averaged potential')
plt.plot([0, z[-1]], [efermi, efermi], label='Fermi level')

n = 6  # get the vacuum level 6 grid-points from the boundary
plt.plot([0.2, 0.2], [efermi, v[n]], 'r:')
plt.text(0.23, (efermi + v[n]) / 2,
         r'$\phi$ = %.2f eV' % (v[n] - efermi), va='center')
plt.plot([z[-1] - 0.2, z[-1] - 0.2], [efermi, v[-n]], 'r:')
plt.text(z[-1] - 0.23, (efermi + v[-n]) / 2,
         r'$\phi$ = %.2f eV' % (v[-n] - efermi),
         va='center', ha='right')

plt.xlabel('$z$, r$\AA$')
plt.ylabel('(Pseudo) electrostatic potential, V')
plt.xlim([0., z[-1]])
plt.show()

write('slab.pov', calc.atoms,
      rotation='-90x',
      show_unit_cell=1,
      transparent=False,
      display=False,
      run_povray=True)