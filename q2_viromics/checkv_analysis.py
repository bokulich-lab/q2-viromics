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

from q2_types.per_sample_sequences import ContigSequencesDirFmt

from q2_viromics._utils import run_command
from q2_viromics.types._format import CheckVDBDirFmt, ViromicsMetadataDirFmt

warnings.simplefilter(action="ignore", category=FutureWarning)


# Create the command for CheckV analysis
def checkv_end_to_end(tmp, sequences, database, num_threads):
    internal_db_name = os.path.join(database.path, os.listdir(database.path)[0])

    cmd = [
        "checkv",
        "end_to_end",
        str(sequences),
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


def checkv_analysis(
    sequences: ContigSequencesDirFmt,
    database: CheckVDBDirFmt,
    num_threads: int = 1,
) -> (
    ContigSequencesDirFmt,
    ContigSequencesDirFmt,
    ViromicsMetadataDirFmt,
    ViromicsMetadataDirFmt,
    ViromicsMetadataDirFmt,
):

    viral_sequences = ContigSequencesDirFmt()
    proviral_sequences = ContigSequencesDirFmt()
    quality_summary = ViromicsMetadataDirFmt()
    contamination = ViromicsMetadataDirFmt()
    completeness = ViromicsMetadataDirFmt()

    for sample_id, contigs_fp in sequences.sample_dict().items():
        viral_path = os.path.join(str(viral_sequences), f"{sample_id}_contigs.fa")
        proviral_path = os.path.join(str(proviral_sequences), f"{sample_id}_contigs.fa")
        quality_summary_path = os.path.join(
            str(quality_summary), f"{sample_id}_quality_summary.tsv"
        )
        contamination_path = os.path.join(
            str(contamination), f"{sample_id}_contamination.tsv"
        )
        completeness_path = os.path.join(
            str(completeness), f"{sample_id}_completeness.tsv"
        )
        with tempfile.TemporaryDirectory() as tmp:
            # Execute the "checkv end_to_end" command
            checkv_end_to_end(tmp, contigs_fp, database, num_threads)

            # Define the filenames and destination paths in a list of tuples
            files_and_destinations = [
                ("viruses.fna", viral_path),
                ("proviruses.fna", proviral_path),
                ("quality_summary.tsv", quality_summary_path),
                ("contamination.tsv", contamination_path),
                ("completeness.tsv", completeness_path),
            ]

            # Ensure the destination directories exist and move files
            for filename, dst in files_and_destinations:
                src = os.path.join(tmp, filename)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)

    return (
        viral_sequences,
        proviral_sequences,
        quality_summary,
        contamination,
        completeness,
    )
