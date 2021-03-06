#!/usr/bin/env python3

from batchprep.Job import Job

class QChemJob(Job):
    tpl_fn = "qchem.in.tpl"
    sub_fn = "subqchem.sh.tpl"
    job_type = "QChemJob"
    job_ext = ".in"
    sublocal_fn = "sublocal_qchem.tpl"

    def __init__(self, keywords={}, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.keywords = keywords

    def render_job(self):
        return super().render_job(
                        keywords=self.keywords,
        )

    def sublocal_kwargs(self):
        return {
                "pal": self.pal,
        }
