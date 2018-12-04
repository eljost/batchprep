#!/usr/bin/env python3

from batchprep.Job import Job

class GaussianJob(Job):
    tpl_fn = "gaussian.gjf.tpl"
    sub_fn = "subgaussian.sh.tpl"
    job_type = "GaussianJob"
    job_ext = ".gjf"
    sublocal_fn = "sublocal_g16.tpl"

    def __init__(self, route, nstates=None, pop_states=None, *args, **kwargs):
        # Gaussian mem is given in total, and not per core
        kwargs["mem"] *= kwargs["pal"]
        super().__init__(*args, **kwargs)

        self.route = route
        self.chk = self.name
        self.nstates = nstates
        self.pop_states = pop_states

        if self.pop_states:
            assert all([0 < pop_state <= nstates for pop_state in pop_states]), \
                "pop_states must be in the range of nstates!"


    def render_job(self):
        return super().render_job(
                        route=self.route,
                        chk=self.chk,
                        nstates=self.nstates,
                        pop_states=self.pop_states,
        )
