# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import shutil
import subprocess

from q2_viromics.utils import run_command
from q2_viromics.types import Virsorter2DbDirFmt


# Create the command to fetch the Virsorter2 database
def vs2_setup(database, n_jobs):
    cmd = [
        "virsorter",
        "setup",
        "-d",
        str(database),
        "-s",
        "-j",
        str(n_jobs),
    ]

    try:
        # Execute the command to create the Minimap2 index database
        run_command(cmd)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running virsorter2 setup, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


# Fetch the Virsorter2 database
def virsorter2_fetch_db(n_jobs: int = 10) -> Virsorter2DbDirFmt:
    # Initialize a directory format object to store the Minimap2 index
    database = Virsorter2DbDirFmt()

    # Construct the command to build the Minimap2 index file
    vs2_setup(database, n_jobs)

    # Clean up the unnecessary directories
    for dir_name in [".snakemake", "conda_envs"]:
        if os.path.exists(os.path.join(str(database.path), dir_name)):
            shutil.rmtree(os.path.join(str(database.path), dir_name))

    return database
