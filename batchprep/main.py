#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys

from natsort import natsorted
import yaml

from batchprep.GaussianJob import GaussianJob
from batchprep.OpenMolcasJob import OpenMolcasJob
from batchprep.OrcaJob import OrcaJob
from batchprep.templates import ENV


JOB_CLASSES = {
    "gaussian": GaussianJob,
    "orca": OrcaJob,
    "openmolcas": OpenMolcasJob,
}


def parse_args(args):
    parser = argparse.ArgumentParser("Prepare job batches from YAML definitions.")
    parser.add_argument("yaml", help=".yaml")
    return parser.parse_args(args)


def run():
    args = parse_args(sys.argv[1:])

    # Load YAML file
    with open(args.yaml) as handle:
        inp_dict = yaml.load(handle)

    # Load appropriate class depending on type
    JobClass = JOB_CLASSES[inp_dict["type"]]

    # Load xyz files
    cwd = Path(".")
    xyz_glob = inp_dict["xyz"]
    assert "*" in xyz_glob, "'*' is missing in xyz glob!"
    xyzs = natsorted(cwd.glob(xyz_glob), key= lambda p: str(p))
    assert len(xyzs) > 0, "Couldn't find any .xyz files!"
    print(f"Found {len(xyzs)} .xyz files.")

    common = inp_dict["common"]
    specific = inp_dict["specific"]
    try:
        queue = inp_dict["queue"]
    except KeyError:
        queue = {}
    try:
        sub_fn = inp_dict["sub_fn"]
    except KeyError:
        sub_fn = None
    try:
        tpl_fn = inp_dict["tpl_fn"]
    except KeyError:
        tpl_fn = None
    jobs = [JobClass(**common, **specific, xyz=xyz, queue=queue,
                     sub_fn=sub_fn, tpl_fn=tpl_fn)
            for xyz in xyzs]
    job_dirs = [job.make_job_dir(cwd) for job in jobs]

    try:
        for attr_name, glob in inp_dict["copy_also"].items():
            to_copy = natsorted(cwd.glob(glob), key=lambda p: str(p))
            # Every dir should get one file, so we need one file for every
            # xyz geometry.
            assert len(to_copy) == len(jobs)
            for job, src_path in zip(jobs, to_copy):
                job.copy_and_set(src_path, attr_name)
    except KeyError:
        pass
    [job.populate_job_dir() for job in jobs]
    job_dirs = [job.job_dir for job in jobs]

    # Bash script to submit jobs
    submit_tpl = ENV.get_template("submit.sh.tpl")
    submit_rendered = submit_tpl.render(job_dirs=job_dirs)
    with open("submit.sh", "w") as handle:
        handle.write(submit_rendered)

    # Bash script to submit jobs locally
    submit_local_tpl = ENV.get_template("submit_local.sh.tpl")
    submit_rendered = submit_local_tpl.render(job_dirs=job_dirs)
    with open("submit_local.sh", "w") as handle:
        handle.write(submit_rendered)


if __name__ == "__main__":
    run()
