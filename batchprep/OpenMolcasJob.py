#!/usr/bin/env python3

from batchprep.Job import Job

class OpenMolcasJob(Job):
    tpl_fn = "openmolcas.in.tpl"
    sub_fn = "submolcas.sh.tpl"
    job_type = "OpenMolcasJob"
    job_ext = ".in"

    def __init__(self, rasscf, caspt2=None, rassi=None,
                 *args, **kwargs):
        # Gaussian mem is given in total, and not per core
        super().__init__(*args, **kwargs)

        # With inline coordinates openmolcas also wants the first
        # two lines of the .xyz file.
        self.xyz_str = self.read_lines_with_skip(self.xyz, skip=0)
        self.rasscf = rasscf
        self.caspt2 = caspt2
        self.rassi = rassi


    def render_job(self):
        return super().render_job(
                fileorb=self.fileorb,
                rasscf=self.rasscf,
                caspt2=self.caspt2,
                rassi=self.rassi,
        )
