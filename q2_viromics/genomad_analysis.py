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

from q2_types.per_sample_sequences import ContigSequencesDirFmt

from q2_viromics._utils import run_command
from q2_viromics.types._format import GenomadDBDirFmt, ViromicsMetadataDirFmt


# Run the command for geNomad analysis
def genomad_end_to_end(
    tmp,
    sequences,
    database,
    num_threads,
    splits,
    min_score,
    min_number_genes,
    conservative_taxonomy,
):
    internal_db_name = os.path.join(database.path, os.listdir(database.path)[0])

    cmd = [
        "genomad",
        "end-to-end",
        "--cleanup",
        "--splits",
        str(splits),
        "--min-score",
        str(min_score),
        "--min-number-genes",
        str(min_number_genes),
        "--threads",
        str(num_threads),
        "--disable-nn-classification",
    ]

    if conservative_taxonomy:
        cmd.append("--conservative-taxonomy")

    cmd.extend(
        [
            str(sequences),
            str(tmp),
            str(internal_db_name),
        ]
    )

    try:
        run_command(cmd)
    except subprocess.CalledProcessError as e:
        raise Exception(
            "An error was encountered while running genomad end-to-end, "
            f"(return code {e.returncode}), please inspect "
            "stdout and stderr to learn more."
        )


def genomad_analysis(
    sequences: ContigSequencesDirFmt,
    database: GenomadDBDirFmt,
    num_threads: int = 1,
    splits: int = 8,
    min_score: float = 0.7,
    min_number_genes: int = 1,
    conservative_taxonomy: bool = False,
) -> (
    ContigSequencesDirFmt,
    ContigSequencesDirFmt,
    ContigSequencesDirFmt,
    ViromicsMetadataDirFmt,
):

    viruses = ContigSequencesDirFmt()
    proviruses = ContigSequencesDirFmt()
    plasmids = ContigSequencesDirFmt()
    virus_summary = ViromicsMetadataDirFmt()

    for id, contigs_fp in sequences.sample_dict().items():
        with tempfile.TemporaryDirectory() as tmp:
            # Execute the "genomad end_to_end" command
            genomad_end_to_end(
                tmp,
                contigs_fp,
                database,
                num_threads,
                splits,
                min_score,
                min_number_genes,
                conservative_taxonomy,
            )
            # Define the filenames and destination paths in a list of tuples
            files_and_destinations = [
                (
                    f"{id}_contigs_summary/{id}_contigs_virus.fna",
                    f"{viruses}/{id}_contigs.fa",
                ),
                (
                    f"{id}_contigs_find_proviruses/{id}_contigs_provirus.fna",
                    f"{proviruses}/{id}_contigs.fa",
                ),
                (
                    f"{id}_contigs_summary/{id}_contigs_plasmid.fna",
                    f"{plasmids}/{id}_contigs.fa",
                ),
                (
                    f"{id}_contigs_summary/{id}_contigs_virus_summary.tsv",
                    f"{virus_summary}/{id}_virus_summary.tsv",
                ),
            ]

            # Ensure the destination directories exist and move files
            for filename, dst in files_and_destinations:
                src = os.path.join(tmp, filename)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)

    return (
        viruses,
        proviruses,
        plasmids,
        virus_summary,
    )
