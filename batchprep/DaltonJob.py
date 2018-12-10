#!/usr/bin/env python3

import itertools as it
from collections import Counter

from batchprep.templates import ENV

from batchprep.elements import ELEMENTS
from batchprep.Job import Job
from batchprep.helper import parse_xyz_file

class DaltonJob(Job):
    tpl_fn = "dalton.dal.tpl"
    tpl_mol_fn = "dalton.mol.tpl"
    sub_fn = "subdalton.sh.tpl"
    job_type = "DaltonJob"
    job_ext = ".dal"
    sublocal_fn = "sublocal_dalton.tpl"

    def __init__(self, basis, run, wavefunctions, properties=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.basis = basis
        self.run = run
        self.wavefunctions = wavefunctions
        self.properties = properties

        self.mol_tpl = ENV.get_template(self.tpl_mol_fn)
        self.prepare_mol()

    def prepare_mol(self):
        atoms, coords = parse_xyz_file(self.xyz)
        atom_counter = Counter(atoms)
        elements = list(atom_counter.keys())
        self.atom_types = len(elements)
        key_func = lambda ac: ac[0]
        atoms_coords_sort = sorted(zip(atoms, coords), key=key_func)
        coords_by_elem = it.groupby(atoms_coords_sort, key=key_func)
        atoms_data = list()
        for elem, elem_coords in coords_by_elem:
            atom_num = atom_counter[elem]
            charge = ELEMENTS[elem].number
            elem_coords = list(elem_coords)
            atoms_data.append((
                        charge,
                        atom_num,
                        elem_coords,
            ))
        mol = self.mol_tpl.render(basis=self.basis, atoms_data=atoms_data)
        return mol

    def write_additional(self):
        mol = self.prepare_mol()
        with open(self.job_dir / "dalton.mol", "w") as handle:
            handle.write(mol)

    def render_job(self):
        return super().render_job(
                        basis=self.basis,
                        run=self.run,
                        wavefunctions=self.wavefunctions,
                        properties=self.properties
        )
