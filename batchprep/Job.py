#!/usr/bin/env python3

import os
from pathlib import Path
import shutil

from batchprep.templates import ENV

class Job:
    sublocal_fn = ""

    def __init__(self, charge, mult, mem, pal, xyz, name, queue,
                 tpl_fn=None, sub_fn=None):
        self.charge = charge
        self.mult = mult
        self.xyz = xyz
        self.mem = mem
        self.pal = pal
        self.queue = queue

        if sub_fn:
            self.sub_fn = sub_fn
        if tpl_fn:
            self.tpl_fn = tpl_fn

        if hasattr(self, "tpl_fn"):
            self.job_tpl = ENV.get_template(self.tpl_fn)
        if hasattr(self, "sub_fn"):
            self.sub_tpl = ENV.get_template(self.sub_fn)

        self.xyz_root = f"{Path(self.xyz).stem}" 
        self.xyz_str = self.read_lines_with_skip(self.xyz)
        self.name = f"{name}_{self.xyz_root}"
        self.input_fn = f"{self.name}{self.job_ext}"


    def read_lines_with_skip(self, xyz_fn, skip=2):
        with open(xyz_fn) as handle:
            lines = handle.readlines()[skip:]
        return "".join(lines)

    def make_job_dir(self, root_dir):
        self.job_dir = root_dir / self.name
        try:
            os.mkdir(self.job_dir)
        except FileExistsError:
            pass

    def populate_job_dir(self):
        # Write the job input
        job_input_path = self.job_dir / self.input_fn

        with open(job_input_path, "w") as handle:
            handle.write(self.render_job())

        self.write_additional()

        # Copy .xyz file
        xyz_path = self.job_dir / self.xyz.name
        shutil.copy(self.xyz, xyz_path)

        # Write submit script
        submit_path = self.job_dir / "subjob.sh"
        with open(submit_path, "w") as handle:
            handle.write(self.render_submit())
        return self.job_dir

    def copy_and_set(self, src_path, attr_name):
        shutil.copy(src_path, self.job_dir / src_path.name)
        setattr(self, attr_name, src_path.name) 

    def write_additional(self):
        pass

    def render_job(self, **kwargs):
        return self.job_tpl.render(charge=self.charge,
                                   mult=self.mult,
                                   xyz_str=self.xyz_str,
                                   mem=self.mem,
                                   pal=self.pal,
                                   **kwargs,
        )
    
    def render_submit(self):
        return self.sub_tpl.render(
                    job_name=self.name,
                    pal=self.pal,
                    mem=self.mem,
                    **self.queue,
        )

    def get_sublocal_tpl(self):
        return ENV.get_template(self.sublocal_fn)

    def sublocal_kwargs(self):
        return {}

    def __str__(self):
        return self.job_type
