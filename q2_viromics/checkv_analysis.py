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
import warnings

import pandas as pd
import qiime2
from q2_types.feature_data import DNAFASTAFormat

from q2_viromics._utils import run_command
from q2_viromics.types._format import CheckVDbDirFmt

warnings.simplefilter(action="ignore", category=FutureWarning)


# Create the command for CheckV analysis
def checkv_end_to_end(tmp, sequences, database, num_threads):
    internal_db_name = os.path.join(database.path, os.listdir(database.path)[0])

    cmd = [
        "checkv",
        "end_to_end",
        str(sequences.path),
        str(tmp),
        "-d",
        str(internal_db_name),
        "-t",
        str(num_threads),
    ]

    try:
        run_command(cmd)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running checkv end_to_end, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


def read_tsv_file(file_name, tmp):
    df = pd.read_csv(
        os.path.join(tmp, file_name), sep="\t", na_values=["NA", "", "NaN"], index_col=0
    )
    df.index.name = "sample_name"
    return df


def checkv_analysis(
    sequences: DNAFASTAFormat,
    database: CheckVDbDirFmt,
    num_threads: int = 10,
) -> (
    DNAFASTAFormat,
    DNAFASTAFormat,
    qiime2.Metadata,
    qiime2.Metadata,
    qiime2.Metadata,
    qiime2.Metadata,
):

    viral_sequences = DNAFASTAFormat()
    proviral_sequences = DNAFASTAFormat()

    with tempfile.TemporaryDirectory() as tmp:
        # Execute the "checkv end_to_end" command
        checkv_end_to_end(tmp, sequences, database, num_threads)

        # Copy the viral sequences file
        shutil.copy(
            os.path.join(tmp, "viruses.fna"),
            os.path.join(str(viral_sequences)),
        )

        # Copy the proviral sequences file
        shutil.copy(
            os.path.join(tmp, "proviruses.fna"),
            os.path.join(str(proviral_sequences)),
        )

        # Read the tsv files into a DataFrames
        quality_summary_df = read_tsv_file("quality_summary.tsv", tmp)
        contamination_df = read_tsv_file("contamination.tsv", tmp)
        completeness_df = read_tsv_file("completeness.tsv", tmp)
        complete_genomes_df = read_tsv_file("complete_genomes.tsv", tmp)

    return (
        viral_sequences,
        proviral_sequences,
        qiime2.Metadata(quality_summary_df),
        qiime2.Metadata(contamination_df),
        qiime2.Metadata(completeness_df),
        qiime2.Metadata(complete_genomes_df),
    )
