# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import subprocess

from q2_viromics._utils import run_command
from q2_viromics.types._format import CheckVDBDirFmt


# Create the command to fetch the CheckV database
def checkv_download_database(database):
    cmd = [
        "checkv",
        "download_database",
        str(database),
    ]

    try:
        # Execute the command to fetch a CheckV database
        run_command(cmd)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running CheckV download_database, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


# Fetch the CheckV database
def checkv_fetch_db() -> CheckVDBDirFmt:
    # Initialize a directory format object to store a CheckV database
    database = CheckVDBDirFmt()

    # Construct the command to fetch the CheckV database
    checkv_download_database(database)

    return database
