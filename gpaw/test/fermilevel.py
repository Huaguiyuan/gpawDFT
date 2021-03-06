import numpy as np

from ase import Atoms
from gpaw import GPAW, FermiDirac, Davidson
from gpaw.test import equal

calc = GPAW(nbands=1,
            eigensolver=Davidson(6),
            occupations=FermiDirac(0.0))
atoms = Atoms('He', pbc=True, calculator=calc)
atoms.center(vacuum=3)

e0 = atoms.get_potential_energy()
niter0 = calc.get_number_of_iterations()
try:
    calc.get_fermi_level()
except ValueError:
    pass  # It *should* raise an error
else:
    raise RuntimeError('get_fermi_level should not be possible for width=0')
calc.set(nbands=3, convergence={'bands': 2})
atoms.get_potential_energy()
homo, lumo = calc.get_homo_lumo()
equal(homo, -15.4473, 0.01)
equal(lumo, -0.2566, 0.01)
calc.write('test')
assert np.all(GPAW('test', txt=None).get_homo_lumo() == (homo, lumo))
ef = calc.get_fermi_level()
equal(ef, -7.85196, 0.01)

calc.set(occupations=FermiDirac(0.1))
e1 = atoms.get_potential_energy()
niter1 = calc.get_number_of_iterations()
ef = calc.get_fermi_level()
equal(ef, -7.85196, 0.01)
calc.write('test')
equal(GPAW('test', txt=None).get_fermi_level(), ef, 1e-8)
