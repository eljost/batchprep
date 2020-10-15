#!/usr/bin/env python3

from batchprep.Job import Job

class OrcaJob(Job):
    tpl_fn = "orca.inp.tpl"
    sub_fn = "suborca.sh.tpl"
    job_type = "OrcaJob"
    job_ext = ".inp"

    def __init__(self, route, blocks=[], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.route = route
        self.blocks = blocks

    def render_job(self):
        return super().render_job(
                        route=self.route,
                        blocks=self.blocks,
        )
