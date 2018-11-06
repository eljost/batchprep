#!/usr/bin/env python3

from batchprep.Job import Job

class GaussianJob(Job):
    tpl_fn = "gaussian.gjf.tpl"
    sub_fn = "subgaussian.sh.tpl"
    job_type = "GaussianJob"
    job_ext = ".gjf"

    def __init__(self, route, *args, **kwargs):
        # Gaussian mem is given in total, and not per core
        kwargs["mem"] *= kwargs["pal"]
        super().__init__(*args, **kwargs)

        self.route = route
        self.chk = self.name

    def render_job(self):
        return super().render_job(
                        route=self.route,
                        chk=self.chk
        )
