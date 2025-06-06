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
import tempfile

import pandas as pd
import qiime2
from q2_types.feature_data import DNAFASTAFormat

from q2_viromics.utils import run_command
from q2_viromics.virsorter2.types._format import Virsorter2DbDirFmt


# Create the command to fetch the Virsorter2 database
def vs2_run_execution(tmp, sequences, database, n_jobs, min_score, min_length):
    cmd = [
        "virsorter",
        "run",
        "-w",
        str(tmp),
        "-d",
        str(database.path),
        "-i",
        str(sequences.path),
        "-j",
        str(n_jobs),
        "--min-score",
        str(min_score),
        "--min-length",
        str(min_length),
        "--use-conda-off",
    ]

    try:
        run_command(cmd)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running virsorter2 run, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


def virsorter2_run(
    sequences: DNAFASTAFormat,
    database: Virsorter2DbDirFmt,
    n_jobs: int = 10,
    min_score: float = 0.5,
    min_length: int = 0,
) -> (DNAFASTAFormat, qiime2.Metadata, qiime2.Metadata):

    viral_sequences = DNAFASTAFormat()

    with tempfile.TemporaryDirectory() as tmp:
        # Execute the "virsorter2 run" command
        vs2_run_execution(tmp, sequences, database, n_jobs, min_score, min_length)

        # Copy the combined viral sequences file
        shutil.copy(
            os.path.join(tmp, "final-viral-combined.fa"),
            os.path.join(str(viral_sequences)),
        )

        # Read the viral score file into a DataFrame
        viral_score_df = pd.read_csv(
            os.path.join(tmp, "final-viral-score.tsv"), sep="\t", index_col=0
        )
        viral_score_df.index.name = "sample_name"

        # Read the viral boundary file into a DataFrame
        viral_boundary_df = pd.read_csv(
            os.path.join(tmp, "final-viral-boundary.tsv"), sep="\t", index_col=0
        )
        viral_boundary_df.index.name = "sample_name"

    return (
        viral_sequences,
        qiime2.Metadata(viral_score_df),
        qiime2.Metadata(viral_boundary_df),
    )
