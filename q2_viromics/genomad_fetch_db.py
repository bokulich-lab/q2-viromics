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

from q2_viromics._utils import run_command
from q2_viromics.types._format import GenomadDBDirFmt


# Create the command to fetch the geNomad database
def genomad_download_database(database):
    cmd = [
        "genomad",
        "download-database",
        str(database),
    ]

    try:
        # Execute the command to fetch a geNomad database
        run_command(cmd)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running geNomad download-database, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


# Fetch the geNomad database
def genomad_fetch_db() -> GenomadDBDirFmt:
    # Initialize a directory format object to store a geNomad database
    database = GenomadDBDirFmt()

    # Construct the command to fetch the geNomad database
    genomad_download_database(database)

    if os.path.exists(os.path.join(str(database), "genomad_db/.ipynb_checkpoints/")):
        shutil.rmtree(os.path.join(str(database), "genomad_db/.ipynb_checkpoints/"))

    return database
